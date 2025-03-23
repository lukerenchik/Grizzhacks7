import pygame
from core.config import GRAVITY, THRUST, PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_HEIGHT, SCROLL_SPEED, OBSTACLE_WIDTH, GAP_HEIGHT


class Player:
    def __init__(self, start_x=100, start_y=300):
        """
        Initialize the Player.
        
        Attributes:
            x, y: Position of the player.
            velocity: Current vertical velocity.
            rect: Pygame Rect for collision detection and drawing.
        """
        self.x = start_x
        self.y = start_y
        self.velocity = 0
        
        # Create a rectangle representing the player's position and size
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Adjust the path if necessary based on your project structure.
        self.image = pygame.image.load("assets/CaptainCwack.png").convert_alpha()

        # Optionally scale the image to match the player's dimensions.
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH * 2.3, PLAYER_HEIGHT * 2.3))

        

    def reset(self):
        """
        Reset the player's state to the initial configuration.
        """
        self.x = 200
        self.y = 375
        self.velocity = 0
        self.rect.topleft = (self.x, self.y)

    def update_gravity(self, gravity_value=GRAVITY):
        """
        Apply gravity to the player's velocity.
        """
        self.velocity += gravity_value

    def apply_thrust(self, thrust_value=THRUST):
        """
        Apply thrust to the player.
        """
        self.velocity += thrust_value

    def update_position(self):
        """
        Update the player's position based on its velocity.
        """
        self.y += self.velocity
        self.rect.y = int(self.y)

    def update(self, thrust=False):
        """
        Update the player's state for one frame.
        
        If thrust is True, apply thrust before gravity.
        Then, update gravity and the player's position.
        """
        if thrust:
            self.apply_thrust()
        self.update_gravity()
        self.update_position()

    def draw(self, screen):
        """
        Render the player on the given Pygame screen.
        
        This method encapsulates all the drawing logic for the player.
        """
        # If using an image, you could do:
        screen.blit(self.image, self.rect)
        # Otherwise, draw a simple rectangle:
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def get_rect(self):
        """
        Return the player's rect for collision detection.
        """
        return self.rect



class Obstacle:
    def __init__(self, x_pos, gap_y, gap_height=GAP_HEIGHT):
        """
        Initialize an obstacle consisting of a top barrier and a bottom barrier.
        
        Parameters:
            x_pos (int): The starting x position of the obstacle.
            gap_y (int): The y coordinate where the gap starts (i.e., the end of the top barrier).
            gap_height (int): The height of the gap (i.e., safe zone). Defaults to GAP_HEIGHT.
        """
        self.x = x_pos
        self.gap_y = gap_y  # Starting y position of the gap
        self.gap_height = gap_height

        # The top barrier extends from the top of the screen (y=0) to gap_y.
        self.top_rect = pygame.Rect(self.x, 0, OBSTACLE_WIDTH, self.gap_y)
        # The bottom barrier extends from gap_y + gap_height to the bottom of the screen.
        self.bottom_rect = pygame.Rect(self.x, self.gap_y + self.gap_height, OBSTACLE_WIDTH, SCREEN_HEIGHT - (self.gap_y + self.gap_height))
    
    def update_position(self, delta_x=SCROLL_SPEED):
        """
        Update the obstacle's x position to simulate scrolling.
        
        Parameters:
            delta_x (int): The amount to move the obstacle horizontally.
                             Default is the SCROLL_SPEED from your config.
                             
        This method updates both the top and bottom barrier positions.
        """
        self.x -= delta_x  # Move the obstacle to the left.
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def draw(self, screen):
        """
        Draw the obstacle on the screen.
        
        This method draws both the top and bottom barriers.
        """
        # Draw the top barrier (stalactite)
        pygame.draw.rect(screen, (0, 255, 0), self.top_rect)
        # Draw the bottom barrier (stalagmite)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_rect)
    
    def get_gap_rect(self):
        """
        Return a pygame.Rect representing the safe zone (the gap).
        """
        return pygame.Rect(self.x, self.gap_y, OBSTACLE_WIDTH, self.gap_height)