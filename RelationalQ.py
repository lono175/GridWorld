import random
#import RLSARSA
import LinearSARSA

#all, mario position, monster, coin,  coin+monster
#predict Q from lower order
#use the difference between the predicted and real one to update higher order relations
class RelationalQ:
    def __init__(self, alpha, epsilon, gamma, actionList, predList):
        self.actionList = actionList
        self.epsilon = epsilon
        self.gamma = gamma
        self.predList = predList
        predicateSize = len(predList)

        self.agent = []
        for i in range(0, predicateSize + 1): #agent[0] is the global Q
            initialQ = 0
            dumpCount = 0 #dump is done by relationalQ
            self.agent.append(LinearSARSA.LinearSARSA(alpha, epsilon, gamma, actionList, initialQ, dumpCount ))
            #self.agent.append(RLSARSA.RLSARSA(alpha))

    def updateAllQ(self, observation):
        marioLoc, objLoc = observation        
        for action in self.actionList:
            self.agent[0].Q[(marioLoc, action)] = self.getQ(observation, action)

    def getQ(self, observation, action):
        Q = 0
        i = 1
        for pred in self.predList:
            feaList = pred.getFeature(observation)
            for fea in feaList:
                Q = Q + self.agent[i].getQ(fea, action)
            i = i + 1
        return Q
        #Q = self.agent[1].getQ(key, action)

        #for obj in objectLoc:
            #type, objX, objY = obj
            #diff = (x-objX, y-objY)

            ##self.agent[type].touch(diff, action)
            ##print "type: ", type
            ##print "diff: ", diff
            #Q = Q + self.agent[type].getQ(diff, action)
        #return Q

         
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

    def start(self, observation):
        #print "-start-"
        #print "obj loc: ", self.getObjLoc(observation)
        marioLoc, objLoc = (observation)
        self.lastObservation = observation
        self.lastAction = self.selectAction(observation)
        self.lastQ = self.getQ(observation, self.lastAction)
        return self.lastAction

    def getDeltaQ(self, lastQ, reward, newQVal):
        return (reward + self.gamma * newQVal - lastQ)

    def updateQ(self, trainingStage, observation, action, deltaQ):
        i = 0
        for pred in self.predList:
            i = i + 1
            if i != trainingStage:
                continue
            feaList = pred.getFeature(observation)
            for fea in feaList:
                #TODO: add regression here, it doesn't work for more than one feature
                self.agent[i].updateQ(fea, action, deltaQ)
        
    def step(self, reward, observation, trainingStage):
        marioLoc, objLoc = observation
        newAction = self.selectAction(observation)
        newQ = self.getQ(observation, newAction)
        deltaQ = self.getDeltaQ(self.lastQ, reward, newQ)
        self.updateQ( trainingStage, self.lastObservation, self.lastAction, deltaQ)

        self.lastObservation = observation
        self.lastAction = newAction
        self.lastQ = newQ
        return newAction

    def end(self, reward, trainingStage):
        diffQ = self.getDeltaQ(self.lastQ, reward, 0)
        self.updateQ( trainingStage, self.lastObservation, self.lastAction, diffQ)


        
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
    

