#/usr/bin/python3
"""A sample training script for training and testing agents playing NeoGame"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game

# a) Setup the agents

game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                       actions=game.get_actions())
opponent = GreedyAgent()

# b) Setup the gym
gym = Gym(player, opponent)

# c) Run training
gym.train(num_episodes=50000)
gym.eval_exp_table()

# d) Run test
gym.test(10000)
gym.eval()

gym.save_model("dq_agent.h5")
