from scores import scores

class GameStats():
	#Track statistics for Alien Invasion
	
	def __init__(self, ai_settings):
		#Initialize statistics
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#start alien invasion in an inactive state
		self.game_active = False
		
		#High score should never be reset
		self.high_score = scores[0]["score"]
		self.high_score_name = scores[0]["name"] + " - "
		
	def reset_stats(self):
		#Initialize statistics that can change during the game
		self.ships_left = 3
		#self.ai_settings.ship_limit
		self.score = 0
