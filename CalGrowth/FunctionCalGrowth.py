import json
import re
# import DataUser, DataCharacter

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
# data_preset1 = DataUser.dataset('preset1')
# list_oparts = ["네브라", "파에스토스", "볼프세크", "님루드", "만드라고라", "로혼치", "에테르", "안티키테라", "보이니치", "하니와",
#     "토템폴", "전지", "콜간테", "위니페소키"]
# list_academy = ["백귀야행", "붉은겨울", "트리니티", "게헨나", "아비도스", "밀레니엄", "아리우스", "산해경", "발키리"]

# 화면에서 받아오는걸로 변경 예정 (list로 받으니까 여러명 대응 필요)
# 그냥 json으로 할까 gui에서 받아오는 방식을 찾아보고 해야할듯
# 계산하는거 먼저 만들고 이후에 여러명 적용.
#-------------------------------------------------------------------------------
# char_name = '시로코'
# char_test = DataCharacter.dataset(char_name)
# char_test.Level_current = 1
# char_test.Skill_current = [1,1,1,1]
# char_test.Level_goal = 80
# char_test.Skill_goal = [5,10,10,10]
#-------------------------------------------------------------------------------

def openDB():
    # DB 열기
    with open('CalGrowth/DatabaseUser.json','r',encoding='UTF-8') as j_databaseUser:
        json_Userdatas = json.load(j_databaseUser)
    with open('CalGrowth/Database.json','r',encoding='UTF-8') as j_database:
        json_datas = json.load(j_database)
    with open('CalGrowth/TableExp.json','r',encoding='UTF-8') as j_tableexp:
        json_table_exp = json.load(j_tableexp)
    with open('CalGrowth/TableCredit.json','r',encoding='UTF-8') as j_tablecredit:
        json_table_credit = json.load(j_tablecredit)
    with open('CalGrowth/TableSkill.json','r',encoding='UTF-8') as j_tableskill:
        json_table_skill = json.load(j_tableskill)
    return json_Userdatas, json_datas, json_table_exp, json_table_credit, json_table_skill

def closeDB(database):
    # DB 닫기
    database.close()

def readCharList(datas):
    return datas.keys()

def readCharAcademy(datas, char_name):
    try:
        return datas[char_name]['Academy']
    except:
        return

def readCharMainOparts(datas, char_name):
    try:
        return datas[char_name]['MainOparts']
    except:
        return
    
def readCharSubOparts(datas, char_name):
    try:
        return datas[char_name]['SubOparts']
    except:
        return

