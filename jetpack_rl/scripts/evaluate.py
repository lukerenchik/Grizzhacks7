import argparse
import pygame
from stable_baselines3 import PPO
from envs.jetpack_gym_wrapper import JetpackGymWrapper

def wait_for_enter(env):
    """
    Display a prompt in the pygame window and wait for the user to press ENTER.
    
    This function renders a "Press ENTER to start evaluation..." message on the screen.
    It continuously polls for events and exits once the ENTER key is pressed.
    
    Parameters:
        env: The Gym wrapper environment (JetpackGymWrapper). Assumes that the underlying
             environment (JetpackEnv) has an attribute 'screen' for rendering.
    
    Returns:
        True if ENTER is pressed, False if the user closes the window.
    """
    # Create a font and render the prompt text.
    font = pygame.font.SysFont("Arial", 30)
    prompt_text = "Press ENTER to start evaluation..."
    text_surface = font.render(prompt_text, True, (255, 255, 255))
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        
        # Render the environment so the background is visible.
        env.render()
        
        # Attempt to get the underlying screen from the wrapped environment.
        if hasattr(env, 'env') and hasattr(env.env, 'screen'):
            screen = env.env.screen
            # Blit the prompt text onto the screen (position it as desired).
            screen.blit(text_surface, (50, 50))
            pygame.display.flip()
        
        # Delay to limit the loop's CPU usage.
        pygame.time.delay(100)
    return True

def evaluate(model, num_episodes=5):
    """
    Evaluate the provided model for a number of episodes and render the performance.
    
    Parameters:
        model: A trained PPO model.
        num_episodes (int): The number of evaluation episodes to run.
    """
    # Create the evaluation environment (agent-controlled).
    env = JetpackGymWrapper(human_control=False)
    
    # Wait for the user to press ENTER using the pygame window.
    if not wait_for_enter(env):
        return
    
    for ep in range(num_episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # Use the trained model to predict the next action.
            action, _states = model.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            
            # Render the environment.
            env.render()
            pygame.time.delay(20)
            
            # Check if the episode has ended.
            done = terminated or truncated

        print(f"Episode {ep+1}: Total Reward: {total_reward}")

    env.close()
    pygame.quit()

def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Evaluate a trained PPO model on the Jetpack RL environment."
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="saves/models/ppo_model",
        help="Path to the trained model to evaluate."
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=5,
        help="Number of evaluation episodes to run."
    )
    args = parser.parse_args()
    
    # Load the trained PPO model from the provided path.
    model = PPO.load(args.model_path)
    
    # Run evaluation.
    evaluate(model, num_episodes=args.episodes)

if __name__ == "__main__":
    main()
