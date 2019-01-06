from AbstractAgent import AbstractAgent
import random


class GreedyAgent(AbstractAgent):
    def __init__(self, actionNum):
        self.actionNum = actionNum
        pass

    def doForward(self, envInfo):
        # exp. 31 actions, [0-30], greedy: 15
        return self.actionNum/2
