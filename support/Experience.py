import logging
import numpy as np

class Experience(object):
    def __init__(self, agentNum, memorysize=50000):
        self.exp = []
        self.temp = []
        self.memCount = []
        self.agentNum = agentNum
        self.memorysize = memorysize
        for i in range(agentNum):
            nextExp = []
            nextTemp = None
            self.exp.append(nextExp)
            self.temp.append(nextTemp)
            self.memCount.append(0)
        logging.basicConfig(filename='exp_logger.log', level=logging.INFO)

        logger = logging.getLogger("wind_logger")
        headerstr = "turbinId,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,action,reward,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,s_,split,power,totalreward,award,penalty"
        logger.critical(headerstr)

    def add(self, turbineId, in_s, in_a, in_r, infoPackage=None):
        # print in_s
        # print len(in_s), in_a, in_r
        if self.temp[turbineId] is not None:
            # do sup
            item = self.temp[turbineId]
            (s, a, r) = item
            s_ = in_s
            item_ = np.hstack((s, [a, r], s_))
            # log_item_ = (s, [a, r], s_)

            # print "logging"
            logger = logging.getLogger("wind_logger")
            logstr = str(turbineId)
            for num in item_:
                logstr += "," + str(num)
            if infoPackage is not None:
                logstr += ",--," + ",".join(infoPackage)
            logger.critical(logstr)

            # store
            # print(item_[26])
            ith = self.memCount[turbineId]
            if ith < self.memorysize:
                self.exp[turbineId].append(item_)
            else:
                self.exp[turbineId][ith%self.memorysize]
            self.memCount[turbineId] += 1

        item = (in_s, in_a, in_r)
        self.temp[turbineId] = item

    def get(self, turbineId):
        return self.exp[turbineId]

    def expLen(self, turbinId):
        return len(self.exp[turbinId])

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
