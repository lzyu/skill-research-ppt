package main

import (
	"bytes"
	"context"
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/wechatpay-apiv3/wechatpay-go/core"
	"github.com/wechatpay-apiv3/wechatpay-go/core/auth/verifiers"
	"github.com/wechatpay-apiv3/wechatpay-go/core/downloader"
	"github.com/wechatpay-apiv3/wechatpay-go/core/notify"
	"github.com/wechatpay-apiv3/wechatpay-go/core/option"
	"github.com/wechatpay-apiv3/wechatpay-go/services/payments/native"
	"github.com/wechatpay-apiv3/wechatpay-go/services/refunddomestic"
	"github.com/wechatpay-apiv3/wechatpay-go/utils"
)

// ==================== 配置信息 ====================
// 实际使用时请从环境变量或配置文件读取

var (
	// 微信支付商户配置（用于 Native 下单 + 查单 + 退款）
	mchID          = os.Getenv("MCH_ID")           // 微信支付商户号
	appID          = os.Getenv("APP_ID")           // 应用ID
	serialNo       = os.Getenv("SERIAL_NO")        // 商户证书序列号
	privateKeyPath = os.Getenv("PRIVATE_KEY_PATH") // 商户私钥文件路径（PEM 格式）
	mchAPIv3Key    = os.Getenv("MCH_APIV3_KEY")    // 商户 APIv3 密钥（用于回调解密）
	payNotifyURL   = os.Getenv("PAY_NOTIFY_URL")   // 支付结果通知地址
	refundNotifyURL = os.Getenv("REFUND_NOTIFY_URL") // 退款结果通知地址
	timeExpireSec  = 870                            // 订单过期时间（秒），默认 14.5 分钟

	// SkillHub 开发者密钥配置（用于 AI 预下单签名）
	skillhubDeveloperID = os.Getenv("SKILLHUB_DEVELOPER_ID") // SkillHub 商户号，格式: sh-XXXXXXXX
	skillhubPubKeyID    = os.Getenv("SKILLHUB_PUB_KEY_ID")   // 密钥 ID，格式: PUB_KEY_xxx
	skillhubPrivateKey  = os.Getenv("SKILLHUB_PRIVATE_KEY")  // SkillHub 颁发的 RSA 2048 私钥（PEM 格式）

	// Skill 信息
	skillID      = os.Getenv("SKILL_ID")      // 在 SkillHub 发布的 Skill slug
	skillVersion = os.Getenv("SKILL_VERSION") // Skill 版本号

	// AI 预下单接口地址（使用 SkillHub 密钥签名）
	aiPreorderURL = "https://payapp.weixin.qq.com/palmpayminiapp/clawagentpay/preorder"
)

// ==================== 微信支付 SDK 客户端 ====================

var wxPayClient *core.Client
var wxNotifyHandler *notify.Handler // SDK 回调验签+解密处理器

// initWechatPayClient 初始化微信支付 SDK 客户端
// 使用官方 SDK: github.com/wechatpay-apiv3/wechatpay-go
func initWechatPayClient() {
	// 从文件加载商户私钥
	mchPrivateKey, err := utils.LoadPrivateKeyWithPath(privateKeyPath)
	if err != nil {
		log.Fatalf("加载微信支付商户私钥失败: %v", err)
	}

	ctx := context.Background()
	// 使用商户私钥等初始化 client，并使它具有自动定时获取微信支付平台证书的能力
	opts := []core.ClientOption{
		option.WithWechatPayAutoAuthCipher(mchID, serialNo, mchPrivateKey, mchAPIv3Key),
	}
	client, err := core.NewClient(ctx, opts...)
	if err != nil {
		log.Fatalf("初始化微信支付客户端失败: %v", err)
	}
	wxPayClient = client
	log.Println("微信支付 SDK 客户端初始化成功")

	// 初始化回调通知处理器（验签 + AES-256-GCM 解密）
	// 用于处理支付结果回调和退款结果回调
	certDownloader := downloader.NewCertificateDownloaderMgr(ctx)
	if err := certDownloader.RegisterDownloaderWithPrivateKey(
		ctx, mchPrivateKey, serialNo, mchID, mchAPIv3Key,
	); err != nil {
		log.Fatalf("注册证书下载器失败: %v", err)
	}
	certVisitor := certDownloader.GetCertificateVisitor(mchID)
	certVerifier := verifiers.NewSHA256WithRSAVerifier(certVisitor)
	wxNotifyHandler, err = notify.NewRSANotifyHandler(mchAPIv3Key, certVerifier)
	if err != nil {
		log.Fatalf("初始化回调通知处理器失败: %v", err)
	}
	log.Println("微信支付回调通知处理器初始化成功")
}

