class ExpCell(object):
    def __init__(self, s, a, r):
        self.s = s
        self.a = a
        self.r = r
        self.s_ = None
        return

    def add(self, s_):
        self.s_ = s_


class RewardPool(object):
    def __init__(self):
        self.exps = []

    def addExp(self, exp):
        self.exps.append(exp)

    def getExps(self):
        return self.exps


class RewardWrapper(object):
    def __init__(self):
        # todo make the list to dict so that the ID can be characteristic
        self.expPools = []

    def makeExpPools(self, agentNum):
        self.__init__()
        for i in range(agentNum):
            nextRewardPool = RewardPool()
            self.expPools.append(nextRewardPool)