import sys,pygame
import copy #for copy objects
import RelationalQ
import SARSA
import Predicate
import GridEnv

         

def Save(agent, filename): 
    import pickle
    output = open(filename, 'wb')
    pickle.dump(agent, output)
    output.close()

def Load(filename):
    import pickle
    input = open(filename, 'rb')
    return pickle.load(input)

def TestRun(controller, type, discrete_size, monsterMoveProb, isUpdate, trainingStage, objSet, maxEpisode, isEpisodeEnd):
    size = 800, 800
    gridSize = (discrete_size, discrete_size)
    delay = 100
    interval = 50
    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))
    env = GridEnv.Grid((discrete_size, discrete_size), size, actionList, monsterMoveProb)

    isTraining = not isEpisodeEnd
    maxStep = 200

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
        marioLoc = getMarioLoc(world, gridSize)
        ob = (marioLoc, objLoc)
        if type == 'RRL':
            action = controller.start(ob)
        elif type == 'SARSA':
            action = controller.start(Predicate.getSarsaFeature(ob))
            #print Predicate.getSarsaFeature(ob)
        elif type == 'LinearSARSA':
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
            clock.tick(10)
            reward, world, flag = env.step(action, isTraining)
            totalReward = totalReward + reward
            if flag:
                if type == 'RRL':
                    controller.end(reward, trainingStage)
                elif type == 'SARSA' or type == 'LinearSARSA':
                    controller.end(reward, isUpdate)
                else:
                    assert False
                break
            objLoc = getObjLoc(world, gridSize)
            marioLoc = getMarioLoc(world, gridSize)
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
def SmallWorldTest(agentConf, maxTrainEpisode, maxTestEpisode):

    discrete_size = 8
    monsterMoveProb = 0.3
    isUpdate = True
    worldConf = (3, 5)

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))

    controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    reward, controller = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, isUpdate, 4, worldConf, maxTrainEpisode, True)
    reward, controller = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, isUpdate, 4, worldConf, maxTestEpisode, True)
    SaveToCSV(reward, 'SarsaComp'+str(maxTrainEpisode)+'.csv')
    #Save(controller, 'SarsaCompController'+'.txt')
    #print controller.Q
    #DumpSARSA(controller)



    #preList = [Predicate.MarioPre(), Predicate.MonsterPre(), Predicate.CoinPre(), Predicate.CoinAndMonsterPre(), Predicate.RestPre()]
    preList = []
    for conf in agentConf:
        preList.append(Predicate.CoinAndMonsterPre(conf[0], conf[1]))
    preList.append(Predicate.RestPre())
    controller = RelationalQ.RelationalQ(0.1, 0.2, 0.9, actionList, preList)
    

    #trainEpisodeList = [0, 50, 100, 150]
    trainEpisode = maxTrainEpisode / len(agentConf)

    trainingStage = 1
    lastConf = agentConf[len(agentConf)-1]
    print "Prepare training--------------"
    for conf in agentConf: #don't run 2-order in the training stage
        #print "stage: ", trainingStage 
        #print "monster: ", conf[0]
        #print "coin: ", conf[1]

        coinNum = conf[1]

        isEpisodeEnd  = False
        if coinNum > 0:
            isEpisodeEnd = True

        reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, conf, trainEpisode, isEpisodeEnd)
        #Save(controller, 'RRL_controller_train_'+str(trainEpisode)+ '_'+str(lastConf)+'_'+str(len(agentConf)) + '.txt')
        #DumpRRL(controller)
        trainingStage = trainingStage + 1

    #DumpRRL(controller)
    #raw_input("Press Enter to continue...")

    #DumpRRL(controller)

    isEpisodeEnd = True
    reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, worldConf, maxTestEpisode, isEpisodeEnd)
    SaveToCSV(reward, 'RRL_test_'+str(trainEpisode)+'_'+str(lastConf)+'_'+str(len(agentConf))+'.csv')
    #Save(controller, 'RRL_test_controller_'+str(trainEpisode)+'_'+str(lastConf)+'_'+str(len(agentConf))+'.txt')

        
def SaveToCSV(list, filename):
    FILE = open(filename,"w")
    for index in list:
        FILE.write(str(list[index]))
        FILE.write(', ')
    FILE.close()
if __name__ == "__main__":
    #reward = Load('convergence.txt')
    #SaveToCSV(reward, 'conv.csv')
    trainEpisodeList = [0, 400, 800, 1200, 1600, 2000, 2400, 2800]
    testEpisode = 100
    agentList =                      \
    [                                \
    [(5, 3)]                         \
    #[(0, 1)],                        \
    #[(0, 2)],                        \
    #[(0, 3)],                        \
    #[(0, 1), (0, 2)],                \
    #[(1, 0), (0, 1)],                 \
    #[(1, 0), (0, 1), (1, 1)],                 \
    #[(1, 0), (0, 1), (1, 1), (0, 2), (1, 2)], \
    #[(0, 1), (0, 2), (0, 3)],        \
    #[(0, 1), (0, 2), (0, 3), (0, 4)],\
    #[(1, 0)],                        \
    #[(1, 0), (0, 1), (1, 1), (2, 0), (2, 1)], \
    #[(1, 0), (2, 0)],                \
    #[(2, 0)],                        \
    #[(1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1), (1, 2), (2, 2)], \
    #[(3, 0)],                        \
    #[(1, 0), (2, 0), (3, 0)],        \
    #[(1, 0), (2, 0), (3, 0), (4, 0)]\
    ]
    for trainEpisode in trainEpisodeList:
        for agentConf in agentList:
            SmallWorldTest(agentConf, trainEpisode, testEpisode)
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
