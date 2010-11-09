import sys,pygame
import copy #for copy objects
import RelationalQ
import SARSA
import Predicate
import SimpleGridEnv
import math

         

def Save(agent, filename): 
    import pickle
    output = open(filename, 'wb')
    pickle.dump(agent, output)
    output.close()

def Load(filename):
    import pickle
    input = open(filename, 'rb')
    return pickle.load(input)

def TestRun(controller, type, gridSize, monsterMoveProb, isUpdate, trainingStage, objSet, maxEpisode, isEpisodeEnd, isDraw, clockRate):
    size = 800, 800
    delay = 100
    interval = 50
    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    actionList = controller.actionList
    env = SimpleGridEnv.SimpleGrid(gridSize, size, actionList, monsterMoveProb)

    isTraining = not isEpisodeEnd
    maxStep = 50

    numOfTurtle = objSet[0]
    numOfCoin = objSet[1]

    print "# coin ", numOfCoin
    print "# Turtle ", numOfTurtle
    print "training stage ", trainingStage
    print "isEpisodeEnd ", isEpisodeEnd

    count = 0
    
    totalReward = 0
    rewardList = {}
    #while 1:
    for i in range(0, maxEpisode):
        #print totalReward
        rewardList[i] = totalReward

        world = env.start(numOfTurtle, numOfCoin)
        objLoc = getObjLoc(world, gridSize)
        marioLoc = env.marioLoc
        ob = (marioLoc, objLoc)
        if type == 'RRL':
            action = controller.start(ob)
        elif type == 'SARSA':
            action = controller.start(Predicate.getSarsaFeature(ob))
        count += 1
        #if count % 100 == 0:
            #print "monster------------------"
            ##print controller.agent[2].Q
            #for y in range(-2, 3):
                #for x in range(-2, 3):
                    #for action in actionList:
                        #controller.agent[2].touch((x, y), action)
                        #print (x, y), " ", action, " ", controller.agent[2].Q[((x, y), action)]
            #print "coin------------------"
            ##print controller.agent[2].Q
            #for y in range(-2, 3):
                #for x in range(-2, 3):
                    #for action in actionList:
                        #controller.agent[3].touch((x, y), action)
                        #print (x, y), " ", action, " ", controller.agent[3].Q[((x, y), action)]
            #print "world------------------"
            #for y in range(0, 3):
                #for x in range(0, 3):
                    #for action in actionList:
                        #controller.agent[1].touch((x, y), action)
                        #print (x, y), " ", action, " ", controller.agent[1].Q[((x, y), action)]
            #print "all------------------"
            #for y in range(0, 3):
                #for x in range(0, 3):
                    #for action in actionList:
                        #controller.agent[0].touch((x, y), action)
                        #print (x, y), " ", action, " ", controller.agent[0].Q[((x, y), action)]
        for j in range(0, maxStep):
            clock.tick(clockRate)
            reward, world, flag = env.step(action, isTraining)
            totalReward = totalReward + reward
            if flag:
                if type == 'RRL':
                    controller.end(reward, trainingStage)
                elif type == 'SARSA':
                    controller.end(reward, isUpdate)
                else:
                    assert False
                break
            objLoc = getObjLoc(world, gridSize)
            marioLoc = env.marioLoc
            ob = (marioLoc, objLoc)
            if type == 'RRL':
                action = controller.step(reward, ob, trainingStage)
            elif type == 'SARSA':
                action = controller.step(reward, Predicate.getSarsaFeature(ob), isUpdate)
            else:
                assert False
            for event in pygame.event.get():
               #action = 0
               if event.type == pygame.QUIT: sys.exit()
            if isDraw:
                screen.blit(env.getScreen(), (0, 0))
                pygame.display.flip()
    #print totalReward
    return rewardList, controller

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
    
def DumpSARSA(controller):
    #print controller.Q
    #print controller.agent[2].Q
    for y in range(-1, 2):
        for x in range(-1, 2):
            for action in controller.actionList:
                fea = ((0, 0), (1, 0), (x, y))
                controller.touch(fea, action)
                key = (fea, action)
                print key, " ", action, " ", controller.Q[key]
def DumpRRL(controller):
    actionList = controller.actionList
    print "monster------------------"
    #print controller.agent[2].Q
    for y in range(-2, 3):
        for x in range(-2, 3):
            for action in actionList:
                controller.agent[2].touch((x, y), action)
                print (x, y), " ", action, " ", controller.agent[2].Q[((x, y), action)]
    print "coin------------------"
    #print controller.agent[2].Q
    for y in range(-2, 3):
        for x in range(-2, 3):
            for action in actionList:
                controller.agent[3].touch((x, y), action)
                print (x, y), " ", action, " ", controller.agent[3].Q[((x, y), action)]
    print "world------------------"
    for y in range(0, 3):
        for x in range(0, 3):
            for action in actionList:
                controller.agent[1].touch((x, y), action)
                print (x, y), " ", action, " ", controller.agent[1].Q[((x, y), action)]
    print "coin and monster------------------"
    for y in range(0, 3):
        for x in range(0, 3):
            for action in actionList:
                controller.agent[4].touch(((x, y), (1, 0)), action)
                print (x, y), " ", action, " ", controller.agent[4].Q[(((x, y), (1, 0)), action)]
