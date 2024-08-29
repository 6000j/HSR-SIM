from Relic import Relic
from Buff import Buff
from Delay import *
from Misc import *
from Result import Special

class Genius(Relic):
    name = "Genius of Brilliant Stars"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.QUANTUM, quaWeak = True):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        self.quaWeak = quaWeak
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.QUANTUM:
            bl.append(Buff("GeniusDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            shred = 0.1
            if self.quaWeak:
                shred = 0.2
            bl.append(Buff("GeniusSHRED", Pwr.SHRED, shred, self.wearerEle, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
