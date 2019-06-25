import pandas as pd
import numpy as np
from collections import deque
import random
from os import path
from keras import Model
from keras. models import save_model, load_model
from keras.layers import Input, Dense, Embedding, Flatten, LSTM, Bidirectional
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.activations import softmax
import tensorflow as tf

from . import DeepQAgent
# TODO: Create a Dueling DQN
# TODO: Prioritized experience replay
# TODO: Create and compare with a policy learning agent


class ReInforce(DeepQAgent.DeepQAgent):
    """ ReInforce PolicyGradient Agent
    """

    def __init__(self, state_size, actions,
                 model=None,
                 epsilon=0.9,
                 decay_rate=1e-5,
                 update_interval=200,
                 memory_size=10000,
                 verbose=0):

        self.actions = actions
        self.actions_size = self.actions.shape[1]
        self.verbose = verbose
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.memory = deque(maxlen=memory_size)
        self.update_dnn_interval = update_interval
        self.episode_counter = 0
        self.state_size = state_size
        self.r_sum = 0
        self.avg_r_sum = []

        if model is None:
            print("Building default model")
            self.dnn_model = self._make_model()
        else:
            self.dnn_model = model

    def __str__(self):
        return "Policy Gradient Agent: ReInforce"

    def reward_loss(self, y_true, y_pred):
        y_cross = tf.abs(y_true) * tf.exp(y_true) * tf.log(y_pred) +tf.abs(y_true)* tf.exp(-y_true)*tf.log(1-y_pred)
        # result = - tf.reduce_sum(y_cross, 1)
        result = - tf.reduce_mean(y_cross, 1)
        return result

    #  def reward_loss(self, y_true, y_pred):
    #     if y_true < 0:
    #         y_cross = -y_true * tf.log(1 - y_pred)
    #     else:
    #         y_cross = y_true * tf.log(y_pred)
    #     # result = - tf.reduce_sum(y_cross, 1)
    #     result = - tf.reduce_mean(y_cross, 1)
    #     return result

    # @tf.function
    # def reward_loss(self, y_true, y_pred):
        
    #     print(y_true, y_pred)

    #     if y_true < 0:
    #         y_cross = -y_true * tf.log(1 - y_pred)
    #     else:
    #         y_cross = y_true * tf.log(y_pred)
    #     # result = - tf.reduce_sum(y_cross, 1)
    #     result = - tf.reduce_mean(y_cross, 1)
    #     return result

   #  def prioritize_replay(self):



    def _make_model(self):
        '''Start with a simple default model for now'''
        input_layer = Input(shape=(self.state_size,))
        embedding = Embedding(input_dim=5, output_dim=3)(input_layer)
        flat = Flatten()(embedding)
        dense_1 = Dense(200, activation='sigmoid')(flat)  # input_layer)
        x = Dense(200, activation='sigmoid')(dense_1)
        x = Dropout(0.1)(x)
        action_dist = Dense(self.actions_size, activation='softmax')(x)
        # action_dist = Dense(self.actions_size, activation='sigmoid')(x)  

        model_act = Model(inputs=input_layer, outputs= action_dist)
        model_act.compile(
                      # loss = 'binary_crossentropy',
                      # loss= 'categorical_crossentropy', 
                     loss = self.reward_loss,
                     # loss = self.
                      optimizer='adam')
                      
        if self.verbose:
            print(model_act.summary())
        return model_act

    def get_action(self, state, actions=None,
                   explore_exploit='none',
                   as_string=False):
        
        state = state.reshape(1, state.shape[0])
        act_dist = self.dnn_model.predict(state)

        idx = np.random.choice(range(act_dist.shape[1]), 
                                         p=act_dist.ravel(), size=2)

        #idx = np.random.choice(range(act_dist.shape[1]), 
        #                                p=act_dist.ravel()/act_dist.sum(), size=2)                                        

        # print(act_dist.ravel()/act_dist.sum())

        action = np.zeros(act_dist.shape[1])
        action[idx] = 1
        return action

    def remember(self, state, action, reward, new_state=None, done=None):
        self.memory.append((state, action, reward))

    def replay_experience(self, batch_size=64, epochs=30):
        if self.verbose > 0:
            print('Doing replay')
        
        # Extract data from the experience buffer
        player_mem = np.asarray(self.memory)
        states = np.vstack(player_mem[:, 0])
        actions = np.vstack(player_mem[:, 1])
        rewards = player_mem[:, 2]

        # Need to deal with the space of rewards. -X -> X becomes 0 < X
        # TODO: Change this and inform user that it is happening. Perhaps by
        # setting a mapping
        #target = actions * 1/np.exp(-1*rewards.astype(float))[:, np.newaxis]
        
        def sigmoid(x):
            return 1/(1+np.exp(-x))

        # target = actions *rewards[:, np.newaxis] # Doesn't converge
        # target = actions * (sigmoid(rewards.astype(float))-0.5)[:, np.newaxis] # Doesn't converge
        # target = actions * np.exp(rewards.astype(float))[:, np.newaxis] # Works like sample weighting
        # target = actions # + sample weight = Works
        # target = actions * rewards[:, np.newaxis] # +custom loss (reduce sum) Not working
        # target = actions * rewards[:, np.newaxis] # +custom loss (reduce mean) 
        # target = actions *rewards[:, np.newaxis] # With sigmoid and binary cross entropy # No convergence
        # target = actions 
        # target = np.stack(actions, rewards[:, np.newaxis])
        target = actions * rewards[:, np.newaxis]
        #print(target.shape)
        # TODO: Use Early stopping or not?
        es = EarlyStopping(monitor='val_loss', mode='min',
                           verbose=0, patience=2)
        history = self.dnn_model.fit(states,
                                     target,
                                     epochs=epochs,
                                     verbose=0,
                                     batch_size=batch_size,
                                     callbacks=[es],
                                     validation_split=0.10,
                                     # sample_weight=np.exp(rewards.astype(float))
                                     )

        return history

