# %%
import numpy as np
from pyneogame.Engine import Game
from tqdm import tqdm
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.ActiveTable import ActiveTable
from pyneogame.Agent.RandomAgent import RandomAgent

# %%
game = Game()
player = GreedyAgent(value_func=Game.calc_score)
player = ActiveTable()
opponent = RandomAgent()

game.get_actions()

# %%
game.get_player_state()
game.deal_cards().get_player_state()

# %%
player_action = player.get_action(game.get_player_state(),
                                  game.get_actions()
                                  )
print(player_action)
# opponent_action = nn.get_action(game.get_nn_state(),
#                                       game.get_actions())
# print(nn_action)


TEST_EPISODES = 1000
player_wins = []
opponent_wins = []

for _ in range(1):
    # for i in tqdm(range(TEST_EPISODES)):
    for i in range(TEST_EPISODES):
        game.deal_cards()
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          )

        opponent_action = opponent.get_action(game.get_opponent_state(),
                                              game.get_actions())

        player_score, opponent_score = (game.set_player_action(player_action)
                                        .set_opponent_action(opponent_action)
                                        .get_scores())

        player.learn(state=game.get_player_state(),
                     action=player_action,
                     reward=player_score-opponent_score)

# %%
player_wins.append(sum(
    list(play > opp for opp, play in
         zip(list(game.opponent_score)[-TEST_EPISODES:],
             list(game.player_score)[-TEST_EPISODES:])
         )))

opponent_wins.append(
    sum(
        list(play < opp for opp, play in
             zip(list(game.opponent_score)[-TEST_EPISODES:],
                 list(game.player_score)[-TEST_EPISODES:])
             )))

print(player_wins)
print(opponent_wins)


print(game.deal_cards().get_env())
if isinstance(player, ActiveTable):
    print('Recommended state')
    state = player.recommend_state()
    print(state)
    print(game.deal_from_recommendation(state).get_env())

print(game.get_actions())
