import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
  """A. class to represent a single alien in the fleet."""
  
  def __init__(self, ss_game):
    """Initialize the alien and set its starting position."""
    super().__init__()
    self.screen = ss_game.screen
    self.settings = ss_game.settings
    
    # Load the alien image and get its rect.
    self.image = pygame.image.load('images/alien.bmp')
    # Rotate the alien ship counterclockwise 90 degrees.
    self.image = pygame.transform.rotate(self.image, -90)
    self.rect = self.image.get_rect()
    
    # Start each new alien near the top right of the screen. Alien ship is SIDEWAYS, so flip the x and y values.
    self.rect.x = self.rect.height
    self.rect.y = self.rect.width
    
    # Store the alien's exact vertical position.
    self.y = float(self.rect.y)
    
  def update(self):
    """Move the alien left and right SIDEWAYS."""
    self.y += self.settings.alien_speed * self.settings.fleet_direction
    self.rect.y = self.y
    