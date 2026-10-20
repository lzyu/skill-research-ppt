<a name="sd2sJ"></a>
# alipay.aipay.agent.payment.verify(A2A商户支付凭证验证)
<a name="COZlz"></a>
## 通用场景
A2A场景下商户拿到支付凭证向支付宝请求验证
<a name="e64DF"></a>
### 公共请求参数
| 参数英文名 | 类型 | 是否必选 | 长度/取值 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| app_id | String | 必选 | 32 | 支付宝分配给开发者的应用ID | 2014072300007148 |
| method | String | 必选 | 128 | 接口名称 | alipay.aipay.agent.payment.verify |
| format | String | 可选 | 40 | 仅支持JSON | JSON |
| charset | String | 必选 | 10 | 请求使用的编码格式，如utf-8,gbk,gb2312等 | utf-8 |
| sign_type | String | 必选 | 10 | 商户生成签名字符串所使用的签名算法类型，目前支持RSA2和RSA，推荐使用RSA2 | RSA2 |
| sign | String | 必选 | 344 | 商户请求参数的签名串，详见[签名](https://ideservice.alipay.com/cms/site/02khjm) | 详见示例 |
| timestamp | String | 必选 | 19 | 发送请求的时间，格式"yyyy-MM-dd HH:mm:ss" | 2014-07-24 03:07:50 |
| version | String | 必选 | 3 | 调用的接口版本，固定为：1.0 | 1.0 |
| biz_content | String | 必选 |  | 请求参数的集合，最大长度不限，除公共参数外所有请求参数都必须放在这个参数中传递，具体参照各产品快速接入文档 | <br /> |

<a name="JSs4E"></a>
### 业务请求参数
| 参数英文名 | 类型 | 是否必选 | 长度/取值 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| trade_no | String | 必须 | 32 | 支付宝交易号，交易的唯一标识 | 20260324008281172041220000012182 |
| payment_proof | String | 必须 | 64 | 支付凭证 | 62922589b11acfc70faf4ebab1da7a9bbc438554e40d0a1dcdc7f35b3085xxxx |
| client_session | String | 可选 | 1024 | 客户端会话标识，用于校验买家安全性、真实性 | ImNsaWVudFNlc3N |

<a name="V1AhR"></a>
### 请求示例
<a name="ZCeUo"></a>
#### 默认示例
<a name="CdRVb"></a>
##### csharp
```
 using System;
using System.Collections.Generic;
using Aop.Api;
using Aop.Api.Request;
using Aop.Api.Response;
using Aop.Api.Domain;
using Aop.Api.Util;
namespace SdkDemoTest
{
    public class AlipayAipayAgentPaymentVerify
    {
        public static void Main(string[] args) 
        {
            // 初始化SDK
            IAopClient alipayClient = new DefaultAopClient(GetAlipayConfig());
            // 构造请求参数以调用接口
            AlipayAipayAgentPaymentVerifyRequest request = new AlipayAipayAgentPaymentVerifyRequest();
            AlipayAipayAgentPaymentVerifyModel model = new AlipayAipayAgentPaymentVerifyModel();
            
            // 设置交易号
            model.TradeNo = "20260324008281172041220000012182";
            
            // 设置支付凭证
            model.PaymentProof = "62922589b11acfc70faf4ebab1da7a9bbc438554e40d0a1dcdc7f35b3085xxxx";
            
            // 设置买家客户端会话标识
            model.ClientSession = "ImNsaWVudFNlc3N";
            
            request.SetBizModel(model);
            AlipayAipayAgentPaymentVerifyResponse response = alipayClient.Execute(request);

            if(!response.IsError)
            {
                Console.WriteLine("调用成功");
            }
            else
            {
                Console.WriteLine("调用失败");
            }
        }

        private static AlipayConfig GetAlipayConfig()
        {
            string privateKey  = "<-- 请填写您的应用私钥，例如：MIIEvQIBADANB ... ... -->";
            string alipayPublicKey = "<-- 请填写您的支付宝公钥，例如：MIIBIjANBg... -->";
            AlipayConfig alipayConfig = new AlipayConfig();
            alipayConfig.ServerUrl = "https://openapi.alipay.com/gateway.do";
            alipayConfig.AppId = "<-- 请填写您的AppId，例如：2019091767145019 -->";
            alipayConfig.PrivateKey = privateKey;
            alipayConfig.Format = "json";
            alipayConfig.AlipayPublicKey = alipayPublicKey;
            alipayConfig.Charset = "UTF-8";
            alipayConfig.SignType = "RSA2";
            return alipayConfig;
        }
    }
}
```
<a name="Hkq6l"></a>
##### java
```
 package com.java.sdk.demo;

import com.alipay.api.AlipayApiException;
import com.alipay.api.AlipayClient;
import com.alipay.api.DefaultAlipayClient;
import com.alipay.api.AlipayConfig;
import com.alipay.api.domain.AlipayAipayAgentPaymentVerifyModel;
import com.alipay.api.request.AlipayAipayAgentPaymentVerifyRequest;
import com.alipay.api.response.AlipayAipayAgentPaymentVerifyResponse;

import com.alipay.api.FileItem;
import java.util.Base64;
import java.util.ArrayList;
import java.util.List;

public class AlipayAipayAgentPaymentVerify {

    public static void main(String[] args) throws AlipayApiException {
        // 初始化SDK
        AlipayClient alipayClient = new DefaultAlipayClient(getAlipayConfig());

        // 构造请求参数以调用接口
        AlipayAipayAgentPaymentVerifyRequest request = new AlipayAipayAgentPaymentVerifyRequest();
        AlipayAipayAgentPaymentVerifyModel model = new AlipayAipayAgentPaymentVerifyModel();
        
        // 设置交易号
        model.setTradeNo("20260324008281172041220000012182");
        
        // 设置支付凭证
        model.setPaymentProof("62922589b11acfc70faf4ebab1da7a9bbc438554e40d0a1dcdc7f35b3085xxxx");
        
        // 设置买家客户端会话标识
        model.setClientSession("ImNsaWVudFNlc3N");
        
        request.setBizModel(model);
        AlipayAipayAgentPaymentVerifyResponse response = alipayClient.execute(request);
        System.out.println(response.getBody());

        if (response.isSuccess()) {
            System.out.println("调用成功");
        } else {
            System.out.println("调用失败");
            // sdk版本是"4.38.0.ALL"及以上,可以参考下面的示例获取诊断链接
            // String diagnosisUrl = DiagnosisUtils.getDiagnosisUrl(response);
            // System.out.println(diagnosisUrl);
        }
    }

    private static AlipayConfig getAlipayConfig() {
        String privateKey  = "<-- 请填写您的应用私钥，例如：MIIEvQIBADANB ... ... -->";
        String alipayPublicKey = "<-- 请填写您的支付宝公钥，例如：MIIBIjANBg... -->";
        AlipayConfig alipayConfig = new AlipayConfig();
        alipayConfig.setServerUrl("https://openapi.alipay.com/gateway.do");
        alipayConfig.setAppId("<-- 请填写您的AppId，例如：2019091767145019 -->");
        alipayConfig.setPrivateKey(privateKey);
        alipayConfig.setFormat("json");
        alipayConfig.setAlipayPublicKey(alipayPublicKey);
        alipayConfig.setCharset("UTF-8");
        alipayConfig.setSignType("RSA2");
        return alipayConfig;
    }
}
```
<a name="RfJjJ"></a>
##### php
```
 <?php
require_once '../aop/AopClient.php';
require_once '../aop/AopCertClient.php';
require_once '../aop/AopCertification.php';
require_once '../aop/AlipayConfig.php';
require_once '../aop/request/AlipayAipayAgentPaymentVerifyRequest.php';

// 初始化SDK
$alipayClient = new AopClient(getAlipayConfig());
// 构造请求参数以调用接口
$request = new AlipayAipayAgentPaymentVerifyRequest();
$model = array();

// 设置交易号
$model['trade_no'] = "20260324008281172041220000012182";

// 设置支付凭证
$model['payment_proof'] = "62922589b11acfc70faf4ebab1da7a9bbc438554e40d0a1dcdc7f35b3085xxxx";

// 设置买家客户端会话标识
$model['client_session'] = "ImNsaWVudFNlc3N";

$request->setBizContent(json_encode($model,JSON_UNESCAPED_UNICODE));
$responseResult = $alipayClient->execute($request);
$responseApiName = str_replace(".","_",$request->getApiMethodName())."_response";
$response = $responseResult->$responseApiName;
if(!empty($response->code)&&$response->code==10000){
    echo("调用成功");
}
else{
    echo("调用失败");
}

function getAlipayConfig()
{
    $privateKey  = '<-- 请填写您的应用私钥，例如：MIIEvQIBADANB ... ... -->';
    $alipayPublicKey = '<-- 请填写您的支付宝公钥，例如：MIIBIjANBg... -->';
    $alipayConfig = new AlipayConfig();
    $alipayConfig->setServerUrl('https://openapi.alipay.com/gateway.do');
    $alipayConfig->setAppId('<-- 请填写您的AppId，例如：2019091767145019 -->');
    $alipayConfig->setPrivateKey($privateKey);
    $alipayConfig->setFormat('json');
    $alipayConfig->setAlipayPublicKey($alipayPublicKey);
    $alipayConfig->setCharset('UTF-8');
    $alipayConfig->setSignType('RSA2');
    return $alipayConfig;
}
```
<a name="f3e18"></a>
##### http
```
 curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.aipay.agent.payment.verify&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'biz_content={
    "trade_no":"20260324008281172041220000012182",
    "payment_proof":"62922589b11acfc70faf4ebab1da7a9bbc438554e40d0a1dcdc7f35b3085xxxx",
    "client_session":"ImNsaWVudFNlc3N"
}' 
```
<a name="GRNHf"></a>
### 公共响应参数
| 参数英文名 | 类型 | 是否必选 | 长度/取值 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| code | String | 必须 | ~ | 网关返回码,[详见文档](https://ideservice.alipay.com/cms/site/02km9f) | 40004 |
| msg | String | 必须 | ~ | 网关返回码描述,[详见文档](https://ideservice.alipay.com/cms/site/02km9f) | Business Failed |
| sub_code | String | 可选 | ~ | 业务返回码，参见具体的API接口文档 |  |
| sub_msg | String | 可选 | ~ | 业务返回码描述，参见具体的API接口文档 |  |
| sign | String | 必须 | 64 | 签名,[详见文档](https://ideservice.alipay.com/cms/site/02kf5q) | DZXh8eeTuAHoYE3w1J+POiPhfDxOYBfUNn1lkeT/V7P4zJdyojWEa6IZs6Hz0yDW5Cp/viufUb5I0/V5WENS3OYR8zRedqo6D+fUTdLHdc+EFyCkiQhBxIzgngPdPdfp1PIS7BdhhzrsZHbRqb7o4k3Dxc+AAnFauu4V6Zdwczo= |

<a name="Z2aPP"></a>
### 业务响应参数
| 参数英文名 | 类型 | 是否必选 | 长度/取值 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| trade_no | String | 必须 | 32 | 支付宝交易号，交易的唯一标识 | 20260324008281172041220000012182 |
| amount | Price | 必须 | 6 | 订单金额，CNY | 0.01 |
| resource_id | String | 必须 | 32 | 卖家自定义的resourceId | out_res_id_0000123 |
| active | Boolean | 必须 | 10 | 支付凭证是否有效 | true |
| out_trade_no | String | 必须 | 16384 | 外部幂等号 | ORDER_1774598472720_etm5dy |

<a name="gBqAb"></a>
### 响应示例
<a name="yaRxf"></a>
#### 正常响应示例
```
 {
    "alipay_aipay_agent_payment_verify_response":{
        "code":"10000",
        "msg":"Success",
        "trade_no":"20260324008281172041220000012182",
        "amount":"0.01",
        "resource_id":"out_res_id_0000123",
        "active":true,
        "out_trade_no":"ORDER_1774598472720_etm5dy"
    },
    "sign":"ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```
<a name="seiub"></a>
#### 异常响应示例
```
 {"alipay_aipay_agent_payment_verify_response":{"code":"20000","msg":"Service Currently Unavailable","sub_code":"isp.unknow-error","sub_msg":"系统繁忙"},"sign":"ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"}
```
<a name="54a2e4df"></a>
### 公共错误码
[前往查看](https://ideservice.alipay.com/cms/site/02km9f)
<a name="kho2m"></a>
### 业务错误码
| 错误码 | 错误描述 | 解决方案 |
| --- | --- | --- |
| SYSTEM_ERROR | 系统繁忙 | 服务器异常 可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| INVALID_PARAMETER | 参数有误 | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试 |
| CLIENT_SESSION_IS_EMPTY | 凭证校验阶段clientSession为空 | C agent需要升级最新CLI |
| PAYMENT_PROOF_AGENT_MISMATCH | 智能体与凭证商户不一致 | 请确认智能体商户与支付凭证所属商户一致 |
| PAYMENT_PROOF_BUYER_MISMATCH | 支付买家与凭证买家不一致 | 卖家凭证水平越权，请检查权限后发起 |
| PAYMENT_PROOF_EMPTY | 支付凭证为空 | 请传入有效的paymentProof参数 |
| PAYMENT_PROOF_ID_MISMATCH | seller_id与凭证商户不一致 | 请确认发起请求的商户与支付凭证所属商户一致 |
| PAYMENT_PROOF_INVALID | 支付凭证格式错误 | 支付凭证需要为64位 |
| PAYMENT_PROOF_NOT_FOUND | 支付凭证过期或不存在 | 请确认支付凭证是否有效，凭证可能已过期 |
| PAYMENT_PROOF_STATUS_INVALID | 支付凭证状态无效 | 请确认支付凭证状态，凭证可能已被使用或失效 |
| PAYMENT_PROOF_TRADE_NO_MISMATCH | 交易号与凭证不一致 | 请确认交易号与支付凭证关联的交易号一致 |
| TRADE_NOT_FOUND | 交易不存在 | 请确认交易号是否正确 |
| TRADE_NO_EMPTY | 交易号不能为空 | 请传入有效的tradeNo参数 |
| TRADE_NO_INVALID | 订单号格式错误 | 订单号长度需要为32位 |
| TRADE_STATUS_CLOSED | 交易已关闭 | 该交易已关闭，无法验证支付凭证 |
| TRADE_STATUS_UNPAID | 交易未支付 | 该交易尚未完成支付，请等待支付完成后再验证 |

