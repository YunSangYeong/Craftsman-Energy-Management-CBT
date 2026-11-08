# Craftsman-Energy-Management-CBT
에너지관리기능사

## 구현 및 실행

React + TypeScript + Vite, 서버/로그인/별도 키 없이 브라우저 저장소를 사용하는 비공식 학습 앱.
최신 표준 v1.4.0 문서(`76b990b8720adfa85c22a0a8f699b17094aa357b`) 전체 폴더를 복사하고 AGENTS.md에 연결했다.
기존 AGENTS.md는 없었으며 README의 원문 제목·설명을 보존했다.
앱은 표준 고정 커밋 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`의 UI/모델/스타일을 재사용했다. 원본 코드 MIT 고지 보존.
다른 프로젝트의 원격 코드/배포는 변경하지 않았다.

Node 24, 저장소 루트에서:

```sh
npm ci --cache /tmp/energy-npm-cache
npm run dev
npm test
npm run build
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npx playwright test
```

시스템 Chromium이 없으면 `npx playwright install --with-deps chromium` 후 환경변수 없이 실행한다.
`npm run test:e2e`는 빌드 후 브라우저 테스트를 실행한다. CI도 이를 사용한다.
공유 환경에서 별도 worktree 없이 현재 체크아웃을 사용한다.

대시보드·실전·랜덤·오답·북마크·통계·JSON/CSV 로컬 등록/승인·기록 백업·확인 후 초기화 제공.
두 모드 답안 선택 후 Space 이동, 마지막 실전 문제 자동 제출 방지, 절대 종료시각/새로고침 복원, 저장 실패·손상 경고 유지.
학습 기준 선택과 상단 상시 안내 배너 없음. 출처·한계는 문제은행 관리와 문항 해설에 표시한다.
자격증 고유 저장 키 사용. 응답 최근 5,000개, 시험 최근 30회. 백업은 내보내기이며 UI 복원 기능은 없다.
localStorage 제한/다른 origin에서는 기록이 보장되지 않는다. 기본 URL의 iframe도 포커스가 내부에 있어야 Space가 작동한다.

## 문제은행과 공식 규칙

실제 **1,000문항** = 자체 제작 계산 조건 변형 960개 + 개념형 40개. 원문 기출 0, 복원 0.
계산은 기존 6유형 × 10조건 + 추가 30유형 × 30조건이며 기존 60개 ID/내용을 전부 보존했다.
중복 제거 후 내부 검토 완료 1,000개, 수량 목표 대비 부족 0개. 독립 개념 1,000개가 아니며 숫자 변형을 포함한다.
외부 전문가 검수·공식 출제기준 전체 대조는 미완료이며 시험 범위·난이도 분포 재현을 보증하지 않는다.
공식 Q-Net 접근이 CONNECT 403으로 차단되어 규칙은 확인 대기인 학습용 설정이다.
[근거·유형·검수 범위·잠정 시험 규칙](docs/question-review.md)을 반드시 확인한다.

## 이전 구현의 배포 기록

대상은 이 저장소의 GitHub Pages만이다. main push → 단위/빌드/PC·모바일 검증 → Pages 자동 배포, PR은 검증만.
배포 사전 확인 `gh api repos/YunSangYeong/Craftsman-Energy-Management-CBT`가 `Get "https://api.github.com/repos/YunSangYeong/Craftsman-Energy-Management-CBT": Forbidden`으로 종료 코드 1을 반환했다.
요청대로 이 첫 차단 후 중단했다. main push/workflow 실행/대체 경로/추가 배포 시도 없음.
Pages 설정·CI·현재 공개 여부는 확인하지 못했으며 이번 배포 성공을 주장하지 않는다.
예상 주소(게시 확인 안 됨): https://YunSangYeong.github.io/Craftsman-Energy-Management-CBT/
사용자 다음 최소 동작: 클라우드 환경 네트워크 설정에서 `api.github.com`의 허용 여부를 확인한다. Forbidden의 세부 원인·저장소 권한·Pages 최초 설정 필요 여부는 아직 확정할 수 없다.
재시도는 사용자 직접 마무리 또는 별도 명시 요청 전까지 하지 않는다.

## 로컬 검증 결과

단위 테스트 1,019개 통과, Chromium PC·Pixel 7 에뮬레이션 브라우저 검사 24개 통과·2개 의도적 건너뜀(데스크톱에서의 터치 전용 검사), 프로덕션 빌드 성공.
390×480/740×360 메뉴 휠 및 터치 위아래 입력·하단 도구·상단 대시보드 접근을 실제 입력으로 확인했다. 실기기 검증은 하지 않았다.
[실행 범위·오류 및 배포 중단 기록](docs/validation.md).

## 이번 확충의 범위

사용자 요청에 따라 게시된 환경 기반의 현재 체크아웃에서 940개를 추가했다. 설치 스크립트·workflow·시험 규칙·다른 프로젝트를 변경하지 않았다.
1,000문항 구현·검증 단계에서는 GitHub push·CI 실행·Pages 배포·클라우드 환경 게시를 하지 않았다. 후속 푸시 요청에 따른 반영 대상은 `work` 브랜치이며 main 병합이나 배포는 포함하지 않는다. 위 Forbidden은 이전 구현 단계 기록이며 이번에 API 재요청을 한 것이 아니다.
