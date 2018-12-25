from sim.generator import FlorisWrapper
import numpy as np

class WindGym(object):

    def __init__(self, turbineNum, greedy=None):
        self.readTurbineMap()
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

    def readTurbineMap(self):
        # TODO: read from csv

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

    def buildActionSpace(self, greedy=None):
        self.yaw_range5 = np.array([-30, -20, -10, -5, -1, 0, 1, 5, 10, 20, 30])

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
        self.yaws = np.array([
            self.yaw_range5[self.currentAngle[0]],
            self.yaw_range5[self.currentAngle[1]],
            self.yaw_range5[self.currentAngle[2]],
            self.yaw_range5[self.currentAngle[3]],
            self.yaw_range5[self.currentAngle[4]],
            self.yaw_range5[self.currentAngle[5]],
            self.yaw_range5[self.currentAngle[6]],
            0,
            0,
            0,
            0
        ])
        # self.yaws = np.array([
        #     self.yaw_range1[self.currentAngle[0]],
        #     0,
        #     self.yaw_range1[self.currentAngle[2]],
        #     30,
        #     self.yaw_range1[self.currentAngle[4]],
        #     -30,
        #     self.yaw_range1[self.currentAngle[6]],
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
        partialRange = self.getRange(turbineId)
        # print turbineId, partialRange
        for i in partialRange:
            influenceYaws[i] = 0

        q = np.copy(self.simulator.run(influenceYaws))
        influenceYaws[turbineId] = 0
        q_ = np.copy(self.simulator.run(influenceYaws))

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

        # todo make log here
        # print turbineId, "penaltyaward", penalty, award, "from", partialRange

        partialReward = award - penalty
        # return sum(pp.tolist())
        return partialReward

    def makeState(self, turbineId):
        # print("direction:", self.simulator.floris.floris_power_0.yaw)  #velocitiesTurbines_directions)
        stateRst = []
        # 2+4+4*5 = 27

        # 2 features for main wind info [direction, speed]
        stateRst.append(self.simulator.wind_angle)
        stateRst.append(self.simulator.wind_speed)

        # 4 features for this turbine info [cur_yaw, speed, wind_frame_x, wind_frame_y]
        stateRst.append(self.yaws[turbineId])
        stateRst.append(self.simulator.floris.floris_power_0.velocitiesTurbines[turbineId])
        stateRst.append(self.turbineXw[turbineId])
        stateRst.append(self.turbineYw[turbineId])

        effRange = self.getRange(turbineId)
        for i in effRange:
            stateRst.append(self.yaws[i])
            stateRst.append(self.simulator.floris.floris_power_0.velocitiesTurbines[i])
            stateRst.append(self.turbineXw[i])
            stateRst.append(self.turbineYw[i])

        while len(stateRst) < 27:
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

    def getRange(self, turbinId):
        label = -1
        rstList = []
        for i in self.indexOrder:
            if turbinId == i:
                label = 0
            if label != -1:
                if self.turbineXw[i] <= self.turbineXw[turbinId]:
                    continue
                if (self.turbineXw[i] - self.turbineXw[turbinId]) < abs(self.turbineYw[i] - self.turbineYw[turbinId]):
                    continue
                rstList.append(i)
                label += 1
        # print "range", rstList
        return rstList