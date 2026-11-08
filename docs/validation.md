# 실제 검증 및 배포 기록

2026-11-08 (KST), `/workspace/Craftsman-Energy-Management-CBT`에서 실행.

| 검사 | 결과 |
| --- | --- |
| npm ci --cache /tmp/energy-npm-cache | 종료 0, lockfile 설치 성공. 최초 기본 캐시 경로 쓰기 실패 후 /tmp 캐시로 해결. 서명/무결성/TLS 검증 유지 |
| npm test | 종료 0, 77/77 통과(은행/계산 61, 모델 16) |
| npm run build | 종료 0, TypeScript 및 Vite production build 성공 |
| PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npx playwright test --reporter=list | 종료 0, 24 통과 / 2 건너뜀 / 실패 0, 27.7초 |
| Python 은행 재생성 | SHA256 동일: 61b8482d03a1389e7e473cc5042f89dc93793762ab14e3c4d38f83e6ea8e5529 |
| git diff --check | 종료 0 |

브라우저는 Linux Chromium PC 및 Pixel 7 모바일 에뮬레이션. 실기기/Safari 미실행.
브라우저 18개는 기준 시나리오를 대상 데이터로 수정한 검사: 학습 기준 메뉴 없음, 모의시험 60개 답변·채점·오답복습, 타이머/만료/복원, 랜덤·북마크·통계, 가져오기·중복·검수·초기화, 저장 손상, 두 모드 Space와 키보드 경계.
추가 6개 통과는 390×480 및 740×360 메뉴 실제 휠(PC/모바일 4개) 및 CDP touchStart/move/end 스와이프(모바일 2개)이다.
하단 초기화 대화상자/백업 다운로드와 상단 대시보드 선택을 확인했으며 scrollTop을 코드로 변경하지 않았다.
2개 건너뜀은 데스크톱 프로젝트에서 중복 실행하지 않는 터치 전용 검사이며 모바일에서는 둘 다 실행했다.
초기 로컬 회귀 실패는 원본 은행 숫자·문구/양식 예제 중복/검사 버튼명 차이를 진단·수정 후 최종 전체 실행으로 검증했다. CI 실패 또는 배포 재시도가 아니다.
상단 안내 컴포넌트를 제거하고 저장 오류와 재개·제출 경고는 보존했다. 공식 규칙/외부 전문가 검수/1,000문항 완료는 이 검사로 보증하지 않는다.

## 배포 사전 확인 — 첫 차단

`gh api repos/YunSangYeong/Craftsman-Energy-Management-CBT --jq '{default_branch,permissions,has_pages}'`

종료 1: `Get "https://api.github.com/repos/YunSangYeong/Craftsman-Energy-Management-CBT": Forbidden`

이 첫 차단에서 배포를 중단했다. 다른 인증/접속 경로, API 재시도, main push, 수동 workflow 실행, workflow 재실행 없음.
원격 반영 없음. 새 CI/Pages 실행 ID 없음. 현재 Pages Source/기존 공개 상태와 공개 화면은 미확인.
예상 기본 주소는 https://YunSangYeong.github.io/Craftsman-Energy-Management-CBT/ 이며 이번 작업에서 게시한 주소가 아니다.
사용자 최소 동작: 환경의 네트워크 설정에서 api.github.com 허용 여부 확인. 세부 거부 원인은 미확정.
사용자가 마무리하며 명시 재요청 전에는 에이전트가 다시 실행하지 않는다.
