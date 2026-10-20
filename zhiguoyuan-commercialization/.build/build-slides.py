from pathlib import Path
import importlib.util,re

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt')
sp=importlib.util.spec_from_file_location('eb','/Users/tpy/.agents/skills/aico-ppt/scripts/edit-bundle.py');eb=importlib.util.module_from_spec(sp);sp.loader.exec_module(eb)
target=root/'zhiguoyuan-skill-commercialization.html';lines=eb.load(target);s=eb.get_template(lines)
R='#b5333b';K='#1a1a1c';M='#585860';G='#d9dde2';B='#566472'
style="width:100%;height:100%;padding:44px 72px 48px;display:flex;flex-direction:column;background:#fff;font-family:'Noto Sans SC',sans-serif;overflow:hidden;position:relative;color:#1a1a1c;"
def t(text,x,y,w,fs=23,c=K,b=400,align='left',extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;line-height:1.45;color:{c};font-weight:{b};text-align:{align};{extra}">{text}</div>'
def hl(x,y,w,c=G,d=False):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:0;border-top:2px {"dashed" if d else "solid"} {c};"></div>'
def vl(x,y,h,c=G):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:0;height:{h}px;border-left:1px solid {c};"></div>'
def ar(a,b,y):return hl(a,y,b-a,B)+t('▶',b-8,y-15,20,21,B,400,'center')
def node(x,y,w,title,body):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:104px;border:1px solid {G};border-radius:14px;background:#fff;padding:12px 14px;"><div style="font-size:24px;font-weight:700;line-height:1.35;">{title}</div><div style="font-size:21px;color:{M};margin-top:6px;line-height:1.4;">{body}</div></div>'
def head(n,title):return f'<div style="font-size:18px;letter-spacing:.06em;color:{R};margin-bottom:8px;">智果园 Skill 资产商业化演进 <span style="float:right;color:#6c7078;letter-spacing:0;">2026.10.20 · {n}/2</span></div><h3 style="margin:0 0 18px;font-size:44px;font-weight:600;letter-spacing:-.02em;line-height:1.2;">{title}</h3>'
def foot(text):return f'<div style="font-size:13px;color:#6c7078;margin-top:12px;">{text} 逐项依据与产品边界见备注及伴生研究文档。</div>'
def section(label,content,ptype):return f'<section data-label="{label}" data-page-type-id="{ptype}" data-template-id="work-report" style="{style}">{content}</section>'

# Two parallel platform columns explain what is sold, what the platform owns,
# and which mechanism can inform Huawei's own commercial product design.
content=''
for x,platform,tag in [(0,'阿里：SkillPay + MachinePay','把知识交付与支付协议分别做深'),(916,'腾讯：SkillHub SkillPay','让免费 Skill 连接可收费的远程服务')]:
 content+=t(platform,x,14,850,31,K,700)+t(tag,x,65,850,24,R,500)
content+=vl(888,15,537)
rows=[
 (125,'卖什么',
  'SkillPay 买断交付完整源文件；周期订阅把原文留云端，按任务给指导，本地 Agent 执行。',
  '公开 Skill 包负责发现和调用；远程业务后端提供付费能力。WorkRally 图像生成展示价 0.36 元/次。'),
 (259,'平台做得好',
  '商品模式、试用、价格、版本和权益统一经营。402 付款后恢复原任务，按权益完成对应交付。',
  '企业认证、商户绑定、开发者身份、定价审核与分发相连接；平台官方样例与第三方服务共同示范收费。'),
 (393,'交易与履约',
  'MachinePay 以签名报价、付款凭证、在线验付和履约回执服务 API 收款；商户仍须做业务核对与幂等。',
  '微信订单登记为 AI 支付码，用户逐笔确认。商户验付后交付；WorkRally 用同一任务标识恢复取结果。')
]
for y,label,left,right in rows:
 for x,body in [(0,left),(916,right)]:
  content+=t(label,x,y,155,23,R,600)+t(body,x+168,y,670,24,K)
 for x in (0,916):content+=hl(x,y+113,850)
content+=t('值得借鉴',0,537,155,23,R,600)+t('先定义购买权益与交付形态，再把试用、续购和持续更新连成商品经营。',168,537,670,24,K,600)
content+=t('值得借鉴',916,537,155,23,R,600)+t('保留低门槛安装入口，把收费控制放在持续提供价值的服务端。',1084,537,670,24,K,600)
baseline=hl(0,0,1776,R)+t('智果园已有可沿用的起点',0,17,1776,28,K,700)
baseline+=t('资产共享与访问授权已具备',0,66,840,24,K,700)+t('独立仓库、SKILL.md 与元数据、许可证、发布审核；指定用户可见、申请审批与撤销、公开安装入口。',0,108,840,23,M)
baseline+=vl(888,66,132)+t('Skill 交易闭环仍需核实与打通',916,66,860,24,K,700)+t('公开 Skill 文档尚未充分披露价格、订单、付费权益、计量和结算；“允许使用”仍需连接可核验的购买权益。',916,108,860,23,M)
page1=section('平台优势与现状',head(1,'阿里经营 Skill 商品权益，腾讯连接付费服务与生态分发')+
 f'<div style="border-top:2px solid {R};position:relative;height:657px;">{content}</div>'+
 f'<div style="position:relative;height:217px;">{baseline}</div>'+foot('来源：支付宝 SkillPay 博客/上架与 MachinePay 指南；SkillHub 官网/教程、WorkRally 契约；华为新版 Skill 托管/发布/管理文档。'),
 'strategy-capability-portfolio')

# Explicit reuse classes are the main decision aid. Existing commercial
# foundations are separated from the new Skill-specific orchestration.
reuse=''
cols=[
 (0,'直接沿用：新版资产广场',[
 ('资产供给与分发','仓库、标准包、元数据、许可证、审核、安装入口。继续兼容免费开源 Skill。'),
 ('访问范围与审批','沿用可见/可用分离及申请撤销；保留企业共享和指定用户授权。'),
 ('复用边界','既有审批控制访问；付费权益还须绑定买家、商品、版本及可用额度。')]),
 (604,'对接复用：华为云商业底座',[
 ('云商店订购与结算','按商品类型和合作模式复用订购、退订及结算；补齐 Skill 与商品/订单映射。'),
 ('Agents 网关鉴权与计量','已有路由、鉴权、用量解析；适配后端与计费口径。当前默认北京四。'),
 ('宿主与外部支付','打通 CodeArts / OfficeAce 等消费端；外部支付另核签约、宿主工具及身份接入。')]),
 (1208,'智果园补齐：Skill 商业编排',[
 ('商品、试用与服务端权益','区分买断文件/订阅/远程按量；定义 SKU、价格和许可，订单驱动授权。'),
 ('任务履约与异常恢复','固定请求和订单，验付、验权后执行；重试不重复扣次，失败可恢复或补偿。'),
 ('质量与作者经营','上架需补任务效果/安全/收费测试；提供订单收益、退款对账及申诉入口。')])
]
for x,title,items in cols:
 reuse+=t(title,x,18,568,27,K,700)
 for j,(a,b) in enumerate(items):
  y=77+j*130
  reuse+=t(a,x,y,565,24,R,600)+t(b,x,y+40,555,23,M)
reuse+=vl(583,19,422)+vl(1187,19,422)
flow=hl(0,0,1776,R)+t('首期建议：免费 Skill 入口 + 付费远程能力，先完成一条可对账的交易闭环',0,18,1776,28,K,700)
flow+=node(0,75,297,'发现与安装','绑定 asset_id / 版本')+ar(297,356,127)
flow+=node(356,75,297,'试用或购买','关联商品、订单与买家')+ar(653,712,127)
flow+=node(712,75,297,'服务端验权','限额、有效期与请求绑定')+ar(1009,1068,127)
flow+=node(1068,75,297,'执行与计量','同一任务只记一次消费')+ar(1365,1424,127)
flow+=node(1424,75,352,'交付与对账','失败恢复 / 补偿 / 售后')
flow+=t('验收以付费任务履约为准：重复请求不重复扣费，已付未交付可恢复，退款与权益及账单一致。',0,199,1776,23,R,600)
prior=hl(0,0,1776)+t('后续演进',0,17,180,24,K,700)+t('知识型高价值 Skill 再评估云端原文保护与组织订阅。源文件买断需讲清许可，保护范围不应承诺超出交付方式。',195,17,1581,23,M)
page2=section('复用与补齐路线',head(2,'智果园复用资产与云商店底座，重点补齐 Skill 商业编排')+
 f'<div style="position:relative;height:474px;border-top:2px solid {R};">{reuse}</div>'+
 f'<div style="position:relative;height:267px;">{flow}</div>'+
 f'<div style="position:relative;height:105px;">{prior}</div>'+foot('对接复用均为建议，未据此认定 Skill 广场已集成。云商店商品能力依类型/合作模式而异；阿里云端保护不等于可直接嵌入的开放服务。'),
 'layered-platform-ops-rail')

for old,new,sec in zip(['双下单与信任链','凭据与履约状态'],['平台优势与现状','复用与补齐路线'],[page1,page2]):
 lab=old if f'data-label="{old}"' in s else new
 a=s.index(f'<section data-label="{lab}"');b=s.index('</section>',a)+len('</section>')
 pid=re.search(r'data-page-id="([^"]+)"',s[a:b]).group(1)
 sec=sec.replace(f'data-label="{new}"',f'data-label="{new}" data-page-id="{pid}"',1)
 s=s[:a]+sec+s[b:];s=s.replace(f"label:'{lab}'",f"label:'{new}'")
s=s.replace("name:'SkillPay商业化'","name:'智果园商业化演进'")
s=re.sub(r'<title>.*?</title>','<title>智果园 Skill 商业化演进</title>',s,count=1,flags=re.S)
eb.set_template(lines,s);eb.save(target,lines);eb.verify(target)
print(target)
