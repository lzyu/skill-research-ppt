from pathlib import Path
import importlib.util,re,json,html
from bs4 import BeautifulSoup
root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/skillhub')
skill=Path('/Users/tpy/.agents/skills/aico-ppt')
sp=importlib.util.spec_from_file_location('eb',skill/'scripts/edit-bundle.py');eb=importlib.util.module_from_spec(sp);sp.loader.exec_module(eb)
p=root/'skillhub-insights-v1.html';lines=eb.load(p);s=eb.get_template(lines)
i=s.index('<section data-label="SkillHub洞察"');j=s.index('</section>',i)+len('</section>')
sec=BeautifulSoup(s[i:j],'html.parser').section
main=sec.find('div',style=lambda v:v and 'grid-template-columns:440px 550px' in v)
assert main is not None
main['style']=main['style'].replace('440px 550px','475px 610px')
red='#b5333b';blue='#566472';muted='#585860'
def group(title,main,detail):
 return f'''<div style="border-bottom:1px solid #e2e4e7;padding:12px 0;"><div style="font-size:24px;font-weight:700;line-height:1.3;">{title}</div><div style="font-size:21px;line-height:1.4;margin-top:5px;">{main}</div><div style="font-size:21px;color:{muted};line-height:1.4;margin-top:3px;">{detail}</div></div>'''
left=f'''<div style="min-width:0;display:flex;flex-direction:column;">
<div style="font-size:27px;font-weight:700;margin-bottom:3px;">生态供给：同步、原创与企业</div>
{group('全球同步','ClawHub 等公开生态 Skills','中文描述与国内下载，补齐长尾覆盖')}
{group('个人与社区发布','本土作者沉淀工具、Prompt 与 SOP','网页或 CLI 接入，持续发布新版本')}
{group('企业与产品团队','官方产品：腾讯文档、ima','垂直领域：钢联问数、电子印章')}
<div style="font-size:21px;line-height:1.4;color:{muted};margin-top:12px;">平台自供给：技能查找、TRACE 评测</div>
<div style="margin-top:auto;padding-top:15px;">
<div style="font-size:19px;font-weight:700;margin-bottom:8px;">下载榜 Top50 来源条目占比</div>
<div style="display:flex;height:16px;width:100%;border-radius:3px;overflow:hidden;"><div style="width:46%;background:{red};"></div><div style="width:28%;background:{blue};"></div><div style="width:26%;background:#a5acb4;"></div></div>
<div style="display:flex;justify-content:space-between;font-size:19px;margin-top:7px;"><span>社区 46%</span><span>ClawHub 28%</span><span>企业 26%</span></div>
<div style="font-size:17px;color:{muted};line-height:1.35;margin-top:7px;">供给渠道样本，不代表全量结构</div></div></div>'''
def step(n,title,detail):
 return f'''<div style="display:grid;grid-template-columns:42px 1fr;gap:12px;align-items:start;"><div style="width:38px;height:38px;border:1px solid #c9cdd2;color:{red};font-family:'JetBrains Mono';font-size:21px;font-weight:700;border-radius:50%;display:flex;align-items:center;justify-content:center;">{n}</div><div><div style="font-size:24px;font-weight:700;line-height:1.3;">{title}</div><div style="font-size:21px;line-height:1.4;color:{muted};margin-top:5px;">{detail}</div></div></div>'''
