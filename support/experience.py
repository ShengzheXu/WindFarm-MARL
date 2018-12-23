class Experience(object):
    def __init__(self, agentNum):
        self.exp = []
        for i in range(agentNum):
            nextExp = []
            self.exp.append(nextExp)

    def add(self, turbineId, s, a, r):
        item = (s, a, r)
        self.exp[turbineId].append(item)

    def sup(self, turbineId, s_):
        if len(self.exp[turbineId]) > 0:
            item = self.exp[turbineId][-1]
            (s, a, r) = item
            item_ = (s, a, r, s_)
            self.exp[turbineId][-1] = item_

    def get(self, turbineId):
        aExp = self.exp[turbineId]
        if len(aExp[-1]) < 4:
            aExp.pop()
        return aExp