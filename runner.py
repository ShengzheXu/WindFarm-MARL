from Simulator import WindGym
from agent.AgentWrapper import AgentWrapper
from support.GraphComputation import GraphComputation
from support.RewardComputation import RewardWrapper
from datetime import datetime
import logging

# todo read exp runner setting from config file
from support.Experience import Experience

episode = 220 #350
# the data we're going to use is hourly
simTime = 30 # 2 * 24
turbineNum = 30
actionNum = 31
batchSize = 128

# modelType = "random"
# modelType = "greedy"
modelType = "dqn"
shareModel = True

# simm = WindGym(turbineNum=turbineNum)
simm = WindGym(turbineNum=turbineNum, csvRead="csv")
# simm = WindGym(turbineNum=turbineNum, greedy="greedy")

agentWrapper = AgentWrapper()
# agentWrapper.makeAgents(agentNum=turbineNum, type="random")
agentWrapper.makeAgents(agentNum=turbineNum, actionNum=actionNum, type=modelType, shareModel=shareModel)
# agentWrapper.makeAgents(agentNum=turbineNum, type="dqn")
agentExperience = Experience(turbineNum)

# how to make these names?
graphComputer = GraphComputation()
rewardComputer = RewardWrapper()
rewardComputer.makeExpPools(agentNum=turbineNum)


def createLogger():
    # create logger
    logger_name = "wind_logger"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)

    # create file handler
    log_path = "./wind_log.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARN)

    # create formatter
    # fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d ::: %(message)s"
    fmt = "%(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def runner():
    starttime = datetime.now()
    # miniaction = [0, 0,0,0,0,0,0,0,0,0,0]
    simm.getTurbineWYw()
    simm.miniStep(0, 0)
    plotPw = []
    rewardPlot = {-1:[]}
    for i in range(turbineNum):
        rewardPlot[i] = []

    for eps in range(0, episode):
        epstime1 = datetime.now()
        epspw = 0
        epscount = 0
        epsReward = {-1:0}
        for i in range(turbineNum):
            epsReward[i] = 0

        for timeI in range(0, simTime):
            simm.step()

            # Q: where is the filter for state, in simulator or in AgentWrapper?
            # A: query to the simmulator
            # state = simm.makeState()

            # envInfo includes wind and turbine position
            envInfo = simm.makeEnvInfo()

            # a turbine list in a generated by wind-topo order
            # instantTopoGraph = graphComputer.getTopoGraph(envInfo)
            instantTopoGraph = simm.getTurbineWYw()
            # print "instanttopo", instantTopoGraph
            # simm.getTurbineWYw()

            for turbineId in instantTopoGraph:
                state = simm.makeState(turbineId)
                action = agentWrapper.doForward(turbineId, state)
                # Q: where to build reward and s'?
                # A: the S_ is the S next time
                reward = simm.miniStep(turbineId, action)
                epsReward[turbineId] += reward
                epscount += 1.0
                agentExperience.sup(turbineId, state)
                agentExperience.add(turbineId, state, action, reward)
                # state_ = simm.makeState()
                # rewardComputer.store(turbineId, state, action, reward, state_)

        for i in range(turbineNum):
            rewardPlot[i].append(epsReward[i])

        print "eps", eps, ":", simm.epsTotalPower / epscount,
        if modelType == "dqn":
            print "with explore rate:", 1-agentWrapper.models[0].agent.epsilon,
        plotPw.append(simm.epsTotalPower/epscount)
        simm.reset()
        if shareModel is True:
            # superExp = []
            # for i in range(turbineNum):
            #     exp = agentExperience.get(i)
            #     superExp.extend(exp)
            totalExpNum = agentExperience.expLen(0) * turbineNum
            print "learn plans", totalExpNum, batchSize, totalExpNum/batchSize
            for i in range(totalExpNum/batchSize):
                superExp = agentExperience.allSampleBatch(batchSize)
                agentWrapper.doBackward(0, superExp)
                print "loss:", agentWrapper.getLoss(0),
            agentWrapper.decayExploreRate()
        else:
            for i in range(turbineNum):
                exp = agentExperience.get(i)
                agentWrapper.doBackward(i, exp)
                print "loss:", agentWrapper.getLoss(i)

        epstime2 = datetime.now()
        print ", time:", (epstime2-epstime1).seconds

    endtime = datetime.now()


    print('total time', (endtime-starttime).seconds)
    for i in range(turbineNum):
        print i, ":", rewardPlot[i]
    # print(rewardPlot)
    # print(simm.epsTotalPowerRecord)
    # print(sum(simm.epsTotalPowerRecord)/len(simm.epsTotalPowerRecord))
    # print(simm.epsEachCount)
    # print plotPw

if __name__ == "__main__":
    createLogger()
    runner()
    # import profile
    # profile.run("runner()", "prof.txt")
    # import pstats
    # p = pstats.Stats("prof.txt")
    # p.sort_stats("cumtime").print_stats()