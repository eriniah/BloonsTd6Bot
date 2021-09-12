#!/usr/bin/env python
import argparse
import json
import time
import datetime
from src.ui_interface import create_delay_handler, MainMenuNavigator, Point


def event_collect_monkey(game, resource):
	monkey = game.locateCenterOnScreen(resource)
	while monkey:
		print('Collected a monkey')
		game.click(monkey)
		time.sleep(5)
		game.click(monkey)
		time.sleep(2)
		monkey = game.locateCenterOnScreen(resource)

def collect_event(game):
	event_collect = game.locateCenterOnScreen('resources/event/collect.PNG')
	if event_collect:
		print('Event detected')
		game.click(event_collect)
		time.sleep(2)
		event_collect_monkey(game, 'resources/event/mystery_monkey_green.PNG')
		event_collect_monkey(game, 'resources/event/mystery_monkey_blue.PNG')
		event_collect_monkey(game, 'resources/event/mystery_monkey_purple.PNG')
		# Click anywhere
		game.click(event_collect)
		time.sleep(2)
		game.hotkey('escape')
	time.sleep(4)

def play(delay_handler):
	print('Start: ' + str(datetime.datetime.now()))
	game = MainMenuNavigator(delay_handler).play()\
		.select_map('dark_castle')\
		.select('easy', 'deflation')

	hero = game.place_tower('hero', Point(600, 380))

	super_monkey = game.place_tower('super_monkey', Point(685, 380))
	super_monkey.upgrade(1, 1, 3, 3, 3)

	ninja_monkey = game.place_tower('ninja_monkey', Point(770, 380))
	ninja_monkey.upgrade(1, 1, 1, 3, 3)

	spike_factory = game.place_tower('spike_factory', Point(1275, 480))
	# spike_factory.upgrade(3)

	farm_monkey = game.place_tower('mortar_monkey', Point(770, 680))
	# place mortar target
	game.relative_click(Point(600, 540))

	game.start()

	while True:
		time.sleep(10)
		# Check for level up screen, if found dismiss, continue and add a minute
		level_up = game.locateCenterOnScreen('resources/menu/level_up.PNG')
		success_next = game.locateCenterOnScreen('resources/menu/next.PNG')
		if level_up:
			print('Leveled up!')
			game.click(level_up)
			time.sleep(1)
			game.click(level_up)
			time.sleep(1)
			game.hotkey('space')
			delay_handler.in_game_action_delay()
		elif success_next:
			game.click(success_next)
			time.sleep(1)
			game.click(game.locateCenterOnScreen('resources/menu/home.PNG'))
			time.sleep(2)
			break

	time.sleep(5)
	collect_event(game)

	print('End: ' + str(datetime.datetime.now()))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('MAP_STRATEGY')
	parser.add_argument('--system-config', dest='system_config', default='./system.json')
	args = parser.parse_args()

	delay_handler = None
	with open(args.system_config, 'r') as config_file:
		system_config = json.load(config_file)
		delay_handler = create_delay_handler(system_config['delays'])

	time.sleep(5)
	count = 1
	while True:
		print('Game: ' + str(count))
		play(delay_handler)
		count += 1
