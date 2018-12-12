from RandomAgent import RandomAgent

class AgentWrapper(object):
    def __init__(self):
        self.models = []

    def makeAgents(self, agentNum, type):
        self.__init__()
        for i in range(agentNum):
            # if (type == 'random'):
            nextAgent = RandomAgent()
            self.models.append(nextAgent)

    def doForward(self, agentId, state):
        action = self.models[agentId].doForward(state)
        return action
