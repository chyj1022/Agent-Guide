"""Small lexical search, no model or network. Usage: python scripts/search_topics.py MCP"""
from pathlib import Path
import argparse
import json
import re
import sys

if hasattr(sys.stdout,'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

parser=argparse.ArgumentParser(description='Search stable topic IDs, Korean/English titles and keywords')
parser.add_argument('query',nargs='+')
parser.add_argument('--limit',type=int,default=8)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
topics=json.loads((root/'metadata/topics.json').read_text(encoding='utf-8'))
words=re.findall(r'[\w-]+',' '.join(args.query).lower())
rank=[]
for t in topics:
    title=(t['id']+' '+t['title']+' '+' '.join(t['keywords'])).lower()
    summary=t['summary'].lower()
    score=sum((5 if w in title else 0)+(1 if w in summary else 0) for w in words)
    if score:rank.append((score,t))
for score,t in sorted(rank,key=lambda x:(-x[0],x[1]['id']))[:max(0,args.limit)]:
    print(json.dumps({'id':t['id'],'title':t['title'],'path':t['path'],'summary':t['summary'],'score':score},ensure_ascii=False))
if not rank:print('No lexical match. Try a synonym or browse docs/ROUTES.md.')
