import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class SidewaysShooter:
  """Overall class to manage game assets and behavior."""
  
  def __init__(self):
    """Initialize the game, and create game resources."""
    pygame.init()
    
    self.clock = pygame.time.Clock()
    self.settings = Settings()
    
    self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    self.screen_rect = self.screen.get_rect()
    pygame.display.set_caption("Sideways Shooter")
    
    # Screen must be defined BEFORE ship, since we're accessing it.
    self.ship = Ship(self)
    
    # Group that holds the bullets, and allows you to manage the bullets fired from the ship.
    self.bullets = pygame.sprite.Group()
    
  def run_game(self):
    while True:
      self._check_events()
      self.ship.update()
      self._update_bullet()
      self._update_screen()
      self.clock.tick(60)
      
  def _check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        self._check_events_keydown(event)
      elif event.type == pygame.KEYUP:
        self._check_events_keyup(event)
  
  def _check_events_keydown(self, event):
    """Respond to keypresses."""
    if event.key == pygame.K_q:
      sys.exit()
    elif event.key == pygame.K_UP:
      self.ship.moving_up = True
    elif event.key == pygame.K_DOWN:
      self.ship.moving_down = True
    elif event.key == pygame.K_SPACE:
      self._fire_bullet()
  
  def _check_events_keyup(self, event):
    if event.key == pygame.K_UP:
      self.ship.moving_up = False
    elif event.key == pygame.K_DOWN:
      self.ship.moving_down = False
      
  def _fire_bullet(self):
    """Create a new bullet and add it to the bullets group."""
    if len(self.bullets) < self.settings.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)
  
  def _update_bullet(self):
    """Update position of bullets and get rid of old bullets."""
    # Apply update() method on all bullets to update their positions.
    self.bullets.update()
    # Get rid of old bullets that have disappeared.
    for bullet in self.bullets.copy():
      if bullet.rect.left >= self.screen_rect.right:
        self.bullets.remove(bullet)
  
  def _update_screen(self):
    """Update images on the screen, and flip to the new screen."""
    self.screen.fill(self.settings.bg_color)
    
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    # Redraw the ship at its current location.
    self.ship.blitme()
    
    # Make the most recently drawn screen available.
    pygame.display.flip()
    

if __name__ == '__main__':
  ss = SidewaysShooter()
  ss.run_game()