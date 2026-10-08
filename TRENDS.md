# 논문 근거와 개발자 해석

조사 기준일: **2026-10-09 (Asia/Seoul)**. 확인 범위: 저자 원문 저장소 arXiv의 초록·제출 이력·comments·관련 DOI. 전문 실험·부록·코드 및 성능 재현은 확인하지 않았습니다. 최신 검색에 나온 일부 원문(2609.09625, 2609.32923)은 열기 실패로 설계 근거에서 제외했습니다. 아래는 완전한 최신 문헌 조사나 최신 순위가 아닙니다.

## Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

- 원문: https://arxiv.org/abs/2005.11401
- 발표/제출일: 2020-05-22 (v1), 2021-04-12 (v4)
- 상태: NeurIPS 2020 채택 표기 확인; 기초 논문이며 최신 발표 아님
- 확인한 사실(초록): 검색 가능한 외부 기억과 생성 모델을 결합하며 지식 갱신과 출처 제공을 다룹니다.
- 개발자 해석: 생성 단계 전에 장비별 개정·시점·출처를 검증하는 검색 기반선을 독립적으로 시험합니다.

## Industrial Semantics-Aware Digital Twins: A Hybrid Graph Matching Approach for Asset Administration Shells

- 원문: https://arxiv.org/abs/2601.06613
- 발표/제출일: 2026-01-10
- 상태: arXiv v1; CCNC 관련 DOI(10.1109/CCNC65079.2026.11366338) 연결 확인, 학회 최종본 전문 미확인
- 확인한 사실(초록): AAS의 서로 다른 어휘와 모델링 관례에 대응해 SPARQL 사전 필터와 RDF2vec 유사도 결합을 제안합니다.
- 개발자 해석: 속성 표시명보다 semantic ID·단위·장비 관계를 명시하는 계약이 먼저 필요합니다.

## Digital Twin AI: Opportunities and Challenges from Large Language Models to World Models

- 원문: https://arxiv.org/abs/2601.01321
- 발표/제출일: 2026-01-04
- 상태: arXiv preprint v1; 조회 페이지에 학회 채택 표기 없음
- 확인한 사실(초록): AI 통합을 modeling, mirroring, intervention, autonomous management의 네 단계로 정리합니다.
- 개발자 해석: 상태 동기화·시뮬레이션·검증·개입을 분리해 자동화의 책임 경계를 명확히 둡니다.

## 이 프로그램의 적용

검색 전에 장비 ID·유효 날짜·최신 개정을 필터링합니다. 다른 장비의 유사한 문장을 점수가 높다는 이유만으로 반환하지 않습니다. 검색 후보 집합 내 문서빈도로 BM25를 계산하고 인용은 문서@개정#절로 고정합니다. no_evidence는 정상적인 결과입니다.

논문의 TSFM·임베딩·LLM·실험 모델을 재현한 것이 아닙니다. 표준 라이브러리 기반의 설명 가능한 오프라인 도구입니다. 논문 성능 수치나 물리 장비 검증을 주장하지 않습니다.
