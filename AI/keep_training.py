#/usr/bin/python3
"""Continue training a saved model"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game

# a) Setup the agents

name = "dq_agent.h5"
training_iterations = 100000
update_interval = training_iterations / 5

game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                       actions=game.get_actions(), update_interval=update_interval)
player.load(name)
opponent = GreedyAgent()

# b) Setup the gym
gym = Gym(player, opponent)

# c) Run training
gym.train(num_episodes=100000)
gym.eval_exp_table()

# d) Run test
gym.test(10000)
gym.eval()

gym.save_model("dq_agent.h5")