// ==================== 数据结构 ====================

// OrderRecord 订单记录（内存存储，生产环境请用数据库）
type OrderRecord struct {
	OutTradeNo   string    `json:"out_trade_no"`
	PaymentCode  string    `json:"payment_code"`
	Amount       int       `json:"amount"` // 单位：分
	Description  string    `json:"description"`
	Query        string    `json:"query"`
	Status       string    `json:"status"`        // INIT / PAID / FULFILLED / REFUNDED
	Result       string    `json:"result"`        // 履约结果
	RefundNo     string    `json:"refund_no"`     // 退款单号
	RefundReason string    `json:"refund_reason"` // 退款原因
	CreatedAt    time.Time `json:"created_at"`
}

// OrderStore 订单存储（内存版，生产环境请用数据库）
type OrderStore struct {
	mu     sync.RWMutex
	orders map[string]*OrderRecord // key: out_trade_no
}

func NewOrderStore() *OrderStore {
	return &OrderStore{
		orders: make(map[string]*OrderRecord),
	}
}

func (s *OrderStore) Save(order *OrderRecord) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.orders[order.OutTradeNo] = order
}

func (s *OrderStore) Get(outTradeNo string) *OrderRecord {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.orders[outTradeNo]
}

// ==================== 请求/响应结构 ====================

// ResourceRequest 商户 Skill 接口请求
type ResourceRequest struct {
	Query string `json:"query"`
}

// L2PaymentRequired AI 预下单 L2 业务 JSON
type L2PaymentRequired struct {
	SkillInfo *SkillInfo `json:"skill_info"`
	PayType   string     `json:"pay_type"`
	PayMode   string     `json:"pay_mode"`
	PayItems  []PayItem  `json:"pay_items"`
	ExpiresAt string     `json:"expires_at"`
}

type SkillInfo struct {
	SkillID      string `json:"skill_id"`
	SkillVersion string `json:"skill_version"`
}

type PayItem struct {
	ProductID string   `json:"product_id"`
	PayData   *PayData `json:"pay_data"`
}

type PayData struct {
	Type  string `json:"type"`
	Value string `json:"value"`
}

// L1PreorderRequest AI 预下单 L1 请求体
type L1PreorderRequest struct {
	SignatureType     string `json:"signature_type"`
	DeveloperPlatform string `json:"developer_platform"`
	DeveloperID       string `json:"developer_id"`
	PubKeyID          string `json:"pub_key_id"`
	NonceStr          string `json:"nonce_str"`
	Timestamp         string `json:"timestamp"`
	Signature         string `json:"signature"`
	PaymentRequired   string `json:"payment_required"`
}

// PreorderResponse AI 预下单响应
type PreorderResponse struct {
	PaymentCode string `json:"payment_code"`
}

// ==================== 主程序 ====================

