from sim.generator import FlorisWrapper
import numpy as np

class WindGym(object):

    def __init__(self, turbineNum):
        self.readTurbineMap()
        self.turbineNum = turbineNum
        self.simulator = FlorisWrapper(self.turbineGrid)
        # self.simulator.floris.configure()
        self.buildActionSpace()
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

    def buildActionSpace(self):
        self.yaw_range1 = np.array([23, 27, 28])
        self.yaw_range2 = np.array([-10, -6, -1])
        self.yaw_range3 = np.array([-2, 1, 4])
        self.yaw_range4 = np.array([0, 0, 0])

        self.currentAngle = []
        for i in range(0, self.turbineNum):
            self.currentAngle.append(0)
        self.makeAction()

    def makeAction(self):
        self.yaws = np.array([
            self.yaw_range1[self.currentAngle[0]],
            self.yaw_range2[self.currentAngle[1]],
            self.yaw_range1[self.currentAngle[2]],
            self.yaw_range2[self.currentAngle[3]],
            self.yaw_range1[self.currentAngle[4]],
            self.yaw_range3[self.currentAngle[5]],
            self.yaw_range1[self.currentAngle[6]],
            0,
            0,
            0,
            0
        ])


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
        q = self.simulator.run(self.yaws)
        # print(self.simulator.floris.ws_array_0)
        # print(self.simulator.floris.floris_windframe_0.turbineX)
        print(self.simulator.floris.velocitiesTurbines_directions)
        # [nDirections, nTurbines]
        self.velocitiesTurbines_directions = self.simulator.floris.velocitiesTurbines_directions
        # [nDirections, nTurbines]
        self.wt_power_directions = self.simulator.floris.wt_power_directions
        # [nDirections]
        self.power_directions = self.simulator.floris.power_directions

        pp = np.copy(q[0:7])
        pp[0] += q[7]
        pp[2] += q[8]
        pp[4] += q[9]
        pp[6] += q[10]
        # print(self.episode, self.stepCnt, turbineId, action, sum(pp.tolist()), pp.tolist())
        self.epsTotalPower += sum(pp.tolist())
        self.epsCount += 1
        return pp.tolist()


    def makeState(self, turbineId):
        # print("direction:", self.simulator.floris.floris_power_0.  #velocitiesTurbines_directions)
        return

    def makeEnvInfo(self):
        return []
