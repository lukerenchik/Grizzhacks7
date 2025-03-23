import pygame
from core.config import SCREEN_HEIGHT

def compute_reward(state, action):
    """
    Compute the reward based on the current state and the agent's action.
    
    For this Jetpack Joyride clone:
      - The agent receives a +1 reward for every frame it survives.
      - If a collision occurs (i.e. game over), it gets a -100 penalty.
      - Additional reward modifications can be added as needed.
    
    Parameters:
        state (dict): A dictionary containing current state information.
                      It may include a key 'collision' indicating whether a collision occurred.
        action: The action taken by the agent at this step (can be used to shape rewards further).
    
    Returns:
        float: The computed reward.
    """
    # Assume state contains a boolean 'collision' flag.
    if state.get("collision", False):
        return -100  # Collision penalty
    else:
        return 1  # Reward for surviving the frame


def check_collision(player, obstacles):
    """
    Check whether the player collides with any obstacles or the screen boundaries.
    
    Parameters:
        player: The player object, expected to have a 'get_rect()' method returning a pygame.Rect,
                as well as a 'y' attribute for the vertical position.
        obstacles (list): List of obstacle objects. Each obstacle is expected to have 
                          'top_rect' and 'bottom_rect' attributes (pygame.Rect).
    
    Returns:
        bool: True if a collision is detected, otherwise False.
    
    Explanation:
        This function performs the following checks:
          - Checks if the player's rect collides with the top or bottom barrier of any obstacle.
          - Checks if the player has moved out of the vertical bounds of the screen.
        It returns a simple boolean value which the environment's _handle_collisions() method can use 
        to update the game state.
    """
    player_rect = player.get_rect()
    
    # Check collision with obstacles (top and bottom barriers)
    for obs in obstacles:
        if player_rect.colliderect(obs.top_rect) or player_rect.colliderect(obs.bottom_rect):
            return True

    # Check collision with screen boundaries (top and bottom)
    if player.y < 0 or (player.y + player_rect.height) > SCREEN_HEIGHT:
        return True

    return False
