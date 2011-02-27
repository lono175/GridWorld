import random
import gridDef
monsterType = gridDef.monsterType
coinType = gridDef.coinType
XType = 1
YType = 2

class LinearSARSA:
    def __init__(self, alpha, epsilon, gamma, actionList, initialQ ):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.actionList = actionList
        self.initialQ = initialQ
        self.Q = {}
    def touch(self, observation, action):
        for fea in observation:
            if not (fea, action) in self.Q:
                self.Q[(fea, action)] = self.initialQ #may use optimistic exploration
    def selectAction(self, observation):
        #use epsilon-greedy
        if random.random() < self.epsilon:
            #select randomly
            action = self.actionList[int(random.random()*len(self.actionList))]
            self.touch(observation, action)
            return action
        else:
            #select the best action
            v = []
            for action in self.actionList:
                self.touch(observation, action)
                v.append(self.getQ(observation, action))
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

    def getQ(self, ob, action):
        Q = 0
        for fea in ob:
            Q = Q + self.Q[(fea, action)]
        return Q
        
    def update(self, lastObservation, lastAction, reward, observation, action):
        newQ = self.getQ(observation, action)
        oldQ = self.getQ(lastObservation, lastAction)
        delta = reward + self.gamma * newQ - oldQ
        self.updateQ(lastObservation, lastAction, delta)

    def updateQ(self, lastObservation, lastAction, delta):
        numOfFeature = len(lastObservation)
        deltaPerFeature = delta/numOfFeature
        print "delta: ", deltaPerFeature
        for fea in lastObservation:
            self.Q[(fea, lastAction)] = self.Q[(fea, lastAction)] + self.alpha*deltaPerFeature
        
    def getFeature(self, ob):
        marioLoc, monLoc, coinLoc = ob

        feaList = []
        #separate it into individual faetures
        i = 0
        for loc in monLoc:
            if i % 2 == 0:
                fea = (monsterType, XType, loc)
            else:
                fea = (monsterType, YType, loc)
            i = i + 1
            feaList.append(fea)
        i = 0
        for loc in coinLoc:
            if i % 2 == 0:
                fea = (coinType, XType, loc)
            else:
                fea = (coinType, YType, loc)
            i = i + 1
            feaList.append(fea)
        return feaList
    def start(self, observation):
        ob = self.getFeature(observation)
        self.lastObservation = ob
        self.lastAction = self.selectAction(ob)
        return self.lastAction

    def step(self, reward, observation, isUpdate):
        ob = self.getFeature(observation)
        self.lastObservation = ob
        newAction = self.selectAction(ob)
        if isUpdate:
            self.update(self.lastObservation, self.lastAction, reward, ob, newAction)
        self.lastObservation = ob
        self.lastAction = newAction
        return newAction
    def end(self, reward, isUpdate):
        if isUpdate:
            oldQ = self.getQ(self.lastObservation, self.lastAction)
            delta = reward - oldQ
            self.updateQ(self.lastObservation, self.lastAction, delta)
    
if __name__ == "__main__":
    
    isUpdate = True
    initialQ = 0
    controller = LinearSARSA(0.5, 0, 0.8, (-1, 1), initialQ)
    ob = ((1,1), (2,2), (3, 3))
    print controller.start(ob)
    print controller.Q
    print controller.step(10, ob, isUpdate)
    print controller.Q
    print controller.step(10, ob, isUpdate)
    print controller.Q
    print controller.step(10, ob, isUpdate)
    print controller.Q
    print controller.step(10, ob, isUpdate)
    print controller.Q
    for i in range(0,100):
        print controller.step(10, ob, isUpdate)
        print controller.Q
    #print controller.end(10, isUpdate)
    #print controller.Q
    #import pickle
    #output = open('data.pkl', 'wb')
    #pickle.dump(controller, output)
    #output.close()
    #input = open('data.pkl', 'rb')
    #ctrl2 = pickle.load(input)
    #print "after load"
    #print controller.Q
    #pickle.loads(xp)
    #y
    
