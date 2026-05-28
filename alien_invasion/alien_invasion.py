import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
  """Overall class to manage game aseets and behavior."""
  
  def __init__(self):
    """Initialize the game, and create game resources."""
    pygame.init()
    
    self.clock = pygame.time.Clock()
    self.settings = Settings()
    
    self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    self.screen_rect = self.screen.get_rect()
    pygame.display.set_caption("Alien Invasion")
    
    # screen must be defined BEFORE ship, since we're accessing it.
    self.ship = Ship(self)
    
    # Group that holds the bullets, and allows you to manage the bullets fired from the ship.
    self.bullets = pygame.sprite.Group()
    
    # Fleet of aliens group
    self.aliens = pygame.sprite.Group()
    
    # Create fleet
    self._create_fleet()
    
  def run_game(self):
    while True:
      self._check_events()
      self.ship.update()
      self._update_aliens()
      self._update_bullets()
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
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = True
    elif event.key == pygame.K_RIGHT:
      self.ship.moving_right = True
    elif event.key == pygame.K_SPACE:
      self._fire_bullet()
  
  def _check_events_keyup(self, event):
    if event.key == pygame.K_LEFT:
      self.ship.moving_left = False
    elif event.key == pygame.K_RIGHT:
      self.ship.moving_right = False
      
  def _fire_bullet(self):
    """Create a new bullet and add it to the bullets group."""
    if len(self.bullets) < self.settings.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)
      
  def _update_bullets(self):
    """Update position of bullets and get rid of old bullets."""
    # Apply update() method on all bullets to update their position.
    self.bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in self.bullets.copy():
      if bullet.rect.bottom <= self.screen_rect.top:
        self.bullets.remove(bullet)
        
  def _update_aliens(self):
    """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
    self._check_fleet_edges()
    self.aliens.update()
        
  def _create_alien(self, x_position, y_position):
    """Create an alien and place it in the row."""
    new_alien = Alien(self)
    new_alien.x = x_position
    new_alien.rect.x = x_position
    new_alien.y = y_position
    new_alien.rect.y = y_position
    self.aliens.add(new_alien)
    
  def _create_fleet(self):
    """Create the fleet of aliens."""
    # Create an alien and keep adding aliens until there's no room left.
    # Spacing between aliens is one alien width and one alien height.
    alien = Alien(self)
    alien_width, alien_height = alien.rect.size
    
    current_x, current_y  = alien_width, alien_height
    while current_y < (self.settings.screen_height - 3 * alien_height):
      while current_x < (self.settings.screen_width - 2 * alien_width):
        self._create_alien(current_x, current_y)
        current_x += 2 * alien_width
      
      # Finished a row; reset x-value, and increment y-value to next row.
      current_x = alien_width
      current_y += 2 * alien_height
  
  def _check_fleet_edges(self):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break
  
  def _change_fleet_direction(self):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in self.aliens.sprites():
      alien.rect.y += self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1
  
  def _update_screen(self):
    """Update images on the screen, and flip to the new screen."""
    self.screen.fill(self.settings.bg_color)
    
    # Draw the bullets
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    # Redraw the ship at its current location.
    self.ship.blitme()
    
    # To make the aliens appear, we need to call draw() for the group of aliens. This method automatically draws each alien in the group at the position specified by its rect attribute.
    self.aliens.draw(self.screen)
    
    # Make the most recently drawn screen available.
    pygame.display.flip()
    

if __name__ == '__main__':
  ai = AlienInvasion()
  ai.run_game()
