import csv
import numpy as np

class PreTrainMachine(object):
    def __init__(self, sLen):
        self.sLen = sLen
        pass

    def transferExp(self, agentExperience):
        # file = 'result/30turbines_correctloss_30_220.log'
        file = 'result/wind_log.log'
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                # print row, len(row)
                turbId = int(row[0])
                # get s from 1 to 1+sLen
                s = []
                for i in range(self.sLen):
                    s.append(float(row[1+i]))
                # get a from 1+sLen
                a = int(float(row[1+self.sLen]))
                r = float(row[1+self.sLen+1])

                agentExperience.add(turbId, s, a, r)