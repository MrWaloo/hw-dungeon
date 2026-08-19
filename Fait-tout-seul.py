import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def clic_image(region_fenetre, template_path):
	capture = pyautogui.screenshot(region=region_fenetre)
	ecran = cv2.cvtColor(np.array(capture), cv2.COLOR_RGB2BGR)
	template = cv2.imread(template_path)
	h, w = template.shape[:2]
	result = cv2.matchTemplate(ecran, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	if max_val >= 0.8:
		top_left = max_loc
		clic_x = top_left[0] + w // 2
		clic_y = top_left[1] + h // 2
		pyautogui.click(clic_x, clic_y)

	else:
		print(f"Image {template_path} non trouvée sur l'écran.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 0. Trouver la fenêtre et l'activer

# 1. Récupération de la fenêtre par son titre exact ou partiel
fenetres = gw.getWindowsWithTitle('Hero Wars | Online action game | RPG')

if fenetres:
	fenetre = fenetres[0]

	# S'assurer que la fenêtre n'est pas réduite
	if fenetre.isMinimized:
		fenetre.restore()

	# Mettre la fenêtre au premier plan (optionnel)
	fenetre.activate()
	time.sleep(1.0)

	# 2. Extraction des coordonnées et dimensions : (left, top, width, height)
	region_fenetre = (fenetre.left, fenetre.top, fenetre.width, fenetre.height)

	# 3. Capture de la zone de la fenêtre

else:
	print("Aucune fenêtre trouvée avec le titre spécifié.")
	exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 1.	Trouver la porte (héro ou titan ou drapeau « to battle ! »)

clic_image(region_fenetre, 'screenshots/Door to battle.png')
time.sleep(1.0)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 2.	Bouton « Attack » ou éventuellement choisir une équipe de titans

clic_image(region_fenetre, 'screenshots/Button Attack.png')
time.sleep(1.0)
