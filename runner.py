from Simulator import WindGym
from agent.AgentWrapper import AgentWrapper
from support.GraphComputation import GraphComputation
from support.RewardComputation import RewardWrapper
from datetime import datetime

# todo read exp runner setting from config file
from support.Experience import Experience

episode = 10 * 5 * 6
# the data we're going to use is hourly
simTime = 5 * 24
turbineNum = 11

simm = WindGym(turbineNum=turbineNum)
# simm = WindGym(turbineNum=turbineNum, greedy="greedy")

agentWrapper = AgentWrapper()
# agentWrapper.makeAgents(agentNum=turbineNum, type="random")
# agentWrapper.makeAgents(agentNum=turbineNum, type="greedy")
agentWrapper.makeAgents(agentNum=turbineNum, type="dqn")
agentExperience = Experience(turbineNum)

# how to make these names?
graphComputer = GraphComputation()
rewardComputer = RewardWrapper()
rewardComputer.makeExpPools(agentNum=turbineNum)

starttime = datetime.now()
# miniaction = [0, 0,0,0,0,0,0,0,0,0,0]
simm.getTurbineWYw()
simm.miniStep(0, 0)


for eps in range(0, episode):
    epspw = 0
    epscount = 0
    for timeI in range(0, simTime):
        simm.step()

        # Q: where is the filter for state, in simulator or in AgentWrapper?
        # A: query to the simmulator
        # state = simm.makeState()

        # envInfo includes wind and turbine position
        envInfo = simm.makeEnvInfo()

        # a turbine list in a generated by wind-topo order
        instantTopoGraph = graphComputer.getTopoGraph(envInfo)
        simm.getTurbineWYw()

        for turbineId in instantTopoGraph:
            state = simm.makeState(turbineId)
            action = agentWrapper.doForward(turbineId, state)
            # Q: where to build reward and s'?
            # A: the S_ is the S next time
            reward = simm.miniStep(turbineId, action)
            epspw += reward
            epscount += 1.0
            agentExperience.sup(turbineId, state)
            agentExperience.add(turbineId, state, action, reward)
            # state_ = simm.makeState()
            # rewardComputer.store(turbineId, state, action, reward, state_)

    print "eps", eps, ":", simm.epsTotalPower/epscount
    simm.reset()
    for i in range(turbineNum):
        exp = agentExperience.get(i)
        agentWrapper.doBackward(i, exp)

endtime = datetime.now()


print('total time', (endtime-starttime).seconds)
print(simm.epsTotalPowerRecord)
print(sum(simm.epsTotalPowerRecord)/len(simm.epsTotalPowerRecord))
print(simm.epsEachCount)
