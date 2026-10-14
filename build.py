#!/usr/bin/env python3
"""零依赖静态站构建：issues/*.json -> public/*.html"""
import json, glob, os, html, re
R=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(R,'public')
SITE='Grok Bot / Claude Code 投资策略教程与新玩法'
CSS="""body{font-family:system-ui,'PingFang TC','Noto Sans CJK SC',sans-serif;max-width:820px;margin:auto;padding:1em;line-height:1.7;color:#222}
a{color:#0a58ca}nav a{margin-right:1em}.item{border:1px solid #ddd;border-radius:8px;padding:.8em 1.2em;margin:1em 0}
.flag{background:#fff3cd;border:2px solid #e0a800;padding:.3em .6em;border-radius:4px;font-weight:bold;display:inline-block}
.note{background:#e7f1ff;padding:.3em .6em;border-radius:4px}.meta{color:#666;font-size:.9em}
details{background:#f6f8fa;border-radius:6px;padding:.4em .8em;margin:.6em 0}summary{cursor:pointer;font-weight:bold}.sum{background:#eef7ee;padding:.4em .6em;border-radius:4px}.caution{color:#a00}
.item ol{padding-left:1.4em}footer{margin-top:3em;border-top:1px solid #ddd;padding-top:1em;color:#a00;font-weight:bold;font-size:.95em}"""
e=html.escape
def page(title,body):
    return f"""<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><style>{CSS}</style></head><body>
<header><h2><a href="index.html">{e(SITE)}</a></h2><nav><a href="index.html">首页</a><a href="anti-scam.html">防骗提醒</a></nav></header>
<main>{body}</main><footer>本站内容仅为工具与教程信息整理，不构成投资建议。交易有风险，请自行判断并承担责任。</footer></body></html>"""
def md(t):  # 极简 markdown：# 标题、- 列表、**粗体**、段落
    o=[];inl=False
    for l in t.splitlines():
        s=e(l.strip()); s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
        if s.startswith('- '):
            if not inl:o.append('<ul>');inl=True
            o.append(f'<li>{s[2:]}</li>');continue
        if inl:o.append('</ul>');inl=False
        if s.startswith('# '):o.append(f'<h1>{s[2:]}</h1>')
        elif s:o.append(f'<p>{s}</p>')
    if inl:o.append('</ul>')
    return '\n'.join(o)
def howto(h):
    if not h: return ''
    if isinstance(h,list): h={'steps':h}
    st=''.join(f'<li>{e(x)}</li>' for x in h.get('steps',[]))
    c=f"<p class=caution>{e(h['caution'])}</p>" if h.get('caution') else ''
    return f"<details open><summary>怎么用</summary>{'<ol>'+st+'</ol>' if st else ''}{c}</details>"
def main():
    os.makedirs(OUT,exist_ok=True)
    issues=sorted((json.load(open(f,encoding='utf-8')) for f in glob.glob(os.path.join(R,'issues','*.json'))),key=lambda x:x['date'],reverse=True)
    lis=[]
    for iss in issues:
        b=[f"<h1>{e(iss['title'])}</h1><p class=meta>发布：{e(iss['date'])}｜收录范围：{e(iss.get('range',''))}</p>"]
        for i,it in enumerate(iss['items'],1):
            b.append('<div class=item>'+f"<h3>{i}. {e(it['title'])}</h3>"+(f"<p class=flag>⚠️ {e(it['flag'])}</p>" if it.get('flag') else '')
              +(f"<p class=sum><strong>一句话总结：</strong>{e(it['summary'])}</p>" if it.get('summary') else '')+howto(it.get('howto'))
              +'<ul>'+''.join(f'<li>{e(p)}</li>' for p in it['points'])+'</ul>'
              +(f"<p class=note>{e(it['note'])}</p>" if it.get('note') else '')
              +f"<p class=meta>作者 {e(it['author'])}｜{e(it['time'])}（台北时间）{('｜'+e(it['stats'])) if it.get('stats') else ''}｜<a href=\"{e(it['url'])}\" rel=\"noopener nofollow\">原帖</a></p></div>")
        fn=f"issue-{iss['date']}.html"; open(os.path.join(OUT,fn),'w',encoding='utf-8').write(page(iss['title'],'\n'.join(b)))
        lis.append(f"<li><a href=\"{fn}\">{e(iss['date'])}｜{e(iss['title'])}</a>（{len(iss['items'])} 条）</li>")
    open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page(SITE,f"<h1>往期列表</h1><p>每期整理 X 上与投资策略相关的 Grok Bot / Claude Code 教程、工具与新玩法。</p><ul>{''.join(lis)}</ul>"))
    for f in glob.glob(os.path.join(R,'pages','*.md')):
        n=os.path.splitext(os.path.basename(f))[0]; t=open(f,encoding='utf-8').read()
        open(os.path.join(OUT,n+'.html'),'w',encoding='utf-8').write(page(t.splitlines()[0].lstrip('# '),md(t)))
    print('built',len(issues),'issues ->',OUT)
if __name__=='__main__':main()
