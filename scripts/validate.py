"""Validate public artifact structure; does not certify semantic source fidelity."""
from pathlib import Path
import csv
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors=[]
def check(ok,message):
    if not ok: errors.append(message)

def anchor(text):
    text=re.sub(r'<[^>]+>','',text).strip().lower()
    text=re.sub(r'[^\w\- ]','',text)
    return text.replace(' ','-')

for file in ROOT.rglob('*.json'):
    try: json.loads(file.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'Invalid JSON {file.relative_to(ROOT)}: {e}')

topic_path=ROOT/'metadata/topics.json'
if topic_path.exists():
    topics=json.loads(topic_path.read_text(encoding='utf-8'))
    check(len(topics)==96,f'Expected 96 topics, got {len(topics)}')
    ids=[t['id'] for t in topics]
    expected={f'AGC-{i:03}' for i in range(1,38)}|{f'AGT-{i:03}' for i in range(1,60)}
    check(set(ids)==expected and len(ids)==len(set(ids)),'Topic IDs missing or duplicated')
    for t in topics:
        p=ROOT/t['path']
        check(p.is_file(),f'Missing topic file {t["path"]}')
        if p.exists(): check(t['id'] in p.read_text(encoding='utf-8'),f'Topic ID absent: {t["id"]}')
        check(bool(t.get('source_anchor')),f'Missing source anchor {t["id"]}')
else: errors.append('Missing metadata/topics.json')

coverage=ROOT/'metadata/page-coverage.csv'
if coverage.exists():
    with coverage.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    check(len(rows)==178,f'Expected 178 page rows, got {len(rows)}')
    for sid,count in [('SRC-01',53),('SRC-02',125)]:
        nums=[int(r['page']) for r in rows if r['source_id']==sid]
        check(sorted(nums)==list(range(1,count+1)),f'Invalid page inventory: {sid}')
    for r in rows:
        for tid in (r['candidate_topic_ids']+';'+r.get('manual_topic_ids','')).split(';'):
            if tid: check(tid in expected,f'Unknown page topic {tid}')
else: errors.append('Missing page coverage')

link_count=0
for file in list(ROOT.rglob('*.md'))+[ROOT/'llms.txt']:
    body=file.read_text(encoding='utf-8')
    check(not re.search(r'(?i)(?:[A-Z]:[\\/]+Users[\\/]|/mnt/c/Users/)',body),f'Private machine path: {file.relative_to(ROOT)}')
    # Fenced code examples may contain sample Markdown links, so skip fences.
    text=re.sub(r'```.*?```','',body,flags=re.S)
    for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
        url=match.group(1).strip().strip('<>')
        parsed=urlsplit(url)
        if parsed.scheme or url.startswith('//'):continue
        target=(file.parent/unquote(parsed.path)).resolve() if parsed.path else file
        link_count+=1
        check(target.is_relative_to(ROOT),f'Link outside package: {file.relative_to(ROOT)} -> {url}')
        check(target.exists(),f'Broken link: {file.relative_to(ROOT)} -> {url}')
        if parsed.fragment and target.is_file() and target.suffix=='.md':
            heads=[anchor(x) for x in re.findall(r'^#{1,6}\s+(.+)$',target.read_text(encoding='utf-8'),flags=re.M)]
            check(unquote(parsed.fragment) in heads,f'Unknown anchor: {file.relative_to(ROOT)} -> {url}')

for file in ROOT.rglob('*'):
    if not file.is_file():continue
    if '__pycache__' in file.parts:continue
    check(file.suffix.lower() not in {'.pdf','.png','.jpg','.zip'},f'Raw or packaged artifact inside source: {file.relative_to(ROOT)}')
    check(not file.name.startswith('.env'),f'Unexpected env file: {file.relative_to(ROOT)}')

if errors:
    print('\n'.join('FAIL '+e for e in errors));sys.exit(1)
print(f'PASS: 96 topic IDs, 178 PDF page entries, JSON syntax, {link_count} local links, public source boundaries')
