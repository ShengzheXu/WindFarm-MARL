import logging
import numpy as np

class Experience(object):
    def __init__(self, agentNum):
        self.exp = []
        self.agentNum = agentNum
        for i in range(agentNum):
            nextExp = []
            self.exp.append(nextExp)
        logging.basicConfig(filename='exp_logger.log', level=logging.INFO)

    def add(self, turbineId, s, a, r):
        item = (s, a, r)
        self.exp[turbineId].append(item)

    def sup(self, turbineId, s_):
        if len(self.exp[turbineId]) > 0:
            item = self.exp[turbineId][-1]
            # print item
            (s, a, r) = item
            item_ = np.hstack((s, [a, r], s_))
            # item_ = (s, [a, r], s_)

            # print "logging"
            logger = logging.getLogger("wind_logger")
            logstr = str(turbineId)+ ":" + str(item_)
            # logger.critical(str(item_))
            logger.critical(logstr)
            self.exp[turbineId][-1] = item_

    def get(self, turbineId):
        aExp = self.exp[turbineId]
        if len(aExp[-1]) < 4:
            aExp = aExp[:-1]
        return aExp

    def expLen(self, turbinId):
        return len(self.exp[turbinId])

    # todo: add memory size upper bound. It's ok now since number of Exp not large.
    def sampleBatch(self, turbineId, batch_size):
        aExp = self.get(turbineId)
        memory = np.array(aExp)
        memory_counter = len(aExp)
        sample_index = np.random.choice(memory_counter, size=batch_size)
        batch_memory = memory[sample_index, :]
        return batch_memory

    def allSampleBatch(self, batch_size):
        each_size = batch_size/self.agentNum
        allBatchMemory = self.sampleBatch(0, each_size + batch_size%self.agentNum)
        for i in range(1, self.agentNum):
            allBatchMemory = np.concatenate((allBatchMemory, self.sampleBatch(i, each_size)), axis=0)
        return allBatchMemory
