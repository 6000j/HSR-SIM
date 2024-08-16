from Lightcone import Lightcone
from Buff import Buff

class PostOp(Lightcone):
    name = "Post-Op Conversation"
    path = "ABU"
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 330.75

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        errBuff = self.level * 0.02 + 0.06
        buffList.append(Buff("PostOpERR", "ERR%", errBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        oghBuff = self.level * 0.03 + 0.09
        buffList.append(Buff("PostOpOGH", "OGH%", oghBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    