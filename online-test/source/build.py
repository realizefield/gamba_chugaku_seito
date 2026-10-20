# -*- coding: utf-8 -*-
import sys, json, math, re, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SETS as BASE
from data_civics import CIV
from fmtlib import fmt
OUT = os.path.dirname(os.path.abspath(__file__))

allsets = {}   # id -> dict
def add(i, title, lead, cats, qs, **meta):
    d = dict(id=i, title=title, lead=lead, cats=[list(c) for c in cats], qs=[list(q) for q in qs]); d.update(meta); allsets[i] = d

for k, s in BASE.items():
    add(k, s['title'], s['lead'], s['cats'], s['qs'], subject='math', section='一次方程式・一次関数', group=s['title'], label='テストをはじめる', math=True, pass_=None)
GN = {'kokkai':'国会','naikaku':'内閣','saiban':'裁判所'}
for k,(t,l,c,qs) in CIV.items():
    g = GN[re.match(r'[a-z]+',k).group(0)]
    add(k, t, l, c, qs, subject='soc', section='公民（三権分立）', group=g, math=False)
EXT = {
 'nk20': ('math','一次関数（単元別）',{'nk20':'⑳ 一次関数とは'}),
 'nk21': ('math','一次関数（単元別）',{'nk21':'㉑ 一次関数の表と式'}),
 'nk22': ('math','一次関数（単元別）',{'nk22':'㉒ 一次関数のグラフ'}),
 'nk23': ('math','一次関数（単元別）',{'nk23':'㉓ グラフの演習'}),
 'nk24': ('math','一次関数（単元別）',{'nk24':'㉔ 式を求める①（傾きと1点）'}),
 'nk25': ('math','一次関数（単元別）',{'nk25':'㉕ 式を求める②（2点・連立）'}),
 'nk26': ('math','一次関数（単元別）',{'nk26':'㉖ 変域'}),
 'nk27': ('math','一次関数（単元別）',{'nk27':'㉗ 一次関数の利用'}),
 'nk28': ('math','一次関数（単元別）',{'nk28':'㉘ 図形と一次関数'}),
 'nk29': ('math','一次関数（単元別）',{'nk29':'㉙ 動点問題'}),
 'asuka1': ('soc','歴史　古代',{'asuka1':'飛鳥時代・大化の改新'}),
 'asuka2': ('soc','歴史　古代',{'asuka2':'飛鳥文化'}),
 'nara1': ('soc','歴史　古代',{'nara1':'奈良時代'}),
 'nara2': ('soc','歴史　古代',{'nara2':'天平文化'}),
 'edo1': ('soc','歴史　江戸時代',{'edo1':'① 幕府の成立と支配'}),
 'edo2': ('soc','歴史　江戸時代',{'edo2':'② 鎖国と外交'}),
 'edo3': ('soc','歴史　江戸時代',{'edo3':'③ 産業と身分制度'}),
 'edo4': ('soc','歴史　江戸時代',{'edo4':'④ 元禄文化と享保・田沼・寛政の改革'}),
 'edo5': ('soc','歴史　江戸時代',{'edo5':'⑤ 化政文化と新しい学問・天保の改革と幕府の衰え'}),
 'sci1': ('sci','物質と密度・気体',{'sci1':'第1講　いろいろな物質（密度）'}),
 'sci2': ('sci','物質と密度・気体',{'sci2':'第2講　物質の状態変化と蒸留'}),
 'sci3': ('sci','物質と密度・気体',{'sci3':'気体の性質と製法'}),
 'jin1': ('sci','人体のはたらき',{'jin1':'第1章　消化と吸収'}),
 'jin2': ('sci','人体のはたらき',{'jin2':'第2章　呼吸と血液'}),
 'jin3': ('sci','人体のはたらき',{'jin3':'第3章　心臓と血液の循環'}),
 'jin4': ('sci','人体のはたらき',{'jin4':'第4章　感覚器官と運動'}),
}
GROUPNAME = json.load(open(os.path.join(OUT,'groupnames.json'))) if os.path.exists(os.path.join(OUT,'groupnames.json')) else {}
loaded=[]
for mod,(subj,sec,names) in EXT.items():
    try:
        m = importlib.import_module('data_'+mod)
    except Exception as e:
        continue
    loaded.append(mod)
    for k,(t,l,c,qs) in m.SETS.items():
        base = k.rsplit('_',1)[0]
        add(k, t, l, c, qs, subject=subj, section=sec, group=GROUPNAME.get(base, names[base]), math=(subj=='math'))

