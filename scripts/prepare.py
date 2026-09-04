from pathlib import Path
from bs4 import BeautifulSoup, Comment
from copy import deepcopy
import re, json

ROOT = Path(__file__).resolve().parent.parent
original = BeautifulSoup((ROOT/'scripts/original.html').read_text(encoding='utf-8'), 'html.parser')
s = original.find_all('html')[1]
copy = (ROOT/'scripts/copy-es-LATAM.txt').read_text(encoding='utf-8')
B = {int(x.split(' ',1)[0]): x.splitlines()[1:] for x in re.split(r'(?m)^Bloque ',copy)[1:]}
def settext(sel, text, root=s):
    x=root.select_one(sel); x.clear(); x.append(text); return x
def tag(name, text='', cls=None):
    x=original.new_tag(name); x.string=text
    if cls: x['class']=cls
    return x
def paras(lines, cls=None):
    return [tag('p', line, cls) for line in lines]
def checklist(sel, lines):
    ul=s.select_one(sel); template=deepcopy(ul.li); ul.clear()
    for line in lines:
        li=deepcopy(template); icon=li.span.extract(); li.clear(); li.append(icon); li.append(line.removeprefix('- ')); ul.append(li)

settext('#urgencia-txt',B[1][0])
settext('.hero h1',B[2][1])
s.select_one('.hero h1').insert_before(tag('p',B[2][0],'produto-eyebrow hero-brand'))
for pill,line in zip(s.select('.pill'),B[2][3:7]):
    icon=pill.span.extract(); pill.clear(); pill.append(icon); pill.append(line.removeprefix('- '))
settext('.hero-sub',B[2][2])
settext('.ps-num',B[2][8])
settext('.ps-desc',B[2][7])
s.select_one('.ps-stars').decompose()

settext('.demo h2',B[3][0]); settext('.demo-sub',B[3][1])
for i in range(2,10,2):
    p=tag('p',cls='demo-sub'); strong=tag('strong',B[3][i]); p.append(strong); p.append(original.new_tag('br')); p.append(B[3][i+1]); s.select_one('.demo-inner').append(p)
for p,line in zip(s.select('.dor-box p'),B[3][11:13]): p.clear(); p.append(line)
settext('.demo .btn',B[3][13].removeprefix('BOTÓN: '))
settext('.ideal-titulo',B[4][0])
for i,card in enumerate(s.select('.ideal-card')):
    settext('h3',B[4][1+i*2],card); settext('p',B[4][2+i*2],card)
settext('.ideal .btn',B[4][11].removeprefix('BOTÓN: '))
settext('.produto-eyebrow:not(.hero-brand)',B[5][0]); settext('.produto-nome','Lonchera Resuelta')
s.select_one('.produto-divider').insert_before(tag('p',B[5][1],'mais-txt'))
checklist('.produto .checklist',B[5][2:8]); settext('.mais-txt:last-child',B[5][8])

settext('.bridge-eyebrow',B[6][0]); settext('.bridge-sub',B[6][7]); settext('.bridge-titulo','2 BONOS INCLUIDOS')
for i,card in enumerate(s.select('.bonus-card')):
    if i>=2: card.decompose(); continue
    idx=1+i*3
    settext('.bonus-num-tag',f'BONO {i+1}',card)
    settext('h3',B[6][idx].split(' — ',1)[1],card)
    settext('p',B[6][idx+1]+' '+B[6][idx+2],card)

settext('.depoimentos h2',B[7][0])
# Keep the reference images until the user supplies their replacements.
for i in range(1,7,2):
    box=tag('div',cls='produto-inner'); box.append(tag('h3',B[7][i])); box.append(tag('p',B[7][i+1],'mais-txt'))
    box['style']='margin-bottom:16px'
    s.select_one('.depo-carousel-wrapper').insert_before(box)
s.select_one('.depoimentos').append(tag('p',B[7][7],'mais-txt'))
settext('.planos-bridge p',B[8][0])
s.select_one('.plano-card').decompose()
settext('.plano-rec-badge','Paquete completo + dos bonos')
settext('.plano-rec-titulo',B[8][1]); settext('.plano-sub',B[8][2])
checklist('.planos .checklist',B[8][3:11])
s.select_one('.preco-de').decompose(); s.select_one('.oferta-tag').decompose()
settext('.preco-hoje-label','Pago único'); settext('.preco-valor',B[8][11])
settext('.planos .btn',B[8][13].removeprefix('BOTÓN: ')); settext('.preco-sub-txt',B[8][12])
selos=s.select_one('.selos'); selos.clear()
for line in B[8][14:16]: selos.append(tag('div',line,'selo-item'))
s.select_one('.urgencia-final').decompose()

