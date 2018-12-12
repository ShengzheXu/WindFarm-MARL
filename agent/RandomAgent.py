from AbstractAgent import AbstractAgent
import random


class RandomAgent(AbstractAgent):
    def __init__(self):
        pass

    def doForward(self, state):
        # generate action from 0 to 360 degree
        actionDegree = random.randint(0,361)
        return actionDegree