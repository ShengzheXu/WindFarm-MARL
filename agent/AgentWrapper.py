from RandomAgent import RandomAgent
from GreedyAgent import GreedyAgent
from DqnAgent import DqnAgent
import tensorflow as tf

class AgentWrapper(object):
    def __init__(self):
        self.models = []

    def makeAgents(self, agentNum, actionNum, type, shareModel=False):
        self.__init__()
        self.agentNum = agentNum
        self.shareModel = shareModel
        if type == 'dqn':
            self.sess = tf.Session()
        for i in range(agentNum):
            if (type == 'random'):
                nextAgent = RandomAgent(actionNum)
            elif (type == 'dqn'):
                nextAgent = DqnAgent(i, self.sess)
            else: # greedy
                nextAgent = GreedyAgent(actionNum)
            self.models.append(nextAgent)
        if type == 'dqn':
            self.sess.run(tf.global_variables_initializer())

    def doForward(self, agentId, state):
        if self.shareModel is True:
            agentId = 0
        action = self.models[agentId].doForward(state)
        return action

    def doBackward(self, agentId, exp):
        if self.shareModel is True:
            agentId = 0
        self.models[agentId].doBackward(exp)

    def getLoss(self, agentId):
        if self.shareModel is True:
            agentId = 0
        return self.models[agentId].getLoss()

    def decayExploreRate(self):
        for i in range(self.agentNum):
            self.models[i].agent.decayExploreRate()
