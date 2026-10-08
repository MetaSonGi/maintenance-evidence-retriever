# 정비 문서 근거 검색기

장비·문서 개정·유효 시점을 먼저 걸러 BM25로 정비 문서의 관련 절을 찾고 인용 ID와 원문을 반환합니다.

## 핵심 기능

검색 전에 장비 ID·유효 날짜·최신 개정을 필터링합니다. 다른 장비의 유사한 문장을 점수가 높다는 이유만으로 반환하지 않습니다. 검색 후보 집합 내 문서빈도로 BM25를 계산하고 인용은 문서@개정#절로 고정합니다. no_evidence는 정상적인 결과입니다.

## 설치·실행

Python 3.10 이상. 외부 패키지·API 키·장비 연결이 필요 없습니다.

```bash
git clone https://github.com/MetaSonGi/maintenance-evidence-retriever.git
cd maintenance-evidence-retriever
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
```

Windows에서 python 대신 py를 사용할 수 있습니다. 다른 디렉터리에서 실행해도 기본 샘플은 main.py 옆 파일에서 읽습니다. 모든 출력 파일 경로는 명시한 위치에 생성합니다.

## 웹에서 결과 확인

다운로드한 `example-report.html`을 브라우저에서 열면 검증한 샘플 결과가 보입니다. 입력을 수정하고 `python main.py --input sample-input.json --html result.html`을 실행하면 새 결과를 브라우저로 볼 수 있습니다. 보고서는 HTML에 결과를 포함하므로 네트워크·CDN·서버가 필요 없습니다. 입력 문자열은 escape해 HTML/스크립트로 실행하지 않습니다. 이는 입력 편집용 웹 앱이 아닌 실행 결과 뷰어입니다.

## 입력·출력 예제

합성 입력: [sample-input.json](sample-input.json). 필드와 형식은 이 파일이 최소 실행 예제입니다. 반환 규칙은 main.py의 `run(data)`에 정의됩니다. 손상된 JSON·필수 필드 누락·잘못된 수치 입력은 CLI가 종료 코드 2로 보고합니다.

```json
{
  "query": "모터 과열 온도",
  "asset_id": "motor-1",
  "as_of": "2026-10-09",
  "top_k": 2,
  "documents": [
    {
      "id": "manual",
      "revision": 1,
      "asset_id": "motor-1",
      "effective_from": "2026-01-01",
      "source": "synthetic/manual-r1",
      "sections": [
        {
          "id": "heat",
          "text": "모터 과열 온도 90 도 기준은 이전 예제입니다."
        }
      ]
    },
    {
      "id": "manual",
      "revision": 2,
      "asset_id": "motor-1",
      "effective_from": "2026-09-01",
      "source": "synthetic/manual-r2",
      "sections": [
        {
          "id": "heat",
          "text": "모터 과열 시 온도 이력을 확인합니다. 전원 차단은 별도 현장 절차를 따릅니다."
        },
        {
          "id": "bearing",
          "text": "베어링 진동 점검 주기를 기록합니다."
        }
      ]
    },
    {
      "id": "other",
      "revision": 1,
      "asset_id": "motor-2",
      "effective_from": "2026-01-01",
      "source": "synthetic/other",
      "sections": [
        {
          "id": "heat",
          "text": "모터 과열 온도 모터 과열 온도"
        }
      ]
    },
    {
      "id": "manual",
      "revision": 3,
      "asset_id": "motor-1",
      "effective_from": "2026-12-01",
      "source": "synthetic/future",
      "sections": [
        {
          "id": "heat",
          "text": "미래 개정 모터 과열 기준"
        }
      ]
    }
  ]
}
```

출력 미리보기(생략 표시 부분은 설명이며 JSON 입력으로 사용하지 마세요):

```text
{
  "status": "evidence_found",
  "hits": [
    {
      "citation": "manual@2#heat",
      "asset_id": "motor-1",
      "source": "synthetic/manual-r2",
      "text": "모터 과열 시 온도 이력을 확인합니다. 전원 차단은 별도 현장 절차를 따릅니다.",
      "matched_terms": [
        "과열",
        "모터",
        "온도"
      ],
      "score": 1.779659
    }
  ],
  "generated_answer": null
}
```

전체 실행 결과: [example-output.json](example-output.json), [example-report.html](example-report.html).

## 설계 판단·통합

검색 전에 장비 ID·유효 날짜·최신 개정을 필터링합니다. 다른 장비의 유사한 문장을 점수가 높다는 이유만으로 반환하지 않습니다. 검색 후보 집합 내 문서빈도로 BM25를 계산하고 인용은 문서@개정#절로 고정합니다. no_evidence는 정상적인 결과입니다.

장비 데이터 수집 계층에서 합성 예제를 실제 데이터 스키마로 변환한 뒤 `run(data)`를 호출할 수 있습니다. Nest.js/Python 작업 큐 또는 테스트 자동화에서 JSON 입출력을 사용하고 XR/WebGL 화면에는 검증된 결과만 표시하는 방식으로 연결할 수 있습니다. 프로그램에는 실제 제어·유료 서비스·사용자 계정 접근 코드가 없습니다.

## 한계

RAG의 검색 단계만 구현합니다. 임베딩·LLM·답변 생성·환각 검증은 없습니다. 한국어 형태소 분석 없이 단어 경계를 사용하므로 표현 차이에 약합니다. 문서는 합성 예제이며 작업 지시나 안전 매뉴얼이 아닙니다.

가상의 경력, 논문 성능 수치, 모델 재현 또는 실물 제조 검증을 주장하지 않습니다. 데이터가 합성 예제인 만큼 현장 적용 전 데이터 품질·운영 조건을 다시 검증해야 합니다.

## 검증·근거

의미 있는 정상·경계·오류 테스트 4개를 실제 실행했습니다. 기록은 [VALIDATION.txt](VALIDATION.txt)에 있습니다. 논문 날짜·상태·확인 범위와 개발자 해석은 [TRENDS.md](TRENDS.md)를 참고하세요.

실행 기준일: 2026-10-09 (Asia/Seoul). 기존 저장소를 수정하지 않고 독립 프로그램으로 구성했습니다.
