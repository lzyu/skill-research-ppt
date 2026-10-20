from pathlib import Path
import importlib.util,re

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/skillhub/skillpay')
sp=importlib.util.spec_from_file_location('eb','/Users/tpy/.agents/skills/aico-ppt/scripts/edit-bundle.py');eb=importlib.util.module_from_spec(sp);sp.loader.exec_module(eb)
path=root/'skillhub-skillpay-commercialization-v2.html';lines=eb.load(path);s=eb.get_template(lines)
R='#b5333b';K='#1a1a1c';M='#585860';G='#d9dde2';B='#566472'
style="width:100%;height:100%;padding:44px 72px 48px;display:flex;flex-direction:column;background:#fff;font-family:'Noto Sans SC',sans-serif;overflow:hidden;position:relative;color:#1a1a1c;"
def txt(text,x,y,w,fs=21,color=K,weight=400,align='left',extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;line-height:1.4;color:{color};font-weight:{weight};text-align:{align};{extra}">{text}</div>'
def line(x,y,w,color=B,dash=False):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:0;border-top:2px {"dashed" if dash else "solid"} {color};"></div>'
def msg(a,b,y,label,color=B,dash=False,fs=21):
 lo=min(a,b);hi=max(a,b);direction='▶' if b>a else '◀'
 return line(lo,y,hi-lo,color,dash)+txt(direction,b-8,y-15,20,21,color,400,'center')+txt(label,lo+12,y-33,hi-lo-24,fs,color,500,'center','background:#fff;')
def node(x,y,w,title,body='',hot=False,h=91):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:1.5px solid {R if hot else G};border-radius:10px;background:#fff;padding:12px 14px;text-align:center;"><div style="font-size:24px;line-height:1.3;font-weight:700;color:{R if hot else K};">{title}</div><div style="font-size:21px;line-height:1.35;color:{M};margin-top:6px;">{body}</div></div>'
def va(x,y,h,label='',lx=None,lw=160):
 ret=f'<div style="position:absolute;left:{x}px;top:{y}px;height:{h}px;width:0;border-left:2px solid {B};"></div>'+txt('▼',x-10,y+h-15,22,20,B,400,'center')
 if label:ret+=txt(label,x+15 if lx is None else lx,y+8,lw,19,M)
 return ret
def head(title):
 return f'<div style="font-size:18px;letter-spacing:.08em;color:{R};margin-bottom:8px;">腾讯 SkillHub 商业化原理 <span style="float:right;color:#6c7078;font-family:\'JetBrains Mono\';letter-spacing:0;">2026.10.20 · V2</span></div><h3 style="margin:0 0 18px;font-size:44px;font-weight:600;letter-spacing:-.02em;line-height:1.2;">{title}</h3>'
def sub(title,body,top=0):
 return f'<div style="margin-top:{top}px;"><div style="font-size:25px;font-weight:700;line-height:1.35;">{title}</div><div style="font-size:21px;line-height:1.48;color:{M};margin-top:7px;">{body}</div></div>'

actors=[(105,'Agent / 用户'),(455,'商户后端'),(825,'微信支付'),(1125,'SkillHub')]
seq=''
for x,name in actors:
 seq+=txt(name,x-110,0,220,25,K,700,'center')
 seq+=f'<div style="position:absolute;left:{x}px;top:43px;height:559px;border-left:1px dashed #bfc5cc;"></div>'
for a,b,y,t,col,d in [
 (105,455,81,'① 调用付费服务',B,False),
 (455,825,128,'② 传统下单：商户、金额、订单号',K,False),
 (825,455,175,'code_url / prepay_id',B,True),
 (455,825,222,'③ x402：签名 + 预支付标识',R,False),
 (825,1125,269,'身份 / 签名校验*',R,True),
 (1125,825,316,'确认开发者身份*',R,True),
 (825,455,363,'返回 payment_code',B,True),
 (455,105,410,'④ 402 + 支付码 + 业务关联 ID',B,False),
 (105,825,457,'⑤ 官方支付工具拉起，用户以 AI 专属卡逐笔确认',R,False),
 (825,455,504,'⑥ 回调 / 查单确认 SUCCESS',R,False),
 (105,455,551,'⑦ 沿用原业务关联 ID 取结果',B,False),
 (455,105,598,'交付结果 / 返回生成状态',B,True),
]:seq+=msg(a,b,y,t,col,d)
seq+=txt('* 按 SkillHub 官方教程表达逻辑校验关系，内部调用方式、缓存和同步依赖未公开。',0,615,1240,17,M)

aside=sub('第一次下单确定商户和金额','传统微信订单保存商户、金额和回调地址。此时仍待支付。')
aside+=sub('第二次预下单建立 Agent 入口','x402 将既有预支付标识登记到微信 AI 支付，换取限时 payment_code。它不新增一次扣款。',22)
aside+=sub('两套验签分别确认身份与付款','SkillHub 开发者签名用于预下单身份校验；商户另验微信回调 / 查单结果，确认这笔订单已付。',22)
aside+=sub('交易款由用户直接付给创作者','平台目前暂免技术服务费，支付渠道费用与结算按渠道规则。供给占比无法推算 GMV。',22)
stats=f'''<div style="display:grid;grid-template-columns:1.2fr 1.05fr 1fr;gap:28px;border-top:2px solid {R};border-bottom:1px solid {G};padding:10px 0 13px;margin-bottom:20px;">
<div><b style="font-size:28px;">付费标签约 10.0%</b><div style="font-size:19px;color:{M};margin-top:4px;">19,962 / 199,545 条，含 paid 与 alipay</div></div>
<div><b style="font-size:28px;">需 API Key 约 19.3%</b><div style="font-size:19px;color:{M};margin-top:4px;">38,568 条，外部凭证依赖与付费分别统计</div></div>
<div><b style="font-size:28px;">平台技术服务费暂免</b><div style="font-size:19px;color:{M};margin-top:4px;">真实成交、复购与平台收入尚无可核验全站数据</div></div></div>'''
roles=[('供给准入','企业认证、绑定微信商户号'),('商品化发布','定价、版本包、支付链路审核'),('分发到 Agent','发现与安装入口、宿主接入'),('交易身份信任','开发者密钥及教程所述验签')]
rolehtml=''.join(f'<div><div style="font-size:23px;font-weight:700;">{a}</div><div style="font-size:21px;line-height:1.4;color:{M};margin-top:5px;">{b}</div></div>' for a,b in roles)
page1=f'''<section data-label="双下单与信任链" data-page-type-id="layered-platform-ops-rail" data-template-id="work-report" style="{style}">{head('两次下单接入 Agent，SkillHub 提供商户验签与分发')}{stats}
<div style="flex:1;min-height:0;display:grid;grid-template-columns:1240px minmax(0,1fr);gap:30px;">
<div style="position:relative;min-width:0;height:641px;">{seq}</div>
<div style="border-left:1px solid {G};padding-left:26px;">{aside}</div></div>
<div style="border-top:2px solid {R};padding-top:13px;margin-top:12px;display:grid;grid-template-columns:repeat(4,1fr);gap:24px;">{rolehtml}</div>
<div style="font-size:13px;color:#6c7078;margin-top:13px;">统计为 2026-10-20 公开 API 非原子快照，按资产条目计；paid 不等同微信已开户或成交。时序采用官方共识，微信 API 与 SkillHub Demo 版本差异及来源详见备注。</div>
</section>'''

# The WorkRally API returns two different identifiers in one response.
ids=node(0,23,430,'invoke 返回 HTTP 402','Body: payment_id = WPAY_…<br/>Header / WeixinPay 节点：<br/>WeixinPay-Required = PMT_…',False,151)
ids+=msg(430,650,45,'支付码',R)+node(650,0,435,'交给微信支付工具','用于拉起付款，最长 15 分钟',True,92)
ids+=msg(430,650,140,'业务关联 ID',B)+node(650,98,435,'content {payment_id}','沿用同一任务查询结果',False,92)
ids+=txt('两者来自同一次 invoke 响应，各自承担对应步骤。Agent 无需解析支付码。',0,192,1090,21,M)

states=node(0,38,250,'待支付','402 / code: NOT_PAID')
states+=node(420,38,250,'generating','已付，生成中')
states+=node(840,38,250,'delivered','交付同一 result_url',True)
states+=msg(250,420,82,'验付后启动',B,False,19)
states+=msg(670,840,82,'生成成功',B,False,19)
states+=va(125,129,75,'未支付超时',140,180)
states+=node(0,204,250,'expired','旧 payment_id 终止')
states+=va(545,129,75,'生成失败 / 超时',560,200)
states+=node(420,204,250,'failed','失败，查看退款状态')
states+=msg(670,840,249,'退款确认',B,False,19)
states+=node(840,204,250,'refunded','退款完成终态')
states+=txt('状态图依据 WorkRally 公开调用契约；支付状态、服务状态及退款状态由商户分别管理。',0,314,1090,17,M)

right=sub('生成中：继续原任务','HTTP 200 + generating 仍未交付。按 retry_after_seconds（5 秒）用同一 payment_id 重试 content。')
right+=sub('已交付：重复取同一结果','delivered 返回相同 result_url。WorkRally 契约承诺同任务不重复扣费、不重复生成。',19)
right+=sub('终态：先处理旧任务，再决定新购','failed / refunded / expired 按错误规则结束旧任务。按契约重新 invoke，不能把“生成中”误判为需要再买。',19)
right+=f'<div style="border-top:1px solid {G};margin-top:23px;padding-top:17px;font-size:25px;font-weight:700;">服务履约仍由商户保证</div>'
right+=sub('请求、回调、履约各有幂等约束','稳定业务订单防重复建单；验签后去重支付通知；唯一任务执行权和持久结果防重复生成。',10)
right+=f'<div style="font-size:21px;color:{M};line-height:1.48;margin-top:13px;">官方 Demo 使用内存 map，不能证明并发、重启与退款恢复已具备生产保证。</div>'

page2=f'''<section data-label="凭据与履约状态" data-page-type-id="layered-platform-ops-rail" data-template-id="work-report" style="{style}">{head('payment_code 发起付款，payment_id 串联任务与交付')}
<div style="border-top:2px solid {R};border-bottom:1px solid {G};padding:13px 0 15px;margin-bottom:20px;font-size:23px;line-height:1.4;"><b>真实案例：腾讯 WorkRally 图片生成 ¥0.36 / 次</b><span style="color:{M};margin-left:24px;">技能包可公开获取，用户无需业务 API Key；付费点在远程图片服务。</span></div>
<div style="flex:1;min-height:0;display:grid;grid-template-columns:1090px minmax(0,1fr);gap:36px;">
<div><div style="font-size:25px;font-weight:700;">同一响应里的两个标识，走向不同接口</div><div style="height:235px;position:relative;">{ids}</div><div style="font-size:25px;font-weight:700;margin-top:0;">支付成功之后，商户还要完成业务状态迁移</div><div style="height:340px;position:relative;">{states}</div></div>
<div style="border-left:1px solid {G};padding-left:28px;">{right}</div></div>
<div style="border-top:2px solid {R};padding-top:13px;margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:32px;">
<div><div style="font-size:23px;font-weight:700;">支付回调的真实性与保密性分开处理</div><div style="font-size:21px;line-height:1.4;color:{M};margin-top:5px;">商户用微信支付公钥 / 平台证书验签，用 APIv3 密钥解密。SkillHub 开发者私钥只用于 AI 预下单身份。</div></div>
<div><div style="font-size:23px;font-weight:700;">实现必须选定同一版本契约</div><div style="font-size:21px;line-height:1.4;color:{M};margin-top:5px;">微信当前 API 采用 Authorization + JSON 对象；SkillHub Demo 仍采用旧端点和 Body 鉴权，不能混接。</div></div></div>
<div style="font-size:13px;color:#6c7078;margin-top:13px;">来源：WorkRally SKILL.md / invoke-flow / troubleshooting，微信 x402 API / FAQ / 支付回调，SkillHub 商户 Demo。本次为公开文档与源码核查，未真实交易；详细证据与恢复边界见伴生文档。</div>
</section>'''
oldlabels=['商业化程度','微信支付机制']
newlabels=['双下单与信任链','凭据与履约状态']
for old,new,sec in zip(oldlabels,newlabels,[page1,page2]):
 label=old if f'data-label="{old}"' in s else new
 a=s.index(f'<section data-label="{label}"');b=s.index('</section>',a)+len('</section>')
 pid=re.search(r'data-page-id="([^"]+)"',s[a:b]).group(1)
 sec=sec.replace(f'data-label="{new}"',f'data-label="{new}" data-page-id="{pid}"',1)
 s=s[:a]+sec+s[b:];s=s.replace(f"label:'{label}'",f"label:'{new}'")
s=re.sub(r'<title>.*?</title>','<title>腾讯 SkillHub / SkillPay 商业化原理 V2</title>',s,count=1,flags=re.S)
eb.set_template(lines,s);eb.save(path,lines);eb.verify(path)
print(path)