var store = NewOrderStore()

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// 初始化微信支付 SDK 客户端
	initWechatPayClient()

	http.HandleFunc("/api/resource", handleResource)
	http.HandleFunc("/api/pay/notify", handlePayNotify)
	http.HandleFunc("/api/refund/notify", handleRefundNotify)
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})

	log.Printf("微信 Agent Pay 商户 Demo 启动，监听端口: %s", port)
	log.Printf("接口地址: POST http://localhost:%s/api/resource", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

// ==================== 核心处理逻辑 ====================

func handleResource(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]any{
			"error": "仅支持 POST 请求",
		})
		return
	}

	var req ResourceRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]any{
			"error": "请求体解析失败: " + err.Error(),
		})
		return
	}

	// 场景判断：通过 Header X-Out-Trade-No 判断是否为支付后重试
	outTradeNo := r.Header.Get("X-Out-Trade-No")
	if outTradeNo != "" {
		verifyAndFulfill(w, outTradeNo, req.Query)
		return
	}

	// 无 X-Out-Trade-No Header：首次请求，创建订单并返回 402
	createPaymentOrder(w, req)
}

// createPaymentOrder 创建支付订单：Native下单 → AI预下单 → 返回402
func createPaymentOrder(w http.ResponseWriter, req ResourceRequest) {
	// 1. 生成商户订单号（string(32) 以内）
	outTradeNo := generateOutTradeNo()

	// 2. 调用微信支付 Native 下单（使用微信支付官方 SDK）
	amount := int64(1) // 0.01 元 = 1 分
	description := fmt.Sprintf("AI付费查询: %s", truncate(req.Query, 50))

	codeURL, err := callNativeOrder(outTradeNo, description, amount)
	if err != nil {
		log.Printf("Native下单失败: %v", err)
		writeJSON(w, http.StatusInternalServerError, map[string]any{
			"error": "创建支付订单失败: " + err.Error(),
		})
		return
	}

	// 3. 调用 AI 预下单接口（使用 SkillHub 开发者密钥签名），获取 payment_code
	paymentCode, err := callAIPreorder(codeURL)
	if err != nil {
		log.Printf("AI预下单失败: %v", err)
		writeJSON(w, http.StatusInternalServerError, map[string]any{
			"error": "AI预下单失败: " + err.Error(),
		})
		return
	}

	// 4. 保存订单记录
	order := &OrderRecord{
		OutTradeNo:  outTradeNo,
		PaymentCode: paymentCode,
		Amount:      int(amount),
		Description: description,
		Query:       req.Query,
		Status:      "INIT",
		CreatedAt:   time.Now(),
	}
	store.Save(order)

	log.Printf("订单创建成功: out_trade_no=%s, payment_code=%s", outTradeNo, paymentCode)

	// 5. 返回 HTTP 402 + WeixinPay-Required + X-Out-Trade-No
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Header().Set("WeixinPay-Required", paymentCode)
	w.Header().Set("X-Out-Trade-No", outTradeNo)
	w.WriteHeader(http.StatusPaymentRequired) // 402

	json.NewEncoder(w).Encode(map[string]any{
		"code":    "PAYMENT_REQUIRED",
		"message": "需要支付后才能获取内容",
		"WeixinPay": map[string]any{
			"WeixinPay-Required": paymentCode,
			"prompt":             "本次使用微信支付，请将 WeixinPay-Required 的值作为 paymentCode 交给 weixinpay_pay，以向用户申请支付授权。",
		},
		"out_trade_no": outTradeNo,
		"amount":       fmt.Sprintf("%.2f", float64(amount)/100),
		"currency":     "CNY",
		"description":  description,
	})
}