def SmallWorldTest():
    #controller = Load('RRL_controller.txt')
    #DumpRRL(controller)
    #return
    #controller = Load('controller.txt')
    #DumpController(controller)

    maxCoinNum = 5
    discrete_size = (1, maxCoinNum+1)
    monsterMoveProb = 0
    maxEpisode = 50000
    isUpdate = True
    isDraw = False
    tickNum = 1000

    actionList = ((0, 1), (0, -1))

    preList = []
    for i in range(maxCoinNum):
        preList.append(Predicate.CoinPre(i+1))
    alpha = 0.1
    epsilon = 1
    controller = RelationalQ.RelationalQ(alpha, epsilon, 0.8, actionList, preList)

    #trainEpisodeList = [0, 50, 100, 150]
    trainEpisodeList = [50000]
    for trainEpisode in trainEpisodeList:
        for trainingStage in range(1, maxCoinNum+1): 
            print "stage: ", trainingStage 

            numOfTurtle = 0
            numOfCoin = trainingStage
            reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, (numOfTurtle, numOfCoin), trainEpisode, True, isDraw, tickNum)
            #DumpRRL(controller)
            #raw_input("Press Enter to continue...")
        Save(controller, 'RRL_Random_controller_train_'+str(trainEpisode)+'.txt')

        
def SaveToCSV(list, filename):
    FILE = open(filename,"w")
    for val in list:
        FILE.write(str(val))
        FILE.write(', ')
    FILE.close()

def RemoveLargeValue(controller, filenamePrefix):
    maxRange = 5
    count = -1
    for agent in controller.agent:
        count = count + 1
        if count == 0:
            continue
        res = []
        keyList = agent.Q.keys()
        for key in keyList:
            index, action = key 
            feature = list(index)
            isBig = False
            for val in feature:
                for tinyVal in list(val):
                    if abs(tinyVal) > maxRange:
                        isBig = True
                        break;

            if not isBig:
                print key, "  ", agent.Q[key]
                res.append(agent.Q[key])
        #SaveToCSV(res, filenamePrefix+str(count)+'.csv')

if __name__ == "__main__":
    #reward = Load('convergence.txt')
    #SaveToCSV(reward, 'conv.csv')
    #SmallWorldTest()
    #controller = Load('RRL_complex_controller_train_'+str(5000)+'.txt')
    #RemoveLargeValue(controller, 'Greedy')

    controller = Load('RRL_Random_controller_train_'+str(50000)+'.txt')
    RemoveLargeValue(controller, 'Random')

    #print controller.agent[1].Q
    #print "------------------"
    #print controller.agent[3].Q
    #print "------------------"
    #print controller.agent[3].Q
    #print "------------------"
    #print controller.agent[4].Q

    #for maxEpisode in range(100, 1000, 100):
        #controller = train(maxEpisode, 'SARSA')
        #Save(controller, 'SARSA-Agent' + str(maxEpisode) + '.txt')

    #for maxEpisode in range(100, 1000, 100):
        #controller = train(maxEpisode, 'RRL')
        #Save(controller, 'RL-Agent' + str(maxEpisode) + '.txt')


    #for maxEpisode in range(100, 1000, 100):
        #controller = Load('SARSA-Agent' + str(maxEpisode) + '.txt')
        #reward = TestRun(controller, 'SARSA')
        #Save(reward, 'SARSA-Reward'+str(maxEpisode)+'.txt')

    #for maxEpisode in range(100, 1000, 100):
        #controller = Load('RL-Agent' + str(maxEpisode) + '.txt')
        #reward = TestRun(controller, 'RRL')
        #Save(reward, 'RRL'+str(maxEpisode)+'.txt')

    #controller = Load('RL-Agent' + str(900) + '.txt')
    #reward = TestRun(controller, 'RRL')
    #Save(reward, 'RRL-Reward-learning-900'+'.txt')

    #controller = Load('SARSA-Agent' + str(900) + '.txt')
    #reward = TestRun(controller, 'SARSA')
    #Save(reward, 'SARSA-Reward-learning-900'+'.txt')

    #reward = Load('SARSA-Reward-learning-900.txt')
    #FILE = open('SARSA_Reward_Diff',"w")
    #for index in reward:
        #FILE.write(str(reward[index]))
        #FILE.write(', ')
        #
    #FILE.close()

    #reward = Load('RRL-Reward-learning-900.txt')
    #FILE = open('RRL_Reward_Diff',"w")
    #for index in reward:
        #FILE.write(str(reward[index]))
        #FILE.write(', ')
        #
    #FILE.close()
