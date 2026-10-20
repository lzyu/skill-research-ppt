from pathlib import Path
import zipfile,xml.etree.ElementTree as E,copy,json,hashlib,re

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/skillhub/skillpay')
build=root/'.build'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for k,v in NS.items():E.register_namespace(k,v)
REL='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
with zipfile.ZipFile(build/'skillhub-skillpay-commercialization-v2-draft.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
with zipfile.ZipFile(root.parent/'output/skillhub-insights.pptx') as z:old={n:z.read(n) for n in z.namelist()}
copied={n:v for n,v in old.items() if n.startswith('ppt/notesMasters/') or n=='ppt/theme/theme2.xml'}
parts.update(copied)
def reladd(xml,typ,target):
 r=E.fromstring(xml);ids={x.get('Id') for x in r};n=1
 while f'rId{n}' in ids:n+=1
 rid=f'rId{n}';E.SubElement(r,f'{{{REL}}}Relationship',{'Id':rid,'Type':NS['r']+'/'+typ,'Target':target})
 return E.tostring(r,encoding='utf-8',xml_declaration=True),rid
parts['ppt/_rels/presentation.xml.rels'],rid=reladd(parts['ppt/_rels/presentation.xml.rels'],'notesMaster','notesMasters/notesMaster1.xml')
pres=E.fromstring(parts['ppt/presentation.xml']);base=E.fromstring(old['ppt/presentation.xml'])
master=E.Element(f'{{{NS["p"]}}}notesMasterIdLst');E.SubElement(master,f'{{{NS["p"]}}}notesMasterId',{f'{{{NS["r"]}}}id':rid})
pos=next((i for i,x in enumerate(pres) if x.tag==f'{{{NS["p"]}}}sldIdLst'),0);pres.insert(pos,master)
if pres.find('p:notesSz',NS) is None:
 sz=base.find('p:notesSz',NS)
 if sz is not None:pres.append(copy.deepcopy(sz))
parts['ppt/presentation.xml']=E.tostring(pres,encoding='utf-8',xml_declaration=True)
report=(root/'skillpay-principles-v2.md').read_text()
sections=re.split(r'(?=^## )',report,flags=re.M)
page1notes='\n'.join(x for x in sections if any(x.startswith('## '+n+'.') for n in ['1','2','3','4','5','9','10']))
page2notes='\n'.join(x for x in sections if any(x.startswith('## '+n+'.') for n in ['6','7','8','10']))
notes=[re.sub(r'```mermaid.*?```','图见正文及伴生文档。',t,flags=re.S) for t in [page1notes,page2notes]]
for i,txt in enumerate(notes,1):
 parts[f'ppt/slides/_rels/slide{i}.xml.rels'],_=reladd(parts[f'ppt/slides/_rels/slide{i}.xml.rels'],'notesSlide',f'../notesSlides/notesSlide{i}.xml')
 rel=E.fromstring(old['ppt/notesSlides/_rels/notesSlide1.xml.rels'])
 for x in rel:
  if x.get('Type','').endswith('/slide'):x.set('Target',f'../slides/slide{i}.xml')
 parts[f'ppt/notesSlides/_rels/notesSlide{i}.xml.rels']=E.tostring(rel,encoding='utf-8',xml_declaration=True)
 note=E.fromstring(old['ppt/notesSlides/notesSlide1.xml']);body=None
 for sh in note.findall('.//p:sp',NS):
  ph=sh.find('p:nvSpPr/p:nvPr/p:ph',NS)
  if ph is not None and ph.get('type')=='body':body=sh.find('p:txBody',NS);break
 assert body is not None
 for el in list(body):
  if el.tag==f'{{{NS["a"]}}}p':body.remove(el)
 for line in txt.split('\n'):
  p=E.SubElement(body,f'{{{NS["a"]}}}p')
  if line:
   rr=E.SubElement(p,f'{{{NS["a"]}}}r');t=E.SubElement(rr,f'{{{NS["a"]}}}t');t.text=line
 # Update the slide number placeholder, if present.
 for sh in note.findall('.//p:sp',NS):
  ph=sh.find('p:nvSpPr/p:nvPr/p:ph',NS)
  if ph is not None and ph.get('type')=='sldNum':
   for t in sh.findall('.//a:t',NS):t.text=str(i)
 parts[f'ppt/notesSlides/notesSlide{i}.xml']=E.tostring(note,encoding='utf-8',xml_declaration=True)
# Replace text triangle glyphs with native DrawingML arrowheads. Some renderers
# substitute the right/left glyphs with colored emoji even with a text font.
for i in (1,2):
 slide=E.fromstring(parts[f'ppt/slides/slide{i}.xml'])
 for sh in slide.findall('.//p:sp',NS):
  glyph=''.join(t.text or '' for t in sh.findall('.//a:t',NS)).strip()
  if glyph not in ('▶','◀','▼'):continue
  props=sh.find('p:spPr',NS);xf=props.find('a:xfrm',NS)
  if xf is None:continue
  off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
  color=sh.find('.//a:rPr/a:solidFill/a:srgbClr',NS)
  fill=color.get('val') if color is not None else '566472'
  scale=6350
  oldx,oldy=int(off.get('x')),int(off.get('y'))
  dx,dy,rot={'▶':(-6,8,5400000),'◀':(8,8,16200000),'▼':(3,1,10800000)}[glyph]
  off.set('x',str(oldx+dx*scale));off.set('y',str(oldy+dy*scale))
  ext.set('cx',str(14*scale));ext.set('cy',str(14*scale));xf.set('rot',str(rot))
  for child in list(props):
   if child is not xf:props.remove(child)
  geo=E.SubElement(props,f'{{{NS["a"]}}}prstGeom',{'prst':'triangle'});E.SubElement(geo,f'{{{NS["a"]}}}avLst')
  sf=E.SubElement(props,f'{{{NS["a"]}}}solidFill');E.SubElement(sf,f'{{{NS["a"]}}}srgbClr',{'val':fill})
  ln=E.SubElement(props,f'{{{NS["a"]}}}ln');E.SubElement(ln,f'{{{NS["a"]}}}noFill')
  tx=sh.find('p:txBody',NS)
  if tx is not None:sh.remove(tx)
  nv=sh.find('p:nvSpPr/p:cNvSpPr',NS)
  if nv is not None:nv.attrib.pop('txBox',None)
 parts[f'ppt/slides/slide{i}.xml']=E.tostring(slide,encoding='utf-8',xml_declaration=True)
ct=E.fromstring(parts['[Content_Types].xml']);seen={x.get('PartName') for x in ct}
for x in E.fromstring(old['[Content_Types].xml']):
 if x.get('PartName','').lstrip('/') in copied and x.get('PartName') not in seen:ct.append(copy.deepcopy(x));seen.add(x.get('PartName'))
for i in (1,2):
 name=f'/ppt/notesSlides/notesSlide{i}.xml'
 if name not in seen:E.SubElement(ct,f'{{{CT}}}Override',{'PartName':name,'ContentType':'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml'})
E.register_namespace('',CT)
parts['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
assert len([n for n in parts if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)])==2
out=build/'skillhub-skillpay-commercialization-v2-with-notes.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
inventory=[{'file':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((root/'sources').rglob('*')) if p.is_file()]
(root/'sources-manifest-v2.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print(out)
