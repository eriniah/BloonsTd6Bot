import pyautogui
import time
import datetime

class Point:
	""" A 2D Point on the screen
	"""

	def __init__(self, x, y):
		""" Create a new point

		Args:
			x: the x coordinate
			y: the y coordinate

		Returns:
			A new point at x,y
		"""
		self.x = x
		self.y = y


class UiInterface:
	""" Common object for interacting with the user interface
	"""

	def move_mouse_to(self, point):
		""" Moves the mouse to the specified point relative to the active window

		Args:
			point: The point to move the mouse to
		"""
		pyautogui.moveTo(point.x, point.y)

	def relative_click(self, point):
		""" Clicks point in the window relative to the window coordinates

		Args:
			point: The relative location to click
		"""
		x = point.x + pyautogui.getActiveWindow().left
		y = point.y + pyautogui.getActiveWindow().top
		self.click(Point(x, y))

	def click(self, point):
		""" Click a point on the screen

		Args:
			point: The point to click as a Point object (x, y)
		"""
		self.move_mouse_to(point)
		time.sleep(0.1)
		pyautogui.click(point.x, point.y)

	def hotkey(self, *keys):
		""" Press a key or key combination

		Args:
			keys: list of keys in the combination to type
		"""
		pyautogui.hotkey(*keys)

	def locateCenterOnScreen(self, img_location):
		""" Locate the center of the provided image on the screen

		Args:
			img_location: The location of the image to search for

		Returns:
			The center of the image location as a Point object or None if not found
		"""
		location = pyautogui.locateCenterOnScreen(img_location)
		return Point(location.x, location.y) if location else None


def create_delay_handler(config):
	""" Create a new delay handler from config
	"""
	return DelayHandler(config['menu_navigate'], config['game_start'], config['in_game_action'])

class DelayHandler:
	""" Handles delays needed to let the UI catch up

	Configured times need to be changed if computer runs slow
	"""

	def __init__(self, menu_navigation_delay, game_start_delay, in_game_action_delay):
		self._menu_navigation_delay = menu_navigation_delay
		self._game_start_delay = game_start_delay
		self._in_game_action_delay = in_game_action_delay
		pass

	def menu_navigation_delay(self):
		""" Wait for the game to navigate menus
		"""
		time.sleep(self._menu_navigation_delay)

	def game_start_delay(self):
		""" Wait for the game to start after hitting play
		"""
		time.sleep(self._game_start_delay)

	def in_game_action_delay(self):
		""" Wait for the game to process an action while in a game
		"""
		time.sleep(self._in_game_action_delay)


class MainMenuNavigator(UiInterface):
	""" Navigator for the main menu (log in screen)
	"""

	def __init__(self, delay_handler):
		""" Create a new Main Menu navigator

		Args:
			delay_handler: Injects delays between actions to let the game catch up

		Returns:
			A new MainMenuNavigator instance
		"""
		self._delay_handler = delay_handler
		self._play_button = self.locateCenterOnScreen('resources/menu/main_menu_play.PNG')

	def play(self):
		""" Click the play button. Opens map navigation

		Returns:
			A MapSelection instance
		"""
		self.relative_click(Point(690, 780))
		self._delay_handler.menu_navigation_delay()
		return MapSelection(self._delay_handler)


class MapSelection(UiInterface):
	""" Class for interacting with the Map Selection view
	"""

	def __init__(self, delay_handler):
		""" Create a new MapSelection instance

		Args:
			delay_handler: The delay handler to inject delays after actions

		Returns:
			A new MapSelection instance

		Raises:
			ValueError: If unable to locate required UI buttons
		"""
		self._delay_handler = delay_handler
		self._next_button = Point(1375, 400)
		self._prev_button = Point(235, 400)

		if not self._next_button or not self._prev_button:
			raise ValueError('Unable to locate next and previous button')

	def _next(self):
		""" Navigate to the next set of maps (right arrow)
		"""
		self.relative_click(self._next_button)

	def _prev(self):
		""" Navigate to the previous set of maps (left arrow)
		"""
		self.relative_click(self._prev_button)

	def select_map(self, map_name):
		""" Select a map that matches the provided image

		Pages through map screens until it finds the map. If found, clicks on it.
		Otherwise nothing happens

		Args:
			map_name: The name of the map

		Returns:
			DifficulyNavigator if success, otherwise None. If None, the page remains on the maps page
		"""
		check = 0
		map_img_location = 'resources/map/' + map_name + '.PNG'
		map_location = self.locateCenterOnScreen(map_img_location)
		while not map_location and check < 10:
			self._next()
			check += 1
			map_location = self.locateCenterOnScreen(map_img_location)
		if not map_location:
			print('Failed to locate map "' + map_name + '"')
			return None
		self.click(map_location)
		self._delay_handler.menu_navigation_delay()
		return DifficulyNavigator(self._delay_handler)

	def back_to_main_menu(self):
		""" Navigate back to the main menu

		Returns:
			A MainMenuNavigator instance
		"""
		self.hotkey('escape')
		self._delay_handler.menu_navigation_delay()
		return MainMenuNavigator()


