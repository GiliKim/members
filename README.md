# 옥탑밭 회원관리 (정적 버전, GitHub Pages용)

- 완전 정적 HTML/JS로 동작합니다. **서버 필요 없음** (Render.com 불필요)
- 데이터는 브라우저 **localStorage**에 저장됩니다.
  - 같은 브라우저/PC에서만 보입니다. 다른 브라우저/PC에서는 안 보일 수 있어요.
  - 메뉴의 **CSV 내보내기/가져오기**로 백업/이동하세요.

## 배포 (GitHub Pages)
1) 새 리포 만들기 (예: `otobap-members-static`)
2) 이 폴더의 `index.html`을 리포 **루트**에 업로드
3) GitHub → Settings → Pages → Source: Deploy from a branch, Branch: main (root) 저장
4) 잠시 후 사이트 주소: `https://<아이디>.github.io/otobap-members-static/`
5) 홈 런처의 `__MEMBERS_URL__`을 위 주소로 교체

## 기능
- 회원 등록(이름/연락처/멤버십/시작일/만료일)
- 만료일 자동 계산(월간/분기/연간) — 입력 없을 때
- 검색(이름/연락처), 상태(활성/만료) 필터, 멤버십 필터
- 삭제
- CSV 내보내기/가져오기

## 한계
- 서버/DB가 없으므로 여러 사람이 동시에 쓰거나, 기기 간 동기화는 되지 않습니다.
- 그런 경우엔 Firebase/Supabase 같은 BaaS 또는 Render/Heroku 등 서버가 필요합니다.
