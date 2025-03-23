import random
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, OBSTACLE_WIDTH, GAP_HEIGHT
from envs.entities import Obstacle

def generate_obstacle(x_position=None):
    """
    Generate a new obstacle with a randomized gap position.
    
    Parameters:
        x_position (int, optional): The x coordinate where the obstacle will be placed.
                                    Defaults to SCREEN_WIDTH (i.e. the right edge of the screen).
    
    Returns:
        Obstacle: A new obstacle instance with a top barrier, a bottom barrier, and a gap.
    
    Explanation:
        This function acts as your obstacle factory. It determines a safe, random gap position within the 
        screen limits. For example, you might choose a margin (say 50 pixels) so that the gap isn't too close 
        to the top or bottom.
    """
    if x_position is None:
        x_position = SCREEN_WIDTH

    margin = 50
    # Randomize gap_y as before
    gap_y = random.randint(margin, SCREEN_HEIGHT - GAP_HEIGHT - margin)
    
    # Introduce dynamic gap height: choose a gap height in a given range.
    min_gap = 300  # Minimum gap height for difficulty control
    max_gap = 500  # Maximum gap height
    dynamic_gap_height = random.randint(min_gap, max_gap)
    
    return Obstacle(x_position, gap_y, dynamic_gap_height)

def get_next_obstacles(window_x, obstacles):
    """
    Retrieve obstacles that are still ahead of a given x-coordinate.
    
    Parameters:
        window_x (int): The x coordinate representing the current view or player's x position.
        obstacles (list): A list of all obstacle instances currently in the game.
    
    Returns:
        list: Obstacles that have not yet passed the given window_x.
    
    Explanation:
        This helper function filters obstacles based on their x position relative to the current view or player.
        For example, in the observation function of your environment, you may want to know the next obstacle(s)
        that the agent should be aware of. This function returns obstacles that haven't yet scrolled past the given
        x coordinate.
    """
    # Filter obstacles: Only keep obstacles whose right edge is still to the right of window_x.
    next_obstacles = [obs for obs in obstacles if (obs.x + OBSTACLE_WIDTH) > window_x]
    return next_obstacles