settext('.garantia h2',B[9][0]); settext('.garantia h3','Siete días para solicitar reembolso.')
settext('.garantia p',B[9][1]+' '+B[9][2])
for row,line in zip(s.select('.garantia-item-row'),['Revisa las combinaciones','Consulta las recetas','Revisa las listas de compras']):
    icon=row.span.extract(); row.clear(); row.append(icon); row.append(line)
settext('.autoridade-eyebrow',B[10][0]); settext('.autoridade-nome',B[10][2])
bio=settext('.autoridade-bio','')
for i in [1,3,4]:
    if bio.contents: bio.append(original.new_tag('br')); bio.append(original.new_tag('br'))
    bio.append(B[10][i])

faq=s.select_one('.faq'); template=deepcopy(s.select_one('.faq-item'))
for x in s.select('.faq-item'): x.decompose()
entries=[]
for line in B[11]:
    if line.startswith('¿'): entries.append([line,[]])
    else: entries[-1][1].append(line)
for i,(question,answer) in enumerate(entries):
    item=deepcopy(template); button=item.select_one('button'); arrow=button.span.extract(); button.clear(); button.append(question); button.append(arrow)
    button['aria-expanded']='false'; button['aria-controls']=f'faq-answer-{i}'; button['type']='button'
    a=settext('.faq-answer','\n\n'.join(answer),item); a['id']=f'faq-answer-{i}'
    faq.select_one('.faq-cta').insert_before(item)
closing=s.select_one('.faq-cta')
for p in [tag('h2',B[12][0]),*paras(B[12][1:4],'mais-txt')]: closing.insert_before(p)
settext('.faq-cta .btn',B[12][4].removeprefix('BOTÓN: '))
for p in paras(B[12][5:7],'mais-txt'): closing.append(p)
footer=s.select_one('footer'); footer.clear(); footer.append(tag('strong',B[12][8])); footer.append(original.new_tag('br')); footer.append(B[12][9])

for a in s.select('a'):
    a.attrs.pop('href',None); a.attrs.pop('target',None)
    if 'btn' in a.get('class',[]): a.name='button'; a['type']='button'; a['aria-disabled']='true'; a['data-cta']='pending'
for x in s.find_all('script'): x.decompose()
for x in s.find_all(string=lambda x:isinstance(x,Comment)): x.extract()
for x in s.find_all(True):
    for attr in list(x.attrs):
        if attr.startswith('on'): del x[attr]
    if 'viewbox' in x.attrs: x['viewBox']=x.attrs.pop('viewbox')
    if 'preserveaspectratio' in x.attrs: x['preserveAspectRatio']=x.attrs.pop('preserveaspectratio')
for i,img in enumerate(s.select('img')):
    img['data-image-slot']=f'image-{i+1:02}'
    img['alt']=f'Imagen de referencia {i+1}'
css='\n'.join(x.text for x in original.find_all('style'))
css+='\n/* Text additions use the original page palette and type scale. */\n.hero-brand{color:var(--marrom)}\n.faq-answer{white-space:pre-line}\n.hero-img,.produto-img,.plano-body>img{height:auto;object-fit:contain}\n'
(ROOT/'app/globals.css').write_text(css,encoding='utf-8')
html=''.join(str(x) for x in s.body.contents)
(ROOT/'app/content.ts').write_text('export const pageHtml = '+json.dumps(html,ensure_ascii=False)+';\n',encoding='utf-8')
(ROOT/'public/reference-images.json').write_text(json.dumps([{'slot':x['data-image-slot'],'url':x['src']} for x in s.select('img')],indent=2),encoding='utf-8')
print('Copy integrated:',len(entries),'FAQs;',len(s.select('[data-cta]')),'CTAs without URLs')

# Reapply the approved assets and checkout after regenerating the original copy.
if (ROOT / "scripts/image-map.json").exists():
    import runpy
    runpy.run_path(str(ROOT / "scripts/update-images.py"))
