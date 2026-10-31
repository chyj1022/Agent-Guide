"""Generate self-contained reading view; source Markdown remains authoritative."""
from pathlib import Path
import html
import re
from urllib.parse import unquote,urlsplit
import markdown

ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'README.md',ROOT/'docs/START_HERE.md',ROOT/'docs/ROUTES.md',ROOT/'docs/PROMPTS.md']
files+=sorted((ROOT/'docs/design').glob('*.md'))
files+=[ROOT/'docs/CONCEPTS.md']+sorted((ROOT/'docs/concepts/agentic').glob('*.md'))+sorted((ROOT/'docs/concepts/agent').glob('*.md'))
files+=sorted((ROOT/'templates').glob('*.md'))+[ROOT/'contracts/README.md',ROOT/'examples/harness/README.md',ROOT/'AGENTS.md',ROOT/'SOURCE_POLICY.md']
files+=sorted((ROOT/'sources').glob('*.md'))+[ROOT/'docs/VERIFICATION.md',ROOT/'PUBLISHING.md']
def docid(p):return 'doc-'+re.sub(r'[^a-z0-9]+','-',str(p.relative_to(ROOT)).replace('\\','/').lower()).strip('-')
ids={p.resolve():docid(p) for p in files}
nav=[]; sections=[]
for p in files:
    source=p.read_text(encoding='utf-8')
    title=re.search(r'^#\s+(.+)$',source,re.M).group(1)
    key=ids[p.resolve()]
    body=markdown.markdown(source,extensions=['extra','toc','sane_lists'])
    body=re.sub(r'\bid="([^"]+)"',lambda m:'id="'+key+'--'+m.group(1)+'"',body)
    def rewrite(m):
        raw=html.unescape(m.group(1));parsed=urlsplit(raw)
        if parsed.scheme or raw.startswith('//'):return m.group(0)
        target=(p.parent/unquote(parsed.path)).resolve() if parsed.path else p.resolve()
        if target in ids:
            dest='#'+ids[target]+('--'+parsed.fragment if parsed.fragment else '')
        else:
            dest=str(target.relative_to(ROOT)).replace('\\','/') if target.is_relative_to(ROOT) else raw
            if parsed.fragment:dest+='#'+parsed.fragment
        return 'href="'+html.escape(dest,quote=True)+'"'
    body=re.sub(r'href="([^"]*)"',rewrite,body)
    nav.append(f'<a class="navitem" href="#{key}" data-for="{key}">{html.escape(title)}</a>')
    sections.append(f'<article class="doc" id="{key}" hidden><div class="filepath">{html.escape(str(p.relative_to(ROOT)).replace(chr(92),"/"))}</div>{body}</article>')

