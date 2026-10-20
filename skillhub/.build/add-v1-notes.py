from pathlib import Path
import zipfile,xml.etree.ElementTree as E,copy,json
r=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/skillhub');b=r/'.build'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for k,v in NS.items():E.register_namespace(k,v)
REL='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
with zipfile.ZipFile(b/'skillhub-insights-v1-draft-final.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
with zipfile.ZipFile(r/'output/skillhub-insights.pptx') as z:old={n:z.read(n) for n in z.namelist()}
copied={n:v for n,v in old.items() if n.startswith(('ppt/notesSlides/','ppt/notesMasters/')) or n=='ppt/theme/theme2.xml'}
parts.update(copied)
def reladd(xml,typ,target):
 root=E.fromstring(xml);ids={x.get('Id') for x in root};n=1
 while f'rId{n}' in ids:n+=1
 rid=f'rId{n}';E.SubElement(root,f'{{{REL}}}Relationship',{'Id':rid,'Type':NS['r']+'/'+typ,'Target':target})
 return E.tostring(root,encoding='utf-8',xml_declaration=True),rid
parts['ppt/slides/_rels/slide1.xml.rels'],_=reladd(parts['ppt/slides/_rels/slide1.xml.rels'],'notesSlide','../notesSlides/notesSlide1.xml')
parts['ppt/_rels/presentation.xml.rels'],rid=reladd(parts['ppt/_rels/presentation.xml.rels'],'notesMaster','notesMasters/notesMaster1.xml')
pres=E.fromstring(parts['ppt/presentation.xml']);base=E.fromstring(old['ppt/presentation.xml'])
master=E.Element(f'{{{NS["p"]}}}notesMasterIdLst')
E.SubElement(master,f'{{{NS["p"]}}}notesMasterId',{f'{{{NS["r"]}}}id':rid})
pos=next((i for i,x in enumerate(pres) if x.tag==f'{{{NS["p"]}}}sldIdLst'),0);pres.insert(pos,master)
if pres.find('p:notesSz',NS) is None:
 ns=base.find('p:notesSz',NS)
 if ns is not None:pres.append(copy.deepcopy(ns))
parts['ppt/presentation.xml']=E.tostring(pres,encoding='utf-8',xml_declaration=True)
ct=E.fromstring(parts['[Content_Types].xml']);seen={x.get('PartName') for x in ct}
for x in E.fromstring(old['[Content_Types].xml']):
 if x.get('PartName','').lstrip('/') in copied and x.get('PartName') not in seen:ct.append(copy.deepcopy(x))
E.register_namespace('',CT)
parts['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
stats=json.loads((r/'statistics-v1.json').read_text())
notes='''腾讯 SkillHub 平台洞察 v1，2026-10-19，聚焦 Skill 资产供给、分发、安装与使用。

定位：全球开源同步、本土个人/团队共建、企业和产品团队发布共同构成Skill供给。平台提供中文发现、版本文件、安全与质量信号，并通过CLI/API及宿主插件交付到使用环境。此处为基于官方能力的分析。

供给：ClawHub等来源贡献全球通用长尾；个人/团队发布本土工具、Prompt和SOP；企业产品包括腾讯文档、ima，垂直样例包括钢联问数、电子印章。平台自身维护查找Skill和TRACE evaluator。来源标签不等于原创身份或质量认证。

规模：本次实际API total=199514，分类count=13。下载榜前50条来源：community23（46%）、clawhub14（28%）、enterprise13（26%）。这是下载头部的来源样本，不是全量供给占比。来源筛选总数口径不可相加，未据此作全量推断。

消费图：Top50 downloads合计53342548；编程5条19695718（36.92%）；AI Agent11条7057027（13.23%）；知识4条5424014（10.17%）；其他39.68%。四组显示一位小数36.9%、13.2%、10.2%、39.7%。下载不是用户数、活跃度或任务成功率。需求画像按技能能力推断，非真实用户调查。

发布：网页、CLI或Agent提交目录/ZIP，成功请求先进入pending_review。GitHub导入是纳入平台发布管理的路径，不等同自动同步所有仓库。平台发布字段与开放Skill内容字段需区分，详见官方发布指引。

分发：SkillHub管理版本文件；下载API GET /api/v1/download支持version/tag，302至对象存储。同步来源与下载来源不是同一概念。网页、CLI、Open API和DSH提供不同发现/获取入口。

安装：从官网分发包只读核查的CLI版本2026.8.5。命令示例skillhub install <slug> --dir ./skills。默认当前目录./skills，记录.skills_store_lock.json。DSH默认$DSH_HOME/skills，通常~/.dsh/skills，可配置。目标仍须为宿主可发现目录。两者Skill安装流程不执行包内脚本、不自动pip/npm安装依赖。连接与凭据另行准备。

版本边界：下载API和DSH支持指定Skill版本。当前CLI install没有--version参数；裸slug版本调用链未统一传递版本，不作所有入口均可固定版本的承诺。CLI更新命令upgrade，依赖包中config更新配置，当前没有uninstall；不在页面泛化这些管理能力。没有发现普通CLI安装自动回退ClawHub原站的链路。

使用和试运行：Agent在安装可见后按需加载指令并完成任务。官网云端沙箱/案例流程有实现，本次未执行会话、Skill或上传文件。未安装外部技能、未发布或登录。

TRACE：五维质量按维度内均分后五维等权；榜单score、TRACE和安全报告分开。开源evaluator跳过trust.scan，不代表平台完整动态实测。旧样本find-skill-skillhub的评测解释与功能有不一致，原因尚未查明，不推广全站结论。

主要来源：
https://github.com/Tencent/skillhub
https://skillhub.cn/tutorials
https://skillhub.cn/ai/release.md
https://skillhub.cn/install/install.sh
https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz
https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md
https://github.com/Tencent/skillhub/blob/main/docs/api/files.md
https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md
https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md
https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/install.ts
https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/config-store.ts
https://api.skillhub.cn/api/skills?sortBy=downloads&order=desc&pageSize=50
https://api.skillhub.cn/api/v1/categories

本地证据：research-supply-distribution-install-v1.md、statistics-v1.json、sources/v1/。
'''
note=E.fromstring(parts['ppt/notesSlides/notesSlide1.xml']);body=None
for shape in note.findall('.//p:sp',NS):
 ph=shape.find('p:nvSpPr/p:nvPr/p:ph',NS)
 if ph is not None and ph.get('type')=='body':body=shape.find('p:txBody',NS);break
assert body is not None
for el in list(body):
 if el.tag==f'{{{NS["a"]}}}p':body.remove(el)
for line in notes.split('\n'):
 p=E.SubElement(body,f'{{{NS["a"]}}}p')
 if line:rr=E.SubElement(p,f'{{{NS["a"]}}}r');t=E.SubElement(rr,f'{{{NS["a"]}}}t');t.text=line
parts['ppt/notesSlides/notesSlide1.xml']=E.tostring(note,encoding='utf-8',xml_declaration=True)
out=b/'skillhub-insights-v1-with-notes.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
assert sum(bool(__import__('re').fullmatch(r'ppt/slides/slide\d+\.xml',n)) for n in parts)==1
print('PPTX notes added:',out)
