#later put the copyrights
# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

import numpy as np

import torch
import torch.nn as nn
from torch.distributions import Normal
from torch.nn.modules import rnn

class ActorCritic(nn.Module):
    is_recurrent = False
    def __init__(self, num_actor_obs, num_critic_obs, num_actions, num_agents=6, 
                 actor_hidden_dims=[256, 256, 256], critic_hidden_dims=[256, 256, 256],
                 activation='elu', init_noise_std=1.0, **kwargs):
        super(ActorCritic, self).__init__()

        activation = get_activation(activation)
        self.num_agents = num_agents

        # Create separate actor and critic models for each agent
        self.actors = nn.ModuleList()
        self.critics = nn.ModuleList()
        
        for _ in range(num_agents):
            # Actor network
            actor_layers = [nn.Linear(num_actor_obs, actor_hidden_dims[0]), activation]
            for l in range(len(actor_hidden_dims) - 1):
                actor_layers += [nn.Linear(actor_hidden_dims[l], actor_hidden_dims[l + 1]), activation]
            actor_layers.append(nn.Linear(actor_hidden_dims[-1], num_actions))
            self.actors.append(nn.Sequential(*actor_layers))

            # Critic network
            critic_layers = [nn.Linear(num_critic_obs, critic_hidden_dims[0]), activation]
            for l in range(len(critic_hidden_dims) - 1):
                critic_layers += [nn.Linear(critic_hidden_dims[l], critic_hidden_dims[l + 1]), activation]
            critic_layers.append(nn.Linear(critic_hidden_dims[-1], 1))
            self.critics.append(nn.Sequential(*critic_layers))

        self.std = nn.Parameter(init_noise_std * torch.ones(num_actions))

        # disable args validation for speedup
        Normal.set_default_validate_args = False
        
        # seems that we get better performance without init
        # self.init_memory_weights(self.memory_a, 0.001, 0.)
        # self.init_memory_weights(self.memory_c, 0.001, 0.)

    @staticmethod
    # not used at the moment
    def update_distribution(self, observations):
        self.distributions = [Normal(actor(obs), self.std) for actor, obs in zip(self.actors, observations)]

    def act(self, observations):
        # Ensure each observation goes to the correct actor
        actions = []
        for idx, (actor, obs) in enumerate(zip(self.actors, observations)):
            # Use the idx-th actor to compute the action for the idx-th agent's observation
            dist = Normal(actor(obs), self.std)
            actions.append(dist.sample())
        return torch.stack(actions)
    # def evaluate(self, critic_observations):
    #     # Ensure each observation goes to the correct critic
    #     values = []
    #     for idx, (critic, obs) in enumerate(zip(self.critics, critic_observations)):
    #         # Use the idx-th critic to compute the value for the idx-th agent's observation
    #         values.append(critic(obs))
    #     return torch.stack(values)

    # def init_weights(sequential, scales):
    #     [torch.nn.init.orthogonal_(module.weight, gain=scales[idx]) for idx, module in
    #      enumerate(mod for mod in sequential if isinstance(mod, nn.Linear))]
    # def act(self, observations):
    #     """
    #     Compute actions for each agent in a multi-agent environment.
        
    #     Args:
    #         observations (torch.Tensor): A tensor of shape (num_envs, num_agents, obs_dim) representing
    #                                     the observations for each agent in each environment.
        
    #     Returns:
    #         torch.Tensor: A tensor of shape (num_envs, num_agents, action_dim) containing the actions
    #                     for each agent in each environment.
    #     """
    #     num_envs, num_agents, _ = observations.shape
    #     actions = []

    #     # Iterate over each agent
    #     for agent_id in range(num_agents):
    #         # Extract observations for the current agent across all environments
    #         agent_obs = observations[:, agent_id, :]  # Shape: (num_envs, obs_dim)
            
    #         # Use the corresponding actor for this agent
    #         actor = self.actors[agent_id]
            
    #         # Compute action distribution and sample actions
    #         dist = Normal(actor(agent_obs), self.std)  # Shape: (num_envs, action_dim)
    #         agent_actions = dist.sample()  # Shape: (num_envs, action_dim)
            
    #         # Store actions for the current agent
    #         actions.append(agent_actions)
        
    #     # Stack actions to have a final shape of (num_envs, num_agents, action_dim)
    #     return torch.stack(actions, dim=1)
    def evaluate(self, critic_observations):
        """
        Compute value estimates for each agent in a multi-agent environment.
        
        Args:
            critic_observations (torch.Tensor): A tensor of shape (num_envs, num_agents, obs_dim) representing
                                                the critic observations for each agent in each environment.
        
        Returns:
            torch.Tensor: A tensor of shape (num_envs, num_agents) containing the value estimates
                        for each agent in each environment.
        """
        num_envs, num_agents, _ = critic_observations.shape
        values = []

        # Iterate over each agent
        for agent_id in range(num_agents):
            # Extract observations for the current agent across all environments
            agent_obs = critic_observations[:, agent_id, :]  # Shape: (num_envs, obs_dim)
            
            # Use the corresponding critic for this agent
            critic = self.critics[agent_id]
            
            # Compute the value estimate for the current agent
            agent_values = critic(agent_obs).squeeze(-1)  # Shape: (num_envs)
            
            # Store values for the current agent
            values.append(agent_values)
        
        # Stack values to have a final shape of (num_envs, num_agents)
        return torch.stack(values, dim=1)
    def init_weights(self, scales):
        """
        Initialize weights for multi-agent networks.
        
        Args:
            scales (list): A list of gain scales for initializing the weights of the networks.
                        It should have the same length as the number of agents.
        """
        for agent_id in range(self.num_agents):
            actor = self.actors[agent_id]
            critic = self.critics[agent_id]
            
            # Initialize actor network weights
            for module in actor:
                if isinstance(module, nn.Linear):
                    torch.nn.init.orthogonal_(module.weight, gain=scales[agent_id])
            
            # Initialize critic network weights
            for module in critic:
                if isinstance(module, nn.Linear):
                    torch.nn.init.orthogonal_(module.weight, gain=scales[agent_id])





    def reset(self, dones=None):
        pass

    def forward(self):
        raise NotImplementedError
    
    @property
    def action_mean(self):
        return self.distribution.mean

    @property
    def action_std(self):
        return self.distribution.stddev
    
    @property
    def entropy(self):
        return self.distribution.entropy().sum(dim=-1)

    def get_actions_log_prob(self, actions):
        return self.distribution.log_prob(actions).sum(dim=-1)

    def act_inference(self, observations):
        actions_mean = self.actor(observations)
        return actions_mean

def get_activation(act_name):
    if act_name == "elu":
        return nn.ELU()
    elif act_name == "selu":
        return nn.SELU()
    elif act_name == "relu":
        return nn.ReLU()
    elif act_name == "crelu":
        return nn.ReLU()
    elif act_name == "lrelu":
        return nn.LeakyReLU()
    elif act_name == "tanh":
        return nn.Tanh()
    elif act_name == "sigmoid":
        return nn.Sigmoid()
    else:
        print("invalid activation function!")
        return None