style='''
:root{font-family:"Malgun Gothic",system-ui,sans-serif;color:#17243b;background:#f1f5fa;line-height:1.8}
*{box-sizing:border-box}body{margin:0}header{padding:18px 28px;background:#12233e;color:white;position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;gap:16px}header b{font-size:22px}header span{color:#bfccdf;font-size:13px}button{border:0;background:#d7e7ff;color:#15335e;padding:10px 15px;border-radius:8px;font-weight:bold;cursor:pointer}.layout{display:grid;grid-template-columns:310px minmax(0,1fr);max-width:1500px;margin:auto}aside{position:sticky;top:83px;height:calc(100vh - 83px);padding:20px 14px 20px 22px;overflow:auto;border-right:1px solid #d5ddeb;background:#f7f9fd}input{width:100%;padding:12px;border:1px solid #bccade;border-radius:8px;font:inherit;background:white}#found{font-size:12px;color:#53637c;margin:8px 0}.navitem{display:block;font-size:13px;line-height:1.6;padding:9px 10px;border-radius:7px;text-decoration:none;color:#304564;border-bottom:1px solid #e6ebf3}.navitem:hover,.navitem.active{background:#dceaff;color:#123e80}.navitem:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #1e69be;outline-offset:2px}main{padding:35px 42px 80px;min-width:0}.doc{background:white;padding:32px 38px;border:1px solid #dde4ef;border-radius:14px;box-shadow:0 6px 24px #233b5d08}.filepath{font:12px ui-monospace,monospace;color:#627792;overflow-wrap:anywhere}h1{font-size:29px;line-height:1.45;margin:12px 0 26px}h2{font-size:21px;margin-top:34px;border-bottom:1px solid #e1e7f0;padding-bottom:9px}h3{font-size:17px;margin-top:25px}a{color:#1457a2;text-underline-offset:3px}p,li{overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#14243b;color:#e1ebf9;padding:19px;border-radius:9px;line-height:1.6;font-size:13px}code{font-family:Consolas,ui-monospace,monospace}p code,li code,td code{background:#edf2f8;padding:2px 5px;border-radius:4px;font-size:.9em}table{border-collapse:collapse;width:100%;font-size:13px;margin:20px 0;display:block;overflow-x:auto}td,th{border:1px solid #dce3ee;padding:10px 12px;text-align:left;vertical-align:top}th{background:#edf3fb}blockquote{border-left:4px solid #5e8cca;margin:18px 0;padding:6px 18px;background:#f2f6fc}.footer{font-size:12px;color:#5a6a80;margin:24px 4px}.doc[hidden],.navitem[hidden]{display:none!important}@media(max-width:850px){header{padding:14px;position:static;align-items:flex-start}.layout{display:block}aside{position:static;height:280px;border-right:0;border-bottom:1px solid #d5ddeb;padding:15px}main{padding:18px 10px}.doc{padding:22px 18px}h1{font-size:24px}header span{display:block}}@media print{header,aside,.filepath,.footer{display:none}.layout{display:block}main{padding:0}.doc{border:0;box-shadow:none;padding:0}pre{background:#f0f0f0;color:black}.doc[hidden]{display:none!important}}
'''
script='''
const articles=[...document.querySelectorAll('.doc')],items=[...document.querySelectorAll('.navitem')];
function show(){let hash=decodeURIComponent(location.hash.slice(1)),doc=articles.find(a=>hash===a.id||hash.startsWith(a.id+'--'))||articles[0];articles.forEach(a=>a.hidden=a!==doc);items.forEach(a=>a.classList.toggle('active',a.dataset.for===doc.id));document.title=doc.querySelector('h1').textContent+' | Agent Guide';if(hash.includes('--'))requestAnimationFrame(()=>document.getElementById(hash)?.scrollIntoView());else window.scrollTo(0,0)}
window.addEventListener('hashchange',show);show();
document.getElementById('q').addEventListener('input',e=>{const q=e.target.value.toLowerCase().trim();let count=0;items.forEach((item,i)=>{const match=!q||articles[i].textContent.toLowerCase().includes(q);item.hidden=!match;if(match)count++});document.getElementById('found').textContent=count+'개 문서 일치 / '+items.length+'개';});
document.getElementById('print').addEventListener('click',()=>window.print());
document.getElementById('found').textContent=items.length+'개 문서, 인터넷 없이 검색 가능';
'''
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Agent Guide</title><style>'+style+'</style></head><body><header><div><b>Agent Guide</b><br><span>96개 개념 · Agent, MCP, 하네스 설계와 검증</span></div><button id="print" type="button">현재 문서 인쇄</button></header><div class="layout"><aside aria-label="문서 탐색"><label for="q">전체 본문 검색</label><input id="q" type="search" placeholder="MCP, 승인, AGT-040 등"><div id="found" aria-live="polite"></div><nav>'+''.join(nav)+'</nav></aside><main>'+''.join(sections)+'<div class="footer">원문 전문 배포본이 아닙니다. 자동 쪽 대응과 직접 확인 범위를 출처 정책에서 구분합니다. Mermaid 구조도는 원문 코드로 표시합니다.</div></main></div><script>'+script+'</script></body></html>'
(ROOT/'guide.html').write_text(page,encoding='utf-8')
print(f'Built guide.html: {len(files)} documents, {len(page.encode("utf-8")):,} bytes')
