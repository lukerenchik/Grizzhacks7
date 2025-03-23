import pygame
import numpy as np
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, SCROLL_SPEED, OBSTACLE_WIDTH  # adjust as needed
from core.procedural_gen import generate_obstacle  # function to generate obstacles
from core import game_logic
from envs.entities import Player, Obstacle  # your game entity classes



class JetpackEnv:
    def __init__(self, human_control=False):
        """
        Initialize the Jetpack environment.
        
        - Set up pygame (screen, clock, etc.).
        - Create the player instance.
        - Initialize an empty list for obstacles.
        - Set up background elements (image, position, etc.).
        - Initialize game variables (score, frame count, etc.).
        - Optionally set a flag for human control.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("JetpackRL")
        self.clock = pygame.time.Clock()
        
        # Game control flags
        self.human_control = human_control
        self.done = False
        
        # Initialize player, obstacles, background, score, and frame count
        self.player = Player()  # ensure Player class is defined in entities.py
        self.obstacles = []     # list to hold obstacle instances
        self.score = 0
        self.frame_count = 0
        
        # Load background image if available
        self.background = None  # TODO: Load your background image here
        self.bg_x = 0  # background scroll position

        # Reset the velocity log for the new episode.
        #self.velocity_log = []

        

    def reset(self):
        """
        Reset the game environment to its initial state.
        
        - Reset the player's position and velocity via its own reset() method.
        - Clear the obstacles list (obstacles are maintained by the environment).
        - Reset the score and frame counter.
        - Reset background scroll variables.
        - Mark the game as not done.
        - Optionally, generate initial obstacles if needed.
        - Return the initial observation state.
        """
        # Reset the player (assumes Player.reset() is implemented)
        self.player.reset()
        
        # Clear obstacles; this is managed by the environment, not the Obstacle class
        self.obstacles = []
        
        # Reset score and frame counter
        self.score = 0
        self.frame_count = 0
        
        # Reset background scroll (assuming you scroll the background horizontally)
        self.bg_x = 0
        
        # Mark environment as active (not done)
        self.done = False
        
        # Optionally, initialize the first obstacle if required:
        # from core.procedural_gen import generate_obstacle
        # self.obstacles.append(generate_obstacle(x_position=SCREEN_WIDTH))
        
        # Return the initial observation state (as defined by your get_state() method)
        return self.get_state()


    def step(self, action):
        """
        Take a single step in the game based on the action.
        
        - Process the action (e.g., thrust if action == 1).
        - Apply gravity to update player's velocity (handled in the Player.update method).
        - Update player's position based on velocity.
        - Scroll the background and obstacles to simulate movement.
        - Use procedural_gen.generate_obstacle() to add new obstacles when needed.
        - Update score (e.g., +1 per frame) and frame counter.
        - Check for collisions and set self.done = True if a collision is detected.
        - Return (observation, reward, done, info) where observation is from get_state().
        """
        
        # Process the input action: if action is 1, apply thrust; otherwise, do nothing.
        thrust = (action == 1)
        
        # Update the player (this applies thrust if needed, then gravity, then updates position).
        self.player.update(thrust)
        
        # Update obstacles: move each obstacle left by calling its update_position method.
        for obs in self.obstacles:
            obs.update_position()
        
        # Remove obstacles that have scrolled completely off-screen.
        self.obstacles = [obs for obs in self.obstacles if (obs.x + obs.top_rect.width) > 0]
        
        # Optionally generate a new obstacle if none exist or if the last obstacle is far enough to the left.
        # For example, if there are no obstacles or the rightmost obstacle's x position is less than 80% of the screen width.
        if not self.obstacles or (self.obstacles[-1].x < SCREEN_WIDTH * 0.8):
            from core.procedural_gen import generate_obstacle
            new_obstacle = generate_obstacle(x_position=SCREEN_WIDTH)
            self.obstacles.append(new_obstacle)
        
        # Update background scroll if using a background image.
        if self.background is not None:
            self.bg_x -= SCROLL_SPEED
            # Reset bg_x if the background image has completely scrolled off.
            if self.bg_x <= -self.background.get_width():
                self.bg_x = 0
        
        # Increment score and frame counter.
        self.score += 1
        self.frame_count += 1
        
        # Check for collisions. This sets self.done = True if a collision is detected.
        self._handle_collisions()
        
        # Log the player's current velocity.
        #self.velocity_log.append(self.player.velocity)

        # Compute reward: using game_logic.compute_reward (which returns -100 on collision, +1 otherwise).
        # Here, we assume that if a collision occurs (self.done is True), the state dictionary includes a collision flag.
        from core import game_logic
        state_info = {"collision": self.done}
        reward = game_logic.compute_reward(state_info, action)
        
        # Get the current observation state.
        observation = self.get_state()
        
        # Construct extra info, such as the current score and frame count.
        info = {"score": self.score, "frame_count": self.frame_count}
        
        return observation, reward, self.done, info


    def print_velocity_stats(self):
        """
        Print statistics for the player's velocity over the episode.
        """
        if not self.velocity_log:
            print("No velocity data logged.")
            return
        min_velocity = min(self.velocity_log)
        max_velocity = max(self.velocity_log)
        avg_velocity = sum(self.velocity_log) / len(self.velocity_log)
        print(f"Player Velocity Stats: min={min_velocity}, max={max_velocity}, avg={avg_velocity}")

    def render(self):
        """
        Render the game elements onto the screen.
        
        - Draw the scrolling background.
        - Draw all obstacles.
        - Draw the player.
        - Optionally, display the current score.
        - Update the display.
        """
        # Render the background.
        # If a background image is set, we implement scrolling by blitting it twice.
        if self.background is not None:
            # Blit the background image at the current scroll position.
            self.screen.blit(self.background, (self.bg_x, 0))
            # Blit a second copy to create a seamless scrolling effect.
            self.screen.blit(self.background, (self.bg_x + self.background.get_width(), 0))
        else:
            # If no background image is set, fill the screen with a solid color (e.g., sky blue).
            self.screen.fill((135, 206, 250))
        
        # Draw each obstacle using its draw method.
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw the player using its draw method.
        self.player.draw(self.screen)
        
        # Optionally, display the current score.
        # Create a font for rendering the score. (You can adjust font size and type as needed.)
        font = pygame.font.SysFont("Arial", 30)
        score_surface = font.render(f"Score: {int(self.score)}", True, (0, 0, 0))
        # Blit the score in the top left corner.
        self.screen.blit(score_surface, (10, 10))
        
        # Update the display to show the new frame.
        pygame.display.flip()




    def get_state(self):
        """
        Return the current state (observation) of the environment as a NumPy array.

        Features included:
            - player_y: The vertical position of the player.
            - player_y_velocity: The current vertical velocity of the player.
            - gap_y: The y coordinate (top) of the gap in the next obstacle.
            - gap_height: The height of the gap (safe zone) in the next obstacle.
            - obstacle_x_distance: The horizontal distance from the player to the next obstacle.
            - player_to_gap_center_y: The vertical difference between the player's position and
                                    the center of the gap.
        
        Returns:
            np.array: An array of these features.
        """
        # Get player's state from the Player object.
        player_y = self.player.y
        player_y_velocity = self.player.velocity
        player_x = self.player.x  # Assume player's x is fixed (e.g., 100)
        
        # Determine the next obstacle.
        # We assume obstacles are moving left, so any obstacle with its right edge greater than
        # the player's x is still ahead.
        obstacles_ahead = [obs for obs in self.obstacles if (obs.x + OBSTACLE_WIDTH) > player_x]
        
        if obstacles_ahead:
            # Choose the closest obstacle (i.e., with the minimum x value).
            next_obstacle = min(obstacles_ahead, key=lambda obs: obs.x)
            gap_y = next_obstacle.gap_y         # Top of the gap.
            gap_height = next_obstacle.gap_height # Height of the gap.
            obstacle_x_distance = next_obstacle.x - player_x
            # Calculate vertical distance from player to the gap center.
            player_to_gap_center_y = player_y - (gap_y + gap_height / 2)
        else:
            # No obstacles ahead: use default values.
            gap_y = 0
            gap_height = 0
            # Set the distance to a high default value (e.g., the width of the screen).
            obstacle_x_distance = SCREEN_WIDTH - player_x
            player_to_gap_center_y = 0

        return np.array([
            player_y,
            player_y_velocity,
            gap_y,
            gap_height,
            obstacle_x_distance,
            player_to_gap_center_y
        ], dtype=np.float32)

    def _handle_collisions(self):    
    # Call the collision checking function.
        if game_logic.check_collision(self.player, self.obstacles):
            # If a collision is detected, mark the episode as done.
            self.done = True