## 接口说明

接口名称：`alipay.aipay.agent.fulfillment.confirm`

## 适用场景

A2A商家履约回执确认。

## 公共请求参数

| 参数 | 类型 | 是否必选 | 最大长度 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| `app_id` | String | 必选 | 32 | 支付宝分配给开发者的应用 ID | `2014072300007148` |
| `method` | String | 必选 | 128 | 接口名称 | `alipay.aipay.agent.fulfillment.confirm` |
| `format` | String | 可选 | 40 | 仅支持JSON | `JSON` |
| `charset` | String | 必选 | 10 | 请求使用的编码格式，如utf-8,gbk,gb2312等 | `utf-8` |
| `sign_type` | String | 必选 | 10 | 商户生成签名字符串所使用的签名算法类型，目前支持RSA2和RSA，推荐使用RSA2 | `RSA2` |
| `sign` | String | 必选 | 344 | 商户请求参数的签名串，详见[签名](https://ideservice.alipay.com/cms/site/02khjm) | `详见示例` |
| `timestamp` | String | 必选 | 19 | 发送请求的时间，格式"yyyy-MM-dd HH:mm:ss" | `2014-07-24 03:07:50` |
| `version` | String | 必选 | 3 | 调用的接口版本，固定为：1.0 | `1.0` |
| `biz_content` | String | 必选 | - | 请求参数的集合，最大长度不限，除公共参数外所有请求参数都必须放在这个参数中传递，具体参照各产品快速接入文档 | - |

## 业务请求参数

| 参数 | 类型 | 是否必选 | 最大长度 | 描述 | 注意事项/枚举值 | 示例值 |
| --- | --- | --- | --- | --- | --- | --- |
| `trade_no` | String | 必选 | 32 | 支付宝交易号 | - | `20260324008281172041220000012182` |

## 常见请求示例

::::aipay-tabs{defaultActiveKey="Java"}
:::aipay-tab{key="Java" title="Java"}
```java
package com.java.sdk.demo;

import com.alipay.api.AlipayApiException;
import com.alipay.api.AlipayClient;
import com.alipay.api.DefaultAlipayClient;
import com.alipay.api.AlipayConfig;
import com.alipay.api.response.AlipayAipayAgentFulfillmentConfirmResponse;
import com.alipay.api.domain.AlipayAipayAgentFulfillmentConfirmModel;
import com.alipay.api.request.AlipayAipayAgentFulfillmentConfirmRequest;

import com.alipay.api.FileItem;
import java.util.Base64;
import java.util.ArrayList;
import java.util.List;

public class AlipayAipayAgentFulfillmentConfirm {

    public static void main(String[] args) throws AlipayApiException {
        // 初始化SDK
        AlipayClient alipayClient = new DefaultAlipayClient(getAlipayConfig());

        // 构造请求参数以调用接口
        AlipayAipayAgentFulfillmentConfirmRequest request = new AlipayAipayAgentFulfillmentConfirmRequest();
        AlipayAipayAgentFulfillmentConfirmModel model = new AlipayAipayAgentFulfillmentConfirmModel();
        
        // 设置交易号
        model.setTradeNo("20260324008281172041220000012182");
        
        request.setBizModel(model);
        AlipayAipayAgentFulfillmentConfirmResponse response = alipayClient.execute(request);
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
:::

:::aipay-tab{key="C#" title="C#"}
```csharp
using System;
using System.Collections.Generic;
using Aop.Api;
using Aop.Api.Request;
using Aop.Api.Response;
using Aop.Api.Domain;
using Aop.Api.Util;
namespace SdkDemoTest
{
    public class AlipayAipayAgentFulfillmentConfirm
    {
        public static void Main(string[] args) 
        {
            // 初始化SDK
            IAopClient alipayClient = new DefaultAopClient(GetAlipayConfig());
            // 构造请求参数以调用接口
            AlipayAipayAgentFulfillmentConfirmRequest request = new AlipayAipayAgentFulfillmentConfirmRequest();
            AlipayAipayAgentFulfillmentConfirmModel model = new AlipayAipayAgentFulfillmentConfirmModel();
            
            // 设置交易号
            model.TradeNo = "20260324008281172041220000012182";
            
            request.SetBizModel(model);
            AlipayAipayAgentFulfillmentConfirmResponse response = alipayClient.Execute(request);

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
:::

:::aipay-tab{key="PHP" title="PHP"}
```php
<?php
require_once '../aop/AopClient.php';
require_once '../aop/AopCertClient.php';
require_once '../aop/AopCertification.php';
require_once '../aop/AlipayConfig.php';
require_once '../aop/request/AlipayAipayAgentFulfillmentConfirmRequest.php';

// 初始化SDK
$alipayClient = new AopClient(getAlipayConfig());
// 构造请求参数以调用接口
$request = new AlipayAipayAgentFulfillmentConfirmRequest();
$model = array();

// 设置交易号
$model['trade_no'] = "20260324008281172041220000012182";

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
:::

:::aipay-tab{key="cURL" title="cURL"}
```bash
curl 'https://openapi.alipay.com/gateway.do?charset=UTF-8&method=alipay.aipay.agent.fulfillment.confirm&format=json&sign=${sign}&app_id=${appid}&version=1.0&sign_type=RSA2&timestamp=${now}' \
 -F 'biz_content={
    "trade_no":"20260324008281172041220000012182"
}'
```
:::

::::

## 公共响应参数

| 参数 | 类型 | 是否必选 | 描述 | 示例值 |
| :--- | :--- | :--- | :--- | :--- |
| code | String | 必选 | 网关返回码，[详见文档](https://opendoc.alipay.com/common/02km9f) | 40004 |
| msg | String | 必选 | 网关返回码描述，[详见文档](https://opendoc.alipay.com/common/02km9f) | Business Failed |
| sub_code | String | 可选 | 业务返回码，参见具体的 API 接口文档 | - |
| sub_msg | String | 可选 | 业务返回码描述，参见具体的 API 接口文档 | - |
| sign | String | 必选 | 签名，[详见文档](https://opendoc.alipay.com/common/02kf5q) | DZXh8eeTuAHoYE3w1J... |

## 业务响应参数

| 参数 | 类型 | 是否必选 | 最大长度 | 描述 | 注意事项/枚举值 | 示例值 |
| --- | --- | --- | --- | --- | --- | --- |
| `trade_no` | String | 必选 | 32 | 支付宝交易号 | - | `20260324008281172041220000012182` |

## 响应示例

::::aipay-tabs{defaultActiveKey="正常示例"}
:::aipay-tab{key="正常示例" title="正常示例"}
```json
{
    "alipay_aipay_agent_fulfillment_confirm_response":{
        "code":"10000",
        "msg":"Success",
        "trade_no":"20260324008281172041220000012182"
    },
    "sign":"ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
}
```
:::

:::aipay-tab{key="异常示例" title="异常示例"}
```json
{"alipay_aipay_agent_fulfillment_confirm_response":{"code":"20000","msg":"Service Currently Unavailable","sub_code":"isp.unknow-error","sub_msg":"系统繁忙"},"sign":"ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"}
```
:::

::::

## 公共错误码

[前往查看公共错误码](https://opendoc.alipay.com/common/02km9f)

## 业务错误码

| 错误码 | 错误描述 | 解决方案 |
| --- | --- | --- |
| `SYSTEM_ERROR` | 系统繁忙 | 服务器异常 可能发生了网络或者系统异常，导致服务调用失败，商户可以用同样的请求发起重试 |
| `INVALID_PARAMETER` | 参数有误 | 请根据接口返回的参数非法的具体错误信息，修改参数后进行重试 |
| `SELLER_IDENTITY_MISMATCH` | 卖家身份校验失败 | 发起请求的商户与交易卖方不匹配，请确认商户身份 |
| `SELLER_ID_EMPTY` | 无法获取卖家身份信息，sellerId为空 | 请检查签名校验是否正常，确保商户身份信息正确 |
| `TRADE_NOT_FOUND` | 交易不存在 | 请确认交易号是否正确 |
| `TRADE_NO_EMPTY` | 交易号不能为空 | 请传入有效的tradeNo参数 |
| `TRADE_NO_INVALID` | 订单号格式有误 | 订单号需为32位 |
| `TRADE_STATUS_INVALID` | 交易状态不允许履约 | 当前交易状态无法进行履约操作，用户已经先行履约完成或交易已关闭 |
