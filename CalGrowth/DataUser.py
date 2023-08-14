class dataset:
    def __init__(self,name):
        self.ID = name
        self.Report = 0
        self.Credit = [0,0]
        self.ScretNote = 0
        self.Oparts = {
            "네브라" :[0,0,0,0],
            "파에스토스" :[0,0,0,0],
            "볼프세크" :[0,0,0,0],
            "님루드" :[0,0,0,0],
            "만드라고라" :[0,0,0,0],
            "로혼치" :[0,0,0,0],
            "에테르" :[0,0,0,0],
            "안티키테라" :[0,0,0,0],
            "보이니치" :[0,0,0,0],
            "하니와" :[0,0,0,0],
            "토템폴" :[0,0,0,0],
            "전지" :[0,0,0,0],
            "콜간테" :[0,0,0,0],
            "위니페소키" :[0,0,0,0],
            "인형" :[0,0,0,0],
            "아틀란티스" :[0,0,0,0],
            "양모" :[0,0,0,0],
            "12면체" :[0,0,0,0]
        }
        self.Bd = {
            "백귀야행" :[0,0,0,0],
            "붉은겨울" :[0,0,0,0],
            "트리니티" :[0,0,0,0],
            "게헨나" :[0,0,0,0],
            "아비도스" :[0,0,0,0],
            "밀레니엄" :[0,0,0,0],
            "아리우스" :[0,0,0,0],
            "산해경" :[0,0,0,0],
            "발키리" :[0,0,0,0]
        }
        self.Note = {
            "백귀야행" :[0,0,0,0],
            "붉은겨울" :[0,0,0,0],
            "트리니티" :[0,0,0,0],
            "게헨나" :[0,0,0,0],
            "아비도스" :[0,0,0,0],
            "밀레니엄" :[0,0,0,0],
            "아리우스" :[0,0,0,0],
            "산해경" :[0,0,0,0],
            "발키리" :[0,0,0,0]
        }
        
    def update(self, data):
        datas = data["Default"]["Student"]
        for student, info in datas.items():
            academy = info["academy"]
            mainoparts = info["mainoparts"]
            suboparts = info["suboparts"]
            if academy != "" and mainoparts != "" and suboparts != "":
                for i in range(4):
                    self.Bd[academy][i] += info["bd"][i]
                    self.Note[academy][i] += info["note"][i]
                    self.ScretNote += info["secretnote"]
                    self.Oparts[mainoparts][i] += info["oparts_main"][i]
                    self.Oparts[suboparts][i] += info["oparts_sub"][i]

    def printList(self, itemtype, item_name):
        if itemtype == 'Oparts':
            list_test = self.Oparts[item_name]
        elif itemtype == 'BD':
            list_test = self.Bd[item_name]
        elif itemtype == 'Note':
            list_test = self.Note[item_name]
        return list_test

    def increase(self, A, B, list):
        if A == 'Bd':
            for i in range(0,4):
                self.Bd[B][i] += list[i] 
        elif A == 'Note':
            for i in range(0,4):
                self.Note[B][i] += list[i]

    def increaseOparts(self, A, A_A, B, list, num):
        if A == 'OpartsBd':
            if A_A == 'Main':
                self.Oparts[B][int(num)-2] += list[int(num)-2]
            elif A_A == 'Sub' and int(num) >= 3:
                self.Oparts[B][int(num)-3] += list[int(num)-2]
            else:
                return
        elif A == 'OpartsNote':
            if A_A == 'Main' or A_A == 'Sub':
                if num == '4':
                    num2 = 0
                elif num == '5' or num == '6':
                    num2 = 1
                elif num == '7':
                    num2 = 2
                elif num == '8' or num == '9':
                    num2 = 3
                else:
                    return
                if A_A == 'Sub':
                    num2 -= 1
            else:
                return
            if num2 >= 0:
                self.Oparts[B][num2] += list[int(num)-2]

    def decrease(self, A, B, list):
        if A == 'Bd':
            target = self.Bd
        elif A == 'Note':
            target = self.Note
        elif A == 'Oparts':
            target = self.Oparts
        for i in range(0,4):
            target[0][B][i] -= list[i]