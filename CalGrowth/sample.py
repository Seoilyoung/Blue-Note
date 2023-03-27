import json
import re

# JSON 파일 읽어오기
with open('CalGrowth/DatabaseUser.json', 'r',encoding='UTF-8') as f:
    data = json.load(f)

# Student 항목에 "시로코" 삽입
print(data["Default"]["Note"])
data["Default"]["Note"]['백귀야행'][0] = 2 
data["Default"]["Student"]["시로코"] = [1,2,2,2,3,7,7,7]
data["Default"]["Student"]["호시노"] = [1,2,2,2,3,7,7,7]
print(data["Default"]["Note"]['백귀야행'][0])

json_data = json.dumps(data, ensure_ascii=False, indent=4)
json_data = re.sub(r'\[\n\s+','[', json_data)
json_data = re.sub(r',\n\s+',',', json_data)
json_data = re.sub(r'\n\s+\]',']', json_data)
# 수정된 데이터 저장
with open('CalGrowth/test.json', 'w',encoding='UTF-8') as f:
    f.write(json_data)
with open('CalGrowth/test.json', 'r',encoding='UTF-8') as f:
    data = json.load(f)
print(data["Default"]["Note"]['백귀야행'][0])