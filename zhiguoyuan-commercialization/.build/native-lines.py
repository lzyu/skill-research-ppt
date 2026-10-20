from pathlib import Path
import zipfile,xml.etree.ElementTree as E,io,collections,copy
from PIL import Image

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/zhiguoyuan-commercialization/.build')
src=root/'zhiguoyuan-skill-commercialization-with-notes.pptx'
with zipfile.ZipFile(src) as z:parts={n:z.read(n) for n in z.namelist()}
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for k,v in NS.items():E.register_namespace(k,v)
def q(k,n):return '{'+NS[k]+'}'+n
total=0
for i in range(1,3):
 rel=E.fromstring(parts[f'ppt/slides/_rels/slide{i}.xml.rels'])
 targets={x.get('Id'):'ppt/'+x.get('Target').replace('../','') for x in rel}
 slide=E.fromstring(parts[f'ppt/slides/slide{i}.xml']);tree=slide.find('p:cSld/p:spTree',NS);count=0
 for pic in list(tree):
  if pic.tag!=q('p','pic'):continue
  blip=pic.find('.//a:blip',NS);im=Image.open(io.BytesIO(parts[targets[blip.get(q('r','embed'))]])).convert('RGBA')
  w,h=im.size;alpha=im.getchannel('A');bb=alpha.point(lambda x:255 if x>200 else 0).getbbox()
  if not bb:continue
  x0,y0,x1,y1=bb
  horizontal=(y1-y0)<=6 and (x1-x0)>12
  vertical=(x1-x0)<=6 and (y1-y0)>12
  if not (horizontal or vertical):continue # retain the actual logo artwork
  xf=pic.find('p:spPr/a:xfrm',NS);off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
  ox,oy,cx,cy=map(int,[off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy')])
  px=im.load();cnt=collections.Counter()
  for yy in range(y0,y1):
   for xx in range(x0,x1):
    r,g,b,a=px[xx,yy]
    if a>240:cnt[(r,g,b)]+=1
  rgb=cnt.most_common(1)[0][0];color=''.join(f'{v:02X}' for v in rgb)
  if horizontal:
   xa=ox+round(x0/w*cx);ya=oy+round((y0+y1)/2/h*cy);dx=round((x1-x0)/w*cx);dy=0
   mid=(x0+x1)//2;stroke=sum(px[mid,yy][3]/255 for yy in range(h))/h*cy
   profile=[max(px[xx,yy][3] for yy in range(y0,y1)) for xx in range(x0,x1)]
  else:
   xa=ox+round((x0+x1)/2/w*cx);ya=oy+round(y0/h*cy);dx=0;dy=round((y1-y0)/h*cy)
   mid=(y0+y1)//2;stroke=sum(px[xx,mid][3]/255 for xx in range(w))/w*cx
   profile=[max(px[xx,yy][3] for xx in range(x0,x1)) for yy in range(y0,y1)]
  dashed=sum(v<40 for v in profile)>len(profile)*.10
  connector=E.Element(q('p','cxnSp'));nv=E.SubElement(connector,q('p','nvCxnSpPr'))
  props=copy.deepcopy(pic.find('p:nvPicPr/p:cNvPr',NS));props.set('name','Editable line '+props.get('id',''))
  nv.append(props);E.SubElement(nv,q('p','cNvCxnSpPr'));E.SubElement(nv,q('p','nvPr'))
  sp=E.SubElement(connector,q('p','spPr'));xfrm=E.SubElement(sp,q('a','xfrm'))
  E.SubElement(xfrm,q('a','off'),{'x':str(xa),'y':str(ya)});E.SubElement(xfrm,q('a','ext'),{'cx':str(dx),'cy':str(dy)})
  geo=E.SubElement(sp,q('a','prstGeom'),{'prst':'line'});E.SubElement(geo,q('a','avLst'))
  ln=E.SubElement(sp,q('a','ln'),{'w':str(max(4000,round(stroke))),'cap':'flat'})
  fill=E.SubElement(ln,q('a','solidFill'));E.SubElement(fill,q('a','srgbClr'),{'val':color})
  E.SubElement(ln,q('a','prstDash'),{'val':'dash' if dashed else 'solid'})
  pos=list(tree).index(pic);tree.remove(pic);tree.insert(pos,connector);count+=1
 parts[f'ppt/slides/slide{i}.xml']=E.tostring(slide,encoding='utf-8',xml_declaration=True)
 print('slide',i,'editable connectors',count);total+=count
out=root/'zhiguoyuan-skill-commercialization-native.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
print('Native lines',total,out)
