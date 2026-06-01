class Settings:
  """A class to store all settings for Sideways Shooter."""
  
  def __init__(self):
    """Initialize the game's settings."""
    self.screen_width = 600
    self.screen_height = 600
    self.bg_color = (230, 230, 230)
    
    # Ship Settings
    self.ship_speed = 1.5
    
    # Bullet Settings
    self.bullet_speed = 2.0
    self.bullet_width = 15
    self.bullet_height = 3
    self.bullet_color = (60, 60, 60)
    self.bullets_allowed = 3
    
    # Alien Settings
    self.alien_speed = 1.0
    self.fleet_drop_speed = 100
    # Fleet direction of 1 represents right; -1 represents left. Remember this is sideways.
    self.fleet_direction = -1