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
            clock.tick(5000)
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
            #screen.blit(env.getScreen(), (0, 0))
            #pygame.display.flip()
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

    discrete_size = 8
    monsterMoveProb = 0.3
    maxEpisode = 50000
    isUpdate = True

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))

    controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    reward, controller = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, isUpdate, 4, (2,5), maxEpisode, True)
    SaveToCSV(reward, 'SarsaComp.csv')
    Save(controller, 'SarsaCompController'+'.txt')
    #print controller.Q
    #DumpSARSA(controller)



    preList = [Predicate.MarioPre(), Predicate.MonsterPre(), Predicate.CoinPre(), Predicate.CoinAndMonsterPre(), Predicate.RestPre()]
    controller = RelationalQ.RelationalQ(0.1, 0.2, 0.9, actionList, preList)
    

    #trainEpisodeList = [0, 50, 100, 150]
    trainEpisodeList = [200]
    for trainEpisode in trainEpisodeList:
        for trainingStage in range(1, 5): #don't run 2-order in the training stage
            print "stage: ", trainingStage 

            numOfTurtle = 0
            numOfCoin = 0

            if trainingStage == 2:
                numOfTurtle = 1
            elif trainingStage == 3:
                numOfCoin = 1
            elif trainingStage == 4:
                numOfCoin = 1
                numOfTurtle = 1
            isEpisodeEnd = trainingStage > 2

            reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, (numOfTurtle, numOfCoin), trainEpisode, isEpisodeEnd)
            #DumpRRL(controller)
            #raw_input("Press Enter to continue...")
        Save(controller, 'RRL_complex_controller_train_'+str(trainEpisode)+'.txt')

        #DumpRRL(controller)
        trainingStage = 5

        isEpisodeEnd = True
        reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, (2, 5), maxEpisode, isEpisodeEnd)
        SaveToCSV(reward, 'RRL_complex'+str(trainEpisode)+'.csv')
        Save(controller, 'RRL_complex_controller_'+str(trainEpisode)+'.txt')
        #DumpRRL(controller)
        #Save(controller, 'RRL_controller'+str(trainEpisode)+'.txt')

        
def SaveToCSV(list, filename):
    FILE = open(filename,"w")
    for index in list:
        FILE.write(str(list[index]))
        FILE.write(', ')
    FILE.close()
def train(maxEpisode, type):
    isTraining = True

    size = 800, 800
    discrete_size = 8
    gridSize = (discrete_size, discrete_size)
    delay = 100
    interval = 50
    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(size)


    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))
    env = Grid((discrete_size, discrete_size), size, actionList)
    maxStep = 200

    numOfTurtle = 0
    numOfCoin = 0
    #trainingStage = 3

    if type == 'RRL':
      
        preList = [Predicate.MarioPre(), Predicate.MonsterPre(), Predicate.CoinPre(), Predicate.CoinAndMonsterPre()]
        controller = RelationalQ.RelationalQ(0.1, 0.2, 0.9, actionList, preList)
    elif type == 'SARSA':
        controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    else:
        assert(0)

    for trainingStage in range(1, 4): #don't run 2-order in the training stage
        print "stage: ", trainingStage 

        numOfTurtle = 0
        numOfCoin = 0

        if type == 'RRL':
            if trainingStage == 2:
                numOfTurtle = 1
            elif trainingStage == 3:
                numOfCoin = 1
            elif trainingStage == 4:
                numOfCoin = 1
                numOfTurtle = 1
        else:
            numOfTurtle = 1
            numOfCoin = 1

        count = 0
        #while 1:
        for i in range(0, maxEpisode):
            world = env.start(numOfTurtle, numOfCoin)
            if type == 'RRL':
                objLoc = getObjLoc(world, gridSize)
                marioLoc = getMarioLoc(world, gridSize)
                ob = (marioLoc, objLoc)
                action = controller.start(ob)
            elif type == 'SARSA':
                action = controller.start(env.getSarsaFeature())
            count += 1
            #if count % 40 == 0:
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
                #print "coin and monster------------------"
                #for y in range(0, 3):
                    #for x in range(0, 3):
                        #for action in actionList:
                            #controller.agent[4].touch(((x, y), (1, 0)), action)
                            #print (x, y), " ", action, " ", controller.agent[4].Q[(((x, y), (1, 0)), action)]
            for j in range(0, maxStep):
                clock.tick(1000)
                reward, world, flag = env.step(action, isTraining)
                if flag:
                    controller.end(reward, trainingStage)
                    break
                if type == 'RRL':
                    objLoc = getObjLoc(world, gridSize)
                    marioLoc = getMarioLoc(world, gridSize)
                    ob = (marioLoc, objLoc)
                    action = controller.step(reward, ob, trainingStage)
                elif type == 'SARSA':
                    action = controller.step(reward, env.getSarsaFeature(), trainingStage)

                for event in pygame.event.get():
                   #action = 0
                   if event.type == pygame.QUIT: sys.exit()
                #screen.blit(env.getScreen(), (0, 0))
                #pygame.display.flip()
    #Save(controller)
    return controller
if __name__ == "__main__":
    #reward = Load('convergence.txt')
    #SaveToCSV(reward, 'conv.csv')
    SmallWorldTest()
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
