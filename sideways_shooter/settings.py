class Settings:
  """A class to store all settings for Sideways Shooter."""
  
  def __init__(self):
    """Initialize the game's settings."""
    self.screen_width = 600
    self.screen_height = 600
    self.bg_color = (230, 230, 230)
    
    # Ship Settings
    self.ship_speed = 1.5
    