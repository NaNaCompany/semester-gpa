# 학기 성적 시뮬레이터

수동 환산표·과목 학점·이전 누적값으로 학기와 누적 평점, 재수강 교체, 미래 목표에 필요한 평균을 계산하는 독립 정적 앱입니다. `dist/index.html`이 진입점입니다. 설치·빌드·서버 API 없이 동작합니다.

## 기능

- 한국어 `/`, 영어 `/en/`, 스페인어 `/es/`, 중국어 간체 `/zh/`, 일본어 `/ja/`, 독일어 `/de/`. 모든 경로에 수동 언어 메뉴가 있으며 UI·오류·상태·도움말·결과 헤더를 현지화합니다. 사용자 과목명·환산등급은 번역하지 않습니다.
- 직접 편집하는 등급=환산점수 표. 예제의 4.5점 환산표는 임의 정책이며 대학 공식 학칙을 대표하지 않습니다.
- 최대 100과목. 학점 가중평균, P/F와 계산 제외 과목, 이전 누적 학점·평점.
- 재수강 시 이전 누적값에 포함된 기존 학점과 환산점수를 수동 지정하여 차감한 뒤 새 성적을 반영합니다. 학교별 대체 여부·상한을 자동 판단하지 않습니다.
- 미래 추가 학점과 목표 누적 평점을 입력하면 필요한 미래 평균과 만점 범위 내 가능 여부를 표시합니다.
- UTF-8 BOM CSV 결과 다운로드. 사용자 과목명의 CSV 인용부호·줄바꿈을 처리하며 수식 시작 문자에는 작은따옴표를 붙입니다.

## 계산·제약

학기 평균은 `Σ(학점×환산점수)/Σ학점`입니다. P/F 및 제외 과목은 두 합계에서 제외합니다. 누적 총점은 `이전학점×이전평점−교체할 이전총점+이번학기총점`입니다. 필요 미래 평균은 `[목표×(예상누적학점+미래학점)−예상누적총점]/미래학점`입니다.

반올림 전 값을 계산하고 화면은 소수 3자리로 표시합니다. JavaScript 부동소수 연산을 사용합니다. 과목 학점 0.1–100, 이전 누적 학점 0–10,000, 미래 학점 0.1–1,000, 만점 1–10, 환산표 최대 30등급입니다. 빈 숫자, 비유한값, 0분모와 모순된 재수강 차감을 거부합니다. 같은 기존 과목의 중복 교체 여부는 사용자가 확인해야 합니다.

과목 평가요소별 점수 예측, 학교 학칙·재수강 제한·졸업요건·학사경고 판정은 제공하지 않습니다. 공식 성적표와 구분된 수동 정책 시나리오입니다. 데이터는 기기에만 머물며 저장·업로드·원격 API가 없습니다. 새로고침·언어 변경 시 입력이 초기화됩니다.

## 검증

2026-10-26 RTK proxy와 번들 Node로 실행했습니다. 아래 `$rtk`와 `$node`는 실행 환경의 해당 실행 파일 절대 경로를 가리킵니다. 개인 경로를 산출물에 포함하지 않도록 기호로 표시합니다.

```powershell
& $rtk proxy $node --check dist/app.js
& $rtk proxy $node --test test.mjs
```

문법 검사 exit 0. Node fixture 7개 통과, 실패 0. 독립 수치 예시로 가중평균 3.75, 누적 3.25/필요 평균 4.5, 재수강 차감 후 3.3을 확인했습니다. P/F·제외, 재수강 모순, 비유한값·0분모·환산표 중복과 범위, CSV 인용·수식 보호, 6개 경로/언어사전 키를 검증했습니다.

브라우저 시각·실제 상호작용 QA는 수행하지 않았습니다. 소스·fixture 검증 완료 상태입니다. `build_locales.py`는 개발 시 경로 생성에 사용하며 배포 시 필요 없습니다.

## 출처

가중평균 산식: NIST Dataplot Reference Manual, Weighted Mean — https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weigmean.pdf

표시된 GPA 정책·목표 계산은 사용자 입력을 이용한 자체 산술이며 특정 대학 정책을 인용하지 않습니다. UI·코드·예제는 자체 제작했습니다. 외부 라이브러리·폰트·이미지·광고·추적 코드가 없습니다.

## Public GitHub Pages release

Launch: https://nanalab.kr/semester-gpa/

Korean is at the root. English, Spanish, Chinese, Japanese and German use `/en/`, `/es/`, `/zh/`, `/ja/`, `/de/`.
GitHub Pages serves `main` → `/docs` using the branch build. No project CNAME is used.

Build: `node scripts/build-public.mjs`. The `dist/` snapshot and its original generators/tests are preserved as the application source. The public build adds metadata, six-locale sitemaps, original JPEG cards, More Apps styling and the existing NaNa publisher integrations. It does not upload selected user files.

Publisher integrations: AdSense, Google Tag Manager, Google Analytics and Cloudflare Web Analytics, with the same publisher settings as the NaNa Lab homepage. These scripts can make network requests independently of local file processing.

Original JPEG cards are rendered from original text and geometry using an installed system font; no font files are redistributed. Existing source references and third-party notices remain applicable.
