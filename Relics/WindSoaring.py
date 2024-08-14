from Relic import Relic
from Buff import Buff

class WindSoaringYunli(Relic):
    name = "The Wind-Soaring Valorous"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buff_lst = [(Buff("WindSoaringATK", "ATK%", 0.12, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))]
        if self.setType == 4:
            buff_lst.append(Buff("WindSoaringCR", "CR%", 0.06, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buff_lst, [], [], []
    
    def useFua(self):
        buffList, debuffList, advList, delayList = super().useFua()
        if self.setType == 4:
            buffList.append(Buff("WindSoaringDMG", "DMG%", 0.36, self.wearerRole, ["ULT"], 1, 1, "SELF", "END"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self):
        buffList, debuffList, advList, delayList = super().useUlt()
        if self.setType == 4:
            buffList.append(Buff("WindSoaringDMG", "DMG%", 0.36, self.wearerRole, ["ULT"], 1, 1, "SELF", "END"))
        return buffList, debuffList, advList, delayList