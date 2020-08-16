import pyautogui
import time
import datetime

def click(point):
	""" Click a point on the screen

	Args:
		point: The point to click as a Point object (x, y)
	"""
	pyautogui.click(point.x, point.y)


class MainMenuNavigator():
	""" Navigator for the main menu (log in screen)
	"""

	def __init__(self):
		self._play_button = pyautogui.locateCenterOnScreen('resources/menu/main_menu_play.PNG')

	def play(self):
		click(self._play_button)
		time.sleep(0.5)
		return MapNavigator()


class DifficulyNavigator():
	""" Navigator for the difficulty selection screen

	Select a difficulty to play the map on
	"""

	def __init__(self):
		self._easy_button = pyautogui.locateCenterOnScreen('resources/difficulty/diff_easy.PNG')
		self._medium_button = pyautogui.locateCenterOnScreen('resources/difficulty/diff_medium.PNG')
		self._hard_button = pyautogui.locateCenterOnScreen('resources/difficulty/diff_hard.PNG')

		if not self._easy_button or not self._medium_button or not self._hard_button:
			raise ValueError('Unable to find all difficulty buttons')


	def _standard(self):
		self._click(pyautogui.locateCenterOnScreen('resources/difficulty/mode_standard.PNG'))

	def easy(self):
		click(self._easy_button)
		time.sleep(0.5)
		self._standard()

	def medium(self):
		click(self._medium_button)
		time.sleep(0.5)
		self._standard()

	def hard(self):
		click(self._hard_button)
		time.sleep(0.5)
		self._standard()

	def deflation(self):
		click(self._easy_button)
		time.sleep(0.5)
		click(pyautogui.locateCenterOnScreen('resources/difficulty/mode_deflation.PNG'))


class MapNavigator():

	def __init__(self):
		self._next_button = pyautogui.locateCenterOnScreen('resources/menu/menu_next.PNG')
		self._prev_button = pyautogui.locateCenterOnScreen('resources/menu/menu_prev.PNG')

		if not self._next_button or not self._prev_button:
			raise ValueError('Unable to locate next and previous button')

	def next(self):
		pyautogui.click(self._next_button.x, self._next_button.y)

	def prev(self):
		pyautogui.click(self._prev_button.x, self._prev_button.y)

	def select_map(self, map_img_location):
		""" Select a map that matches the provided image

		Args:
			map_img_location: The location of the image to search for on the screen

		Returns:
			DifficulyNavigator if success, otherwise None. If None, the page remains on the maps page
		"""
		check = 0
		map_location = pyautogui.locateCenterOnScreen(map_img_location)
		while not map_location and check < 10:
			self.next()
			check+=1
			map_location = pyautogui.locateCenterOnScreen(map_img_location)
		pyautogui.click(map_location.x, map_location.y)
		time.sleep(0.5)
		return DifficulyNavigator()

def action_wait():
	time.sleep(0.05)
	pass

def play_game():
	MainMenuNavigator().play().select_map('resources/map/dark_castle.PNG').deflation()
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen('resources/menu/menu_ok.PNG'))
	time.sleep(2)
	window = pyautogui.getWindowsWithTitle(title='BloonsTD6')[0]

	pyautogui.hotkey('u')
	action_wait()
	x = window.left + 600
	y = window.top + 380
	pyautogui.moveTo(x, y)
	pyautogui.click(x, y, duration=0.05)
	action_wait()

	# Super Monkey
	pyautogui.hotkey('s')
	action_wait()
	x = window.left + 685
	y = window.top + 380
	pyautogui.moveTo(x, y)
	pyautogui.click(x, y, duration=0.05)
	action_wait()
	pyautogui.click(x, y, duration=0.05)
	action_wait()
	pyautogui.hotkey(',')
	action_wait()
	pyautogui.hotkey(',')
	action_wait()
	pyautogui.hotkey('/')
	action_wait()
	pyautogui.hotkey('/')
	action_wait()
	pyautogui.hotkey('/')
	action_wait()

	# Ninja Monkey
	pyautogui.hotkey('d')
	action_wait()
	x = window.left + 770
	y = window.top + 380
	pyautogui.moveTo(x, y)
	pyautogui.click(x, y, duration=0.05)
	action_wait()
	pyautogui.click(x, y, duration=0.05)
	action_wait()
	pyautogui.hotkey(',')
	action_wait()
	pyautogui.hotkey(',')
	action_wait()
	pyautogui.hotkey(',')
	action_wait()
	pyautogui.hotkey('/')
	action_wait()
	pyautogui.hotkey('/')
	action_wait()

	# Start the game
	pyautogui.hotkey('escape')
	action_wait()
	print('Start: ' + str(datetime.datetime.now()))
	pyautogui.hotkey('space')
	action_wait()
	pyautogui.hotkey('space')
	action_wait()

	# Sleep for 7 minutes since that is how long this map takes
	count = 7
	while count > 0:
		time.sleep(60)
		# Check for level up screen, if found dismiss, continue and add a minute
		level_up = pyautogui.locateCenterOnScreen('resources/menu/level_up.PNG')
		if level_up:
			click(level_up)
			time.sleep(1)
			click(level_up)
			time.sleep(1)
			pyautogui.hotkey('space')
			action_wait()
			pyautogui.hotkey('space')
			action_wait()
			count += 7 # Not sure if ff is automatically on so add double the time in case if running on normal speed
		else:
			# Only count down if no level up. Makes up for lost time sitting on confirmation screen
			count -= 1

	# Navigate back to main menu
	click(pyautogui.locateCenterOnScreen('resources/menu/next.PNG'))
	time.sleep(1)
	click(pyautogui.locateCenterOnScreen('resources/menu/home.PNG'))
	time.sleep(5)
	print('End: ' + str(datetime.datetime.now()))

if __name__ == "__main__":
	print('Open Bloons TD6 within 5 seconds...')
	time.sleep(5)
	count = 1
	while True:
		print('Game: ' + str(count))
		play_game()
		count += 1