// verifyAndFulfill 验证支付并履约：查单验证 → 返回付费内容
// outTradeNo 从请求 Header X-Out-Trade-No 中获取
func verifyAndFulfill(w http.ResponseWriter, outTradeNo string, query string) {

	// 1. 查询本地订单记录
	order := store.Get(outTradeNo)
	if order == nil {
		writeJSON(w, http.StatusNotFound, map[string]any{
			"error": "订单不存在: " + outTradeNo,
		})
		return
	}

	// 2. 幂等：如果已经履约过，直接返回缓存结果
	if order.Status == "FULFILLED" {
		log.Printf("订单已履约，返回缓存结果: out_trade_no=%s", outTradeNo)
		writeJSON(w, http.StatusOK, map[string]any{
			"code":              "SUCCESS",
			"message":           "付费内容（已缓存）",
			"out_trade_no":      outTradeNo,
			"content":           order.Result,
			"already_fulfilled": true,
		})
		return
	}

	// 3. 调用微信支付查单 API 验证支付状态（使用微信支付官方 SDK）
	tradeState, transactionID, err := callQueryOrder(outTradeNo)
	if err != nil {
		// 查单失败返回 402，让 Agent 稍后重试（可能是网络抖动，不一定是服务端错误）
		log.Printf("查单失败: %v", err)
		writeJSON(w, http.StatusPaymentRequired, map[string]any{
			"code":         "NOT_PAID",
			"message":      "支付状态校验中，请稍后重试",
			"out_trade_no": outTradeNo,
		})
		return
	}

	// 4. 校验支付状态
	if tradeState != "SUCCESS" {
		log.Printf("订单未支付: out_trade_no=%s, trade_state=%s", outTradeNo, tradeState)
		writeJSON(w, http.StatusPaymentRequired, map[string]any{
			"code":         "NOT_PAID",
			"message":      "订单尚未支付完成",
			"out_trade_no": outTradeNo,
			"trade_state":  tradeState,
		})
		return
	}

	// 5. 支付成功，执行业务逻辑（生成付费内容）
	bizQuery := query
	if bizQuery == "" {
		bizQuery = order.Query
	}
	result, err := executeBusiness(bizQuery)
	if err != nil {
		// 业务逻辑执行失败，主动发起退款
		log.Printf("业务执行失败，发起退款: out_trade_no=%s, error=%v", outTradeNo, err)
		refundErr := callRefund(outTradeNo, int64(order.Amount), "服务异常无法提供内容: "+err.Error())
		if refundErr != nil {
			log.Printf("退款请求失败: out_trade_no=%s, error=%v", outTradeNo, refundErr)
			writeJSON(w, http.StatusInternalServerError, map[string]any{
				"code":         "FULFILL_AND_REFUND_FAILED",
				"message":      "服务异常且退款失败，请联系客服",
				"out_trade_no": outTradeNo,
			})
			return
		}

		// 退款受理成功，更新订单状态
		order.Status = "REFUNDED"
		order.RefundReason = err.Error()
		store.Save(order)

		writeJSON(w, http.StatusOK, map[string]any{
			"code":          "REFUNDED",
			"message":       "服务无法提供付费内容，已发起全额退款",
			"out_trade_no":  outTradeNo,
			"refund_reason": err.Error(),
		})
		return
	}

	// 6. 更新订单状态为已履约
	order.Status = "FULFILLED"
	order.Result = result
	store.Save(order)

	log.Printf("履约成功: out_trade_no=%s, transaction_id=%s", outTradeNo, transactionID)

	// 7. 返回付费内容
	writeJSON(w, http.StatusOK, map[string]any{
		"code":              "SUCCESS",
		"message":           "付费内容",
		"out_trade_no":      outTradeNo,
		"transaction_id":    transactionID,
		"content":           result,
		"already_fulfilled": false,
	})
}

// ==================== 业务逻辑 ====================

// executeBusiness 执行业务逻辑（模拟）
// 生产环境中，这里是真正的业务处理，如调用下游 API、生成报告等
// 返回 error 表示不可恢复的失败，将触发退款
func executeBusiness(query string) (string, error) {
	// 模拟：正常情况下返回付费内容
	// 如需测试退款流程，可将 query 设为 "trigger_refund" 触发模拟失败
	if query == "trigger_refund" {
		return "", fmt.Errorf("下游服务不可用，无法生成内容")
	}
	return generatePaidContent(query), nil
}

// ==================== 微信支付 Native 下单 & 查单 & 退款（官方 SDK）====================

