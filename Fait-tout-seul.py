import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time


#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def trouver_image(region_fenetre, template_path):
	capture = pyautogui.screenshot(region=region_fenetre)
	ecran = cv2.cvtColor(np.array(capture), cv2.COLOR_RGB2BGR)
	template = cv2.imread(template_path)
	h, w = template.shape[:2]
	result = cv2.matchTemplate(ecran, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	print(f"Recherche de l'image {template_path} : max_val = {max_val}, max_loc = {max_loc}")
	if max_val >= 0.9:
		top_left = max_loc
		return (top_left[0] + w // 2, top_left[1] + h // 2)  # Retourne le centre de l'image trouvée
	else:
		return None

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def attendre_image(region_fenetre, template_path, timeout=10):
	start_time = time.time()
	while time.time() - start_time < timeout:
		position = trouver_image(region_fenetre, template_path)
		if position:
			return position
		time.sleep(0.5)  # Attendre un peu avant de réessayer
	return None  # Retourne None si l'image n'est pas trouvée dans le délai imparti

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def clic_position(position):
	if position:
		pyautogui.click(position[0], position[1])
	else:
		print("Position non trouvée pour le clic.")

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

def clic_image(region_fenetre, template_path):
	position = trouver_image(region_fenetre, template_path)
	if position:
		clic_position(position)
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

else:
	print("Aucune fenêtre trouvée avec le titre spécifié.")
	exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 1.	Boucle

boucles = 3
while boucles > 0:
	boucles -= 1

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 2.	Trouver la porte (drapeau « to battle ! »)
# TODO :
# - ajouter un timeout pour éviter une boucle infinie si l'image n'est pas trouvée
# - prévoir de valider la porte et de récupérer l'or

	pos = attendre_image(region_fenetre, 'screenshots/Door To battle.png', 3)
	if pos:
		clic_position(pos)
		print("Porte trouvée.")
	else:
		print("Porte non trouvée dans le délai imparti.")
		exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 3.	Bouton « Attack » ou « Accept this fate »

	pos_Attack = None
	pos_Accept = None
	start_time = time.time()
	while time.time() - start_time < 10:  # Timeout de 10 secondes
		pos_Attack = attendre_image(region_fenetre, 'screenshots/Button Attack.png', 1)
		if pos_Attack:
			clic_position(pos_Attack)
			break
		pos_Accept = attendre_image(region_fenetre, 'screenshots/Button Accept this fate.png', 1)
		if pos_Accept:
			clic_position(pos_Accept)
			break

	if not pos_Attack and not pos_Accept:
		print("Bouton 'Attack' ou 'Accept this fate' non trouvé dans le délai imparti.")
		exit(1)

	elif pos_Accept:
		continue	# Recommence la boucle après avoir accepté le destin

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 4.	Bouton « To battle » ou « Accept this fate »

	pos_ToBattle = None
	pos_Accept = None
	start_time = time.time()
	while time.time() - start_time < 10:  # Timeout de 10 secondes
		pos_ToBattle = attendre_image(region_fenetre, 'screenshots/Button To battle.png', 1)
		if pos_ToBattle:
			clic_position(pos_ToBattle)
			break
		pos_Accept = attendre_image(region_fenetre, 'screenshots/Button Accept this fate.png', 1)
		if pos_Accept:
			clic_position(pos_Accept)
			break

	if not pos_ToBattle and not pos_Accept:
		print("Bouton 'To battle' ou 'Accept this fate' non trouvé dans le délai imparti.")
		exit(1)

	elif pos_Accept:
		continue	# Recommence la boucle après avoir accepté le destin

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 5.	Bouton « To battle »

	pos_ToBattle = attendre_image(region_fenetre, 'screenshots/Button To battle.png', 3)
	if pos_ToBattle:
		clic_position(pos_ToBattle)
	else:
		print("Bouton 'To battle' non trouvé dans le délai imparti.")
		exit(1)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# 6.	Bouton « AUTO » ou « OK »

	AUTO_green = False
	pos_AUTO = None
	pos_OK = None
	start_time = time.time()
	while time.time() - start_time < 100:  # Timeout de 100 secondes
		if not AUTO_green:
			pos_AUTO = attendre_image(region_fenetre, 'screenshots/Button AUTO gray.png', 1)
			if pos_AUTO:
				if trouver_image(region_fenetre, 'screenshots/Button AUTO green.png') is None:
					clic_position(pos_AUTO)
					AUTO_green = True
		pos_OK = attendre_image(region_fenetre, 'screenshots/Button OK.png', 1)
		if pos_OK:
			clic_position(pos_OK)
			time.sleep(2)
			break

	if not pos_AUTO and not pos_OK:
		print("Bouton 'AUTO' ou 'OK' non trouvé dans le délai imparti.")
		exit(1)

