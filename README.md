# Blue-Scheduler
블루아카이브 일정 관리 프로그램

개발 언어 : python 3.11.2, PyQt6

1. Home
    1) 공지가 올라오는 사이트 크롤링
    2) 넥슨 커뮤니티 - 주요사항 / 공지사항
    3) [제거] 트위터 - 공식 홈페이지 같이 작게 출력. 트위터 디벨로퍼 승인 받으면 그때 시작
                    - 트위터 API 유료화 전환에 따른 제외
    4) [예정] 일정에 추가 기능
    5) 슬라이드쇼 - 업데이트 상세 페이지에서 이미지 추출 후 출력
        - 이미지 재사용 : 글 내용이 수정되면 글 제목이 변경되는 점을 이용해서 제목이 변경될 때 이미지를 새로 크롤링 하도록 변경. 이미지 다운로드 빈도 감소 

[예정] 2. 일정
    1) 달력 형식
        - 모듈에는 마음에 드는게 없음. 그래서 달력 이미지에 테이블위젯을 위에 덮어서 일정 구현 예정 
    2) 하이퍼링크 형식으로 글 클릭시 사이트, 이미지로 이동 기능
    3) 알림 기능
  
3. 재화 계산 - 다수 계산 과정 진행중
    1) 보유 재화, 성장 필요 재화 계산
        - [예정] 비의서, 크레딧, 보고서 추가 예정
    2) 리스트위젯으로 프리셋 구현
        - 컨테이너 만들어서 아이템 관리.
        - 스크롤 없이 완벽히 나오려면 아이템 높이가 매우 낮아져서 가독성이 낮아짐. 그래서 스크롤이 가능하도록 구현. 보기 좋게 하려고 스크롤은 보이지 않게 했음.
    3) [예정] 프리셋 3개 예정(2~3달 필요한 재화, 모두 필요한 재화, 여유분)
        - 프리셋 버튼 우하단 빈공간에 추가해서 관리 예정
    4) [보류] 스크린샷 읽어와서 현재보유 재화 계산(매번 수기로 입력하려면 귀찮다.) 화면 인식 방식은 비추천
        - 버튼으로 구현할 수 있지만 일단 보류
    6) [예외] 하츠네 미쿠 - 필요 재화가 다른 캐릭터와 비교했을 때 방식이 달라서 계산에서 제외. 추후 추가 예정

4. AP 가이드
    1) 이벤트 제목, 점검 일정 입력
    2) 템플릿에 일정 출력 / 이미지 저장
    3) [예정] 일정에 추가 기능
    4) [예정] 이미지 공유
  
[예정] 5. 인게임 연동
    1) api가 공개돼 있나?
    2) 카페 상황, 현재 ap, 총력전,대항전 티켓 보유수
    3) 재화 연동

[예정] 7. 캐시 비우기
    1) images폴더 제거


당장 목표
테이블 클릭했을 때 색 변경되는거 해제
휠 기능 삭제
캐릭터별 정보 입력

[참고 자료]
https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python