class DifficulyNavigator(UiInterface):
	""" Navigator for the difficulty selection screen

	Select a difficulty to play the map on
	"""

	def __init__(self, delay_handler):
		""" Create a new difficulty manager

		Args:
			delay_handler: Injects delays after UI operations to let the game catch up

		Returns:
			A new DifficultyManager instance

		Raises:
			ValueError: If unable to locate required UI buttons
		"""
		self._delay_handler = delay_handler
		self._easy_button = self.locateCenterOnScreen('resources/difficulty/diff_easy.PNG')
		self._medium_button = self.locateCenterOnScreen('resources/difficulty/diff_medium.PNG')
		self._hard_button = self.locateCenterOnScreen('resources/difficulty/diff_hard.PNG')

		if not self._easy_button or not self._medium_button or not self._hard_button:
			raise ValueError('Unable to find all difficulty buttons')

	def select(self, difficulty, mode):
		""" Select the difficulty and game mode

		Args:
			difficulty: easy, medium or hard
			mode: standard, deflation, etc.

		Returns:
			GameInterface instance or None if there was an issue
		"""
		if difficulty == 'easy':
			self.click(self._easy_button)
		elif difficulty == 'medium':
			self.click(self._medium_button)
		elif difficulty == 'hard':
			self.click(self._hard_button)
		else:
			print('Unknown difficulty "' + difficulty + '"')
			return None
		self._delay_handler.menu_navigation_delay()

		# mode_button = self.locateCenterOnScreen('resources/difficulty/mode_' + mode + '.PNG')
		# TODO: assuming deflation
		mode_button = Point(1075, 400)
		if not mode_button:
			print('Unable to find mode "' + mode + '" under difficulty "' + difficulty + '"')
			return None
		self.relative_click(mode_button)
		self._delay_handler.game_start_delay()

		# Some game modes have a notification at the beginning. Acknowledge it
		ok_button = Point(800, 670)
		self.relative_click(ok_button)
		self._delay_handler.menu_navigation_delay()

		return GameInterface(self._delay_handler)


# dict of towers to hotkeys
tower_types = {
	'hero': 'u',
	'dart_monkey': 'q',
	'boomerang_monkey': 'w',
	'bomb_shooter': 'e',
	'tack_shooter': 'r',
	'ice_monkey': 't',
	'glue_gunner': 'y',
	'sniper_monkey': 'z',
	'monkey_sub': 'x',
	'monkey_buccaneer': 'c',
	'monkey_ace': 'v',
	'heli_pilot': 'b',
	'mortar_monkey': 'n',
	'dartling_gunner': 'm',
	'wizard_monkey': 'a',
	'super_monkey': 's',
	'ninja_monkey': 'd',
	'alchemist': 'f',
	'druid': 'g',
	'banana_farm': 'h',
	'engineer_monkey': 'l',
	'spike_factory': 'j',
	'monkey_village': 'k'
}


class GameInterface(UiInterface):
	""" Class for interacting with bloons while in a game
	"""

	def __init__(self, delay_handler):
		self._delay_handler = delay_handler

	def place_tower(self, tower_type, location):
		""" Place a new tower

		Args:
			tower_type: The type of tower to place

		Returns:
			A Tower instance for the new tower
		"""
		print("Placing {}".format(tower_type))
		self.hotkey(tower_types[tower_type])
		self._delay_handler.in_game_action_delay()
		self.relative_click(location)
		self._delay_handler.in_game_action_delay()
		return TowerInterface(self._delay_handler, tower_type, location)

	def start(self):
		# Twice start and activate FF
		self.hotkey('space')
		self._delay_handler.in_game_action_delay()
		self.hotkey('space')
		self._delay_handler.in_game_action_delay()


upgrade_hotkeys = [',', '.', '/']
# targets for most towers
tower_targets = [
	'first',
	'last',
	'close',
	'strong'
]

class TowerInterface(UiInterface):
	""" Represents a single tower on the map
	"""

	def __init__(self, delay_handler, tower_type, location):
		""" Create a new tower

		Args:
			delay_handler: Inject delays for UI operations
			tower_type: The type of the tower as a string
			location: The x, y location of the tower as a Point object

		Returns:
			The new tower instance
		"""
		self._delay_handler = delay_handler
		self.tower_type = tower_type
		self.location = location
		self.upgrades = [0, 0, 0]

	def upgrade(self, *paths):
		""" Upgrade a monkey

		Args:
			paths: A tuple of paths to upgrade the monkey on. 1, 2 or 3 ex: (1, 1) would put to points into the top tree
		"""
		self.relative_click(self.location)
		self._delay_handler.in_game_action_delay()
		for path in paths:
			print("Upgrading {} ability {}".format(self.tower_type, path))
			self.upgrades[path - 1] += 1
			self.hotkey(upgrade_hotkeys[path - 1])
			self._delay_handler.in_game_action_delay()
		self.hotkey('escape')
		self._delay_handler.in_game_action_delay()

	def target(self, target):
		""" Change target

		Args:
			target: Change target
		"""
		print("Targeting {}".format(target))

		# Naive implementation that only supports setting once
		index = None
		for i, t in enumerate(tower_targets):
			if t == target:
				index = i

		if not index:
			print("Target {} not found".format(target))
			return

		self.relative_click(self.location)
		self._delay_handler.in_game_action_delay()
		for i in index:
				self.hotkey('tab')
				self._delay_handler.in_game_action_delay()

		self.hotkey('escape')
		self._delay_handler.in_game_action_delay()