def label_of(s):
    if s.get('label'): return s['label']
    n = s['id'].rsplit('_',1)[-1] if '_' in s['id'] else s['id'][-1]
    return '第%s回' % n
for s in allsets.values():
    s['label'] = label_of(s)
    n = len(s['qs'])
    s['n'] = n
    if s.get('pass_', 'x') == 'x': s['pass_'] = math.ceil(n*0.8)
    s['min'] = 30 if n>=20 else (15 if n>=8 else 5)
    for c in s['cats']:
        for j in range(len(c)): c[j] = c[j].replace('χ','x')

SUBJ = [('math','数学'),('eng','英語'),('kanji','国語（漢字）'),('sci','理科'),('soc','社会')]
def order(ids): return sorted(ids, key=lambda i:(i.rsplit('_',1)[0] if '_' in i else i[:-1], i))
SECORDER = ['一次方程式・一次関数','一次関数（単元別）','物質と密度・気体','人体のはたらき','公民（三権分立）','歴史　古代','歴史　江戸時代']
def student_data():
    subs=[]
    for sid,sn in SUBJ:
        secs={}
        for i in allsets:
            s=allsets[i]
            if s['subject']!=sid: continue
            secs.setdefault(s['section'],{}).setdefault(s['group'],[]).append(i)
        seclist=[]
        for sec in sorted(secs, key=lambda x: SECORDER.index(x) if x in SECORDER else 99):
            groups=[]
            for g,ids in secs[sec].items():
                sets=[]
                for i in sorted(ids):
                    s=allsets[i]
                    sets.append(dict(id=i,label=s['label'],title=s['title'],math=s['math'],pass_=s['pass_'],n=s['n'],min=s['min'],
                        cats=[[fmt(c[0],s['math']),fmt(c[1],s['math'])] for c in s['cats']],
                        qs=[dict(c=q[0],q=fmt(q[1],s['math']),ch=[fmt(x,s['math']) for x in q[2]],a=q[3]) for q in s['qs']]))
                groups.append(dict(name=g,sets=sets))
            seclist.append(dict(name=sec,groups=groups))
        subs.append(dict(id=sid,name=sn,sections=seclist))
    return subs


KCSS = open(os.path.join(OUT,'katex_inline.css'),encoding='utf-8').read()
def sheets_blobs():
    import gzip, base64, secrets
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    st={}; te={}
    for (sec,g),sets in groups().items():
        sets=sorted(sets,key=lambda s:s['id']); k=sec+'|'+g
        st[k]=''.join(problems_html(g,sets)).replace('テスト（講師用）','テスト')
        te[k]=dict(p=''.join(problems_html(g,sets)),a=''.join(answers_html(g,sets)))
    def gz(o): return gzip.compress(json.dumps(o,ensure_ascii=False,separators=(',',':')).encode('utf-8'),9)
    salt=secrets.token_bytes(16); iv=secrets.token_bytes(12)
    key=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=200000).derive('kogen'.encode('utf-8'))
    ct=AESGCM(key).encrypt(iv,gz(te),None)
    return json.dumps(dict(css=PRINT_CSS,s=st),ensure_ascii=False,separators=(',',':')).replace('</','<\\/'), base64.b64encode(salt+iv+ct).decode()

