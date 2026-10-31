"""Build public indexes from curated metadata, never from unpublished originals."""
from pathlib import Path
import csv
import json

ROOT=Path(__file__).resolve().parents[1]
def dump(path,value):
    (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

topics=[]
for filename in ['agentic-topics.json','agent-topics.json']:
    topics.extend(json.loads((ROOT/'metadata'/filename).read_text(encoding='utf-8')))
with (ROOT/'metadata/page-coverage.csv').open(encoding='utf-8-sig',newline='') as f: pages=list(csv.DictReader(f))
related={
    'AGC-001':['AGT-001','AGT-003'], 'AGC-007':['AGT-012','AGT-032'],
    'AGC-011':['AGT-027','AGT-029'], 'AGC-012':['AGT-016','AGT-017'],
    'AGC-014':['AGT-023','AGT-031'], 'AGC-024':['AGT-040','AGT-056'],
    'AGC-029':['AGT-034','AGT-046'], 'AGC-034':['AGT-044','AGT-058']}
for t in topics:
    t['pdf_page_candidates']=[int(r['page']) for r in pages if r['source_id']==t['source_id'] and t['id']==r['candidate_topic_ids'].split(';')[0]]
    t['pdf_mapping_status']='automatic_candidates_not_verified_citations'
    t['manually_sampled_pages']=[int(r['page']) for r in pages if t['id'] in r.get('manual_topic_ids','').split(';')]
    t['related_topics']=related.get(t['id'],[])+[a for a,values in related.items() if t['id'] in values]
dump(Path('metadata/topics.json'),topics)

lines=['# 전체 개념 색인','','96개 주제를 강의 순서와 안정적인 ID로 찾습니다. 본문은 원자료 재서술이며 설계 적용과 복습 문답은 AI 보완입니다. PDF 쪽별 대응의 자동 추정은 확정 인용이 아닙니다.','',
       '기계 판독: [topics.json](../metadata/topics.json). 적용 경로: [ROUTES](ROUTES.md). 출처: [정책](../SOURCE_POLICY.md).','']
for sid,title in [('SRC-01','Agentic AI, 위임과 조직 통제'),('SRC-02','AI Agent, 도구와 실행 상태')]:
    lines+=['## '+title,'']
    for t in topics:
        if t['source_id']==sid:
            path='../'+t['path']
            lines += [f'- [{t["id"]} {t["title"]}]({path}): {t["summary"]}']
    lines+=['']
(ROOT/'docs/CONCEPTS.md').write_text('\n'.join(lines).rstrip('\n')+'\n',encoding='utf-8')

sources=json.loads((ROOT/'metadata/sources.json').read_text(encoding='utf-8'))
(ROOT/'sources').mkdir(exist_ok=True)
for src in sources:
    sid=src['id']
    lines=[f'# {sid}, {src["name"]}','','사용자 제공 이미지 PDF의 출처 카드입니다. 이 파일에는 PDF 본문이나 OCR 전문을 배포하지 않습니다.','',
           f'- PDF 쪽 수: {src["pages"]}',f'- 개념 주제 수: {src["topic_count"]}',f'- SHA-256: `{src["sha256"]}`','',
           '전체 주제의 본문 판독에는 같은 강의의 보관 HTML을 보조로 활용했습니다. PDF는 쪽별 OCR을 수행했고 두 PDF 전체에서 합계 4쪽만 제한적으로 직접 시각 대조했습니다. 모든 문장이나 그림을 원본과 수동 대조한 상태가 아닙니다.','',
           '[쪽별 대응 CSV](../metadata/page-coverage.csv), [판독/공개 정책](../SOURCE_POLICY.md), [전체 주제 JSON](../metadata/topics.json)을 함께 읽으세요.','',
           '## 주제와 본문 경로','']
    for t in topics:
        if t['source_id']==sid:
            lines.append(f'- [{t["id"]} {t["title"]}](../{t["path"]}), 보조 HTML 앵커 `{t["source_anchor"]}`')
    if src.get('auxiliary_original_url'):
        lines += ['', '## 보관 HTML에서 확인한 원문 링크', '',
                  f'[사이트 원문]({src["auxiliary_original_url"]}). 보관 HTML의 링크를 확인한 것이며 현재 온라인 내용의 일치를 검증한 것은 아닙니다.']
    (ROOT/'sources'/f'{sid}.md').write_text('\n'.join(lines).rstrip('\n')+'\n',encoding='utf-8')
print(f'Built {len(topics)} topic records, concept index and source cards')
