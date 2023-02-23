class dataset:
    def __init__(self,name):
        self.ID = name
        self.Level_current = 0
        self.Skill_current = [0,0,0,0]
        self.Level_goal = 0
        self.Skill_goal = [0,0,0,0]

    def all(self):
        print(self.ID, self.Level_current, self.Skill_current, self.Level_goal, self.Skill_goal)