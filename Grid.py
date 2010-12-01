import sys,pygame
import copy #for copy objects
import RelationalQ
import SARSA
import Predicate
import GridEnv
import random
import csv #for csv output

         

def Save(agent, filename): 
    import pickle
    output = open(filename, 'wb')
    pickle.dump(agent, output)
    output.close()

def Load(filename):
    import pickle
    input = open(filename, 'rb')
    return pickle.load(input)

def TestRun(controller, type, discrete_size, monsterMoveProb, objSet, maxStep):
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

    isTraining = False
    isUpdate = True

    numOfTurtle = objSet[0]
    numOfCoin = objSet[1]

    print "# coin ", numOfCoin
    print "# Turtle ", numOfTurtle

    count = 0
    
    totalReward = 0
    rewardList = []
    obList = []
    totalStep = 0

    while True:
        if totalStep > maxStep:
            break
        #print totalReward

        world = env.start(numOfTurtle, numOfCoin)
        objLoc = getObjLoc(world, gridSize)
        marioLoc = getMarioLoc(world, gridSize)
        ob = (marioLoc, objLoc)
        if type == 'SARSA':
            ob = Predicate.getSarsaFeature(ob)

        action = controller.start(ob)

        count += 1
        while True:
            if totalStep > maxStep:
                break
                
            totalStep += 1
            clock.tick(5000)

            reward, world, flag = env.step(action, isTraining)
            ob = list(ob)
            ob.append(action)
            obList.append(ob)
            rewardList.append(reward)
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

            if type == 'SARSA':
                ob = Predicate.getSarsaFeature(ob)

            if type == 'RRL':
                action = controller.step(reward, ob, trainingStage)
            elif type == 'SARSA':
                action = controller.step(reward, ob, isUpdate)
            else:
                assert False

            for event in pygame.event.get():
               if event.type == pygame.QUIT: sys.exit()

            #screen.blit(env.getScreen(), (0, 0))
            #pygame.display.flip()
    #print totalReward
    return rewardList, obList

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
def GetSample():
    discrete_size = 8
    monsterMoveProb = 0.3
    isUpdate = True

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))
    controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    reward, controller = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, isUpdate, 4, (1,1), maxEpisode, True)
    
def SmallWorldTest(agentConf, maxTrainEpisode, maxTestEpisode):

    discrete_size = 8
    monsterMoveProb = 0.3
    isUpdate = True

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))

    #controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    #reward, controller = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, isUpdate, 4, (2,5), maxEpisode, True)
    #SaveToCSV(reward, 'SarsaComp.csv')
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
        Save(controller, 'RRL_controller_train_'+str(trainEpisode)+ '_'+str(lastConf)+'_'+str(len(agentConf)) + '.txt')
        #DumpRRL(controller)
        trainingStage = trainingStage + 1

    #DumpRRL(controller)
    #raw_input("Press Enter to continue...")

    #DumpRRL(controller)

    isEpisodeEnd = True
    reward, controller = TestRun(controller, 'RRL', discrete_size, monsterMoveProb, isUpdate, trainingStage, (2, 5), maxTestEpisode, isEpisodeEnd)
    SaveToCSV(reward, 'RRL_test_'+str(trainEpisode)+'_'+str(lastConf)+'_'+str(len(agentConf))+'.csv')
    #Save(controller, 'RRL_test_controller_'+str(trainEpisode)+'_'+str(lastConf)+'_'+str(len(agentConf))+'.txt')

def ToBinary(num, len):
    digitList = []
    for i in range(0, len-1):
        digitList.append('0')
    if num >= 0:
        digitList[num] = '1'
    #else:
        #digitList[len -num -1] = '1'
    return digitList
    #resStr = ''
    #for digit in digitList:
        #resStr += digit
    #return resStr

        
def SaveToCSV(list, filename):
    FILE = open(filename,"w")
    for index in list:
        FILE.write(str(index))
        FILE.write(', ')
    FILE.close()
def SaveMatToCSV(mat, filename):
    writer = csv.writer(open(filename, "w"))
    for row in mat:
        res = []
        for cell in row:
            for num in cell:
                res = res + ToBinary(num, 8)
        writer.writerow(res)
    
def SaveNumberToCSV(mat, filename, lenList):
    writer = csv.writer(open(filename, "w"))
    for row in mat:
        res = []
        index = 0
        for num in row:
            maxLen =lenList[index]  
            #print "max: ", maxLen
            #print num
            assert maxLen > num
            res = res + ToBinary(num, maxLen)
            index = index + 1
        writer.writerow(res)
