import json
import DataUser, DataCharacter

# 필요값은 화면에서 캐릭터 목표 정보 받아오기, 변수에 저장, json에 옮기기
# User값은 화면에서 캐릭터 현재 정보 받아오기, 변수에 저장, json에 옮기기
# 값 불러올때는 json 불러오고 화면에 json값 옮기기
# 버튼으로 하려면 함수로 나눠야 하나?
# 실시간으로 반영하는건 어렵나?


# 초안 - 전체 필요 개수 파악

# 변수 정의
# user = 유저 보유 재화
# preset1 = 총 필요 재화
# preset2 = 1~2달 필요 재화
data_preset1 = DataUser.dataset('preset1')
list_oparts = ["네브라", "파에스토스", "볼프세크", "님루드", "만드라고라", "로혼치", "에테르", "안티키테라", "보이니치", "하니와",
    "토템폴", "전지", "콜간테", "위니페소키"]
list_academy = ["백귀야행", "붉은겨울", "트리니티", "게헨나", "아비도스", "밀레니엄", "아리우스", "산해경", "발키리"]

# 화면에서 받아오는걸로 변경 예정 (list로 받으니까 여러명 대응 필요)
# 그냥 json으로 할까
char_test = DataCharacter.dataset('시로코')
char_test.Level_current = 1
char_test.Skill_current = [1,1,1,1]
char_test.Level_goal = 80
char_test.Skill_goal = [5,10,10,10]

# DB 열기
with open('CalGrowth/Database.json','r',encoding='UTF-8') as j_database:
    json_datas = json.load(j_database)
with open('CalGrowth/TableExp.json','r',encoding='UTF-8') as j_tableexp:
    json_table_exp = json.load(j_tableexp)
# print(json.dumps(json_datas, ensure_ascii=False))

# 학생별 레벨업 재화 계산
for exp in json_table_exp['level']:
    if int(exp) <= char_test.Level_goal:
        data_preset1.Credit[1]+=json_table_exp['level'][exp]
print(data_preset1.Credit[1])













# sum_note = 0
# for json_data in json_datas :
#     if json_data['MainOparts']=='보이니치':
#         for i in range(0,4):
#             data_preset1.Oparts['보이니치'][i] +=json_data['Skill_Bd']['Main'][i]
#             # 보이니치 +=json_data['Skill_Note']['Main']
#     if json_data['SubOparts']=='보이니치':
#         for i in range(0,4):
#             data_preset1.Oparts['보이니치'][i] +=json_data['Skill_Bd']['Sub'][i]
#             # 보이니치 +=json_data['Skill_Note']['Sub']
    
# 밀레니엄 소속 T3 노트 개수
# 이런식으로 한땀한땀 변수에 저장해서 DataUserbase에 옮기기
# 이렇게 우선 하고 좀더 시간 줄일만한거 생각해보기

# DB 닫기
j_database.close()
j_tableexp.close()
# print(data_preset1.all())