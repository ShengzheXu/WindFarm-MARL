from AbstractAgent import AbstractAgent
from RlBrain import DoubleDQN
import tensorflow as tf

class DqnAgent(AbstractAgent):
    def __init__(self, turbineId, sess):
        self.istrain = True
        self.ACTION_SPACE = 11
        self.MEMORY_SIZE = 50000
        self.sess = sess
        self.initOneAgent(turbineId, allfeature_len=26)

    def initOneAgent(self, who, allfeature_len):
        if self.istrain is True:
            e_greedy_start = 0.7
            e_greedy_end = 0.99
            # greedy_increment = (e_greedy_end - e_greedy_start) / self.train_episode
            greedy_increment = 0.985 # 0.99
        else:
            e_greedy_start = 0.7
            e_greedy_end = 0.7
            greedy_increment = None
        with tf.variable_scope(str(who) + '_DDQN'):
            double_DQN = DoubleDQN(agent_name=str(who) + '_DDQN',
                                   n_actions=self.ACTION_SPACE, n_features=allfeature_len, memory_size=self.MEMORY_SIZE,
                                   batch_size=128, e_greedy_start=e_greedy_start, e_greedy_end=e_greedy_end,
                                   e_greedy_increment=greedy_increment, double_q=True, sess=self.sess,
                                   output_graph=True)
        self.agent = double_DQN
        return double_DQN

    def doForward(self, state):
        # print (state)
        action_number = self.agent.choose_action(state)
        return action_number

    def doBackward(self, experience):
        # print experience
        self.agent.learn(experience)

    def getLoss(self):
        return self.agent.cost_his[-1]