def GenData(filename):
    writer = csv.writer(open(filename, "w"))
    size = 4
    for i in range(1, 10000):
        res = []
        len = size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)
        len = size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)
        len = size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)
        len = size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)

        len = size*size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)
        len = size*size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)

        len = size*size*size*size
        digit = random.random()*len
        res = res + ToBinary(int(digit), len)

        #len = 256*16
        #digit = random.random()*len
        #res = res + ToBinary(int(digit), len)

        #len = 64*64
        #digit = random.random()*len
        #res = res + ToBinary(int(digit), len)
        writer.writerow(res)
def TupleToNumber(tuple, lenList):
    number = 0
    index = 0
    for val in tuple:
        number = val + number*lenList[index]
        #else:
            #number = val
        index = index + 1
    return number
def ExtractFeature(feature, gridSize):
    res = []
    #gridSize = 4
    offset = gridSize - 1
    gridLenSize = 2*gridSize
    actionSize = 2
    actionLenSize = 2*actionSize
    actionOff = actionSize - 1
    for row in feature:
        newFea = []
        newFea.append(row[1])
        newFea.append(row[2])
        newFea.append(row[3])

        monFeature = (newFea[0][0] + offset, newFea[0][1] + offset, newFea[2][0] + actionOff, newFea[2][1] + actionOff);
        coinFeature = (newFea[1][0] + offset, newFea[1][1] + offset, newFea[2][0] + actionOff, newFea[2][1] + actionOff);
        secondOrder = (newFea[0][0] + offset, newFea[0][1] + offset, newFea[1][0] + offset, newFea[1][1] + offset, newFea[2][0] + actionOff, newFea[2][1] + actionOff);

        monNum = TupleToNumber(monFeature, [gridLenSize, gridLenSize, actionLenSize, actionLenSize])
        coinNum = TupleToNumber(coinFeature, [gridLenSize, gridLenSize, actionLenSize, actionLenSize])
        secondNum = TupleToNumber(secondOrder, [gridLenSize, gridLenSize, gridLenSize, gridLenSize, actionLenSize, actionLenSize])
        preTuple = [monFeature, coinFeature, secondOrder]
        #print preTuple
        #pre = [monNum, coinNum, secondNum]
        pre = [monNum, coinNum]
        res.append(pre)
    #for row 
    return res
if __name__ == "__main__":
    #GenData('obList.csv')
    #print TupleToNumber((7,7,3,3), [8,8,4,4])


    discrete_size = 8
    monsterMoveProb = 0.2
    isUpdate = True
    maxStep = 10000

    actionList = ((0, 1), (0, -1), (1, 0), (-1, 0))

    controller = SARSA.SARSA(0.1, 0.2, 0.9, actionList)
    reward, ob = TestRun(controller, 'SARSA', discrete_size, monsterMoveProb, (1,1), maxStep)
    #print ob
    ob = ExtractFeature(ob, discrete_size)
    maxSize = 2*discrete_size*2*discrete_size*4*4;
    #print reward
    #print ob

    SaveToCSV(reward, 'rewardList.csv')
    #SaveNumberToCSV(ob, 'obList.csv', [8*8*4*4, 8*8*4*4, 8*8*8*8*4*4])
    SaveNumberToCSV(ob, 'obList.csv', [maxSize, maxSize])

    #reward = Load('convergence.txt')
    #SaveToCSV(reward, 'conv.csv')

    #trainEpisodeList = [10000]
    #testEpisode = 20000
    #agentList =                      \
    #[                                \
    ##[(0, 1)],                        \
    ##[(0, 2)],                        \
    ##[(0, 3)],                        \
    ##[(0, 1), (0, 2)],                \
    ##[(1, 0), (0, 1), (1, 1)],                 \
    ##[(1, 0), (0, 1), (1, 1), (0, 2), (1, 2)], \
    ##[(0, 1), (0, 2), (0, 3)],        \
    ##[(0, 1), (0, 2), (0, 3), (0, 4)],\
    ##[(1, 0)],                        \
    ##[(1, 0), (0, 1), (1, 1), (2, 0), (2, 1)], \
    ##[(1, 0), (2, 0)],                \
    #[(2, 0)],                        \
    #[(1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1), (1, 2), (2, 2)], \
    ##[(3, 0)],                        \
    ##[(1, 0), (2, 0), (3, 0)],        \
    ##[(1, 0), (2, 0), (3, 0), (4, 0)]\
    #]
    #for trainEpisode in trainEpisodeList:
        #for agentConf in agentList:
            #SmallWorldTest(agentConf, trainEpisode, testEpisode)
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
