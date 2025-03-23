import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

from envs.jetpack_gym_wrapper import JetpackGymWrapper

# Custom callback for logging losses, policy entropy, and episode lengths.
class LoggingCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(LoggingCallback, self).__init__(verbose)
        self.losses = []
        self.entropies = []
        self.steps = []
        self.episode_lengths = []
        self.ep_steps = []  # Timesteps corresponding to the rollout's average episode length

    def _on_step(self) -> bool:
        # Log combined loss if available.
        if "policy_loss" in self.locals:
            policy_loss = self.locals["policy_loss"]
            value_loss = self.locals.get("value_loss", 0)
            entropy_loss = self.locals.get("entropy_loss", 0)
            combined_loss = policy_loss + value_loss + entropy_loss
            self.losses.append(combined_loss)
            self.steps.append(self.num_timesteps)
        # Log policy entropy (using key "policy_entropy" or fallback "entropy").
        if "policy_entropy" in self.locals:
            self.entropies.append(self.locals["policy_entropy"])
        elif "entropy" in self.locals:
            self.entropies.append(self.locals["entropy"])
        return True

    def _on_rollout_end(self) -> None:
        # Log average episode length from the Monitor wrapper.
        if self.model.ep_info_buffer:
            lengths = [ep_info["l"] for ep_info in self.model.ep_info_buffer if "l" in ep_info]
            if lengths:
                self.episode_lengths.append(np.mean(lengths))
                self.ep_steps.append(self.num_timesteps)

    def _on_training_end(self) -> None:
        # Save all logged metrics so that we can plot them later.
        np.savez("saves/plots/training_logs.npz",
                 steps=np.array(self.steps),
                 losses=np.array(self.losses),
                 entropies=np.array(self.entropies),
                 ep_steps=np.array(self.ep_steps),
                 episode_lengths=np.array(self.episode_lengths))


# Plotting functions.
def plot_reward_curve(log_file, save_path):
    """
    Plot the raw reward curve per episode from the monitor log.
    """
    df = pd.read_csv(log_file, skiprows=1)
    plt.figure()
    plt.plot(df["r"])
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Reward Curve")
    plt.savefig(os.path.join(save_path, "reward_curve_lowgv_stablereward.png"))
    plt.close()

def plot_average_reward(log_file, save_path):
    """
    Plot a moving average (window=10) of the episode rewards.
    """
    df = pd.read_csv(log_file, skiprows=1)
    df["reward_ma"] = df["r"].rolling(window=10).mean()
    plt.figure()
    plt.plot(df["reward_ma"])
    plt.xlabel("Episode")
    plt.ylabel("Average Reward (10-episode MA)")
    plt.title("Average Reward per Episode Over Time")
    plt.savefig(os.path.join(save_path, "average_reward_lowgv_stablereward.png"))
    plt.close()

def plot_loss_curve(training_logs_file, save_path):
    """
    Plot the loss curve based on the logged loss data from the custom callback.
    """
    data = np.load(training_logs_file)
    steps = data["steps"]
    losses = data["losses"]
    plt.figure()
    plt.plot(steps, losses)
    plt.xlabel("Timesteps")
    plt.ylabel("Combined Loss")
    plt.title("Loss Curve")
    plt.savefig(os.path.join(save_path, "loss_curve_lowgv_stablereward.png"))
    plt.close()

def plot_entropy_curve(training_logs_file, save_path):
    """
    Plot the policy entropy over time.
    """
    data = np.load(training_logs_file)
    steps = data["steps"]
    entropies = data["entropies"]
    plt.figure()
    plt.plot(steps, entropies)
    plt.xlabel("Timesteps")
    plt.ylabel("Policy Entropy")
    plt.title("Policy Entropy Curve")
    plt.savefig(os.path.join(save_path, "entropy_curve_lowgv_stablereward.png"))
    plt.close()

def plot_episode_length_curve(training_logs_file, save_path):
    """
    Plot the average episode length over time.
    """
    data = np.load(training_logs_file)
    ep_steps = data["ep_steps"]
    episode_lengths = data["episode_lengths"]
    plt.figure()
    plt.plot(ep_steps, episode_lengths)
    plt.xlabel("Timesteps")
    plt.ylabel("Average Episode Length")
    plt.title("Episode Length Over Time")
    plt.savefig(os.path.join(save_path, "episode_length_curve_lowgv_stablereward.png"))
    plt.close()

def main():
    # Create directories for saving models, logs, and plots.
    os.makedirs("saves/models", exist_ok=True)
    os.makedirs("saves/plots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Create the Gym environment wrapped with Monitor to log episode rewards.
    env = JetpackGymWrapper()
    env = Monitor(env, filename="logs/monitor.csv")
    
    # Initialize the PPO model.
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./logs/tensorboard/")
    
    # Create the custom logging callback.
    logging_callback = LoggingCallback()
    
    # Set total timesteps for training.
    total_timesteps = 2000000  # Adjust as needed.
    model.learn(total_timesteps=total_timesteps, callback=logging_callback)
    
    # Save the trained model.
    model.save("saves/models/ppo_model_2mil_lowgv_stablereward")
    
    # Plot and save training graphs.
    plot_reward_curve("logs/monitor.csv", "saves/plots")
    plot_average_reward("logs/monitor.csv", "saves/plots")
    
    # Load training logs and plot loss, entropy, and episode lengths.
    training_logs_file = "saves/plots/training_logs.npz"
    if os.path.exists(training_logs_file):
        plot_loss_curve(training_logs_file, "saves/plots")
        plot_entropy_curve(training_logs_file, "saves/plots")
        plot_episode_length_curve(training_logs_file, "saves/plots")
    else:
        print("Training logs not found. Additional metric plots were not generated.")

if __name__ == "__main__":
    main()
