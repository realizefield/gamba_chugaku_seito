# -*- coding: utf-8 -*-
import re, json, subprocess, os, html as H
_here=os.path.dirname(os.path.abspath(__file__))
_p=None; _cache={}
def tex(t):
    global _p
    if t in _cache: return _cache[t]
    if _p is None:
        _p=subprocess.Popen(['node','texsrv.js'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,cwd=_here,encoding='utf-8')
    _p.stdin.write(json.dumps(t)+"\n"); _p.stdin.flush()
    r=json.loads(_p.stdout.readline())
    if r is None: raise ValueError('KaTeX failed: '+t)
    _cache[t]=r; return r
MATHCH = r"A-Za-z0-9+\-−＋＝=()（）.,，{}|√×÷：:"
RUN = re.compile(r"[A-Za-z0-9+\-−＋＝=(（{√][%s ]*" % MATHCH)
TRIG = re.compile(r"[A-Za-z{√＝=＋+×÷：]")
def to_tex(run):
    r=run.strip()
    while True:
        n=re.sub(r"\{([^{}|]+)\|([^{}|]+)\}", lambda m:"\\dfrac{%s}{%s}"%(m.group(1),m.group(2)), r)
        if n==r: break
        r=n
    r=re.sub(r"√(\d+)", r"\\sqrt{\1}", r)
    r=r.replace("√","\\sqrt")
    rep={"＝":"=","＋":"+","−":"-","×":"\\times ","÷":"\\div ","：":"\\colon ","，":",","（":"(","）":")","χ":"x"," ":"\\,"}
    for k,v in rep.items(): r=r.replace(k,v)
    return r
def fmt(s, math=False):
    s=s.replace('χ','x')
    if not math:
        s=re.sub(r"\{([^{}|]+)\|([^{}|]+)\}", lambda m:"%s/%s"%(m.group(1),m.group(2)), s)  # 保険（通常は使わない）
        return H.escape(s)
    out=[];i=0
    for m in RUN.finditer(s):
        out.append(H.escape(s[i:m.start()]))
        run=m.group(0); core=run.rstrip(); tail=run[len(core):]
        if TRIG.search(core): out.append(tex(to_tex(core)))
        else: out.append(H.escape(core))
        out.append(H.escape(tail)); i=m.end()
    out.append(H.escape(s[i:]))
    return ''.join(out)
