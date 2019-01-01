from AbstractAgent import AbstractAgent
import random


class RandomAgent(AbstractAgent):
    def __init__(self):
        pass

    def doForward(self, state):
        # generate action from 0 to 360 degree
        # action space is 0, 1, 2
        # actionDegree = random.randint(0, 2)
        # action space is 0 - 10
        actionDegree = random.randint(0, 10)
        # print(actionDegree)
        return actionDegree
