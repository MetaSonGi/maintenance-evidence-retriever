"""장비·문서 개정·유효 시점을 먼저 걸러 BM25로 정비 문서의 관련 절을 찾고 인용 ID와 원문을 반환합니다."""
import argparse, json, math, html
from pathlib import Path

def finite(value, name, minimum=None):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(name + ': finite number required')
    if minimum is not None and value < minimum:
        raise ValueError(name + ': below minimum')
    return value

def report(result, title):
    payload=html.escape(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:32px auto;padding:20px;background:#101b2b;color:#ecf4ff}pre{padding:24px;background:#192b40;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}h1{color:#80e4c5}</style><h1>'+html.escape(title)+'</h1><p>오프라인 샘플 계산 결과 · 실물 장비 연결 없음</p><pre>'+payload+'</pre></html>'

def cli(run,title):
    parser=argparse.ArgumentParser(description=title)
    parser.add_argument('--input',default=str(Path(__file__).with_name('sample-input.json')))
    parser.add_argument('--html',help='optional standalone HTML result path')
    args=parser.parse_args()
    try:
        data=json.loads(Path(args.input).read_text(encoding='utf-8'))
        result=run(data)
        if args.html: Path(args.html).write_text(report(result,title),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError) as exc:
        parser.exit(2, 'input error: '+str(exc)+'\n')

import re
from collections import Counter
from datetime import date

def tokens(text):return re.findall(r'[\w]+',text.lower(),flags=re.UNICODE)
def run(data):
    query=tokens(data['query']);asset=data['asset_id'];as_of=date.fromisoformat(data['as_of']);k=data.get('top_k',3)
    if type(k) is not int or k<1:raise ValueError('positive top_k required')
    latest={};seen=set()
    for d in data['documents']:
        identity=(d['id'],d['revision'])
        if identity in seen:raise ValueError('duplicate document revision')
        seen.add(identity)
        if type(d['revision']) is not int or d['revision']<1:raise ValueError('positive revision required')
        published=date.fromisoformat(d['effective_from'])
        if d['asset_id']!=asset or published>as_of:continue
        previous=latest.get(d['id'])
        if previous is None or d['revision']>previous['revision']:latest[d['id']]=d
    sections=[]
    for d in latest.values():
        section_ids=set()
        for section in d['sections']:
            if section['id'] in section_ids:raise ValueError('duplicate section ID')
            section_ids.add(section['id']);terms=tokens(section['text']);sections.append((d,section,Counter(terms),len(terms)))
    if not query or not sections:return {'status':'no_evidence','hits':[],'generated_answer':None}
    n=len(sections);avg=max(1,sum(s[3] for s in sections)/n);hits=[]
    for d,s,counts,length in sections:
        score=0;matched=[]
        for term in sorted(set(query)):
            tf=counts[term]
            if not tf:continue
            df=sum(1 for item in sections if item[2][term]);idf=math.log(1+(n-df+0.5)/(df+0.5))
            score+=idf*(tf*2.2)/(tf+1.2*(0.25+0.75*length/avg));matched.append(term)
        if score>0:hits.append({'citation':f"{d['id']}@{d['revision']}#{s['id']}",'asset_id':asset,'source':d['source'],
                              'text':s['text'],'matched_terms':matched,'score':round(score,6)})
    hits=sorted(hits,key=lambda h:(-h['score'],h['citation']))[:k]
    return {'status':'evidence_found' if hits else 'no_evidence','hits':hits,'generated_answer':None}

if __name__ == "__main__": cli(run,'정비 문서 근거 검색기')