// callNativeOrder 调用微信支付 Native 下单接口
// 使用微信支付官方 SDK: github.com/wechatpay-apiv3/wechatpay-go
// 文档: https://pay.weixin.qq.com/doc/v3/merchant/4012791877
func callNativeOrder(outTradeNo, description string, amount int64) (string, error) {
	svc := native.NativeApiService{Client: wxPayClient}

	// 设置订单过期时间，避免订单永不过期
	timeExpire := time.Now().Add(time.Duration(timeExpireSec) * time.Second)

	resp, _, err := svc.Prepay(context.Background(), native.PrepayRequest{
		Appid:       core.String(appID),
		Mchid:       core.String(mchID),
		Description: core.String(description),
		OutTradeNo:  core.String(outTradeNo),
		NotifyUrl:   core.String(payNotifyURL),
		TimeExpire:  core.Time(timeExpire),
		Amount: &native.Amount{
			Total:    core.Int64(amount),
			Currency: core.String("CNY"),
		},
	})
	if err != nil {
		return "", fmt.Errorf("Native下单失败: %w", err)
	}

	return *resp.CodeUrl, nil
}

// callQueryOrder 调用微信支付查单接口
// 使用微信支付官方 SDK
// 文档: https://pay.weixin.qq.com/doc/v3/merchant/4012791880
func callQueryOrder(outTradeNo string) (tradeState string, transactionID string, err error) {
	svc := native.NativeApiService{Client: wxPayClient}

	resp, _, err := svc.QueryOrderByOutTradeNo(context.Background(), native.QueryOrderByOutTradeNoRequest{
		OutTradeNo: core.String(outTradeNo),
		Mchid:      core.String(mchID),
	})
	if err != nil {
		return "", "", fmt.Errorf("查单失败: %w", err)
	}

	tradeState = *resp.TradeState
	if resp.TransactionId != nil {
		transactionID = *resp.TransactionId
	}
	return tradeState, transactionID, nil
}

// callRefund 调用微信支付退款接口
// 使用微信支付官方 SDK
// 文档: https://pay.weixin.qq.com/doc/v3/merchant/4012791883
func callRefund(outTradeNo string, amount int64, reason string) error {
	svc := refunddomestic.RefundsApiService{Client: wxPayClient}

	outRefundNo := "RF_" + outTradeNo[6:] // 退款单号：RF_ + 原订单号后缀

	resp, _, err := svc.Create(context.Background(), refunddomestic.CreateRequest{
		OutTradeNo:  core.String(outTradeNo),
		OutRefundNo: core.String(outRefundNo),
		Reason:      core.String(truncate(reason, 80)),
		NotifyUrl:   core.String(refundNotifyURL),
		Amount: &refunddomestic.AmountReq{
			Refund:   core.Int64(amount),
			Total:    core.Int64(amount),
			Currency: core.String("CNY"),
		},
	})
	if err != nil {
		return fmt.Errorf("退款请求失败: %w", err)
	}

	log.Printf("退款受理成功: out_trade_no=%s, out_refund_no=%s, status=%v",
		outTradeNo, outRefundNo, *resp.Status)

	// 更新订单退款单号
	if order := store.Get(outTradeNo); order != nil {
		order.RefundNo = outRefundNo
		store.Save(order)
	}

	return nil
}

// handlePayNotify 处理微信支付结果回调通知
// 文档: https://pay.weixin.qq.com/doc/v3/merchant/4012791877
func handlePayNotify(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	// 使用 SDK ParseNotifyRequest：自动验证签名 + AES-256-GCM 解密通知报文
	content := make(map[string]interface{})
	_, err := wxNotifyHandler.ParseNotifyRequest(r.Context(), r, content)
	if err != nil {
		log.Printf("[pay_notify] 验签/解密失败: %v", err)
		writeJSON(w, http.StatusBadRequest, map[string]any{"code": "FAIL", "message": err.Error()})
		return
	}

	outTradeNo, _ := content["out_trade_no"].(string)
	tradeState, _ := content["trade_state"].(string)
	transactionID, _ := content["transaction_id"].(string)
	log.Printf("[pay_notify] out_trade_no=%s trade_state=%s transaction_id=%s", outTradeNo, tradeState, transactionID)

	// 仅当支付成功时更新本地订单状态
	if tradeState == "SUCCESS" && outTradeNo != "" {
		order := store.Get(outTradeNo)
		if order != nil && order.Status == "INIT" {
			order.Status = "PAID"
			store.Save(order)
			log.Printf("[pay_notify] 订单状态更新: out_trade_no=%s status=PAID", outTradeNo)
		}
	}

	// 返回成功，告知微信支付停止重试
	writeJSON(w, http.StatusOK, map[string]any{"code": "SUCCESS", "message": "成功"})
}

