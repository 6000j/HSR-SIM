# actionOrder = [1,1,2] means single attack, single attack, double attack

class Enemy:
    broken = False
    
    def __init__(self, enemyID: int, level: int, spd: float, toughness: int, actionOrder: list, weakness: list, adjacent: list):
        self.enemyID = enemyID
        self.name = f"Enemy {self.enemyID}"
        self.level = level
        self.spd = spd
        self.toughness = toughness
        self.gauge = self.toughness
        self.actionOrder = actionOrder
        self.weakness = weakness
        self.adjacent = adjacent
        self.currAV = 10000 / self.spd
        self.turn = 0
        
    def __str__(self) -> str:
        res = f"Enemy {self.enemyID} | LVL: {self.level} | SPD: {self.spd} | "
        res += f"Weakness: {self.weakness} | Toughness: {self.toughness}"
        return res
    
    def getUniMul(self) -> float:
        return 1.0 if self.broken else 0.9
    
    def redToughness(self, toughness: int) -> bool:
        self.guage = max(self.gauge - toughness, 0)
        if self.gauge == 0:
            self.broken = True
            return True
        return False
    
    def recover(self):
        if self.broken:
            self.gauge = self.toughness
            self.broken = False
        
    def takeTurn(self) -> int:
        self.recover()
        res = self.turn
        self.turn = self.turn + 1
        self.currAV = 10000 / self.spd
        return self.actionOrder[res % len(self.actionOrder)]
    
    def isChar(self) -> bool:
        return False
    
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
        