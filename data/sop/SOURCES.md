# SOURCES

본 SOP 코퍼스(`sop-corpus/`), 인력 페르소나(`personas.yaml`), 인시던트 시나리오(`incident-scenarios.yaml`), 평가 골드셋(`../eval/rag-goldset.yaml`)은 아래 공개 레퍼런스를 **참고만 하여 새로 집필한 가상 문서**다. 실존 조직·설비·인물과 무관하며, 특정 문서를 그대로 옮긴 부분은 없다.

## 조사 출처

1. **NIST SP 800-61 인시던트 대응 생애주기** — Rapid7 Blog, "Introduction to Incident Response Life Cycle of NIST SP 800-61"
   https://www.rapid7.com/blog/post/2017/01/11/introduction-to-incident-response-life-cycle-of-nist-sp-800-61/
   참고 내용: 준비-탐지/분석-격리/근절/복구-사후분석의 4단계 구조를 SOP-ESC-005의 판정·에스컬레이션 절차 설계에 참고.

2. **인시던트 심각도(P1-P4) 등급 체계** — Rootly, "Incident Response Support Levels: P1, P2, P3 Explained"
   https://rootly.com/incident-response/support-levels
   참고 내용: 등급별 정의(전체 중단/부분 장애/경미한 이슈)를 SOP-ESC-005의 등급 매트릭스 설계에 참고.

3. **ITIL 인시던트 관리 — 영향/긴급도/우선순위** — PagerDuty, "Using the Incident Priority Matrix"
   https://www.pagerduty.com/resources/digital-operations/learn/incident-priority-matrix/
   참고 내용: 영향(impact)과 긴급도(urgency)를 분리해 우선순위를 산출하는 매트릭스 개념을 SOP-ESC-005 4.1-4.3에 참고.

4. **데이터센터 온습도 권장범위(ASHRAE)** — TechTarget, "Data center temperature and humidity guidelines"
   https://www.techtarget.com/searchdatacenter/tip/Data-center-temperature-and-humidity-guidelines
   참고 내용: 흡기온도 18-27°C, 상대습도 40-60% 권장범위를 SOP-THM-002 목적·검증 절차에 참고.

5. **콜드아일/핫아일 격리 및 CRAC·CRAH 구조** — AKCP, "A Look at Data Center Cooling Technology"
   https://www.akcp.com/2021/06/10/a-look-at-data-center-cooling-technology/
   참고 내용: CRAC(직접팽창식)와 CRAH(냉수식)의 차이, 콜드아일/핫아일 격리 원리를 SOP-THM-002 설비 점검 절차에 참고.

6. **Uptime Institute Tier 등급 및 전력 이중화(N+1, 2N)** — CoreSite, "Breaking Down Data Center Tier Level Classifications" / "What is Data Center Redundancy? N, N+1, 2N"
   https://www.coresite.com/blog/breaking-down-data-center-tiers-classifications
   https://www.coresite.com/blog/data-center-redundancy-n-1-vs-2n-1
   참고 내용: Tier III(N+1, 동시유지보수 가능) 개념과 UPS 이중화 모델을 SOP-PWR-001·SOP-THM-002의 예비 설비 절차에 참고.

7. **GPU 서버 열스로틀링 및 열관리** — Dell, "PowerEdge: How To Troubleshoot GPU Thermal Throttling and Detection Issues"
   https://www.dell.com/support/kbdoc/en-us/000452203/poweredge-troubleshooting-gpu-thermal-throttling-and-detection-issues
   참고 내용: GPU 열스로틀링 시작 온도대(85-95°C)와 원인 진단 순서를 SOP-GPU-003 4.1-4.2에 참고.

8. **MOP(운영절차서)/EOP(비상절차서) 작성 관행** — Uptime Institute Journal, "The Making of a Good Method of Procedure"
   https://journal.uptimeinstitute.com/the-making-of-a-good-method-of-procedure/
   참고 내용: MOP의 필수 구성요소(목적·범위·사전조건·단계별 절차·완료판정·롤백)와 "실전에서 쓸 수 있을 만큼 짧아야 한다"는 EOP 원칙을 전체 SOP 서식(§1-7 구조, 단일 행동 단위 절 분리)에 참고.

## 명시
- 위 8건은 모두 공개(무료 열람 가능) 웹 문서이며, 본 코퍼스는 이를 **참고 자료**로만 사용해 문장·수치·시나리오를 전부 새로 작성했다.
- "한빛 IDC", 등장인물(임도윤·박서연·김하은·이준혁·정민석), 시나리오 3종은 전부 가상이며 실제 사건·인물과 무관하다.
- 인용은 위 각 항목당 15단어 미만의 개념 요약으로 한정했으며, 원문을 그대로 발췌한 문장은 없다.