// handleRefundNotify 处理微信支付退款结果回调通知
// 文档: https://pay.weixin.qq.com/doc/v3/merchant/4012791888
func handleRefundNotify(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	// 使用 SDK ParseNotifyRequest：自动验证签名 + AES-256-GCM 解密通知报文
	refund := new(refunddomestic.Refund)
	_, err := wxNotifyHandler.ParseNotifyRequest(r.Context(), r, refund)
	if err != nil {
		log.Printf("[refund_notify] 验签/解密失败: %v", err)
		writeJSON(w, http.StatusBadRequest, map[string]any{"code": "FAIL", "message": err.Error()})
		return
	}

	log.Printf("[refund_notify] out_trade_no=%v out_refund_no=%v status=%v",
		refund.OutTradeNo, refund.OutRefundNo, refund.Status)

	// 根据退款状态更新本地订单
	if refund.OutTradeNo != nil {
		outTradeNo := *refund.OutTradeNo
		order := store.Get(outTradeNo)
		if order != nil {
			if refund.OutRefundNo != nil {
				order.RefundNo = *refund.OutRefundNo
			}
			if refund.Status != nil {
				switch *refund.Status {
				case refunddomestic.STATUS_SUCCESS:
					order.Status = "REFUNDED"
					log.Printf("[refund_notify] 退款成功: out_trade_no=%s", outTradeNo)
				case refunddomestic.STATUS_CLOSED:
					log.Printf("[refund_notify] 退款关闭: out_trade_no=%s", outTradeNo)
				case refunddomestic.STATUS_ABNORMAL:
					log.Printf("[refund_notify] 退款异常（需人工介入）: out_trade_no=%s", outTradeNo)
				}
			}
			store.Save(order)
		}
	}

	// 返回成功，告知微信支付停止重试
	writeJSON(w, http.StatusOK, map[string]any{"code": "SUCCESS", "message": "成功"})
}

// ==================== AI 预下单（SkillHub 开发者密钥签名）====================

// callAIPreorder 调用 AI 预下单接口
// 注意：此接口使用 SkillHub 颁发的开发者密钥签名，而非微信支付 API 证书
func callAIPreorder(codeURL string) (string, error) {
	// 1. 构造 L2 业务 JSON
	l2 := L2PaymentRequired{
		SkillInfo: &SkillInfo{
			SkillID:      skillID,
			SkillVersion: skillVersion,
		},
		PayType: "SKILL_PAY",
		PayMode: "AUTH_AND_PAY",
		PayItems: []PayItem{
			{
				ProductID: "SP" + time.Now().Format("060102") + "A001",
				PayData: &PayData{
					Type:  "code_url",
					Value: codeURL,
				},
			},
		},
		ExpiresAt: fmt.Sprintf("%d", time.Now().Add(15*time.Minute).Unix()),
	}

	l2Bytes, err := json.Marshal(l2)
	if err != nil {
		return "", fmt.Errorf("序列化 L2 JSON 失败: %w", err)
	}

	// 2. Base64 编码 L2
	paymentRequired := base64.StdEncoding.EncodeToString(l2Bytes)

	// 3. 构造签名串（5 行，每行以 \n 结尾）
	timestamp := fmt.Sprintf("%d", time.Now().Unix())
	nonceStr := generateNonceStr()
	signString := fmt.Sprintf("POST\n/palmpayminiapp/clawagentpay/preorder\n%s\n%s\n%s\n",
		timestamp, nonceStr, paymentRequired)

	// 4. SHA256withRSA 签名（使用 SkillHub 开发者私钥）
	signature, err := signWithSkillHubKey(signString)
	if err != nil {
		return "", fmt.Errorf("签名失败: %w", err)
	}

	// 5. 组装 L1 请求体
	l1 := L1PreorderRequest{
		SignatureType:     "SKILLHUB-SHA256-RSA2048",
		DeveloperPlatform: "SKILLHUB",
		DeveloperID:       skillhubDeveloperID,
		PubKeyID:          skillhubPubKeyID,
		NonceStr:          nonceStr,
		Timestamp:         timestamp,
		Signature:         signature,
		PaymentRequired:   paymentRequired,
	}

	l1Bytes, err := json.Marshal(l1)
	if err != nil {
		return "", fmt.Errorf("序列化 L1 请求失败: %w", err)
	}

	// 6. 发送请求
	req, err := http.NewRequest("POST", aiPreorderURL, bytes.NewReader(l1Bytes))
	if err != nil {
		return "", fmt.Errorf("创建请求失败: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("请求失败: %w", err)
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("AI预下单失败, HTTP %d: %s", resp.StatusCode, string(respBody))
	}

	var result PreorderResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return "", fmt.Errorf("解析响应失败: %w", err)
	}

	return result.PaymentCode, nil
}

