from Character import Character
from Lightcones.MemoriesOfThePast import MOTP
from Relics.Musketeer import Musketeer
from Planars.Vonwacq import Vonwacq
from RelicStats import RelicStats
from Buff import Buff
from Result import Result
from Turn import Turn
from Misc import *

class Tingyun(Character):
    # Standard Character Settings
    name = "Tingyun"
    path = Path.HARMONY
    element = Element.LIGHTNING
    scaling = Scaling.ATK
    baseHP = 846.70
    baseATK = 529.20
    baseDEF = 396.90
    baseSPD = 112
    maxEnergy = 130
    ultCost = 130
    currEnergy = 130
    currAV = 0
    rotation = ["E", "A", "A"]
    dmgDct = {AtkType.BSC: 0, AtkType.SPECIAL: 0, AtkType.BRK: 0}
    
    # Unique Character Properties
    beneTarget = Role.DPS
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else MOTP(role, 5)
        self.relic1 = r1 if r1 else Musketeer(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Vonwacq(role)
        self.relicStats = subs if subs else RelicStats(14, 2, 0, 2, 4, 10, 4, 4, 4, 4, 0, 0, Pwr.ATK_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.extend([Buff("TingyunBasicDMG", Pwr.DMG_PERCENT, 0.4, self.role, [AtkType.BSC], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("TingyunTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("TingyunTraceDEF", Pwr.DEF_PERCENT, 0.225, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("TingyunTraceDMG", Pwr.DMG_PERCENT, 0.08, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM)
                         ])
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.1, 0], [10, 0], 25, self.scaling, 1, "TingyunBasic"))
        tl.append(Turn(self.name, self.beneTarget, self.getTargetID(enemyID), Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [0.66, 0], [0, 0], 0, Scaling.ATK, 0, "TYAllyBonus"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "TingyunSkill"))
        bl.append(Buff("Benediction", Pwr.ATK_PERCENT, 0.55, self.beneTarget, [AtkType.ALL], 3, 1, self.beneTarget, TickDown.END))
        bl.append(Buff("TingyunSkillSPD", Pwr.SPD_PERCENT, 0.2, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "TingyunUlt"))
        bl.append(Buff("TingyunUltEnergy", Pwr.ERR_F, 60, self.beneTarget, [AtkType.ALL], 1, 1, self.beneTarget, TickDown.PERM))
        bl.append(Buff("TingyunUltDMG", Pwr.DMG_PERCENT, 0.56, self.beneTarget, [AtkType.ALL], 2, 1, self.beneTarget, TickDown.END))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (turn.charRole == self.beneTarget) and (turn.moveName not in bonusDMG) and (turn.targeting != Targeting.NA):
            tl.append(Turn(self.name, self.beneTarget, result.enemiesHit[0], Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [0.64, 0], [0, 0], 0, Scaling.ATK, 0, "TYBeneBonus"))
        return bl, dbl, al, dl, tl
    
    