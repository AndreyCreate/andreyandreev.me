from pathlib import Path
from html.parser import HTMLParser
import re
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'ai-business/index.html'
class Tags(HTMLParser):
 def __init__(self,s):
  super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def test_offer_and_boundaries():
 s=PAGE.read_text()
 for text in ['195 000 ₽','Старт 21 сентября','три недели','Два общих Zoom','Три индивидуальные встречи','до 8 участников','оплачиваются отдельно','Между встречами','программа их не гарантирует','внедрение под ключ в программу не входят']:
  assert text in s
 assert 'ai-agents-cta' not in s
 assert 'https://andreyandreev.me/ai-business/' in s

def test_only_existing_assets_and_video_destinations():
 source=Tags((ROOT/'ai-agents/index.html').read_text()).tags
 new=Tags(PAGE.read_text()).tags
 assert [a['data-video'] for _,a in new if 'data-video' in a]==[a['data-video'] for _,a in source if 'data-video' in a]
 for _,a in new:
  for k in ['src','poster']:
   v=a.get(k,'')
   if v.startswith('/'):assert (ROOT/v.lstrip('/')).is_file(),v
 assert len([a for _,a in new if 'data-video' in a])==5

def test_dialog_primary_payment_exact_and_secondary():
 tags=Tags(PAGE.read_text()).tags
 ctas=[a for t,a in tags if t=='a' and a.get('data-action')]
 assert len(ctas)==5
 for a in ctas:
  if a['data-action']=='dialog':
   assert a['href']=='https://t.me/andrey_andreev'
   assert 'pill-coral' in a['class']
  else:
   assert a['href']=='https://andreyandreev.createtoday.ru/hero/get/of_r6-pemaaf45z'
   assert 'pill-coral' not in a.get('class','')
 ids={a['id'] for _,a in tags if a.get('id')}
 for t,a in tags:
  if t=='a' and a.get('href','').startswith('#') and a['href']!='#':assert a['href'][1:] in ids
