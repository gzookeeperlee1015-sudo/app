1. 프로젝트 받아오기
컴퓨터에서 작업할 폴더를 열고 터미널(또는 CMD)을 켠 뒤, 아래 명령어를 순서대로 입력

저장소 다운로드:
git clone https://github.com/gzookeeperlee1015-sudo/-.git
(내 컴퓨터에 프로젝트 폴더가 생성)

해당 폴더로 이동:
cd -

작업 브랜치로 전환:
git checkout 2branch
( 함께 작업할 공간인 2branch로 이동하는 필수 단계)

2. 작업할 때 지켜야 할 것 (중요)

본인 폴더에서만 작업: backend 은 backend 폴더에서, frontend 은 frontend 폴더에서만 코딩.

수시로 깃Github에 올리기: 작업한 내용은 틈틈이 아래 명령어를 입력해 저장.

git add . (수정한 파일 선택)

git commit -m "작업 내용 짧게 적기" (저장 기록 남기기)

git push origin 2branch (내 컴퓨터의 코드를 깃허브 서버로 업로드)

3. 
작업을 시작하기 전에는 항상 git pull origin 2branch를 먼저 입력해서, 다른 팀원이 먼저 올려둔 코드가 있는지 꼭 확인 그래야 코드 꼬임을 방지할 수 있음