steps=''.join([step('01','发布：目录或 ZIP 入库','网页 / CLI / Agent 发布，版本审核后可见'),step('02','分发：检索后获取版本包','榜单、搜索与 API；指定版本 ZIP 下载'),step('03','安装：文件落到宿主目录','CLI 默认 ./skills；DSH 默认 ~/.dsh/skills'),step('04','使用：宿主加载并执行','依赖与账号需就绪；云端案例未实跑')])
mid=f'''<div style="min-width:0;border-left:1px solid #e2e4e7;padding-left:25px;display:flex;flex-direction:column;">
<div style="font-size:27px;font-weight:700;margin-bottom:20px;">分发安装：从平台到宿主</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:space-between;gap:16px;">{steps}</div>
<div style="border-top:1px solid #e2e4e7;margin-top:17px;padding-top:12px;"><div style="font-family:'JetBrains Mono',monospace;font-size:19px;color:#1a1a1c;">skillhub install &lt;slug&gt; --dir ./skills</div><div style="font-size:21px;line-height:1.4;color:{muted};margin-top:8px;">Skill 安装只落文件，不自动装依赖；<br/>目标目录仍须被宿主发现。</div></div></div>'''
stats=json.loads((root/'statistics-v1.json').read_text());cat=stats['categories_in_sample']
vals=[('开发编程',cat['dev-programming']['download_share_pct'],red),('AI Agent',cat['ai-agent']['download_share_pct'],blue),('知识管理',cat['knowledge-management']['download_share_pct'],blue)]
vals.append(('其他',100-sum(x[1] for x in vals),'#a5acb4'))
bars=''
for name,v,c in vals:
 bars+=f'''<div style="display:grid;grid-template-columns:94px 1fr 68px;align-items:center;gap:10px;margin-top:12px;font-size:19px;"><span>{name}</span><div style="height:16px;background:#f0f1f3;border-radius:3px;"><div style="width:{v}%;height:100%;background:{c};border-radius:3px;"></div></div><b style="font-family:'JetBrains Mono';font-size:19px;text-align:right;">{v:.1f}%</b></div>'''
def demand(name,detail):
 return f'''<div style="display:grid;grid-template-columns:100px 1fr;gap:10px;padding:12px 0;border-bottom:1px solid #ececec;"><div style="font-size:21px;font-weight:700;line-height:1.4;">{name}</div><div style="font-size:21px;color:{muted};line-height:1.4;">{detail}</div></div>'''
right=f'''<div style="min-width:0;border-left:1px solid #e2e4e7;padding-left:25px;display:flex;flex-direction:column;">
<div style="font-size:27px;font-weight:700;margin-bottom:8px;">消费画像：通用任务与专业服务</div>
{demand('开发与 Agent','编程、浏览器操作、技能发现与自改进')}
{demand('知识与办公','摘要、文档协作、数据与内容处理')}
{demand('行业业务','专业数据查询、业务接口与服务对接')}
<div style="font-size:21px;font-weight:700;margin-top:20px;">Top50 样本内，下载记录的类别占比</div>
<div style="margin-top:4px;">{bars}</div>
<div style="font-size:19px;color:{muted};line-height:1.4;margin-top:15px;">编程类 5 条贡献 36.9%，AI Agent 有 11 条。<br/>下载不代表活跃用户或任务成功。</div>
<div style="font-size:17px;color:{muted};line-height:1.35;margin-top:auto;padding-top:11px;">消费需求按技能能力推断，非真实用户分群</div>
</div>'''
children=[x for x in main.children if getattr(x,'name',None)]
assert len(children)==3
for old,new in zip(children,[left,mid,right]):old.replace_with(BeautifulSoup(new,'html.parser').div)
sec.h3.string='SkillHub 围绕 Skill 打通生态供给、可信分发与宿主安装'
sec['data-page-type-id']='layered-platform-ops-rail'
# Preserve the original rest of the slide while changing the positioning and implication.
oldtext='公开 API 条目数 199,511'
for node in sec.find_all(string=True):
 t=str(node)
 if t==oldtext:node.replace_with('公开 API 条目数 199,514')
 if t=='面向中国用户的 Agent 能力供给网络':node.replace_with('面向中国用户的 Skill 发现与分发平台')
 if t=='全球同步扩大覆盖，本土共建与企业服务补充专业能力':node.replace_with('全球同步补齐长尾，本土原创与企业供给扩展任务覆盖')
 if t=='多类资产与宿主消费共同建设，':node.replace_with('以 Skill 为管理单元，贯通来源版本、')
 if t=='把版本、质量证据和实际任务结果关联。':node.replace_with('安装条件、质量证据和实际任务结果。')
sec['data-label']='SkillHub洞察V1'
s=s[:i]+str(sec)+s[j:]
s=s.replace("label:'SkillHub洞察'","label:'SkillHub洞察V1'")
s=re.sub(r'<title>.*?</title>','<title>腾讯 SkillHub 洞察 v1</title>',s,count=1,flags=re.S)
eb.set_template(lines,s);eb.save(p,lines);eb.verify(p)
print('Updated',p)
