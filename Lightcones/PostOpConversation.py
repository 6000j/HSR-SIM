from Lightcone import Lightcone
from Buff import Buff

class PostOp(Lightcone):
    name = "Post-Op Conversation"
    path = "ABU"
    baseHP = 952.6
    baseATK = 423.36
    baseDEF = 396.90

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        breakBuff = self.level * 0.07 + 0.21
        buffList.append(Buff("MotpBE", "BE%", breakBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self):
        buffList, debuffList, advList, delayList = super().useBsc()
        errGain = self.level + 3
        buffList.append(Buff("MotpBonusEnergy", "ERR_T", errGain, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    