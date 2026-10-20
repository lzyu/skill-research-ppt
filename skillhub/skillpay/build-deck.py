from pathlib import Path
import importlib.util,re,json

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/skillhub/skillpay')
sp=importlib.util.spec_from_file_location('eb','/Users/tpy/.agents/skills/aico-ppt/scripts/edit-bundle.py')
eb=importlib.util.module_from_spec(sp);sp.loader.exec_module(eb)
target=root/'skillhub-skillpay-commercialization-v1.html'
lines=eb.load(target);s=eb.get_template(lines)
red='#b5333b';ink='#1a1a1c';muted='#585860';slate='#566472';line='#d9dde2'
style="width:100%;height:100%;padding:44px 72px 48px;display:flex;flex-direction:column;background:#fff;font-family:'Noto Sans SC',sans-serif;overflow:hidden;position:relative;color:#1a1a1c;"
def head(label,title):
 return f'''<div style="font-size:18px;letter-spacing:.08em;color:{red};margin-bottom:8px;">腾讯 SkillHub 商业化洞察 <span style="float:right;color:#6c7078;font-family:'JetBrains Mono';letter-spacing:0;">2026.10.20</span></div><h3 style="margin:0 0 18px;font-size:44px;font-weight:600;letter-spacing:-.02em;line-height:1.2;">{title}</h3>'''
def para(t,mt=10):return f'<div style="font-size:21px;line-height:1.5;margin-top:{mt}px;color:{muted};">{t}</div>'
def h(t):return f'<div style="font-size:27px;font-weight:700;line-height:1.3;margin-bottom:16px;">{t}</div>'
def stat(v,unit,txt):return f'''<div><div style="font-size:43px;font-weight:700;font-family:'JetBrains Mono';line-height:1.15;">{v}<span style="font-size:24px;font-family:'Noto Sans SC';margin-left:8px;">{unit}</span></div><div style="font-size:21px;color:{muted};margin-top:7px;">{txt}</div></div>'''
stats=''.join([stat('19.95','万条','公开 Skill 条目 199,545'),stat('10.0%','','付费标签 19,962 条'),stat('19.3%','','需 API Key 标签 38,568 条')])
left=f'''<div style="min-width:0;">{h('付费供给约占一成')}
<div style="font-size:21px;line-height:1.4;">付费标签 10.0%，其余条目约 90.0%</div>
<div style="display:flex;width:100%;height:26px;margin-top:15px;overflow:hidden;border-radius:2px;"><div style="width:8.55%;background:{red};"></div><div style="width:1.45%;background:{slate};"></div><div style="width:90%;background:#e9ebee;"></div></div>
<div style="margin-top:15px;font-size:21px;">
<div style="display:grid;grid-template-columns:1fr 98px 78px;padding:13px 0;border-bottom:1px solid {line};"><b style="color:{red};">paid 标签</b><span>17,061</span><b>8.5%</b></div>
<div style="display:grid;grid-template-columns:1fr 98px 78px;padding:13px 0;border-bottom:1px solid {line};"><b style="color:{slate};">alipay 标签</b><span>2,901</span><b>1.5%</b></div>
</div>
{para('两标签是官网付费识别的两种取值。<br/>Pay Skill 目录另计 19,974 条，口径不同。',14)}
<div style="margin-top:23px;border-top:1px solid {line};padding-top:15px;font-size:24px;font-weight:700;">API Key 依赖与付费分别统计</div>
{para('需 Key 占 19.3%，表示外部凭证依赖。<br/>与付费标签交叉的仅约 332 条，<br/>不能将需 Key 的条目全部算成付费。',9)}
</div>'''
mid=f'''<div style="min-width:0;border-left:1px solid {line};padding-left:27px;">{h('主要收费点在远程服务')}
<div style="font-size:25px;line-height:1.45;font-weight:700;">典型模式：Skill 包免费获取，<br/>商户后端按服务调用收费</div>
{para('商家自主设定单次价格。Agent 按技能指令调用 API，用户在支付工具中授权。',11)}
<div style="margin-top:23px;border-top:1px solid {line};padding-top:17px;">
<div style="display:flex;justify-content:space-between;font-size:24px;font-weight:700;"><span>WorkRally 图片生成</span><span style="color:{red};">¥0.36 / 次</span></div>
{para('腾讯科技（深圳）有限公司认证供给<br/>无需用户 API Key，远程生成并交付图片',8)}</div>
<div style="margin-top:20px;border-top:1px solid {line};padding-top:17px;">
<div style="display:flex;justify-content:space-between;font-size:24px;font-weight:700;"><span>喜鹊标书解读</span><span style="color:{red};">¥1 / 次</span></div>
{para('北京喜鹊云智科技有限公司认证供给<br/>无需用户 API Key，交付摘要和三份 Word',8)}</div>

</div>'''
right=f'''<div style="min-width:0;border-left:1px solid {line};padding-left:27px;">{h('服务商变现，平台暂免服务费')}
<div style="display:flex;align-items:baseline;gap:14px;"><b style="font-family:'JetBrains Mono';font-size:57px;line-height:1;color:{red};">0</b><b style="font-size:25px;">当前平台技术服务费</b></div>
{para('官网明确暂不收取技术服务费。<br/>支付渠道费用及结算仍按渠道规则。',14)}
<div style="margin-top:22px;padding-top:18px;border-top:1px solid {line};font-size:25px;font-weight:700;">用户直接付款给创作者</div>
{para('SkillHub 提供展示、投诉处理及平台服务；交易款按渠道规则结算至绑定账户。',9)}
<div style="margin-top:23px;padding-top:18px;border-top:1px solid {line};font-size:25px;font-weight:700;">已证实供给，成交规模仍待披露</div>
{para('全站 GMV、付费转化、复购和平台收入<br/>未见公开可核验数据。',9)}
</div>'''
roles=[('身份与支付准入','企业认证、绑定微信商户号<br/>个人提供支付宝接入路径'),('资产商品化与审核','版本包、按次定价和费用说明<br/>校验支付链路后审核上架'),('发现、分发与宿主接入','官网、CLI / API 获取 Skill<br/>向支持支付的 Agent 分发'),('支付身份与售后协同','提供开发者密钥和接入指南<br/>展示交易边界、协助投诉退款')]
rolehtml=''.join(f'<div style="min-width:0;"><div style="font-size:24px;font-weight:700;">{a}</div><div style="font-size:21px;line-height:1.45;color:{muted};margin-top:8px;">{b}</div></div>' for a,b in roles)
page1=f'''<section data-label="商业化程度" data-page-id="page-bf94d875082549fbb7c24f90f4f49f99" data-page-type-id="layered-platform-ops-rail" data-template-id="work-report" style="{style}">{head('商业化程度','SkillHub 已有按次收费供给，平台暂不收技术服务费')}
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:35px;border-top:2px solid {red};border-bottom:1px solid {line};padding:13px 0 17px;margin-bottom:23px;">{stats}</div>
<div style="flex:1;min-height:0;display:grid;grid-template-columns:520px 570px minmax(0,1fr);gap:27px;">{left}{mid}{right}</div>
<div style="border-top:2px solid {red};margin-top:20px;padding-top:14px;"><div style="font-size:24px;font-weight:700;margin-bottom:14px;">SkillHub 将服务供给接入 Agent 的工作</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:27px;">{rolehtml}</div></div>
<div style="font-size:13px;color:#6c7078;margin-top:16px;">口径：2026-10-20 同参数公开 API 的非原子快照，按条目计数，比例为近似值。付费标签不代表已开通微信收款或已成交；paid 标签不能直接等同微信份额。来源及查询链接见备注。</div>
</section>'''

