from datetime import datetime

from sim.generator import FlorisWrapper
import numpy as np
import csv

class WindGym(object):

    def __init__(self, turbineNum, greedy=None, csvRead=None):
        self.readTurbineMap(csvRead)
        self.turbineNum = turbineNum
        self.simulator = FlorisWrapper(self.turbineGrid)
        self.simulator.floris.configure()
        self.buildActionSpace(greedy)
        self.episode = 0
        self.stepCnt = 0
        self.epsTotalPower = 0
        self.epsCount = 0
        self.epsTotalPowerRecord = []
        self.epsEachCount = 0

    def readTurbineMap(self, csvRead=None):
        # TODO: read from csv
        if csvRead is not None:
            file = 'data/mini30turbines.csv'
            min_xlong = 0x3f3f3f3f
            min_ylat = 0x3f3f3f3f
            loglat = []
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                        continue
                    # print row[22]
                    row_xlong = float(row[22])
                    row_ylat = float(row[23])
                    if row_xlong < min_xlong:
                        min_xlong = row_xlong
                    if row_ylat < min_ylat:
                        min_ylat = row_ylat
                    loglat.append((row_xlong, row_ylat))

                    if line_count == 0:
                        # print(f'Column names are {", ".join(row)}')
                        # line_count += 1
                        pass
                    else:
                        # print(f'\tx{row[22] and y{row[23]}')
                        # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                        line_count += 1
                # print(f'Processed {line_count} lines.')
            posList = []
            for gis in loglat:
                (row_xlong, row_ylat) = gis
                h_distance = (row_xlong-min_xlong) * 110
                v_distance = (row_ylat-min_ylat) * 85
                posList.append([h_distance, v_distance])
            self.turbineNum = line_count-1
            self.turbineGrid = 1000 * np.array(posList)
            # for item in self.turbineGrid:
            #     (x, y) = item
            #     print x, ",", y
            # print self.turbineGrid

        else:
            h_distance = 2
            v_distance = 0.75
            self.turbineNum = 7
            self.turbineGrid = 500 * np.array([[h_distance,  0],
                                           [0, 2*v_distance],
                                           [h_distance, 3*v_distance],
                                           [0, 5*v_distance],
                                           [h_distance, 6*v_distance],
                                           [0, 7*v_distance],
                                           [h_distance, 9*v_distance],
                                           [1+h_distance, 0],
                                           [1+h_distance, 3*v_distance],
                                           [1+h_distance, 6*v_distance],
                                           [1+h_distance, 9*v_distance]])
            for item in self.turbineGrid:
                (x, y) = item
                print x, ",", y
            # print self.turbineGrid

    def buildActionSpace(self, greedy=None):
        # self.yaw_range5 = np.array([-20, -10, -5, -1, 0, 1, 5, 10, 23, 27, 28])
        self.yaw_range6 = np.array([-30, -28, -26, -24, -22, -20, -18, -16, -14, -12,
                                    -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10,
                                    12, 14, 16, 18, 20, 22, 24, 26, 28, 30])

        # self.yaw_range1 = np.array([23, 27, 28])
        # self.yaw_range2 = np.array([-10, -6, -1])
        # self.yaw_range3 = np.array([-2, 1, 4])
        # self.yaw_range4 = np.array([0, 0, 0])
        if (greedy is not None):
            # best_yaws          = np.array([27, -1, 27, -1, 27,  1, 27,  0,  0,  0,  0])
            self.yaw_range1 = np.array([27])
            self.yaw_range2 = np.array([-1])
            self.yaw_range3 = np.array([1])
            self.yaw_range4 = np.array([0])


        self.currentAngle = []
        for i in range(0, self.turbineNum):
            self.currentAngle.append(5)
        self.makeAction()

    def makeAction(self):
        yawList = []
        for i in range(self.turbineNum):
            yawList.append(self.yaw_range6[self.currentAngle[i]])
        self.yaws = np.array(yawList)

        # self.yaws = np.array([
        #     self.yaw_range6[self.currentAngle[0]],
        #     self.yaw_range6[self.currentAngle[1]],
        #     self.yaw_range6[self.currentAngle[2]],
        #     self.yaw_range6[self.currentAngle[3]],
        #     self.yaw_range6[self.currentAngle[4]],
        #     self.yaw_range6[self.currentAngle[5]],
        #     self.yaw_range6[self.currentAngle[6]],
        #     0,
        #     0,
        #     0,
        #     0
        # ])


    def reset(self):
        self.stepCnt = 0
        self.episode += 1
        self.epsTotalPowerRecord.append(self.epsTotalPower)
        self.epsTotalPower = 0
        self.epsEachCount = self.epsCount
        self.epsCount = 0
        return

    def step(self):
        # TODO: read from csv
        self.stepCnt += 1
        self.simulator.randomizeWind()
        # print(self.episode, self.stepCnt, self.simulator.floris.windrose_speeds)

    def miniStep(self, turbineId, action):
        # todo modify the angle based on the action space
        self.currentAngle[turbineId] = action
        self.makeAction()
        # print(self.yaws)

        # set downsteam turbines to be greedy
        influenceYaws = np.copy(self.yaws)
        partialRange = self.getDownStream(turbineId)
        # print turbineId, partialRange
        for i in partialRange:
            influenceYaws[i] = 0

        activeList = []
        activeList.append(turbineId)
        for i in partialRange:
            activeList.append(i)
        upStream = self.getUpStream(turbineId)
        for i in upStream:
            activeList.append(i)
        # print turbineId, "up:", upStream, "down:", partialRange, "active:", activeList
        from sim.ActiveTurbines import ActiveTurbines
        activeTurbIo = ActiveTurbines()
        activeTurbIo.writeActiveList(activeList)

        simutime1 = datetime.now()
        q = np.copy(self.simulator.run(influenceYaws))
        simutime2 = datetime.now()
        influenceYaws[turbineId] = 0
        q_ = np.copy(self.simulator.run(influenceYaws))
        simutime3 = datetime.now()
        # print "1st simu", (simutime2-simutime1).seconds, "2nd simu", (simutime3-simutime2).seconds

        # print(self.simulator.floris.ws_array_0)
        # print(self.simulator.floris.floris_windframe_0.turbineX)
        # print(self.simulator.floris.velocitiesTurbines_directions)
        # print(self.simulator.floris.floris_power_0.velocitiesTurbines)
        # [nDirections, nTurbines]
        # self.velocitiesTurbines_directions = self.simulator.floris.velocitiesTurbines_directions
        # [nDirections, nTurbines]
        # self.wt_power_directions = self.simulator.floris.wt_power_directions
        # [nDirections]
        # self.power_directions = self.simulator.floris.power_directions

        # pp = np.copy(q[0:7])
        # pp[0] += q[7]
        # pp[2] += q[8]
        # pp[4] += q[9]
        # pp[6] += q[10]
        # print(self.episode, self.stepCnt, turbineId, action, sum(pp.tolist()), pp.tolist())
        # print("power of 135: ", pp[1], pp[3], pp[5])
        self.epsTotalPower += sum(q.tolist())
        # self.epsTotalPower += pp[1] + pp[3] + pp[5]
        self.epsCount += 1

        penalty = q[turbineId] - q_[turbineId]
        award = 0
        for i in partialRange:
            award += q[i] - q_[i]

        partialReward = award + penalty

        # todo make log here
        import logging
        logger = logging.getLogger("wind_logger")
        logstr = str(turbineId)+" action "+str(action)+" penaltyaward "+str(partialReward)+" ("+str(penalty)+" + "\
                 + str(award)+") from "+ str(partialRange)
        logger.info(logstr)
        # print turbineId, "action", action, "penaltyaward", partialReward, penalty, award, "from", partialRange


        # return sum(pp.tolist())
        return partialReward

    def makeState(self, turbineId):
        # print("direction:", self.simulator.floris.floris_power_0.yaw)  #velocitiesTurbines_directions)
        stateRst = []
        # 2+4+4*5 = 26

        # 2 features for main wind info [direction, speed]
        stateRst.append(self.simulator.wind_angle)
        stateRst.append(self.simulator.wind_speed)

        # 4 features for this turbine info [cur_yaw, speed, wind_frame_x, wind_frame_y]
        stateRst.append(self.yaws[turbineId])
        stateRst.append(self.simulator.floris.floris_power_0.velocitiesTurbines[turbineId])
        stateRst.append(self.turbineXw[turbineId])
        stateRst.append(self.turbineYw[turbineId])

        effRange = self.getDownStream(turbineId)
        count = 0
        for i in effRange:
            stateRst.append(self.yaws[i])
            stateRst.append(self.simulator.floris.floris_power_0.velocitiesTurbines[i])
            stateRst.append(self.turbineXw[i])
            stateRst.append(self.turbineYw[i])
            count += 1
            if count >= 5:
                break

        while len(stateRst) < 26:
            stateRst.append(0)
        # for j in range(len(effRange), 5):
        #     for kk in range(5):
        #         stateRst.append(0)
        # print "state", stateRst
        return stateRst


    def makeEnvInfo(self):
        return []

    def getTurbineWYw(self):
        xw = self.simulator.floris.floris_windframe_0.turbineXw
        yw = self.simulator.floris.floris_windframe_0.turbineYw
        xorder = sorted(xw)
        hashed_index = {}
        index_order = []
        for i in xorder:
            for j in range(len(xw)):
                if xw[j] != i:
                    continue
                if hashed_index.has_key(j):
                    continue
                hashed_index[j] = 1
                index_order.append(j)
        self.indexOrder = index_order
        self.turbineXw = xw
        self.turbineYw = yw
        # print index_order
        return index_order

    def getUpStream(self, turbineId):
        rstList = []
        for i in self.indexOrder:
            # selected by a rectangle, in the range of 1000m for y_up and y_down
            if abs(self.turbineYw[i] - self.turbineYw[turbineId]) > 1000:
                continue

            if self.turbineXw[i] >= self.turbineXw[turbineId]:
                continue
            # selected by a sector
            # if (self.turbineXw[i] - self.turbineXw[turbinId]) < abs(self.turbineYw[i] - self.turbineYw[turbinId]):
            #     continue

            rstList.append(i)

        # print turbinId, "range", rstList
        return rstList

    def getDownStream(self, turbineId):
        label = -1
        rstList = []
        for i in self.indexOrder:
            if turbineId == i:
                label = 0
            if label != -1:
                # selected by a rectangle, in the range of 1000m for y_up and y_down
                if abs(self.turbineYw[i] - self.turbineYw[turbineId]) > 1000:
                    continue

                if self.turbineXw[i] <= self.turbineXw[turbineId]:
                    continue
                # selected by a sector
                # if (self.turbineXw[i] - self.turbineXw[turbinId]) < abs(self.turbineYw[i] - self.turbineYw[turbinId]):
                #     continue

                rstList.append(i)
                label += 1
        # print turbinId, "range", rstList
        return rstList