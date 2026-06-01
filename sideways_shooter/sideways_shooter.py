import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class SidewaysShooter:
  """Overall class to manage game assets and behavior."""
  
  def __init__(self):
    """Initialize the game, and create game resources."""
    pygame.init()
    # Start Sideways Shooter in an active state.
    self.game_active = True
    
    self.clock = pygame.time.Clock()
    self.settings = Settings()
    
    self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    self.screen_rect = self.screen.get_rect()
    pygame.display.set_caption("Sideways Shooter")
    
    # Create an instance to store game statistics.
    self.stats = GameStats(self)
    
    # Screen must be defined BEFORE ship, since we're accessing it.
    self.ship = Ship(self)
    
    # Group that holds the bullets, and allows you to manage the bullets fired from the ship.
    self.bullets = pygame.sprite.Group()
    
    # Fleet of aliens group.
    self.aliens = pygame.sprite.Group()
    
    # Create fleet.
    self._create_fleet()
    
  def run_game(self):
    while True:
      self._check_events()
      
      if self.game_active:
        self.ship.update()
        self._update_aliens()
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
        
    # Check for any bullets that have hit aliens.
    self._check_bullet_alien_collisions()
    
  def _check_bullet_alien_collisions(self):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(
      self.bullets, self.aliens, True, True
    )
    # Respawn new fleet when one is destroyed.
    if not self.aliens:
      # Destroy existing bullet sprites and create new fleet.
      self.bullets.empty()
      self._create_fleet()
        
  def _update_aliens(self):
    """Check if fleet is at an edge, then update the poistions of all aliens in the fleet."""
    self._check_fleet_edges()
    self.aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
      self._ship_hit()
        
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
    
    current_x, current_y = self.screen_rect.width - alien_width, alien_height
    while current_x > (self.ship.rect.right + 2 * alien_width):
      while current_y < (self.screen_rect.height - alien_height):
          self._create_alien(current_x, current_y)
          current_y += 2 * alien_height
      
      # Finished a row; reset y-value, and decrement x-value to next column.
      current_x -= 2 * alien_width
      current_y = alien_height
      
  def _check_fleet_edges(self):
    """Respond appropriately if any aliens have reached the top or bottom edge."""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break
  
  def _change_fleet_direction(self):
    """Drop the entire fleet(left) and change the fleet's direction."""
    for alien in self.aliens.sprites():
      alien.rect.x -= self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1
    
  def _ship_hit(self):
    """Respond to the sdhip being hit by an alien."""
    if self.stats.ships_left > 0:
      # Decrement the remaining ships.
      self.stats.ships_left -= 1
      
      # Get rid of any remaining bullets and aliens.
      self.bullets.empty()
      self.aliens.empty()
      
      # Create a new fleet and center the ship.
      self._create_fleet()
      self.ship.center_ship()
      
      # Pause
      sleep(0.5)
    
    else:
      self.game_active = False
  
  def _update_screen(self):
    """Update images on the screen, and flip to the new screen."""
    self.screen.fill(self.settings.bg_color)
    
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    # Redraw the ship at its current location.
    self.ship.blitme()
    
    # To make the aliens appear, we need to call draw() for the group of aliens. This method automatically draws each alien in the group at the position specified by its rect attribute.
    self.aliens.draw(self.screen)
    
    # Make the most recently drawn screen available.
    pygame.display.flip()
    

if __name__ == '__main__':
  ss = SidewaysShooter()
  ss.run_game()