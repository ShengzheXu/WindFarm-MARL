from generator import FlorisWrapper


class WindGym(object):

    def __init__(self):
        self.readTurbineMap()
        self.simulator = FlorisWrapper(turbine_grid)
        self.buildActionSpace()

    def readTurbineMap(self):
        # TODO: read from csv

        h_distance = 2
        v_distance = 0.75
        turbine_grid = 500 * np.array([[h_distance,  0],
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
        return turbine_grid

    def buildActionSpace(self):
        self.yaw_range1 = np.array([23, 27, 28])
        self.yaw_range2 = np.array([-10, -6, -1])
        self.yaw_range3 = np.array([-2, 1, 4])
        self.yaw_range4 = np.array([0])

    def reset(self):
        return

    def step(self):
        # TODO: read from csv

        simulator.randomizeWind()
        yaws = np.array([
            yaw_range1[y1],
            yaw_range2[y2],
            yaw_range1[y3],
            yaw_range2[y4],
            yaw_range1[y5],
            yaw_range3[y6],
            yaw_range1[y7],
            0,
            0,
            0,
            0
        ])
        q = simulator.run(yaws)

        # [nDirections, nTurbines]
        self.velocitiesTurbines_directions = simulator.get("velocitiesTurbines_directions")
        # [nDirections, nTurbines]
        self.wt_power_directions = simulator.get("wt_power_directions")
        # [nDirections]
        self.power_directions = simulator.get("power_directions")

        pp = np.copy(q[0:7])
        pp[0] += q[7]
        pp[2] += q[8]
        pp[4] += q[9]
        pp[6] += q[10]

        return pp.tolist()

    def makeState(self):
        return
