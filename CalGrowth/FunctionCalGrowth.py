import json
import re

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

def openDBuser():
    with open('CalGrowth/DatabaseUser.json','r',encoding='UTF-8') as j_databaseUser:
        json_Userdatas = json.load(j_databaseUser)
    return json_Userdatas

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
    
def readCharMemo(datas, char_name):
    try:
        return datas["Default"]["Student"][char_name]['memo']
    except:
        return

# 학생 정보 생성
def insertStudent(data, index, char_name, academy, mainoparts, suboparts):
    if academy == 'SRT':
        academy = '발키리'
    data["Default"]["Student"][char_name] = {'index' : index, 'academy' : academy, 'mainoparts' : mainoparts, 'suboparts' : suboparts,
                                             'level_current' : 0, 'level_goal' : 0,'skill_current' : [0,0,0,0], 'skill_goal' : [0,0,0,0], 'liberation_current':0, 'liberation_goal':0,
                                             'oparts_main' : [0,0,0,0], 'oparts_sub' : [0,0,0,0], 'bd' : [0,0,0,0], 'note' : [0,0,0,0], 'secretnote' : 0}
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
# 학생 정보 삭제
def deleteStudent(data, index):
    for name, info in data["Default"]["Student"].items():
        if index == info["index"]:
            del data["Default"]["Student"][name]
            break
    # 목록에서 사라지니까 아래 목록의 index를 다 1 줄인다.
    if index >=0:
        for name, info in data["Default"]["Student"].items():
            if index < info["index"]:
                info["index"] -= 1
                if "Default" in name:
                    char_name = "Default " + str(info["index"])
                    data["Default"]["Student"][char_name] = data["Default"]["Student"].pop(name)

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
# 학생 정보 수정(학생명 변경시)
def updateStudent(data, index, char_name, academy, mainoparts, suboparts):
    if academy == 'SRT':
        academy = '발키리'

    for name, info in data["Default"]["Student"].items():
        if index == info["index"]:
            data["Default"]["Student"][char_name] = data["Default"]["Student"].pop(name)
            data["Default"]["Student"][char_name]["academy"] = academy
            data["Default"]["Student"][char_name]["mainoparts"] = mainoparts
            data["Default"]["Student"][char_name]["suboparts"] = suboparts
            break

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])

# 학생 메모 업데이트
def updateMemo(data, index, char_name, memo):
    for name, info in data["Default"]["Student"].items():
        if index == info["index"]:
            data["Default"]["Student"][char_name]["memo"] = memo
            break
        
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)

# 학생 정보 init
def initStudent(data, index, char_name):
    for name, info in data["Default"]["Student"].items():
        if index == info["index"]:
            data["Default"]["Student"][char_name] = data["Default"]["Student"].pop(name)
            data["Default"]["Student"][char_name]["academy"] = ""
            data["Default"]["Student"][char_name]["mainoparts"] = ""
            data["Default"]["Student"][char_name]["suboparts"] = ""
            data["Default"]["Student"][char_name]["skill_current"] = [0, 0, 0, 0]
            data["Default"]["Student"][char_name]["skill_goal"] = [5, 10, 10, 10]
            data["Default"]["Student"][char_name]["liberation_current"] = [0,0,0]
            data["Default"]["Student"][char_name]["liberation_goal"] = [25,25,25]
            data["Default"]["Student"][char_name]["oparts_main"] = [0, 0, 0, 0]
            data["Default"]["Student"][char_name]["oparts_sub"] = [0, 0, 0, 0]
            data["Default"]["Student"][char_name]["bd"] = [0, 0, 0, 0]
            data["Default"]["Student"][char_name]["note"] = [0, 0, 0, 0]
            data["Default"]["Student"][char_name]["memo"] = ""
            break

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
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

    sorted_student = dict(sorted(data["Default"]["Student"].items(), key=lambda x: x[1]["index"]))
    data["Default"]["Student"] = sorted_student

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
# 학생 스킬 테이블 수정
def updateTable(data, index, row, column, value):
    if row==0 or row==1:
        menu = "skill"
    elif row==2 or row==3:
        menu = "liberation"

    if row%2 == 0:
        menu = menu + "_goal"
    elif row%2 == 1:
        menu = menu + "_current"

    for name, info in data["Default"]["Student"].items():
        if index == info["index"]:
            # 데이터 수정 
            if row==0 or row==1:
                data["Default"]["Student"][name][menu][column] = value
            elif row==2 or row==3:
                data["Default"]["Student"][name][menu][column-1] = value
                
            # 공백 오류 통제
            if info["academy"] != "":
                result = 0
            else:
                result = 1
            break
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    json_data = re.sub(r'\[\n\s+','[', json_data)
    json_data = re.sub(r',\n\s+',',', json_data)
    json_data = re.sub(r'\n\s+\]',']', json_data)
    with open('CalGrowth/DatabaseUser.json', 'w',encoding='UTF-8') as f:
        f.write(json_data)
    # print(data["Default"]["Student"])
    return data, result
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
    
# 학생 테이블 계산
def calSkillTable(data, data_skill, database, char_name):
    # 해당 함수에서는 스킬 변수 수정이 없으므로 변수로 저장해서 이용 가능
    if char_name in database and char_name in data["Default"]["Student"]:
        list_goal = data["Default"]["Student"][char_name]['skill_goal']
        list_current = data["Default"]["Student"][char_name]['skill_current']
        list_liberation_goal = data["Default"]["Student"][char_name]['liberation_goal']
        list_liberation_current = data["Default"]["Student"][char_name]['liberation_current']
        
        #[T1,T2,T3,T4]
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
        # Liberation 계산
        # TableSkill의 Liberation = [오파츠T1,오파츠T2,재료노트T1,재료노트T2,재료노트T3]
        for i in range(3):
            for liberation_level in range(list_liberation_current[i]+1, list_liberation_goal[i]+1):
                list_oparts_main[0] += data_skill['Liberation'][str(liberation_level)][0]
                list_oparts_main[1] += data_skill['Liberation'][str(liberation_level)][1]

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