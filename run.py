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

def play(delay_handler, map_strategy):
	print('Starting map {} at {}'.format(map_strategy['map'], str(datetime.datetime.now())))
	game = MainMenuNavigator(delay_handler).play()\
		.select_map(map_strategy['map'])\
		.select(map_strategy['difficulty'], map_strategy['mode'])

	for tower_config in map_strategy['towers']:
		tower = game.place_tower(tower_config['tower'], Point(tower_config['location']['x'], tower_config['location']['y']))
		if 'upgrades' in tower_config:
			tower.upgrade(*list(map(lambda x: x['path'], tower_config['upgrades'])))

		if 'target' in tower_config:
			tower.target(tower_config['target'])

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
	parser.add_argument('map_strategy')
	parser.add_argument('--system-config', dest='system_config', default='./system.json')
	args = parser.parse_args()

	delay_handler = None
	with open(args.system_config, 'r') as config_file:
		system_config = json.load(config_file)
		delay_handler = create_delay_handler(system_config['delays'])

	with open(args.map_strategy, 'r') as config_file:
		map_strategy = json.load(config_file)

	time.sleep(5)
	count = 1
	while True:
		print('Game: ' + str(count))
		play(delay_handler, map_strategy)
		count += 1
