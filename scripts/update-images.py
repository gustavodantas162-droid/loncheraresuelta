from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import json

root=Path(__file__).resolve().parent.parent
names=['2baf60da-c88c-406b-89c8-d36140fd5594','27c55ba3-bea2-4e67-89e3-12a17a5d4858','add3e43d-7745-4a1e-9009-151fc0cbd482','954a87fb-7ed3-4dae-b468-fc22b9fa8408','80bcdf09-30b0-4906-a84d-1ba491fb2142','dc36f3ea-bdc6-416a-80cd-9e4251e78126','48053343-f578-4cd0-a58d-ce11ddf0dcd5','319209fd-f33f-4b17-a50f-69fc47a62e92','7461edc8-ada2-4faf-976a-7b5f512eb8e1','f45dac74-9135-4fba-a4cd-1800276c290f','3c95f6fc-a889-4c07-89e1-a0ae77dccc58','789c27de-7899-4d65-a9a1-21cc5dd48d0e','4da5275f-4fef-4043-ad32-92be54f67d5a','6c5be2db-968d-4098-b61a-add998c8c767','f611df19-813c-454f-ac39-0bb48231fff1','b45d9288-5d6b-4375-9456-77bcded373c3','7341bc95-2ace-4bc6-a49f-c7c53caef74b']
alts=['Portada del recetario Lonchera Resuelta','Muffins de banana y avena','Bolitas de coco y cacao','Panecillos de queso y tapioca','Mini quiches de espinaca','Mini panqueques de avena y garbanzos crocantes','Trufas de dátil y cacao','Pudín de chía y mango y mini tostadas caprese','Semana 1, lunes: pizza y fruta','Semana 1, viernes: rollitos y pera','Semana 1, jueves: tortitas y galletas','Semana 1, viernes: rollitos y pera','Portada del plan de cuatro semanas','Semana 2, viernes: arepitas y mango','Semana 2, martes: quiche y zanahoria dulce','Lonchera Resuelta: paquete completo','Niña con una lonchera de sándwiches, frutas y panqueques']
assets=root/'public/images'; assets.mkdir(exist_ok=True)
manifest=[]
for i,(name,alt) in enumerate(zip(names,alts),1):
    dest=assets/f'lonchera-{i:02}.webp'
    if not dest.exists():
        with Image.open(Path('C:/Users/gucad/AppData/Local/Temp')/f'codex-clipboard-{name}.png') as im:
            im.save(dest,'WEBP',quality=92,method=6)
    with Image.open(dest) as im: width,height=im.size
    manifest.append(dict(src=f'/images/{dest.name}',alt=alt,width=width,height=height))

path=root/'app/content.ts'
s=BeautifulSoup(json.loads(path.read_text(encoding='utf-8').split(' = ',1)[1].rstrip(';\n')),'html.parser')
def image(i):
    x=s.new_tag('img',attrs={**manifest[i-1],'loading':'lazy','decoding':'async'})
    return x
track=s.select_one('#carouselTrack'); track.clear()
for i in range(1,9):
    x=s.new_tag('div',attrs={'class':'carousel-item'}); x.append(image(i)); track.append(x)
track['aria-label']='Vista del recetario: 40 recetas dulces y saladas'
if not s.select_one('#plansCarouselTrack'):
    heading=s.new_tag('div',attrs={'class':'demo-inner'});
    h=s.new_tag('h2'); h.string='Por dentro del plan de 4 semanas'; heading.append(h)
    p=s.new_tag('p',attrs={'class':'demo-sub'}); p.string='20 combinaciones de loncheras escolares, organizadas de lunes a viernes.'; heading.append(p)
    wrapper=s.new_tag('div',attrs={'class':'carousel-wrapper'})
    plans=s.new_tag('div',attrs={'class':'carousel-track','id':'plansCarouselTrack','aria-label':'Vista del plan de cuatro semanas'})
    for i in range(9,16):
        x=s.new_tag('div',attrs={'class':'carousel-item'}); x.append(image(i)); plans.append(x)
    wrapper.append(plans)
    track.parent.insert_after(wrapper); wrapper.insert_before(heading)
for sel,i in [('.hero-img',17),('.produto-img',16),('.plano-rec-card .plano-body > img',16)]:
    old=s.select_one(sel); old.attrs.update(manifest[i-1])
for x in s.select('[data-cta]'):
    x.name='a'; x['href']='https://pay.hotmart.com/Y107459178H?checkoutMode=10&bid=1788488400949'; x['data-cta']='checkout'
    x.attrs.pop('type',None); x.attrs.pop('aria-disabled',None)
for x in s.find_all('svg'):
    if 'viewbox' in x.attrs: x['viewBox']=x.attrs.pop('viewbox')
    if 'preserveaspectratio' in x.attrs: x['preserveAspectRatio']=x.attrs.pop('preserveaspectratio')
path.write_text('export const pageHtml = '+json.dumps(str(s),ensure_ascii=False)+';\n',encoding='utf-8')
(root/'scripts/image-map.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated 17 images, 8 recipe slides, 7 plan slides, 4 checkout links.')