# A flat editable sequence table retains actor and message relationships.
def cell(title,body='',redtext=False):
 return f'<div style="padding:17px 20px;min-width:0;"><div style="font-size:24px;font-weight:700;line-height:1.35;color:{red if redtext else ink};">{title}</div><div style="font-size:21px;color:{muted};line-height:1.45;margin-top:7px;">{body}</div></div>'
rows=[
 ('01','创建订单',cell('调用付费业务接口','读取 Skill 指令，向商户发起业务请求'),cell('先下传统微信订单','金额、商户订单号、notify_url<br/>Native / JSAPI 等现有支付接口'),cell('返回微信预支付标识','code_url / prepay_id<br/>保留原有微信订单及收款主体')),
 ('02','申请支付码',cell('等待商户返回支付请求','商户的签名私钥保留在后端<br/>不下发给 Agent 或 Skill 包'),cell('再做 x402 预下单','用 SkillHub 开发者 RSA 密钥签名<br/>将既有微信预支付标识登记到 AI 支付'),cell('校验开发者身份，返回 payment_code','此码用于拉起支付，有效期最长 15 分钟<br/>它本身不证明付款成功',True)),
 ('03','用户授权',cell('支付工具拉起卡片','宿主须支持 weixinpay_ 工具<br/>保留支付码原文，避免模型改写'),cell('返回 HTTP 402 + 支付码','WeixinPay-Required: payment_code<br/>也支持 HTTP 200 兼容投递'),cell('用户扫码到微信 Liteapp 逐笔确认','从 AI 专属卡余额支付<br/>与用户微信主账户资金隔离',True)),
 ('04','验付交付',cell('继续原任务，获取业务结果','可沿用原订单关联取回结果<br/>具体重试方式由服务接口约定'),cell('以微信回调 / 查单结果验付','验证签名、订单、金额及 SUCCESS<br/>履约并幂等保存结果，失败按需退款',True),cell('通知商户支付结果','沿用 notify_url / 微信查单与退款<br/>资金按渠道规则结算至商户绑定账户')),
]
rowhtml=''
for n,t,a,b,c in rows:
 rowhtml+=f'<div style="display:grid;grid-template-columns:150px 460px 590px 1fr;border-bottom:1px solid {line};min-height:134px;"><div style="padding:18px 15px 16px 0;"><div style="font-size:27px;font-family:\'JetBrains Mono\';font-weight:700;color:{red};">{n}</div><div style="font-size:22px;font-weight:700;margin-top:7px;">{t}</div></div>{a}{b}{c}</div>'
