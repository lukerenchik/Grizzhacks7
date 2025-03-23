import gymnasium as gym
from gymnasium import spaces
import numpy as np
from core.config import SCREEN_HEIGHT, SCREEN_WIDTH
from envs.jetpack_env import JetpackEnv

class JetpackGymWrapper(gym.Env):
    """
    A Gymnasium wrapper for the Jetpack environment.
    
    Action Space:
        Discrete(2): 
          0 - No thrust
          1 - Apply thrust
    
    Observation Space:
        A Box with six features:
          [player_y, player_y_velocity, gap_y, gap_height, obstacle_x_distance, player_to_gap_center_y]
    """
    def __init__(self, human_control=False):
        super().__init__()
        self.env = JetpackEnv(human_control=human_control)
        
        # Define action space: 0 (no thrust) or 1 (thrust)
        self.action_space = spaces.Discrete(2)
        
        # Define observation space:
        # For example, we assume:
        #   player_y in [0, SCREEN_HEIGHT]
        #   player_y_velocity in [-50, 50] (adjust as needed)
        #   gap_y in [0, SCREEN_HEIGHT]
        #   gap_height in [100, 250] (adjust based on dynamic gap range)
        #   obstacle_x_distance in [0, SCREEN_WIDTH]
        #   player_to_gap_center_y in [-SCREEN_HEIGHT, SCREEN_HEIGHT]
        low = np.array([0, -50.0, 0, 150, 0, -SCREEN_HEIGHT], dtype=np.float32)
        high = np.array([SCREEN_HEIGHT, 50.0, SCREEN_HEIGHT, 400, SCREEN_WIDTH, SCREEN_HEIGHT], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        
    def reset(self, **kwargs):
        """
        Reset the environment and return the initial observation and an info dict.
        """
        observation = self.env.reset()
        return observation, {}
    
    def step(self, action):
        """
        Take a step in the environment using the provided action.
        
        Returns:
            observation (np.array): The current state.
            reward (float): The reward for the step.
            terminated (bool): Whether the episode ended due to a terminal condition (collision).
            truncated (bool): False (unless you implement a separate timeout mechanism).
            info (dict): Additional information (e.g., score, frame count).
        """
        observation, reward, done, info = self.env.step(action)
        # In Gymnasium, step returns (obs, reward, terminated, truncated, info)
        return observation, reward, done, False, info
    
    def render(self, mode='human'):
        """
        Render the environment.
        """
        self.env.render()
    
    def close(self):
        """
        Clean up the environment.
        """
        if hasattr(self.env, "close"):
            self.env.close()
