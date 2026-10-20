from pathlib import Path
import importlib.util,re

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt')
sp=importlib.util.spec_from_file_location('eb','/Users/tpy/.agents/skills/aico-ppt/scripts/edit-bundle.py');eb=importlib.util.module_from_spec(sp);sp.loader.exec_module(eb)
target=root/'gpt-alipay-research.html';lines=eb.load(target);s=eb.get_template(lines)
R='#b5333b';K='#1a1a1c';M='#585860';G='#d9dde2';B='#566472'
style="width:100%;height:100%;padding:44px 72px 48px;display:flex;flex-direction:column;background:#fff;font-family:'Noto Sans SC',sans-serif;overflow:hidden;position:relative;color:#1a1a1c;"
def t(text,x,y,w,fs=21,c=K,b=400,align='left',extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;line-height:1.4;color:{c};font-weight:{b};text-align:{align};{extra}">{text}</div>'
def hl(x,y,w,c=B,d=False):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:0;border-top:2px {"dashed" if d else "solid"} {c};"></div>'
def vl(x,y,h,c=B,d=False):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:0;height:{h}px;border-left:2px {"dashed" if d else "solid"} {c};"></div>'
def ar(a,b,y,label='',c=B,d=False,fs=21):
 lo,hi=min(a,b),max(a,b)
 out=hl(lo,y,hi-lo,c,d)+t('▶' if b>a else '◀',b-8,y-15,20,21,c,400,'center')
 if label:out+=t(label,lo+10,y-34,hi-lo-20,fs,c,500,'center','background:#fff;')
 return out
def down(x,y,h,label='',lx=None,lw=180):
 out=vl(x,y,h)+t('▼',x-10,y+h-15,22,20,B,400,'center')
 if label:out+=t(label,x+15 if lx is None else lx,y+12,lw,19,M)
 return out
def box(x,y,w,h,title,body='',hot=False,fs=24):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:1.5px solid {R if hot else G};border-radius:14px;background:#fff;padding:15px 17px;text-align:center;"><div style="font-size:{fs}px;line-height:1.3;font-weight:700;color:{R if hot else K};">{title}</div><div style="font-size:21px;line-height:1.4;color:{M};margin-top:8px;">{body}</div></div>'
def sub(title,body,mt=0):return f'<div style="margin-top:{mt}px;"><div style="font-size:25px;font-weight:700;line-height:1.35;">{title}</div><div style="font-size:21px;line-height:1.48;color:{M};margin-top:8px;">{body}</div></div>'
def head(n,topic,title):return f'<div style="font-size:18px;letter-spacing:.07em;color:{R};margin-bottom:8px;">支付宝 SkillPay 与 MachinePay 原理研究 <span style="float:right;color:#6c7078;letter-spacing:0;">2026.10.20 · {n}/4</span></div><h3 style="margin:0 0 18px;font-size:44px;font-weight:600;letter-spacing:-.02em;line-height:1.2;">{title}</h3>'
def footer(text):return f'<div style="font-size:13px;color:#6c7078;margin-top:14px;">{text} 详细来源、代码版本与证据边界见备注及伴生研究文档。</div>'
def section(label,content):return f'<section data-label="{label}" data-page-type-id="layered-platform-ops-rail" data-template-id="work-report" style="{style}">{content}</section>'

# P1: one shared purchase handshake, two distinct fulfillment models.
top=''
for x,title,body in [(0,'作者提交源 Skill','名称、文件、价格与收费模式'),(470,'SkillPay 商品化','扫描审核、版本、试用和权益'),(940,'作者自主分发','购买指令、二维码或商品页')]:
 top+=box(x,0,390,105,title,body)
top+=ar(390,470,53)+ar(860,940,53)
top+=t('作者负责创造与维护，平台承接付款之后的交付和持续经营。',1363,12,413,21,M)

fork=box(0,18,230,102,'Agent 请求资源','没有有效权益')
fork+=ar(230,322,69)
fork+=box(322,18,278,102,'402 + 付款要求','保留原请求上下文')
fork+=ar(600,690,69)
fork+=box(690,18,410,102,'支付宝付款后恢复原请求','SkillPay 验付并建立权益')
fork+=vl(895,120,56)+hl(265,176,630)+down(265,176,38)+down(835,176,38)
fork+=box(0,214,530,215,'买断：交付完整源文件','完整 Skill 进入本地 Agent<br/>一次购买可下载该 Skill 全部版本<br/>后续由本地读取、执行和保存')
fork+=box(570,214,530,215,'订阅：交付期限内使用权','本地保留入口与公开资源<br/>完整原文留云端，按任务提供指导<br/>当前不自动续费，到期重新取得权益')
fork+=t('支付后按商品模式分叉，订阅并不等于每次任务重新扣款。',0,451,1100,21,R,500)

aside=sub('商品 ID 定位售卖对象，交易号追踪付款','merchantId / productId 说明“谁的哪个商品”；支付凭据用于恢复本轮请求，后续还要判断权益是否可用。')
aside+=sub('平台管理交付，而非只弹出收银台','商品模式、试用、版本和可用期决定后续交付。付费成功后仍可能处于权益发放中或发放失败。',24)
aside+=sub('资金直达作者，费率不能据此推断','官网称款项实时到作者支付宝账户。退款由作者处理，周期订单整单全退；未查到统一公开抽佣费率。',24)
check=''
for x,a,b in [(0,'支付确认','钱是否付给对应交易'),(454,'权益可用','当前买家是否仍可使用'),(908,'资源交付','文件或执行指导是否取得'),(1362,'任务完成','本地执行与产物是否合格')]:
 check+=t(a,x,0,410,24,K,700)+t(b,x,40,410,21,M)
page1=section('Skill商品与交付',head(1,'SkillPay','SkillPay 经营 Skill 商品，付款后分为源文件与使用权两种交付')+
 f'<div style="height:123px;position:relative;border-top:2px solid {R};padding-top:14px;margin-bottom:20px;"><div style="position:relative;top:13px;">{top}</div></div>'+
 f'<div style="flex:1;min-height:0;display:grid;grid-template-columns:1100px minmax(0,1fr);gap:36px;"><div><div style="font-size:27px;font-weight:700;margin:12px 0 8px;">同一购买握手，取得不同商品权益</div><div style="height:500px;position:relative;">{fork}</div></div><div style="border-left:1px solid {G};padding-left:28px;padding-top:12px;">{aside}</div></div>'+
 f'<div style="border-top:2px solid {R};padding-top:14px;margin-top:15px;"><div style="font-size:24px;font-weight:700;margin-bottom:15px;">沿四个判断点恢复原任务</div><div style="position:relative;height:85px;">{check}</div></div>'+footer('来源：SkillPay 官方博客、FAQ、上架页、2026-09-29 更新日志和官方消费侧支付规则。此处聚焦 Skill 商品平台。'))

# P2: semantic trust/compute boundaries follow the official SVG.
cloud=f'<div style="position:absolute;left:0;top:0;width:1120px;height:664px;border:1px solid {G};border-radius:14px;"></div>'
cloud+=vl(555,45,595,G,True)+t('本地 Agent',20,15,500,27,K,700,'center')+t('SkillPay 云端保护',590,15,500,27,K,700,'center')
cloud+=box(35,73,455,115,'用户任务 + 影子 Skill','本地入口、公开资源与必要上下文')
cloud+=down(262,188,48)
cloud+=ar(262,665,236,'当前任务请求 + 有效上下文',B,False,19)
cloud+=box(665,186,420,102,'权益与请求判断','有效期、试用及能力边界')
cloud+=down(875,288,43)
cloud+=box(665,331,420,124,'完整原文隔离保存','根据当前任务生成有限执行文本<br/>拒绝套取，裁剪无关知识')
cloud+=ar(665,490,396,'任务专用指导',R,False,19)
cloud+=box(35,339,455,115,'本地校验指导与输入','信息不足先追问，信息充分再执行')
cloud+=down(262,454,51)
cloud+=box(35,505,455,112,'运行工具并形成最终结果','脚本、数据处理、文件产物由本地完成')
cloud+=t('云端不运行脚本<br/>也不计算最终答案',637,493,475,25,R,700,'center')
cloud+=t('云端输出的是执行方法，本地仍承担工具权限和产物检查。',615,581,480,21,M,400,'center')
protect=sub('正常任务：返回必要指导','围绕当前问题，只披露完成任务所需的方法，不把完整 Skill 作为回答。')
protect+=sub('套取全文：拒绝并回到任务','角色扮演、覆盖指令、编码或多轮拼接等请求，属于持续防护与回归评测范围。',23)
protect+=sub('边界请求：帮助与最小披露并行','有限执行文本仍能被观察。保护目标是提高整份原文复制成本，不能据此声称不可破解。',23)
protect+=sub('原文保护与数据传输分别判断','云端会接收任务和有效上下文。具体资料传输依实现，不能从“原文不落地”推出“用户资料绝不出云”。',23)
page2=section('云端保护与执行',head(2,'SkillPay','订阅原文留云端，云端给任务指导，本地 Agent 继续执行')+
 f'<div style="border-top:2px solid {R};padding-top:13px;margin-bottom:22px;font-size:23px;line-height:1.4;">云端保护控制知识披露；用户的 Agent 仍负责校验、脚本执行和最终输出。</div>'+
 f'<div style="flex:1;min-height:0;display:grid;grid-template-columns:1120px minmax(0,1fr);gap:36px;"><div style="height:664px;position:relative;">{cloud}</div><div style="padding-left:28px;border-left:1px solid {G};">{protect}</div></div>'+
 f'<div style="border-top:2px solid {R};padding-top:13px;margin-top:15px;display:grid;grid-template-columns:1fr 1fr;gap:35px;">'+sub('访问门槛：权益仍需有效','到期、退款、冻结或额度等状态可能影响可用性。订阅不代表不限次数，试用次数不等于完整任务数。')+sub('执行门槛：拿到指导后还要完成任务','平台只返回必要指导。本地仍需检查输入、工具权限和产物，拿到指导不等于任务已经完成。')+'</div>'+footer('依据官方云端保护/防御架构图和消费者前端状态重绘；图中的任务与上下文为架构语义，不是已公开的生产 HTTP 字段规范。'))

# P3: online RMB A402 flow, not the generic /settle graphic.
seq=''
for x,name in [(95,'买家 Agent'),(465,'商户 API'),(830,'支付宝 / 支付工具'),(1120,'用户')]:
 seq+=t(name,x-125,0,250,25,K,700,'center')+vl(x,45,595,G,True)
msgs=[(95,465,85,'① 请求付费资源',B,False),(465,95,174,'② 402 + Payment-Needed',R,True),(95,830,221,'③ 提交付款要求和原任务上下文',B,False),(830,1120,268,'展示商户与金额',B,False),(1120,830,315,'④ 确认支付',R,False),(830,95,362,'取得 trade_no + payment_proof（及 client_session）',B,True),(95,465,409,'⑤ 原请求 + Payment-Proof',R,False),(465,830,456,'⑥ payment.verify',R,False),(830,465,503,'active + 金额 + 订单 + 资源',B,True),(465,95,597,'⑦ 交付结果',B,True),(465,830,644,'⑧ fulfillment.confirm（履约回执）',B,True)]
for a,b,y,label,c,d in msgs:seq+=ar(a,b,y,label,c,d,20)
seq+=t('本地建单，RSA2 签报价',320,112,300,21,K,500,'center','background:#fff;')
seq+=t('商户对本地账并锁定唯一履约',280,529,390,21,K,500,'center','background:#fff;')

payload=sub('Payment-Needed：付款前的签名报价','金额 / 币种、out_trade_no、resource_id、pay_before、卖家与 service_id，连同 seller_signature 一起封装。')
payload+=f'<div style="font-size:21px;color:{M};line-height:1.45;margin-top:10px;">商户本地用应用私钥做 RSA2 签名，生成报价无需先调用支付宝扣款。</div>'
payload+=sub('Payment-Proof：付款后的验付材料','包含 trade_no、payment_proof，以及通道需要时的 client_session。商户将它们交支付宝在线 verify。',24)
payload+=sub('Base64URL 负责封装，真实性另行校验','解码可读不代表可信。报价签名、支付宝验付和商户业务核对各自承担不同验证。',24)
payload+=sub('图示采用用户确认支付路径','钱包已开通不等于任意消费均已授权。自动付款须符合另行授予的范围和风控条件。',24)
page3=section('MachinePay支付协议',head(3,'MachinePay','MachinePay 先签报价，付款后带票重试，商户在线验付')+
 f'<div style="border-top:2px solid {R};padding-top:13px;margin-bottom:20px;font-size:23px;line-height:1.4;">接入前注册商户应用与服务：service_id 关联服务 URL、单价及说明；一次调用再生成本地订单。</div>'+
 f'<div style="flex:1;min-height:0;display:grid;grid-template-columns:1240px minmax(0,1fr);gap:30px;"><div style="position:relative;height:670px;">{seq}</div><div style="border-left:1px solid {G};padding-left:26px;">{payload}</div></div>'+
 f'<div style="border-top:2px solid {R};margin-top:12px;padding-top:13px;font-size:21px;line-height:1.45;">人民币接入指南使用 payment.verify 与 fulfillment.confirm。产品页的通用 /verify、/settle、交易哈希图，不能直接当成这套人民币 API。</div>'+footer('主图按在线指南的交付后回执路径；官方代码模板也有先确认后返回结果的顺序，具体差异见备注。确认接口不是第二次扣款。'))

# P4: reconcile two records, then manage exactly which local work may resume.
ledger=box(0,23,445,165,'支付宝交易事实','trade_no + payment_proof<br/>active、金额、订单与资源返回值')
ledger+=ar(445,645,105,'verify 后核对',R,False,19)
ledger+=box(645,23,445,165,'商户业务订单','out_trade_no + resource_id<br/>价格、请求摘要、结果与履约状态')
ledger+=t('核对当前订单买的是什么，再决定是否执行。active=true 不能代替业务关联和并发控制。',0,212,1090,21,M)
states=box(0,28,225,111,'待支付','本地订单与签名报价')
states+=ar(225,286,84)
states+=box(286,28,225,111,'已验付','已匹配本次购买')
states+=ar(511,572,84)
states+=box(572,28,260,111,'PENDING_CONFIRM','唯一结果已持久保存',True,22)
states+=ar(832,891,84)
states+=box(891,28,199,111,'FULFILLED','回执确认完成',False,22)
states+=down(702,139,60)
states+=box(488,199,428,105,'回执失败或状态未知','恢复同一订单，按错误码核实状态')
states+=t('确认成功后转入最终完成',916,201,170,19,M)
states+=t('重试回执 / 读已有结果<br/>不重新生成，也不直接要求再付一次',0,219,415,22,R,600)
states+=t('这是 alipay/ai 当前模板的本地状态抽象，数据库事务和幂等端口仍需商户实现。',0,314,1090,17,M)
rules=sub('业务请求也要固定','示例 resource_id 可以只是路径。同一路径接收不同 prompt 或文件时，商户还应绑定请求摘要和购买范围。')
rules+=sub('网络失败先恢复原单','回执待确认已有业务结果，应重试确认或取存量结果。支付状态未知不应直接创建新订单要求再买。',23)
rules+=sub('回执确认与资金结算分开理解','fulfillment.confirm 的含义是“商家履约回执”。公共接口没有公开其与资金释放、退款的完整内部条件。',23)
rules+=sub('过期与重试策略需按版本核对','当前模板和 ACT 映射例的截止检查、回执顺序不同；重复确认也可能返回交易状态错误。',23)
page4=section('验付与恢复',head(4,'MachinePay','支付宝验证支付事实，商户核对业务账并恢复唯一履约')+
 f'<div style="border-top:2px solid {R};padding-top:14px;margin-bottom:18px;font-size:23px;line-height:1.4;">验付接口返回成功后，还要匹配金额、订单、资源和交易号，保留并发控制与可恢复的结果状态。</div>'+
 f'<div style="flex:1;min-height:0;display:grid;grid-template-columns:1090px minmax(0,1fr);gap:36px;"><div><div style="font-size:26px;font-weight:700;">同一交易，需要对齐两边记录</div><div style="position:relative;height:245px;">{ledger}</div><div style="font-size:26px;font-weight:700;">生成结果与履约回执分开持久化</div><div style="position:relative;height:345px;">{states}</div></div><div style="border-left:1px solid {G};padding-left:28px;">{rules}</div></div>'+
 f'<div style="border-top:2px solid {R};padding-top:13px;margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:36px;">'+sub('SkillPay：经营商品权益和知识交付','决定买断文件、订阅期限、试用、版本和云端原文保护；有效权益下的使用不等于每次重新购买。')+sub('MachinePay：让资源请求具备收款与验付协议','商户签报价，支付宝付款与验付，商户承担业务绑定、幂等和交付。两者复用支付能力，不宜推定全部流量走同一内部链路。')+'</div>'+footer('原理图依据公开 API、alipay/ai 固定 commit 模板及 ACT 对接例；非支付宝内部数据库状态。amount、client_session 等文档差异详见备注。'))

labels=['Skill商品与交付','云端保护与执行','MachinePay支付协议','验付与恢复']
pages=[page1,page2,page3,page4]
# Reuse two pages of the established shell, then add the other two via the
# supported bundle API so page identity, DOM and navigation stay synchronized.
for old,new,sec in zip(['双下单与信任链','凭据与履约状态'],labels[:2],pages[:2]):
 lab=old if f'data-label="{old}"' in s else new
 a=s.index(f'<section data-label="{lab}"');b=s.index('</section>',a)+len('</section>')
 pid=re.search(r'data-page-id="([^"]+)"',s[a:b]).group(1)
 sec=sec.replace(f'data-label="{new}"',f'data-label="{new}" data-page-id="{pid}"',1)
 s=s[:a]+sec+s[b:];s=s.replace(f"label:'{lab}'",f"label:'{new}'")
for label,sec in zip(labels[2:],pages[2:]):
 if f'data-label="{label}"' in s:
  a=s.index(f'<section data-label="{label}"');b=s.index('</section>',a)+len('</section>')
  pid=re.search(r'data-page-id="([^"]+)"',s[a:b]).group(1)
  s=s[:a]+sec.replace(f'data-label="{label}"',f'data-label="{label}" data-page-id="{pid}"',1)+s[b:]
 else:
  s=re.sub(r'\s+(?=<div class="slide-fit")',lambda m:eb.SEP,s)
  block='<div class="slide-fit" data-idx="2"><div class="slide-canvas">'+sec+'</div></div>'
  s=eb.insert_page(s,block,labels[0],'原理',label)
  s=re.sub(r'\s+(?=<div class="slide-fit")',lambda m:eb.SEP,s)
  s=eb.move_page(s,label,labels[labels.index(label)-1])
s=s.replace("name:'SkillPay商业化'","name:'支付宝原理研究'")
s=re.sub(r'<title>.*?</title>','<title>支付宝 SkillPay / MachinePay 原理研究</title>',s,count=1,flags=re.S)
eb.set_template(lines,s);eb.save(target,lines);eb.verify(target)
print(target)
