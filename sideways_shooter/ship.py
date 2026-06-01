import pygame

class Ship:
  """A class to manage the ship."""
  
  def __init__(self, ss_game):
    """Initialize the ship and set its starting position."""
    self.screen = ss_game.screen
    self.screen_rect = ss_game.screen.get_rect()
    self.settings = ss_game.settings
    
    # Load the ship image and get its rect.
    self.image = pygame.image.load('images/ship.bmp')
    # Rotate the ship image 90 degrees clockwise.
    self.image = pygame.transform.rotate(self.image, -90)
    self.rect = self.image.get_rect()
    
    # Start each new ship at the left middle of the screen.
    self.rect.midleft = self.screen_rect.midleft
    
    # Store a float for the ship's exact horizontal position.
    self.x = float(self.rect.x)
    
  def update(self):
    """Update the ship's position based on the movement flag."""
    # Update the ship's x-value, not the rect.
    return
  
  def blitme(self):
    """Draw the ship at its current location."""
    self.screen.blit(self.image, self.rect)
    