# 학생 정보 생성
def insertStudent(data, char_name, index, academy, mainoparts, suboparts):
    if academy == 'SRT':
        academy = '발키리'
    data["Default"]["Student"][char_name] = {'index' : index, 'academy' : academy, 'mainoparts' : mainoparts, 'suboparts' : suboparts,
                                             'level_current' : 0, 'level_goal' : 0,'skill_current' : [0,0,0,0], 'skill_goal' : [0,0,0,0], 
                                             'oparts_main' : [0,0,0,0], 'oparts_sub' : [0,0,0,0], 'bd' : [0,0,0,0], 'note' : [0,0,0,0], 'secretnote' : 0}
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 학생 정보 삭제
def deleteStudent(data, char_name, index):
    if char_name in data["Default"]["Student"]:
        del data["Default"]["Student"][char_name]
    # index가 -1인 경우:중복학생 / 아니면 목록에서 사라지니까 아래 목록의 index를 다 1 줄인다.
    if index >=0:
        for name, info in data["Default"]["Student"].items():
            if index < info["index"]:
                info["index"] -= 1
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 학생 정보 수정
def updateStudent(data, char_name_before, char_name_after, academy, mainoparts, suboparts):
    if academy == 'SRT':
        academy = '발키리'
    if char_name_before in data["Default"]["Student"]:
        data["Default"]["Student"][char_name_after] = data["Default"]["Student"].pop(char_name_before)
        data["Default"]["Student"][char_name_after]["academy"] = academy
        data["Default"]["Student"][char_name_after]["mainoparts"] = mainoparts
        data["Default"]["Student"][char_name_after]["suboparts"] = suboparts
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 리스트 순서 수정
def updateIndex(data, index1, index2):
    for name, info in data["Default"]["Student"].items():
        index = info["index"]
        if index1 < index2 and (index1 < index and index <= index2):
            info["index"] -= 1
        elif index2 < index1 and (index2 <= index and index < index1):
            info["index"] += 1
        elif index == index1:
            info["index"] = index2
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 학생 스킬 테이블 수정
def updateTable(data, char_name, row, column, value):
    if row == 0:
        menu = "skill_goal"
    elif row == 1:
        menu = "skill_current"
    data["Default"]["Student"][char_name][menu][column] = value
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 재화 테이블 수정
def updateTable2(data, item_type, item_name, column, value):
    data["Default"][item_type][item_name][3-column] = value
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data
# 학생 테이블 계산
def calSkillTable(data, data_skill, database, char_name):
    # 해당 함수에서는 스킬 변수 수정이 없으므로 변수로 저장해서 이용 가능
    list_goal = data["Default"]["Student"][char_name]['skill_goal']
    list_current = data["Default"]["Student"][char_name]['skill_current']
    list_oparts_main = [0,0,0,0]
    list_oparts_sub = [0,0,0,0]
    list_bd = [0,0,0,0]
    list_note = [0,0,0,0]
    num_secretnote = 0
    # BD 스킬 계산
    if list_goal[0] > list_current[0]:
        for i in range(list_current[0]+1, list_goal[0]+1):
            if i >= 2:
                for j in range(4):
                    list_bd[j] += data_skill['Skill_Bd'][str(i)][j]
                #BD 관련 오파츠 계산
                list_oparts_main[i-2] += database[char_name]["Skill_Bd"]["Main"][i-2]
                if i >= 3:
                    list_oparts_sub[i-3] += database[char_name]["Skill_Bd"]["Sub"][i-2]
    # Note 스킬 계산
    for n in range(1,4):
        if list_goal[n] > list_current[n]:
            for i in range(list_current[n]+1, list_goal[n]+1):
                if i == 10:
                    num_secretnote += 1
                if i >= 2 and i <= 9:
                    for j in range(4):
                        list_note[j] += data_skill['Skill_Note'][str(i)][j]
                    #노트 관련 오파츠 계산
                    if i == 4:
                        num2 = 0
                    elif i == 5 or i == 6:
                        num2 = 1
                    elif i == 7:
                        num2 = 2
                    elif i == 8 or i == 9:
                        num2 = 3
                    else:
                        continue
                    list_oparts_main[num2] += database[char_name]["Skill_Note"]["Main"][i-2]
                    list_oparts_sub[num2-1] += database[char_name]["Skill_Note"]["Sub"][i-2]
    # data에 입력                
    data["Default"]["Student"][char_name]['bd'] = list_bd
    data["Default"]["Student"][char_name]['note'] = list_note
    data["Default"]["Student"][char_name]['secretnote'] = num_secretnote
    data["Default"]["Student"][char_name]['oparts_main'] = list_oparts_main
    data["Default"]["Student"][char_name]['oparts_sub'] = list_oparts_sub
    # json 형식 지정 / 저장
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    return data





# # 학생 레벨업 재화 계산
# for exp in json_table_exp['level']:
#     if  (char_test.Level_current < int(exp)) and (int(exp) <= char_test.Level_goal):
#         data_preset1.Report += json_table_exp['level'][exp]
# data_preset1.Credit[1] += data_preset1.Report*7
# # 학생 BD 재화 계산
# for credit in json_table_credit['Skill_Bd']:
#     if (char_test.Skill_current[0] < int(credit)) and (int(credit) <= char_test.Skill_goal[0]):
#         data_preset1.Credit[0] += json_table_credit['Skill_Bd'][credit]
#         data_preset1.increase('Bd',json_datas[char_name]['Academy'],json_table_skill['Skill_Bd'][credit])
#         data_preset1.increaseOparts('OpartsBd', 'Main',json_datas[char_name]['MainOparts'],json_datas[char_name]['Skill_Bd']['Main'],credit)
#         data_preset1.increaseOparts('OpartsBd', 'Sub',json_datas[char_name]['SubOparts'],json_datas[char_name]['Skill_Bd']['Sub'],credit)
# # 학생 노트 재화 계산
# for credit in json_table_credit['Skill_Note']:
#     for i in range(1,4):
#         if (char_test.Skill_current[i] < int(credit)) and (int(credit) <= char_test.Skill_goal[i]):
#             if credit == '10':
#                 data_preset1.ScretNote += 1
#                 data_preset1.Credit[0] += json_table_credit['Skill_Note'][credit]
#             else:
#                 data_preset1.Credit[0] += json_table_credit['Skill_Note'][credit]
#                 data_preset1.increase('Note',json_datas[char_name]['Academy'],json_table_skill['Skill_Note'][credit])
#                 data_preset1.increaseOparts('OpartsNote', 'Main',json_datas[char_name]['MainOparts'],json_datas[char_name]['Skill_Note']['Main'],credit)
#                 data_preset1.increaseOparts('OpartsNote', 'Sub',json_datas[char_name]['SubOparts'],json_datas[char_name]['Skill_Note']['Sub'],credit)
            



# print(data_preset1.all()) #임시확인용
# 이런식으로 한땀한땀 변수에 저장해서 DataUserbase에 옮기기
# 이렇게 우선 하고 좀더 시간 줄일만한거 생각해보기
