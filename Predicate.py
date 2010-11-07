monsterType = 2
coinType = 3
def getObjLoc(observation):
    res = []
    for y in range(0, self.height):
        for x in range(0, self.width):
            key = (x, y)
            if(observation[key] == 2):
                res.append( (2, x, y))
            elif (observation[key] == 3):
                res.append( (3, x, y))
    return res
def pow2(key):
    return key[0]*key[0] + key[1]*key[1]
def getNearObj(observation, type):
    marioLoc, objLoc = observation
    objDist = []
    for obj in objLoc:
        if obj[0] == type:
            key = (obj[1] - marioLoc[0], obj[2] - marioLoc[1])
            objDist.append((pow2(key), key[0], key[1]))
    objDist.sort(key=lambda obj: obj[0])   

    res = []
    for obj in objDist:
       res.append(obj[1])
       res.append(obj[2]) 
    return tuple(res)
def getSarsaFeature(observation):
    marioLoc, objLoc = observation
    coinLoc = getNearObj(observation, coinType)
    monLoc = getNearObj(observation, monsterType)
    return (marioLoc, monLoc, coinLoc)
    
class RestPre:
    def __init__(self):
        self.order = -1
    def getFeature(self, observation):
        coinLoc = getNearObj(observation, coinType)
        monLoc = getNearObj(observation, monsterType)
        return (monLoc, coinLoc)
class MarioPre:
    def __init__(self):
        self.order = 0

    def getFeature(self, observation):
        marioLoc, objLoc = observation
        return [marioLoc]

class CoinPre:
    def __init__(self):
        self.order = 1
    def getFeature(self, observation):
        marioLoc, objLoc = observation
        res = []
        for obj in objLoc:
            if obj[0] == coinType:
                res.append((obj[1] - marioLoc[0], obj[2] - marioLoc[1]))
        return res

class MonsterPre:
    def __init__(self):
        self.order = 1

    def getFeature(self, observation):
        marioLoc, objLoc = observation
        res = []
        for obj in objLoc:
            if obj[0] == monsterType:
                res.append((obj[1] - marioLoc[0], obj[2] - marioLoc[1]))
        return res

class CoinAndMonsterPre:
    def __init__(self):
        self.order = 2

    def getFeature(self, observation):
        marioLoc, objLoc = observation
        res = []
        for coin in objLoc:
            if coin[0] == coinType:
                for monster in objLoc:
                    if monster[0] == monsterType:
                        coinDiff = (coin[1] - marioLoc[0], coin[2] - marioLoc[1])
                        monsterDiff = (monster[1] - marioLoc[0], monster[2] - marioLoc[1])
                        res.append((coinDiff, monsterDiff))
        return res

if __name__ == "__main__":
    pre = RestPre()
    marioLoc = (0,0)
    objList = [(2, 1,1), (3, 5, 1), (2, -1, 0), (3, 1, 2)]
    print pre.getFeature((marioLoc, objList))

