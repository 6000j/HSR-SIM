from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from RelicStats import RelicStats
from Planar import Planar
from Turn import Turn
from Result import *
from Misc import *
import logging

logger = logging.getLogger(__name__)

class Character:
    # Standard Character Properties
    name = "Character"
    path = "PATH"
    element = "ELE"
    scaling = "ATK"
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 100
    maxEnergy = 100
    ultCost = 100
    currEnergy = maxEnergy / 2
    currAV = 100.0
    rotation = ["E", "A", "A"]
    dmgDct = {AtkType.BSC: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0}
    hasSpecial = False
    hasSummon = False
    specialEnergy = False
    basics = 0
    skills = 0
    ults = 0
    fuas = 0
    turn = 0
    
    # Unique Character Properties
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int) -> None:
        self.pos = pos
        self.role = role
        self.priority = 0
        self.currSPD = 100
        self.defaultTarget = defaultTarget
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.element.name}-{self.path.name} | {self.role.name} | POS:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        return self.parseEquipment("EQUIP")
    
    def useSkl(self, enemyID=-1):
        self.skills = self.skills + 1
        return *self.parseEquipment(AtkType.BSC, enemyID=enemyID), []
    
    def useBsc(self, enemyID=-1):
        self.basics = self.basics + 1
        return *self.parseEquipment(AtkType.SKL, enemyID=enemyID), []
    
    def useUlt(self, enemyID=-1):
        self.ults = self.ults + 1
        return *self.parseEquipment(AtkType.ULT, enemyID=enemyID), []
        
    def useFua(self, enemyID=-1):
        self.fuas = self.fuas + 1
        return *self.parseEquipment(AtkType.FUA, enemyID=enemyID), []
        
    def useHit(self, enemyID=-1):
        return *self.parseEquipment("HIT", enemyID=enemyID), []
    
    def ownTurn(self, turn: Turn, result: Result):
        if result.atkType[0] in self.dmgDct:
            self.dmgDct[result.atkType[0]] = self.dmgDct[result.atkType[0]] + result.turnDmg
        self.dmgDct[AtkType.BRK] = self.dmgDct[AtkType.BRK] + result.wbDmg
        self.currEnergy = min(self.maxEnergy, self.currEnergy + result.errGain)
        return *self.parseEquipment("OWN", turn=turn, result=result), []
    
    def special(self):
        return ""
    
    def handleSpecialStart(self, specialRes: Special):
        return *self.parseEquipment("SPECIALS", special=specialRes), []
    
    def handleSpecialEnd(self, specialRes: Special):
        return *self.parseEquipment("SPECIALE", special=specialRes), []
    
    def allyTurn(self, turn: Turn, result: Result):
        return *self.parseEquipment("ALLY", turn=turn, result=result), []
        
    def parseEquipment(self, actionType: str, turn=None, result=None, special=None, enemyID=-1):
        buffList, debuffList, advList, delayList = [], [], [], []
        equipmentList = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipmentList.append(self.relic2)
            
        for equipment in equipmentList:
            if actionType == AtkType.BSC:
                buffs, debuffs, advs, delays = equipment.useBsc(enemyID)
            elif actionType == AtkType.SKL:
                buffs, debuffs, advs, delays = equipment.useSkl(enemyID)
            elif actionType == AtkType.ULT:
                buffs, debuffs, advs, delays = equipment.useUlt(enemyID)
            elif actionType == AtkType.FUA:
                buffs, debuffs, advs, delays = equipment.useFua(enemyID)
            elif actionType == "EQUIP":
                buffs, debuffs, advs, delays = equipment.equip()
            elif actionType == "HIT":
                buffs, debuffs, advs, delays = equipment.useHit(enemyID)
            elif actionType == "SPECIALS":
                buffs, debuffs, advs, delays = equipment.specialStart(special)
            elif actionType == "SPECIALE":
                buffs, debuffs, advs, delays = equipment.specialEnd(special)
            elif actionType == "OWN":
                buffs, debuffs, advs, delays = equipment.ownTurn(turn, result)    
            elif actionType == "ALLY":
                buffs, debuffs, advs, delays = equipment.allyTurn(turn, result)
                
            buffList.extend(buffs)
            debuffList.extend(debuffs)
            advList.extend(advs)
            delayList.extend(delays)
        return buffList, debuffList, advList, delayList
    
    def addEnergy(self, amount: float):
        self.currEnergy = min(self.maxEnergy, self.currEnergy + amount)
        
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
    def getRelicScalingStats(self) -> tuple[float, float]:
        return self.relicStats.getScalingValue(self.scaling)
    
    def getSPD(self) -> float:
        return self.relicStats.getSPD()
    
    def canUseUlt(self) -> bool:
        return self.currEnergy >= self.ultCost
    
    def isChar(self) -> bool:
        return True
    
    def isSummon(self) -> bool:
        return False
    
    def takeTurn(self) -> str:
        res = self.turn
        self.turn = self.turn + 1
        return self.rotation[res % len(self.rotation)]
    
    def gettotalDMG(self) -> tuple[str, float]:
        ttl = sum(self.dmgDct.values())
        res = ""
        for key, val in self.dmgDct.items():
            res += f"-{key.name}: {val:.3f} | {val / ttl * 100 if ttl > 0 else 0:.3f}%\n"
        return res, ttl
    
    def getBaseStat(self) -> tuple[float, float, float]:
        if self.scaling == Scaling.ATK:
            baseStat = self.baseATK + self.lightcone.baseATK
        if self.scaling == Scaling.HP:
            baseStat = self.baseHP + self.lightcone.baseHP
        if self.scaling == Scaling.DEF:
            baseStat = self.baseDEF + self.lightcone.baseDEF
        return baseStat, *self.getRelicScalingStats()
    
    def standardAVred(self, av: float):
        self.currAV = max(0, self.currAV - av)
        
    def getTargetID(self, enemyID: int):
        if enemyID == -1:
            return self.defaultTarget
        return enemyID
    
    def extendLists(self, bl: list, dbl: list, al: list, dl: list, tl: list, nbl: list, ndbl: list, nal: list, ndl: list, ntl: list):
        bl.extend(nbl)
        dbl.extend(ndbl)
        al.extend(nal)
        dl.extend(ndl)
        tl.extend(ntl)
        return bl, dbl, al, dl, tl
        
    
        