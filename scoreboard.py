import scores
import game_stats as stats
import pygame.font

class ScoreBoard():
#A class to report scoring information
	
	def __init__(self, ai_settings, screen, stats):
		#Initialize scorekeeping attributes
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
				
		#Font settings for scoring information
		self.text_color = 230, 0, 0
		self.font = pygame.font.Font("VT323-Regular.ttf", 48)
		
		#Prepare the initial score images
		self.prep_score()
		self.prep_high_score(False)
		
	def prep_score(self):
		#Turn the score into a rendered image
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
				
		#Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 0

	def prep_high_score(self, current):
		#Turn the high score into a rendered image
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		high_score_name = self.stats.high_score_name
		if current:
			self.high_score_image = self.font.render("Current Player " + high_score_str, True, self.text_color, self.ai_settings.bg_color)
		if not current:
			self.high_score_image = self.font.render(high_score_name + high_score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#Center the high score at the top of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
			
	def show_score(self, state):
		if state != "dead":
			#Draw score to the screen if the score is not reset
			self.screen.blit(self.score_image, self.score_rect)
			self.screen.blit(self.high_score_image, self.high_score_rect)
			#Render the ships left
			for x in range(self.stats.ships_left):
				render_image("spaceshipTiny.png", self.screen, x)
					
		else:
			#Draw the score as 0 if the score needs reset
			stats.reset_stats()
			self.screen.blit(self.score_image, self.score_rect)
				
def render_text(text, screen, x, y):
	font = pygame.font.Font("VT323-Regular.ttf", 48)
	textstr = font.render(str(text), True, (0, 0, 0))
	textstr_rect = textstr.get_rect()
	screen.blit(textstr, textstr_rect)

def render_image(image, screen, x):
	image = pygame.image.load("images/" + image)
	image_rect = image.get_rect()
	screen.blit(image, (23 * x, 0))
	
	
	
	
	
	
	
	
	
	
	
	
			
