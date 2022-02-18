class Settings():
	#A class to store all settings for Alien Invasion
	
	def __init__(self):
		#Initialize the game's static settings
		#Screen Settings
		self.screen_width = 1160
		self.screen_height = 800
		self.screen_size = (self.screen_width, self.screen_height)
		self.bg_color = (30, 30, 30)
		
		#Ship settings
		self.ship_speed_factor = 2.5
		self.ship_limit = 2
		
		#Bullet settings
		self.bullet_speed_factor = 20.5
		self.bullet_width = 5
		self.bullet_height = 30
		self.bullet_color = 230, 0, 0
		self.bullets_allowed = 1
		
		#Alien Settings
		self.alien_speed_factor = 3.5
		self.fleet_drop_speed = 40
		#fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1
		
		#How quickly the game speeds update
		self.speedup_scale = 1.12
		
		self.initialize_dynamic_settings
		
	def initialize_dynamic_settings(self):
		#Initialize dynamic settings
		self.ship_speed_factor = 2.5
		self.bullet_speed_factor = 20.5
		self.alien_speed_factor = 1.5
		
		#fleet direction of 1 represents right. -1 represents left
		self.fleet_direction = 1
		
		#Scoring
		self.alien_points = 100
		
	def increase_speed(self):
		#Increase speed settings
		if self.ship_speed_factor < 15.5:
			self.ship_speed_factor *= self.speedup_scale
			self.bullet_speed_factor *= self.speedup_scale
			self.alien_speed_factor *= self.speedup_scale
			self.alien_points = 100

		
	
	
	
	
	
	
	
