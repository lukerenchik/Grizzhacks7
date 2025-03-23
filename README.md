# 🚀 JetpackRL: Reinforcement Learning Jetpack Joyride Clone

JetpackRL is a procedurally generated infinite runner game inspired by *Jetpack Joyride*. Built with Pygame and Gym, this project allows both humans and reinforcement learning agents to play and compete. The goal: avoid crashing into obstacles, floor, or ceiling while surviving as long as possible.

Trained using **Stable Baselines3 (PPO)** with a custom **Gym environment**, the AI learns how to time its thrusts to stay alive in an increasingly difficult environment.

---

## 🎮 Gameplay Overview

- Player controls vertical thrust (like Flappy Bird meets Jetpack Joyride)
- Environment scrolls continuously with procedurally generated obstacles
- Crash = game over
- Score = time survived (1 point per frame)

---


## 📊 Features

- ✅ Procedural level generation
- ✅ Pygame environment wrapped as a Gym interface
- ✅ Human play mode with keyboard control
- ✅ Leaderboard system with top scores
- ✅ PPO-trained RL agent using Stable Baselines3
- ✅ Reward visualization and training plots
- ✅ Evaluation mode to test trained agents

---

## 🧠 Agent Design

**Observation Space:**
- Player vertical position
- Player vertical velocity
- Distance to next obstacle
- Gap vertical position
- Gap height
- Vertical distance to gap center

**Action Space:**
- `0`: Do nothing
- `1`: Activate vertical thrust

**Reward Structure:**
- `+1` per frame survived
- `-100` on collision with obstacle, floor, or ceiling
- Max episode length: 2000 frames

---


## 🏁 Results

### 📈 Reward Curve
*(Insert reward_curve.png here)*  
The agent successfully learns to navigate the environment, reaching high scores reliably after ~X episodes.

### 🤖 AI vs Human Scores
- Best AI Score: `XXXX`
- Best Human Score: `YYYY`
- *(Insert leaderboard screenshot or table)*

---

## 🛠️ How to Run

### 🔧 Installation
```bash
pip install -r requirements.txt
```

### 🕹️ Play as Human
python -m scripts.play_human

### 🤖 Train Agent
python scripts/train.py

### 🧪 Evaluate Trained Agent
python scripts/evaluate.py

### 📊 Generate Plots
python scripts/plot_rewards.py

### 📂 Project Structure

jetpack_rl/
├── envs/                  # Game logic, Gym wrapper
├── core/                  # Procedural gen, leaderboard, config
├── scripts/               # Train, play, evaluate, plot
├── saves/                 # Trained models, leaderboard, plots
├── logs/                  # Training logs and Monitor outputs

