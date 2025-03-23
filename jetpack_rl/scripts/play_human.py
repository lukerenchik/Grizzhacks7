import pygame
from envs.jetpack_env import JetpackEnv
from core.leaderboard import save_score, print_leaderboard
import matplotlib.pyplot as plt

def main():
    # Initialize the human-playable environment.
    env = JetpackEnv(human_control=True)
    # Reset the environment to start a new game.
    observation = env.reset()
    
    # Create a clock object to control the frame rate.
    clock = pygame.time.Clock()
    
    # Game loop.
    running = True
    while running:
        # Handle Pygame events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Read keyboard state.
        keys = pygame.key.get_pressed()
        # If space bar is pressed, set action to 1 (thrust); otherwise, action is 0.
        action = 1 if keys[pygame.K_SPACE] else 0
        
        # Step the environment using the given action.
        observation, reward, done, info = env.step(action)
        
        # Render the environment (background, obstacles, player, score, etc.)
        env.render()
        
        # Check if the game is over.
        if done:
            running = False
        
        # Cap the frame rate (e.g., 60 frames per second).
        clock.tick(60)
    
    # Quit Pygame.
    pygame.quit()
    
    # After game over, display the final score.
    print(f"Game Over! Final Score: {info.get('score', 0)}")
    
    # Optionally, prompt for the player's name and save the score.
    name = input("Enter your name for the leaderboard: ")
    save_score(name, info.get("score", 0))
    
    # Print the current leaderboard.
    print_leaderboard()

    # After running an episode:
    # plt.hist(env.velocity_log, bins=50)
    #plt.xlabel("Player Velocity")
    #plt.ylabel("Frequency")
    #plt.title("Distribution of Player Velocity")
    #plt.show()

if __name__ == "__main__":
    main()
