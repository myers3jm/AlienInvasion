import sys
from time import sleep
import scores
import pygame
from bullet import Bullet
from alien import Alien
import game_stats as stats
import tkinter
from tkinter import *
import operator

def get_number_aliens_x(ai_settings, alien_width):
	#Determine the number of aliens that will fit in a row
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	#Determine the number of rows of aliens that fit on the screen
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	#Create an alien and place it in the row
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	#Create a full fleet of aliens
	#Create an alien and find the number of aliens in a row
	#Spacing between each alien is equal to one alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#Create the fleet
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#Create an alien and place it in the row
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	#Respond to keypresses
	if event.key == pygame.K_d:
		ship.moving_right = True
	elif event.key == pygame.K_a:
		ship.moving_left = True
	elif event.key == pygame.K_ESCAPE:
		pygame.quit()
		sys.exit()
	elif event.key == pygame.K_SPACE:
		ship.firing = True

def check_keyup_events(event, ship):
	#Respond to key releases
	if event.key == pygame.K_d:
		ship.moving_right = False
	elif event.key == pygame.K_a:
		ship.moving_left = False
	elif event.key == pygame.K_SPACE:
		ship.firing = False
		
def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
	#Respond to keypresses and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
			
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	#Start a new game if the player clicks Play
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and stats.game_active == False:
		
		#Reset the game settings
		ai_settings.initialize_dynamic_settings()
		
		#Hide mouse cursor
		pygame.mouse.set_visible(False)
	
		#Reset game stats
		stats.reset_stats()
		stats.game_active = True
		
		#Empty list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	#Update images on the screen and flip to the new screen
	#Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)
	
	#Draw the score information
	sb.show_score("alive")
	
	#Draw the play button if the game is inactive
	if stats.game_active == False:
		play_button.draw_button()

	#Make the most recently drawn screen visible
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#Update position of bullets and get rid of old bullets
	#Update bullet positions
	bullets.update()

	#Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)
	
def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#Respond to alien/bullet collisions
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		#Destroy existing bullets, speed up the game, and create a new fleet
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens):
	#Respond appropriately if any aliens have reached an edge
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	#Drop the entire fleet and change the fleet's direction
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	#Respond to the ship being hit by an alien
	if stats.ships_left > 0:
		#Decrement ships left
		stats.ships_left -= 1
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		#Pause
		sleep(0.5)
	
	else:
		name_Enter = TextEntry(stats.score)
		name_Enter.run(name_Enter)
		stats.reset_stats()
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	#Check if any aliens hit the bottom of the screen
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Treat this as if a ship got hit
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
				
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	#Check if the fleet is at an edge, then update the positions of all aliens in the fleet
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#Look for alien/ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	
	#Look for aliens hitting the bottom of the screen
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
	#Check to see if there's a new high score
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score(True)

class Title(Frame):
	def __init__(self, parent = None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.title()
	def title(self):
		self.winfo_toplevel().title("Player Name")
		
class TextEntry():
	def __init__(self, score):
		#Initialize all variables
		self.score = score
		
	def make_assets(self):
		#Create new Tkinter window
		self.root = Tk()
		self.root.iconbitmap("images/alien.png")
		title = Title(self.root)
		
		#Create Tk Frames
		self.topF = Frame(self.root)
		self.topF.grid(row = 0, column = 0)
		self.botF = Frame(self.root)
		self.botF.grid(row = 0, column = 0)
		
		#Create TextEntry assets
		self.namelabel = Label(self.topF, text = "Player Name: ")
		self.namelabel.grid(row = 0, column = 0)
		self.nameEntry = Entry(self.topF)
		self.nameEntry.grid(row = 0, column = 1)
		self.nameEntry.focus_force()
		
	def done(self):
		file = open("scores.py", "+a")
		self.nameScore = ("{'name':'" + str(self.nameEntry.get()) + "', 'score': " + str(int(self.score)) + "}")
		file.write("\nscores.append(" + self.nameScore + ")")
		file.write("\nscores = sorted(scores, key=lambda k: k['score'], reverse=True)\n \n")
		file.close()
		print("done")
		self.root.destroy()
		
	def button(self):
		self.goButton = Button(self.topF, text = "Enter", command = self.done)
		self.goButton.grid(row = 2, column = 0)	
		
		self.root.mainloop()

	def run(self, title):
		title.make_assets()
		title.button()
