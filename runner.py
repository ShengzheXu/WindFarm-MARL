from Simulator import WindGym
from agent.AgentWrapper import AgentWrapper
from support.GraphComputation import GraphComputation
from support.RewardComputation import RewardWrapper

# todo read exp runner setting from config file
episode = 10
simTime = 10
turbineNum = 11

simm = WindGym(turbineNum=turbineNum)

agentWrapper = AgentWrapper()
agentWrapper.makeAgents(agentNum=turbineNum, type="random")

# how to make these names?
graphComputer = GraphComputation()
rewardComputer = RewardWrapper()
rewardComputer.makeExpPools(agentNum=turbineNum)


for eps in range(0, episode):
    simm.reset()
    for timeI in range(0, simTime):
        simm.step()

        # Q: where is the filter for state, in simulator or in AgentWrapper?
        # A: query to the simmulator
        # state = simm.makeState()

        # envInfo includes wind and turbine position
        envInfo = simm.makeEnvInfo()

        # a turbine list in a generated by wind-topo order
        instantTopoGraph = graphComputer.getTopoGraph(envInfo)

        for turbineId in instantTopoGraph:
            state = simm.makeState(turbineId)
            action = agentWrapper.doForward(turbineId, state)
            # Q: where to build reward and s'?
            # A: the S_ is the S next time
            reward = simm.miniStep(turbineId, action)
            # state_ = simm.makeState()
            # rewardComputer.store(turbineId, state, action, reward, state_)


