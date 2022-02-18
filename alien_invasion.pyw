import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf
import game_stats as stats

ai_settings = Settings()
stats = GameStats(ai_settings)

def run_game():
	#Initialize game and create a screen object
	pygame.init()
	ai_settings = Settings()
	scale_factor = 0.75
	screen = pygame.display.set_mode((1920*scale_factor, 1080*scale_factor))
	pygame.display.set_caption("Alien Invasion")
	surface = pygame.image.load("images/alien.png")
	pygame.display.set_icon(surface)
	
	#Set background color
	bg_color = (230, 230, 230)

	#Make the play button
	play_button = Button(ai_settings, screen, "Play")

	#Make a ship, a group of bullets, and a group of aliens
	bullets = Group()
	aliens = Group()
	ship = Ship(ai_settings, screen, bullets)


	#Create a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)

	#Create an instance to store game stats and create a scoreboard
	sb = ScoreBoard(ai_settings, screen, stats)

	#Start the main loop for the game.
	while True:
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen,stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
