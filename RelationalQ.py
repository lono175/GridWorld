import random
#import RLSARSA
import LinearSARSA

#all, mario position, monster, coin,  coin+monster
#predict Q from lower order
#use the difference between the predicted and real one to update higher order relations
#conf: (2, 1) 2 monster, 1 coin
#conf: (0, 0) mario location
class RelationalQ:
    def __init__(self, alpha, epsilon, gamma, actionList, agentList):
        self.actionList = actionList
        self.epsilon = epsilon
        self.gamma = gamma
        self.initialQ = 0
        self.dumpCount = 0 #dump is done by relationalQ
        #self.predList = predList

        self.agent = {}
        self.dirtyAgent = {}
        for conf in agentList:
            self.agent[conf] = LinearSARSA.LinearSARSA(alpha, epsilon, gamma, actionList, self.initialQ, self.dumpCount )

    def getCurConf(self, observation):
        marioLoc, objLoc = observation
        monNum = 0
        coinNum = 0
        for obj in objLoc:
            if obj[0] == coinType:
                coinNum = coinNum + 1
            else if obj[0] == monsterType:
                monNum = monNum + 1
        return (monNum, coinNum)

    def addDirtyAgent(self, conf):
        #agent[0] is the global Q
        if not conf in self.dirtyAgent:
            #if the agent is clean, copy the agent to the dirty list
            if conf in self.agent:
                self.dirtyAgent[conf] = self.agent[conf]
            else:
                self.dirtyAgent[conf] = LinearSARSA.LinearSARSA(alpha, epsilon, gamma, actionList, self.initialQ, self.dumpCount ) 

    def updateAllQ(self, observation):
        marioLoc, objLoc = observation        
        for action in self.actionList:
            self.agent[0].Q[(marioLoc, action)] = self.getQ(observation, action)

    def getQ(self, observation, action):
        Q = 0
        curConf = self.getCurConf(observation)
        for conf in self.agent:
            if conf == curConf: #use the value in the dirty list
                continue
            feaList = Predicate.GetRelFeature(observation, conf[0], conf[1])
            for fea in feaList:
                Q = Q + self.agent[conf].getQ(fea, action)

        #check if the curConf is in dirtyAgent or not
        if curConf == self.trainingStage:
            #it is still clean
            Q = Q + self.agent[curConf].getQ(Predicate.GetRelFeature(observation, curConf[0], curConf[1]) 
        else:
            #it is dirty
            self.addDirtyAgent(curConf)
            Q = Q + self.dirtyAgent[curConf].getQ(Predicate.GetRelFeature(observation, curConf[0], curConf[1]) 
        return Q
         
    def selectAction(self, observation):
        marioLoc, objLoc = observation
        self.updateAllQ(observation)

        #use epsilon-greedy
        if random.random() < self.epsilon:
            #select randomly
            action = self.actionList[int(random.random()*len(self.actionList))]
            return action
        else:
            #select the best action
            v = []
            for action in self.actionList:
                v.append(self.agent[0].Q[(marioLoc, action)])
            assert len(v) > 0
            m = max(v)
            select = int(random.random()*v.count(m))

            i = 0
            maxCount = 0
            for value in v:
                if value == m:
                    if maxCount == select:
                        action = self.actionList[i]
                        break
                    maxCount = maxCount + 1
                i = i + 1
            return action

    def start(self, observation, trainingStage):
        #print "-start-"
        #print "obj loc: ", self.getObjLoc(observation)
        marioLoc, objLoc = (observation)
        self.trainingStage = trainingStage
        self.lastObservation = observation
        self.lastAction = self.selectAction(observation)
        self.lastQ = self.getQ(observation, self.lastAction)
        return self.lastAction

    def getDeltaQ(self, lastQ, reward, newQVal):
        return (reward + self.gamma * newQVal - lastQ)

    def updateQ(self, observation, action, deltaQ):
        #find current conf
        curConf = self.getCurConf(observation)
        if curConf != self.trainingStage:
           #it is dirty
           self.addDirtyAgent(curConf)
           self.dirtyAgent[curConf].updateQ(Predicate.GetRelFeature(observation, conf[0], conf[1]), action, deltaQ)
        else:
           #it is clean
           self.agent[curConf].updateQ(Predicate.GetRelFeature(observation, conf[0], conf[1]), action, deltaQ)

        
    def step(self, reward, observation):
        marioLoc, objLoc = observation
        newAction = self.selectAction(observation)
        newQ = self.getQ(observation, newAction)
        deltaQ = self.getDeltaQ(self.lastQ, reward, newQ)
        self.updateQ( self.lastObservation, self.lastAction, deltaQ)

        self.lastObservation = observation
        self.lastAction = newAction
        self.lastQ = newQ
        return newAction

    def end(self, reward):
        diffQ = self.getDeltaQ(self.lastQ, reward, 0)
        self.updateQ( self.lastObservation, self.lastAction, diffQ)


        
def getMarioLoc(observation, size):
    height, width = size
    for y in range(0, height):
        for x in range(0, width):
            key = (y, x)
            if(observation[key] == 1):
                return key
    return (-1, -1)
     
def getObjLoc(observation, size):
    res = []
    height, width = size
    for y in range(0, height):
        for x in range(0, width):
            key = (y, x)
            if(observation[key] == 2):
                res.append( (2, y, x))
            elif (observation[key] == 3):
                res.append( (3, y, x))
    return res

import Predicate
if __name__ == "__main__":
    
    preList = [Predicate.CoinAndMonsterPre(0, 1), Predicate.CoinAndMonsterPre(1, 0), Predicate.CoinAndMonsterPre(1, 1)]
    size = (5, 1)
    controller = RelationalQ(0.2, 0, 0.5, (-1, 1), preList)
    trainingStage = 3
    world = {}
    world[(0, 0)] = 1
    world[(1, 0)] = 0
    world[(2, 0)] = 2
    world[(3, 0)] = 0
    world[(4, 0)] = 3

    objLoc = getObjLoc(world, size)
    marioLoc = getMarioLoc(world, size)
    ob = (marioLoc, objLoc)
    print controller.start(ob)

    #print "all"
    #print controller.agent[0].Q
    #print "world"
    #print controller.agent[1].Q
    #print "turtle"
    #print controller.agent[2].Q
    #print "coin"
    #print controller.agent[3].Q
    for i in range(0, 10):
        
        objLoc = getObjLoc(world, size)
        marioLoc = getMarioLoc(world, size)
        ob = (marioLoc, objLoc)
        print controller.step(1, ob, trainingStage)
        #print controller.start(world)
        #print "all"
        #print controller.agent[0].Q
        #print "world"
        #print controller.agent[1].Q
        #print "turtle"
        #print controller.agent[2].Q
        #print "coin"
        #print controller.agent[3].Q

    #print controller.end(1, trainingStage)

    print "world"
    print controller.agent[1].Q

    print "turtle"
    print controller.agent[2].Q

    print "coin"
    print controller.agent[3].Q

    #import pickle
    #output = open('data.pkl', 'wb')
    #pickle.dump(controller, output)
    #output.close()
    #input = open('data.pkl', 'rb')
    #ctrl2 = pickle.load(input)
    #print "after load"
    #print ctrl2.Q
    #pickle.loads(xp)
    #y
    

