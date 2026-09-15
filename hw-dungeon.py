import random
import time
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def find_image(window_region, template_path):
	screenshot = pyautogui.screenshot(region=window_region)
	screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
	template = cv2.imread(template_path)
	if template is None:
		print(f"Template image {template_path} not found.")
		return None
	h, w = template.shape[:2]
	result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
	# Get all positions >= 0.9
	loc = np.where(result >= 0.9)
	if pts := list(zip(*loc[::-1])): # List of tuples (x, y)
		# Randomly select a position among the matches
		top_left = random.choice(pts)
		return (top_left[0] + w // 2, top_left[1] + h // 2)
	else:
		return None

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def wait_for_image(window_region, template_path, timeout=10):
	start_time = time.time()
	while time.time() - start_time < timeout:
		if position := find_image(window_region, template_path):
			return position
		time.sleep(0.2)  # Wait a bit before retrying
	return None  # Return None if image is not found within the timeout

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def click_position(position):
	if position:
		pyautogui.click(position[0], position[1])
	else:
		print("Position not found for click.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def click_image(window_region, template_path):
	if position := find_image(window_region, template_path):
		click_position(position)
	else:
		print(f"Image {template_path} not found on screen.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 0. Find the window and activate it

# Retrieve the window by its exact or partial title
if windows := gw.getWindowsWithTitle('Hero Wars | Online action game | RPG'):
	window = windows[0]

	# Ensure the window is not minimized
	if window.isMinimized:
		window.restore()

	# Bring window to foreground (optional)
	window.activate()
	time.sleep(1.0)

	# Extract coordinates and dimensions: (left, top, width, height)
	window_region = (window.left, window.top, window.width, window.height)

else:
	print("No window found with the specified title.")
	exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 1. Divination Cards
if pos_oracle := wait_for_image(window_region, 'screenshots/Button Oracle\'s Trials.png', 1):
	click_position(pos_oracle)

	while pos_claim := wait_for_image(window_region, 'screenshots/Button Claim Divination Card.png', 2):
		click_position(pos_claim)
		time.sleep(0.5)  # Wait a bit after clicking claim

	if pos_close := wait_for_image(window_region, 'screenshots/Button Close Oracle\'s Trials.png', 1):
		click_position(pos_close)
		time.sleep(0.5)  # Wait a bit after clicking close
	else:
		print("'Close' button not found after claiming divination cards.")
		exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 2. Loop

battles = 0
retries = 0
door_found = None
while True:
	battles += 1

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 3. Find the door ("To battle!" flag) or activate the door to be activated

	pos_door = None
	pos_activate = None
	is_activated = False
	start_time = time.time()
	while time.time() - start_time < 20:  # 20-second timeout
		door_priority = door_found is not None and (battles - door_found) % 10 == 0
		if (not door_priority or is_activated) and (pos_door := wait_for_image(window_region, 'screenshots/Door To battle.png', 1)):
			click_position(pos_door)
			print(
				f"{time.strftime('%Y-%m-%d %H:%M:%S')}: Door found,"
				f" starting battle #{battles}."
			)
			break
		if not is_activated:
			if pos_activate := wait_for_image(window_region, 'screenshots/Button Activate.png', 1):
				door_found = battles  # Record the battle number when the door was found
				start_time = time.time()
				click_position(pos_activate)
				if pos_collect := wait_for_image(window_region, 'screenshots/Button Collect.png', 10):
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
	# 4. "Attack" or "Accept this fate" button

	pos_attack = None
	pos_accept = None
	start_time = time.time()
	while time.time() - start_time < 12:  # 12-second timeout
		if pos_attack := wait_for_image(window_region, 'screenshots/Button Attack.png', 1):
			click_position(pos_attack)
			break
		if pos_accept := wait_for_image(window_region, 'screenshots/Button Accept this fate.png', 1):
			click_position(pos_accept)
			break

	if not pos_attack and not pos_accept:
		print("'Attack' or 'Accept this fate' button not found within the timeout.")
		retries += 1
		if retries >= 3:
			exit(1)
		print(f"Retrying... Attempt {retries} of 3.")
		battles -= 1  # Decrement battles count since this attempt failed
		continue

	elif pos_accept:
		continue  # Restart the loop after accepting fate

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 5. "To battle" or "Accept this fate" button

	retries = 0
	pos_to_battle = None
	pos_accept = None
	start_time = time.time()
	while time.time() - start_time < 12:  # 12-second timeout
		if pos_to_battle := wait_for_image(window_region, 'screenshots/Button To battle.png', 1):
			click_position(pos_to_battle)
			break
		if pos_accept := wait_for_image(window_region, 'screenshots/Button Accept this fate.png', 1):
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
	# 6. "To battle" button

	if pos_to_battle := wait_for_image(window_region, 'screenshots/Button To battle.png', 3):
		click_position(pos_to_battle)
	else:
		print("'To battle' button not found within the timeout.")
		exit(1)

	#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
	# 7. "Auto" or "OK" button

	Auto_is_green = False
	pos_Auto = None
	pos_ok = None
	start_time = time.time()
	while time.time() - start_time < 100:  # 100-second timeout
		if not Auto_is_green:
			if pos_Auto := wait_for_image(window_region, 'screenshots/Button Auto gray.png', 3):
				if find_image(window_region, 'screenshots/Button Auto green.png') is None:
					click_position(pos_Auto)
					Auto_is_green = True
		if pos_ok := wait_for_image(window_region, 'screenshots/Button OK.png', 1):
			click_position(pos_ok)
			time.sleep(1.0)  # Wait a bit after clicking OK
			break

	if not pos_Auto and not pos_ok:
		print("'Auto' or 'OK' button not found within the timeout.")
		exit(1)