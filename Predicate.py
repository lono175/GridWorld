from __future__ import generators
import copy
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

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
class CoinPre:
    def __init__(self, order):
        self.order = order #order = 1 for one coin predicate
    def getFeature(self, observation):
        marioLoc, objLoc = observation
        coinList = []
        for obj in objLoc:
            if obj[0] == coinType:
                coinList.append((obj[1] - marioLoc[0], obj[2] - marioLoc[1]))
        coinList = sorted(coinList, key=lambda obj: obj[1]) 
        coinList = sorted(coinList, key=lambda obj: -(obj[0]*obj[0]+obj[1]*obj[1])) 
        
        feaList = []
        for i in xuniqueCombinations(coinList, self.order):
           feaList.append(i) 
        #feaList = self.getCoinLoc(coinList, self.order-1)
        res = []
        while feaList != []:
            last = feaList.pop()
            last.reverse()
            res.append(tuple(last))

        return res
    #def getCoinLoc(self, coinList, depth):
        #res = []
        #if depth == 0:
            #for obj in coinList:
                #res.append([obj])    
            #return res
        #else:
            #popCount = len(coinList) - depth - 1
            #last = coinList.pop()
            #lowerCoinList = self.getCoinLoc(copy.copy(coinList), depth-1)
            #print "---------------------------"
            #coinList.append(last)

            #print "lower ", lowerCoinList
            #print "coin ", coinList
            #while coinList != [] and lowerCoinList != []:
               #last = coinList.pop()
               #print "last ", last
               #print "coin2 ", coinList
               #print "lower2 ", lowerCoinList
               #for feature in lowerCoinList:
                   #feature.append(last)
                   #res.append(copy.copy(feature))
                   #feature.pop() #append will change list itself
               #print "res ", res
               #for i in range(0, popCount):
                   #lowerCoinList.pop()
               #popCount = popCount - 1
        #res.reverse()
        #return res
        
        

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
    coinPre = CoinPre(1)
    marioLoc = (0,0)
    objList = [(3, 0, -1), (3, 0, 1), (3, 0, 3), (3, 0, 2)]
    print coinPre.getFeature((marioLoc, objList))
    #pre = RestPre()
    #marioLoc = (0,0)
    #objList = [(2, 1,1), (3, 5, 1), (2, -1, 0), (3, 1, 2)]
    #print pre.getFeature((marioLoc, objList))

