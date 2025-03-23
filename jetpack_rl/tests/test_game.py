import pytest
import pygame

# Import the constants from your config
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, OBSTACLE_WIDTH, GAP_HEIGHT, SCROLL_SPEED, GRAVITY, THRUST

# Import modules to test
from envs.entities import Player, Obstacle
from core import game_logic
from core.procedural_gen import generate_obstacle, get_next_obstacles

# Ensure pygame is initialized for tests that require it.
pygame.init()

##############################
# Tests for the Player class #
##############################

def test_player_reset():
    """
    Test that the player's reset method correctly restores the initial position and velocity.
    """
    player = Player()
    # Change state from defaults.
    player.x = 500
    player.y = 500
    player.velocity = 10
    player.rect.topleft = (500, 500)
    # Reset should bring player back to starting state.
    player.reset()
    assert player.x == 100
    assert player.y == 300
    assert player.velocity == 0
    assert player.get_rect().topleft == (100, 300)

def test_player_update_without_thrust():
    """
    Test that calling update() without thrust applies gravity and updates the position.
    
    Since initial velocity is 0, after one update, the velocity should equal GRAVITY and
    the y position should increase by GRAVITY.
    """
    player = Player()
    initial_y = player.y
    player.update(thrust=False)
    expected_y = initial_y + GRAVITY  # because velocity starts at 0 then increases by GRAVITY
    assert abs(player.y - expected_y) < 1e-3

def test_player_update_with_thrust():
    """
    Test that calling update() with thrust modifies the velocity in a cumulative way.
    
    The velocity should be updated by adding the thrust and then gravity.
    """
    player = Player()
    initial_velocity = player.velocity
    player.update(thrust=True)
    expected_velocity = initial_velocity + THRUST + GRAVITY
    assert abs(player.velocity - expected_velocity) < 1e-3

##############################
# Tests for the Obstacle class #
##############################

def test_obstacle_initialization():
    """
    Test that an Obstacle is correctly initialized with top and bottom barrier rects.
    
    The top barrier should extend from y=0 to gap_y, and the bottom barrier should extend 
    from gap_y + gap_height to the bottom of the screen.
    """
    x_pos = 1366
    gap_y = 200
    gap_height = 150
    obstacle = Obstacle(x_pos, gap_y, gap_height)
    
    # Verify the top barrier's position and size.
    assert obstacle.top_rect.topleft == (x_pos, 0)
    assert obstacle.top_rect.height == gap_y

    # Verify the bottom barrier's position and size.
    expected_bottom_y = gap_y + gap_height
    expected_bottom_height = SCREEN_HEIGHT - expected_bottom_y
    assert obstacle.bottom_rect.topleft == (x_pos, expected_bottom_y)
    assert obstacle.bottom_rect.height == expected_bottom_height

def test_obstacle_update_position():
    """
    Test that update_position() moves the obstacle left by SCROLL_SPEED and updates its rects.
    """
    x_pos = 1366
    gap_y = 200
    obstacle = Obstacle(x_pos, gap_y, GAP_HEIGHT)
    old_x = obstacle.x
    obstacle.update_position()
    assert obstacle.x == old_x - SCROLL_SPEED
    # Check that both barrier rects update their x position.
    assert obstacle.top_rect.x == obstacle.x
    assert obstacle.bottom_rect.x == obstacle.x

###################################
# Tests for procedural_gen module #
###################################

def test_generate_obstacle():
    """
    Test that generate_obstacle() creates an obstacle with default x position and gap within safe margins.
    """
    obstacle = generate_obstacle()
    # Default x_position should be SCREEN_WIDTH.
    assert obstacle.x == SCREEN_WIDTH
    margin = 50
    # gap_y should be within [margin, SCREEN_HEIGHT - GAP_HEIGHT - margin]
    assert margin <= obstacle.gap_y <= (SCREEN_HEIGHT - GAP_HEIGHT - margin)
    # If dynamic gap height is enabled, we might check it lies within a defined range.
    # Here, we assume a range of 100 to 200 for example purposes.
    min_gap = 100
    max_gap = 200
    assert min_gap <= obstacle.gap_height <= max_gap

def test_get_next_obstacles():
    """
    Test that get_next_obstacles() returns only the obstacles that are still ahead of the given window_x.
    
    It filters out obstacles that have scrolled past the current view.
    """
    # Create three obstacles with varying x positions.
    obstacles = [
        Obstacle(1400, 200, GAP_HEIGHT),
        Obstacle(1300, 250, GAP_HEIGHT),
        Obstacle(1200, 300, GAP_HEIGHT)
    ]
    window_x = 1250
    next_obs = get_next_obstacles(window_x, obstacles)
    
    # Only obstacles whose (x + OBSTACLE_WIDTH) > window_x should remain.
    expected = [obs for obs in obstacles if (obs.x + OBSTACLE_WIDTH) > window_x]
    assert next_obs == expected

#################################
# Tests for game_logic module   #
#################################

def test_compute_reward_no_collision():
    """
    Test that compute_reward() returns +1 when no collision is detected.
    """
    state = {"collision": False}
    action = 0  # Action is not affecting reward in this simple case.
    reward = game_logic.compute_reward(state, action)
    assert reward == 1

def test_compute_reward_collision():
    """
    Test that compute_reward() returns -100 when a collision is detected.
    """
    state = {"collision": True}
    action = 0
    reward = game_logic.compute_reward(state, action)
    assert reward == -100

def test_check_collision_no_collision():
    """
    Test that check_collision() returns False when there is no collision.
    
    The player is positioned safely and no obstacles are present.
    """
    player = Player()
    player.y = 300
    player.rect.y = 300
    obstacles = []
    collision = game_logic.check_collision(player, obstacles)
    assert collision is False

def test_check_collision_with_obstacle():
    """
    Test that check_collision() returns True when the player's rect collides with an obstacle.
    
    The player's position is set so that it overlaps with the top barrier of an obstacle.
    """
    player = Player()
    # Place the player so that its rect is near the top.
    player.y = 100
    player.rect.y = 100
    # Create an obstacle where the gap starts below the player's position.
    obstacle = Obstacle(100, 150, GAP_HEIGHT)  # Top barrier covers from 0 to 150.
    obstacles = [obstacle]
    collision = game_logic.check_collision(player, obstacles)
    assert collision is True
