import random
import time
import cv2
import numpy as np
import pyAutogui
import pygetwindow as gw

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def find_image(window_region, template_path):
	screenshot = pyAutogui.screenshot(region=window_region)
	screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
	template = cv2.imread(template_path)
	h, w = template.shape[:2]
	result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
	# Get all positions >= 0.9
	loc = np.where(result >= 0.9)
	pts = list(zip(*loc[::-1]))  # List of tuples (x, y)
	if pts:
		# Randomly select a position among the matches
		top_left = random.choice(pts)
		return (top_left[0] + w // 2, top_left[1] + h // 2)
	else:
		return None

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def wait_for_image(window_region, template_path, timeout=10):
	start_time = time.time()
	while time.time() - start_time < timeout:
		position = find_image(window_region, template_path)
		if position:
			return position
		time.sleep(0.2)  # Wait a bit before retrying
	return None  # Return None if image is not found within the timeout

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def click_position(position):
	if position:
		pyAutogui.click(position[0], position[1])
	else:
		print("Position not found for click.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def click_image(window_region, template_path):
	position = find_image(window_region, template_path)
	if position:
		click_position(position)
	else:
		print(f"Image {template_path} not found on screen.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 0. Find the window and activate it

# 1. Retrieve the window by its exact or partial title
windows = gw.getWindowsWithTitle('Hero Wars | Online action game | RPG')

if windows:
	window = windows[0]

	# Ensure the window is not minimized
	if window.isMinimized:
		window.restore()

	# Bring window to foreground (optional)
	window.activate()
	time.sleep(1.0)

	# 2. Extract coordinates and dimensions: (left, top, width, height)
	window_region = (window.left, window.top, window.width, window.height)

else:
	print("No window found with the specified title.")
	exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 1. Loop

battles = 0
while True:
	battles += 1

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 2. Find the door ("To battle!" flag) or activate the door to be activated

	pos_door = None
	pos_activate = None
	is_activated = False
	start_time = time.time()
	while time.time() - start_time < 20:  # 20-second timeout
		pos_door = wait_for_image(
			window_region, 'screenshots/Door To battle.png', 1
		)
		if pos_door:
			click_position(pos_door)
			print(
				f"{time.strftime('%H:%M:%S')}: Door found,"
				f" starting battle #{battles}."
			)
			break
		if not is_activated:
			pos_activate = wait_for_image(
				window_region, 'screenshots/Button Activate.png', 1
			)
			if pos_activate:
				start_time = time.time()
				click_position(pos_activate)
				pos_collect = wait_for_image(
					window_region, 'screenshots/Button Collect.png', 10
				)
				if pos_collect:
					click_position(pos_collect)
					print("Activation and collection completed.")
					time.sleep(1.0)  # Wait a bit after collection
					is_activated = True
				else:
					print("'Collect' button not found after activation.")
					exit(1)
				continue

	if not pos_door:
		print("Door not found within the timeout.")
		exit(1)

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 3. "Attack" or "Accept this fate" button

	pos_attack = None
	pos_accept = None
	start_time = time.time()
	while time.time() - start_time < 12:  # 12-second timeout
		pos_attack = wait_for_image(
			window_region, 'screenshots/Button Attack.png', 1
		)
		if pos_attack:
			click_position(pos_attack)
			break
		pos_accept = wait_for_image(
			window_region, 'screenshots/Button Accept this fate.png', 1
		)
		if pos_accept:
			click_position(pos_accept)
			break

	if not pos_attack and not pos_accept:
		print(
			"'Attack' or 'Accept this fate' button not found within the timeout."
		)
		exit(1)

	elif pos_accept:
		continue  # Restart the loop after accepting fate

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 4. "To battle" or "Accept this fate" button

	pos_to_battle = None
	pos_accept = None
	start_time = time.time()
	while time.time() - start_time < 12:  # 12-second timeout
		pos_to_battle = wait_for_image(
			window_region, 'screenshots/Button To battle.png', 1
		)
		if pos_to_battle:
			click_position(pos_to_battle)
			break
		pos_accept = wait_for_image(
			window_region, 'screenshots/Button Accept this fate.png', 1
		)
		if pos_accept:
			click_position(pos_accept)
			break

	if not pos_to_battle and not pos_accept:
		print(
			"'To battle' or 'Accept this fate' button not found within the"
			' timeout.'
		)
		exit(1)

	elif pos_accept:
		continue  # Restart the loop after accepting fate

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 5. "To battle" button

	pos_to_battle = wait_for_image(
		window_region, 'screenshots/Button To battle.png', 3
	)
	if pos_to_battle:
		click_position(pos_to_battle)
	else:
		print("'To battle' button not found within the timeout.")
		exit(1)

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 6. "Auto" or "OK" button

	is_Auto_green = False
	pos_Auto = None
	pos_ok = None
	start_time = time.time()
	while time.time() - start_time < 100:  # 100-second timeout
		if not is_Auto_green:
			pos_Auto = wait_for_image(
				window_region, 'screenshots/Button Auto gray.png', 3
			)
			if pos_Auto:
				if (
					find_image(
						window_region, 'screenshots/Button Auto green.png'
					)
					is None
				):
					click_position(pos_Auto)
					is_Auto_green = True
		pos_ok = wait_for_image(window_region, 'screenshots/Button OK.png', 1)
		if pos_ok:
			click_position(pos_ok)
			time.sleep(1.0)  # Wait a bit after clicking OK
			break

	if not pos_Auto and not pos_ok:
		print("'Auto' or 'OK' button not found within the timeout.")
		exit(1)