from Lightcone import Lightcone
from Buff import *
from Misc import *
from Result import Special

class Scent(Lightcone):
    name = "Scent Alone Stays True  "
    path = Path.ABUNDANCE
    baseHP = 1058.4
    baseATK = 529.20
    baseDEF = 529.20
    
    beStat = 0

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        beBuff = self.level * 0.1 + 0.5
        buffList.append(Buff("ScentBE", Pwr.BE_PERCENT, beBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
class ScentLingsha(Scent):
    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
        
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        vuln = self.level * 0.02 + 0.08
        extraVuln = self.level * 0.02 + 0.06 if self.beStat >= 1.5 else 0
        dbl.append(Debuff("ScentVuln", self.wearerRole, Pwr.VULN, vuln + extraVuln, Role.ALL, [AtkType.ALL], 2))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        if special.specialName == "Lingsha":
            self.beStat = special.attr3
        return super().specialStart(special)

class ScentGallagher(Scent):
    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
        
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        vuln = self.level * 0.02 + 0.08
        extraVuln = self.level * 0.02 + 0.06 if self.beStat >= 1.5 else 0
        dbl.append(Debuff("ScentVuln", self.wearerRole, Pwr.VULN, vuln + extraVuln, Role.ALL, [AtkType.ALL], 2))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        if special.specialName == "Gallagher":
            self.beStat = special.attr1
        return super().specialStart(special)
    
    

    