page2=f'''<section data-label="微信支付机制" data-page-type-id="layered-platform-ops-rail" data-template-id="work-report" style="{style}">{head('微信支付机制','微信 SkillPay 将微信订单接入 Agent，商户验付后履约')}
<div style="border-top:2px solid {red};border-bottom:1px solid {line};padding:14px 0 16px;margin-bottom:18px;"><b style="font-size:25px;">SkillHub 在交易前完成接入与分发</b><div style="font-size:21px;line-height:1.5;color:{muted};margin-top:7px;">企业认证及微信商户绑定，提供开发者密钥，配置按次价格，审核并发布 Skill，接入支持支付的 Agent。实际服务与订单由商户后端承接。</div></div>
<div style="flex:1;min-height:0;">
<div style="display:grid;grid-template-columns:150px 460px 590px 1fr;border-bottom:2px solid {red};"><div></div><div style="padding:10px 20px 13px;font-size:26px;font-weight:700;">Agent 与用户</div><div style="padding:10px 20px 13px;font-size:26px;font-weight:700;">商户业务后端</div><div style="padding:10px 20px 13px;font-size:26px;font-weight:700;">微信支付</div></div>{rowhtml}
</div>
<div style="border-top:2px solid {red};padding-top:14px;margin-top:20px;display:grid;grid-template-columns:1.08fr 1fr;gap:34px;">
<div><div style="font-size:24px;font-weight:700;">三类凭证用途不同</div><div style="font-size:21px;line-height:1.5;color:{muted};margin-top:7px;">业务 API Key 用于外部服务接入；SkillHub RSA 密钥签名 AI 预下单；微信商户证书与 APIv3 密钥处理支付请求和回调。</div></div>
<div><div style="font-size:24px;font-weight:700;">落地需对齐官方接口版本</div><div style="font-size:21px;line-height:1.5;color:{muted};margin-top:7px;">微信当前 API 与 SkillHub 教程 / Demo 的端点、鉴权位置和报文结构不同。不能混接；本次依据官方文档和源码，未真实交易。</div></div>
</div>
<div style="font-size:13px;color:#6c7078;margin-top:15px;">来源：微信 AI 支付接入准备、开发指引、x402 API、FAQ；SkillHub 接入教程、官方商户 Demo 及 WorkRally Skill。详细链接、版本差异与可核验范围见备注和伴生研究文档。</div>
</section>'''

# The existing one-slide deck is the user's established shell. Preserve its ID,
# and add the second page through the supported bundle API.
label='SkillHub洞察V1'
if 'data-label="商业化程度"' in s:label='商业化程度'
i=s.index('<section data-label="'+label+'"');j=s.index('</section>',i)+len('</section>')
s=s[:i]+page1+s[j:]
s=s.replace("label:'"+label+"'","label:'商业化程度'")
s=re.sub(r'\s+(?=<div class="slide-fit")',lambda m:eb.SEP,s)
if 'data-label="微信支付机制"' in s:
 a=s.index('<section data-label="微信支付机制"');b=s.index('</section>',a)+len('</section>')
 pid=re.search(r'data-page-id="([^"]+)"',s[a:b]).group(1)
 replacement=page2.replace('data-label="微信支付机制"',f'data-label="微信支付机制" data-page-id="{pid}"',1)
 s=s[:a]+replacement+s[b:]
if 'data-label="微信支付机制"' not in s:
 block='<div class="slide-fit" data-idx="1"><div class="slide-canvas">'+page2+'</div></div>'
 s=eb.insert_page(s,block,'商业化程度','机制','微信支付机制')
s=re.sub(r'\s+(?=<div class="slide-fit")',lambda m:eb.SEP,s)
s=eb.move_page(s,'微信支付机制','商业化程度')
s=s.replace("name:'SkillHub洞察'","name:'SkillPay商业化'")
s=re.sub(r'<title>.*?</title>','<title>腾讯 SkillHub / SkillPay 商业化洞察</title>',s,count=1,flags=re.S)
eb.set_template(lines,s);eb.save(target,lines);eb.verify(target)
print(target)
