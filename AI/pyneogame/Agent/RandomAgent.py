import random
from . import BaseAgent # Work for python dev_script


class RandomAgent(BaseAgent.BaseAgent):

    def __str__(self):
        return "Random Agent"

    def get_action(self, state, actions, as_string=False):

        action = random.choice(actions)

        if as_string:
            return ''.join([str(x) for x in action])
        else:
            return action
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self


