import json

# 필요값은 화면에서 캐릭터 목표 정보 받아오기, 변수에 저장, json에 옮기기
# User값은 화면에서 캐릭터 현재 정보 받아오기, 변수에 저장, json에 옮기기
# 값 불러올때는 json 불러오고 화면에 json값 옮기기
# 버튼으로 하려면 함수로 나눠야 하나?
# 실시간으로 반영하는건 어렵나?

보이니치=[0,0,0,0]

print(보이니치)
with open('CalGrowth/Database.json','r',encoding='UTF-8') as f:
    json_datas = json.load(f)
print(json.dumps(json_datas, ensure_ascii=False))

sum_note = 0
for json_data in json_datas :
    if json_data['MainOparts']=='보이니치':
        for i in range(0,4):
            보이니치[i] +=json_data['Skill_Bd']['Main'][i]
            # 보이니치 +=json_data['Skill_Note']['Main']
    if json_data['SubOparts']=='보이니치':
        for i in range(0,4):
            보이니치[i] +=json_data['Skill_Bd']['Sub'][i]
            # 보이니치 +=json_data['Skill_Note']['Sub']
    
# 밀레니엄 소속 T3 노트 개수
# 이런식으로 한땀한땀 변수에 저장해서 UserDatabase에 옮기기
# 이렇게 우선 하고 좀더 시간 줄일만한거 생각해보기

f.close()
print(보이니치)