def build_student():
    d = student_data()
    for sub in d:
        for sec in sub['sections']:
            for g in sec['groups']: g['k']=sec['name']+'|'+g['name']
    tpl = open(os.path.join(OUT,'student_tpl.html'),encoding='utf-8').read()
    sj,tenc = sheets_blobs()
    page = tpl.replace('__SHEETS__',sj).replace('__TENC__',tenc).replace('__KATEXCSS__', KCSS).replace('__DATA__', json.dumps(d, ensure_ascii=False, separators=(',',':')).replace('</','<\\/'))
    open(os.path.join(OUT,'student.html'),'w',encoding='utf-8').write(page)
    return len(page)

PRINT_CSS = """
@page{size:A4;margin:13mm 14mm}
*{box-sizing:border-box}
body{font-family:'Noto Sans CJK JP','BIZ UDPGothic','Yu Gothic',sans-serif;font-size:10.5pt;line-height:1.75;color:#000;margin:0}
.sheet{page-break-after:always}.sheet:last-child{page-break-after:auto}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #000;padding-bottom:6px;margin-bottom:10px;gap:10px}
.hd .t{font-size:14pt;font-weight:700;line-height:1.35}.hd .s{font-size:8.5pt;letter-spacing:.08em}
.hd .nm{font-size:10pt;white-space:nowrap}
.q{break-inside:avoid;margin:0 0 9px;padding:0 0 6px;border-bottom:1px dotted #999}
.qt{margin:0 0 3px}.no{display:inline-block;min-width:2.6em;font-weight:700}
.ch{display:grid;grid-template-columns:1fr 1fr;gap:1px 14px;padding-left:2.6em}
.ch div{display:flex;gap:6px}.ch b{flex:none;font-weight:700}
.ans{float:right;font-size:9.5pt;margin-left:10px}.ans u{display:inline-block;width:3em;text-decoration:none;border-bottom:1px solid #000}
.cl{font-size:9pt;font-weight:700;margin:8px 0 4px;padding:1px 6px;background:#e8e8e8}
.key{display:grid;grid-template-columns:repeat(auto-fill,minmax(5.5em,1fr));gap:2px 6px;font-size:10pt;margin-bottom:10px;border:1px solid #000;padding:6px 8px}
.key span b{display:inline-block;min-width:1.9em}
table{border-collapse:collapse;width:100%;font-size:9.5pt}
th,td{border:1px solid #777;padding:3px 6px;vertical-align:top;text-align:left}
th{background:#e8e8e8}tr{break-inside:avoid}
td.n{white-space:nowrap;text-align:center;width:2.6em}td.a{white-space:nowrap;text-align:center;width:3.2em;font-weight:700}
.w{font-size:8.6pt;color:#222}.w div{margin:0}
h3.sub{font-size:11pt;margin:12px 0 4px}
.tc{font-size:8.5pt;margin-top:8px;border:1px solid #000;padding:3px 8px;display:inline-block}
.katex{font-size:1.1em}
""" 

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def problems_html(g, sets, teacher=True):
    out=[]
    for s in sets:
        m=s['math']
        o=['<section class="sheet"><div class="hd"><div><div class="s">江原予備校　GAMBA　テスト（講師用）</div><div class="t">%s　%s</div></div><div class="nm">名前（　　　　　　　　　）　　　　<b>　　　</b>／%d点</div></div>'%(esc(s['group']),s['label'] if s['label']!='テストをはじめる' else '',s['n'])]
        last=-1
        for i,q in enumerate(s['qs']):
            if len(s['cats'])>1 and q[0]!=last:
                last=q[0]; o.append('<div class="cl">%s</div>'%fmt(s['cats'][q[0]][0],m))
            o.append('<div class="q"><div class="ans">答え <u></u></div><p class="qt"><span class="no">問%d</span>%s</p><div class="ch">%s</div></div>'%(i+1,fmt(q[1],m),''.join('<div><b>%s</b><span>%s</span></div>'%("アイウエ"[j],fmt(c,m)) for j,c in enumerate(q[2]))))
        o.append('</section>'); out.append(''.join(o))
    return out
