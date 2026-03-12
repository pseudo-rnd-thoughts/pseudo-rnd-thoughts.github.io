
import gymnasium as gym
import numpy as np
import torch
from gymnasium import VectorizeMode
from torch import nn


value_fn = nn.Sequential(
    nn.Linear(4, 32),
    nn.ReLU(),
    nn.Linear(32, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
)

def compute_gae_next_step(
    observations,  # T+1
    rewards,       # T
    terminations,  # T
    truncations,   # T
    gamma=0.99, gae_lambda=0.95, num_envs=1
):
    timesteps = len(rewards)
    values = value_fn(torch.tensor(observations)).detach().numpy().squeeze(-1)
    advantages = np.zeros((timesteps, num_envs))
    gae = np.zeros(num_envs)
    episode_over = terminations | truncations

    for t in reversed(range(timesteps)):
        next_val = np.logical_not(terminations[t]) * values[t + 1]
        delta = rewards[t] + gamma * next_val - values[t]
        gae = delta + gamma * gae_lambda * (1 - episode_over[t]) * gae
        advantages[t] = gae

    # Mask the first step of each new episode: its obs is stale.
    mask = np.ones((timesteps, num_envs))  # Binary mask of invalid losses
    mask[1:] = np.logical_not(episode_over[:-1])

    return advantages, mask


def compute_gae_same_step(
    observations,       # T
    next_observations,  # T
    rewards,            # T
    terminations,       # T
    truncations,        # T
    gamma=0.99, gae_lambda=0.95, num_envs=1
):
    timesteps = len(rewards)
    values = value_fn(torch.tensor(observations)).detach().numpy().squeeze(-1)
    next_values = value_fn(torch.tensor(next_observations)).detach().numpy().squeeze(-1)
    advantages = np.zeros((timesteps, num_envs))
    gae = np.zeros(num_envs)
    episode_over = terminations | truncations

    for t in reversed(range(timesteps)):
        next_val = np.logical_not(terminations[t]) * next_values[t]
        delta = rewards[t] + gamma * next_val - values[t]
        gae = delta + gamma * gae_lambda * (1 - episode_over[t]) * gae
        advantages[t] = gae

    # No masking needed: every step has a valid observation.

    return advantages


def rollout_next_step(seed: int = 123, rollout_length: int = 200, num_envs: int = 1, max_episode_steps: int = 20):
    next_step_envs = gym.make_vec(
        "CartPole-v1",
        num_envs=num_envs,
        vectorization_mode=VectorizeMode.SYNC,
        vector_kwargs={"autoreset_mode": gym.vector.AutoresetMode.NEXT_STEP},
        max_episode_steps=max_episode_steps
    )
    dead_action = next_step_envs.single_action_space.sample()
    [env.action_space.seed(seed+i) for i, env in enumerate(next_step_envs.envs)]

    next_step_obs = np.zeros((rollout_length+1, num_envs, *next_step_envs.single_observation_space.shape), dtype=next_step_envs.observation_space.dtype)
    next_step_rewards = np.zeros((rollout_length, num_envs), dtype=np.float32)
    next_step_terminations = np.zeros((rollout_length, num_envs), dtype=np.bool)
    next_step_truncations = np.zeros((rollout_length, num_envs), dtype=np.bool)

    obs, info = next_step_envs.reset(seed=seed)
    next_step_envs.action_space.seed(seed)

    episode_over = np.zeros(num_envs, dtype=np.bool)
    for t in range(rollout_length):
        actions = np.stack([
            dead_action if episode_over[i] else env.action_space.sample()
            for i, env in enumerate(next_step_envs.envs)
        ])
        next_obs, rewards, terminations, truncations, _ = next_step_envs.step(actions)

        next_step_obs[t] = obs
        next_step_rewards[t] = rewards
        next_step_terminations[t] = terminations
        next_step_truncations[t] = truncations

        obs = next_obs
        episode_over = np.logical_or(terminations, truncations)

    next_step_obs[-1] = next_obs

    return next_step_obs, next_step_rewards, next_step_terminations, next_step_truncations


def rollout_same_step(seed: int = 123, rollout_length: int = 200, num_envs: int = 1, max_episode_steps: int = 20):
    same_step_envs = gym.make_vec(
        "CartPole-v1",
        num_envs=num_envs,
        vectorization_mode=VectorizeMode.SYNC,
        vector_kwargs={"autoreset_mode": gym.vector.AutoresetMode.SAME_STEP},
        max_episode_steps=max_episode_steps
    )
    [env.action_space.seed(seed + i) for i, env in enumerate(same_step_envs.envs)]

    same_step_obs = np.zeros((rollout_length, num_envs, *same_step_envs.single_observation_space.shape), dtype=same_step_envs.observation_space.dtype)
    same_step_next_obs = np.zeros((rollout_length, num_envs, *same_step_envs.single_observation_space.shape), dtype=same_step_envs.observation_space.dtype)
    same_step_rewards = np.zeros((rollout_length, num_envs), dtype=np.float32)
    same_step_terminations = np.zeros((rollout_length, num_envs), dtype=np.bool)
    same_step_truncations = np.zeros((rollout_length, num_envs), dtype=np.bool)

    obs, info = same_step_envs.reset(seed=seed)
    same_step_envs.action_space.seed(seed)

    for t in range(rollout_length):
        actions = np.stack([env.action_space.sample() for env in same_step_envs.envs])

        next_obs, rewards, terminations, truncations, infos = same_step_envs.step(actions)
        same_step_obs[t] = obs
        same_step_rewards[t] = rewards
        same_step_terminations[t] = terminations
        same_step_truncations[t] = truncations
        if np.any(terminations | truncations):
            same_step_next_obs[t] = infos["final_obs"][0]
        else:
            same_step_next_obs[t] = next_obs

        obs = next_obs

    return same_step_obs, same_step_next_obs, same_step_rewards, same_step_terminations, same_step_truncations


if __name__ == "__main__":
    _rollout_length = 200
    _seed = np.random.randint(1, 10000)
    _max_episode_steps = 20
    _num_envs = 2

    # NEXT_STEP COMPUTATION
    next_step_obs, next_step_rewards, next_step_terminations, next_step_truncations = rollout_next_step(
        rollout_length=_rollout_length, seed=_seed, max_episode_steps=_max_episode_steps, num_envs=_num_envs)
    print(f'{np.sum(next_step_terminations)=}, {np.sum(next_step_truncations)=}')
    assert np.any(next_step_terminations) and np.any(next_step_truncations)

    next_step_advantage, next_step_mask = compute_gae_next_step(
        next_step_obs, next_step_rewards, next_step_terminations, next_step_truncations,
        gamma=0.99, gae_lambda=0.95, num_envs=_num_envs
    )
    next_step_num_episodes = np.sum(next_step_terminations | next_step_truncations)
    assert next_step_num_episodes == np.sum(np.logical_not(next_step_mask)), f'{next_step_num_episodes=}, {np.sum(np.logical_not(next_step_mask))=}'

    print(f'{next_step_advantage.squeeze()=}, {next_step_num_episodes=}')
    next_step_advantage = next_step_advantage[np.nonzero(next_step_mask)[0]]
    print(f'{next_step_advantage.shape=}, {np.nonzero(next_step_mask)[0].shape=}')

    # SAME_STEP COMPUTATION
    same_step_obs, same_step_next_obs, same_step_rewards, same_step_terminations, same_step_truncations = rollout_same_step(
        rollout_length=_rollout_length, seed=_seed, max_episode_steps=_max_episode_steps, num_envs=_num_envs)
    assert np.any(same_step_terminations) and np.any(same_step_truncations), f'{np.sum(same_step_terminations)=}, {np.sum(same_step_truncations)=}'
    bound = _rollout_length - np.sum(same_step_terminations | same_step_truncations) + 1

    # The same-step implementation has actually taken more timesteps, therefore, we need to limit the same-step rollout for the same timesteps
    same_step_obs = same_step_obs[:bound]
    same_step_next_obs = same_step_next_obs[:bound]
    same_step_rewards = same_step_rewards[:bound]
    same_step_terminations = same_step_terminations[:bound]
    same_step_truncations = same_step_truncations[:bound]

    same_step_advantage = compute_gae_same_step(
        same_step_obs, same_step_next_obs, same_step_rewards, same_step_terminations, same_step_truncations,
        gamma=0.99, gae_lambda=0.95, num_envs=_num_envs
    )
    same_step_num_episodes = np.sum(same_step_terminations | same_step_truncations)
    assert next_step_num_episodes == same_step_num_episodes, f'{next_step_num_episodes=}, {same_step_num_episodes=}'
    print(f'{same_step_advantage.squeeze()=}, {next_step_num_episodes=}')

    # COMPARISON
    assert next_step_advantage.shape == same_step_advantage.shape, f'{next_step_advantage.shape=}, {same_step_advantage.shape=}'
    error = next_step_advantage - same_step_advantage
    print(f'{error.squeeze()=}')
    assert np.allclose(next_step_advantage, same_step_advantage)

