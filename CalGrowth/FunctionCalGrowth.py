import json

with open('CalGrowth/Database.json','r',encoding='UTF-8') as f:
    json_datas = json.load(f)
print(json.dumps(json_datas, ensure_ascii=False))

sum_note = 0
for json_data in json_datas :
    # if json_data['Academy']=='밀레니엄':
        sum_note +=json_data['Skill_Note']['Main'][2]
print(sum_note)