// signWithSkillHubKey 使用 SkillHub 开发者私钥进行 SHA256withRSA 签名
func signWithSkillHubKey(signString string) (string, error) {
	// 解析 PEM 格式私钥
	block, _ := pem.Decode([]byte(skillhubPrivateKey))
	if block == nil {
		return "", fmt.Errorf("无法解析 SkillHub 私钥 PEM")
	}

	key, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		// 尝试 PKCS1 格式
		key, err = x509.ParsePKCS1PrivateKey(block.Bytes)
		if err != nil {
			return "", fmt.Errorf("解析私钥失败: %w", err)
		}
	}

	rsaKey, ok := key.(*rsa.PrivateKey)
	if !ok {
		return "", fmt.Errorf("私钥不是 RSA 类型")
	}

	// SHA256 哈希
	hashed := sha256.Sum256([]byte(signString))

	// PKCS1v15 签名
	sig, err := rsa.SignPKCS1v15(rand.Reader, rsaKey, crypto.SHA256, hashed[:])
	if err != nil {
		return "", fmt.Errorf("签名失败: %w", err)
	}

	// Base64 编码
	return base64.StdEncoding.EncodeToString(sig), nil
}

// ==================== 工具函数 ====================

// generateOutTradeNo 生成商户订单号（不超过32位）
func generateOutTradeNo() string {
	// 格式: WX402_ + 时间戳(14位) + 随机串(12位) = 32位
	ts := time.Now().Format("20060102150405")
	randBytes := make([]byte, 6)
	rand.Read(randBytes)
	randStr := hex.EncodeToString(randBytes)
	return fmt.Sprintf("WX402_%s%s", ts, randStr)
}

// generateNonceStr 生成32位随机字符串
func generateNonceStr() string {
	b := make([]byte, 16)
	rand.Read(b)
	return hex.EncodeToString(b)
}

// generatePaidContent 生成付费内容（模拟业务逻辑）
func generatePaidContent(query string) string {
	return fmt.Sprintf(
		"【付费内容】针对您的查询「%s」，以下是详细分析结果：\n\n"+
			"1. 这是通过微信 Agent Pay 支付后获取的付费内容\n"+
			"2. 商户已通过微信查单 API 验证支付成功\n"+
			"3. 本内容具有幂等性，重复请求将返回相同结果\n\n"+
			"生成时间: %s",
		query, time.Now().Format("2006-01-02 15:04:05"),
	)
}

// truncate 截断字符串
func truncate(s string, maxLen int) string {
	runes := []rune(s)
	if len(runes) <= maxLen {
		return s
	}
	return string(runes[:maxLen]) + "..."
}

// writeJSON 写入 JSON 响应
func writeJSON(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
