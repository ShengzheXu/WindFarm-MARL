from Simulator import WindGym


# todo read exp runner setting from config file
episode = 100
simTime = 100

simm = WindGym()

# todo implement model a list of DQN for each turbine
models = [DQN()]


for eps in range(0, episode):
    simm.__init__()
    for timeI in range(0, simTime):
        state = simm.makeState()
        GatGraph = [] # list from topo-sort or GAT
        for turbine in GatGraph:
            model = models.get(turbine)
            action = model.forward(state)
            simm.getReward(action)