def answers_html(g, sets):
    out=[]
    for s in sets:
        m=s['math']
        o=['<section class="sheet"><div class="hd"><div><div class="s">江原予備校　GAMBA　解答・解説（講師用・生徒に渡さないでください）</div><div class="t">%s　%s</div></div><div class="nm">全%d問</div></div>'%(esc(s['group']),s['label'] if s['label']!='テストをはじめる' else '',s['n'])]
        o.append('<div class="key">'+''.join('<span><b>問%d</b>%s</span>'%(i+1,"アイウエ"[q[3]]) for i,q in enumerate(s['qs']))+'</div>')
        o.append('<table><tr><th>問</th><th>正解</th><th>解説とつまずきメモ</th></tr>')
        for i,q in enumerate(s['qs']):
            ans=fmt(q[2][q[3]],m)
            w=''.join('<div>%s：%s</div>'%("アイウエ"[j],fmt(t,m)) for j,t in sorted(q[4].items()))
            o.append('<tr><td class="n">%d</td><td class="a">%s<br>%s</td><td>%s%s</td></tr>'%(i+1,"アイウエ"[q[3]],ans,fmt(q[5],m),('<div class="w">'+w+'</div>') if w else ''))
        o.append('</table>')
        if len(s['cats'])>1:
            o.append('<h3 class="sub">分類ごとの復習と指導のポイント</h3><table><tr><th>分類</th><th>該当問</th><th>復習する教材</th><th>指導のポイント</th></tr>')
            for ci,c in enumerate(s['cats']):
                qn=[str(i+1) for i,q in enumerate(s['qs']) if q[0]==ci]
                o.append('<tr><td>%s</td><td class="n" style="width:5em">%s</td><td>%s</td><td>%s</td></tr>'%(fmt(c[0]+('（'+c[1]+'）' if c[1] else ''),m),'・'.join(qn),esc(c[2]),fmt(c[3],m)))
            o.append('</table>')
        o.append('</section>'); out.append(''.join(o))
    return out
def doc(parts, title):
    return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>%s</title><style>%s\n%s</style></head><body>%s</body></html>'%(esc(title),KCSS,PRINT_CSS,''.join(parts))

def groups():
    gs={}
    for i,s in sorted(allsets.items()):
        gs.setdefault((s['section'],s['group']),[]).append(s)
    return gs

def build_pdfs():
    from playwright.sync_api import sync_playwright
    pdfdir=os.path.join(OUT,'pdf'); os.makedirs(pdfdir,exist_ok=True)
    SUBJN={'math':'数学','sci':'理科','soc':'社会'}
    gs=groups(); files=[]
    with sync_playwright() as pw:
        br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox'])
        pg=br.new_page()
        n=0
        for (sec,g),sets in sorted(gs.items(), key=lambda kv:(SECORDER.index(kv[0][0]) if kv[0][0] in SECORDER else 99, kv[1][0]['id'])):
            sets=sorted(sets,key=lambda s:s['id']); n+=1
            subj=SUBJN[sets[0]['subject']]
            base='%02d_%s_%s'%(n,subj,re.sub(r'[／/\s　]+','_',g))
            for kind,fn in (('問題',problems_html),('解答解説',answers_html)):
                html=doc(fn(g,sets),'%s %s'%(g,kind))
                hp=os.path.join(OUT,'tmp_%s.html'%kind); open(hp,'w',encoding='utf-8').write(html)
                pg.goto('file://'+hp); pg.wait_for_timeout(300)
                path=os.path.join(pdfdir,'%s_%s.pdf'%(base,kind))
                pg.pdf(path=path,format='A4',print_background=True,prefer_css_page_size=True)
                files.append(path)
        br.close()
    return files

if __name__=='__main__':
    print('loaded', loaded, 'sets', len(allsets))
    print('student.html bytes', build_student())
    if '--pdf' in sys.argv:
        fs=build_pdfs(); print(len(fs),'pdfs')
