# hw-dungeon

Ce script python permet d'automatiser les combats du donjon dans le jeu Hero Wars.

Il fonctionne sous Windows 11.  
Il s'appuie sur la reconnaissance des captures d'écran partielles dans le répertoire "screenshots" pour savoir où cliquer sur l'écran.  
Ces captures faites tiennent compte de la taille de la fenêtre du jeu. Les captures fournies avec le script sont faites pour une version en anglais sur un écran de résolution 2560 * 1440 (2K) avec la fenêtre du jeu maximisée :

![Capture de l'écran](documentation/Screen%202K.png)

Si votre configuration est différente, il faudra refaire les captures et remplacer les fichiers dans le répertoire "screenshots".

## Prérequis

1. [Installer python](https://learn.microsoft.com/en-us/windows/dev-environment/python?tabs=winget) sauf si vous avez déjà python sur votre machine. Le script a été développé avec python3.13 mais peut fonctionner avec une version supérieure sans problème.

2. Télécharger ce projet depuis le dépôt github :
- bouton "<> Code"
- "Download ZIP"

![Download ZIP](documentation/Download%20ZIP.png)

3. Extraire le fichier ZIP dans un répertoire sur votre PC. Ce répertoire sera le "répertoire du script" dans le reste de cette documentation. Dans mon exemple ce sera la répertoire `D:\Documents\github\hw-dungeon`.

4. Tester si python est correctement installé et fonctionne, pour cela dans le répertoire du script, faire un clic-droit et sélectionner "Ouvrir dans le Terminal". Une fenêtre PowerShell s'ouvre :

![Fenêtre PowerShell ](documentation/PowerShell.png)

Dans cette fenêtre taper `python --version`. Quelque chose de ce genre doit être retourné :
```shell
PS D:\Documents\github\hw-dungeon> python --version
Python 3.13.11
PS D:\Documents\github\hw-dungeon>
```

5. Afin d'isoler le script dans un environnement dédié, créer un venv. Dans la fenêtre PowerShell, taper ces lignes les unes après les autres en attendant que la ligne précédente ait terminé :
```
python -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt
```

Ces trois lignes font ceci :
- créer un venv dans le répertoire "venv" (rapide)
- mettre le module "pip" du venv à jour (rapide)
- installer les modules python nécessaires au bon fonctionnement du script (long)

--> À partir d'ici, si tout s'est déroulé sans erreur, le script est exécutable.

## Exécution du script

Le script est limité au donjon de Hero Wars. Il faut démarrer le jeu et aller jusqu'au donjon :

![Donjon](documentation/Dongeon.png)

Remarques :
- C'est à vous de débloquer les cartes de divination, le script ne le fera pas. Si des cartes de divination sont disponibles, elles seront utilisées.
- Les équipes doivent être faites, attention à reformer les équipes dont des membres ont été tués un jour précédent.
- La fenêtre du jeu doit être visible durant l'exécution du script.
- Si leu jeu est lancé dans un onglet de navigateur, l'onglet doit être activé.
- Le PC devient inutilisable lorsque le script est lancé parce qu'il va cliquer dans le fenêtre du jeu.
- Pour stopper le script, il faut diminuer la fenêtre du jeu afin que le script ne trouve pas le prochain bouton ou faire la combinaison CTRL+C dans le fenêtre PowerShell, ce qui stoppera le script avec une erreur sans gravité.

Dans le répertoire du script, faire un clic-droit et sélectionner "Ouvrir dans le Terminal". Dans la fenêtre PowerShell taper :
```shell
venv\Scripts\python hw-dungeon.py
```

Le script s'exécutera jusqu'à ce qu'il soit stoppé avec CTRL+C ou jusqu'à ce qu'il ne trouve pas le prochain bouton dans un certain laps de temps.

## Fonctionnement

Vous pouvez lire le code du script et le modifier à votre guise. Si vous l'améliorez, merci de proposer une PR sur le dépôt github [MrWaloo/hw-dungeon](https://github.com/MrWaloo/hw-dungeon).

Au début, le script recherche une fenêtre dont le titre est "Hero Wars | Online action game | RPG" et active cette fenêtre si trouvée.

Puis le script boucle sur les actions suivantes :

### 1ère étape

|  |  |  |
| -- | -- | -- |
| Clic au-dessus de la porte du donjon | screenshots/Door To battle.png | ![](screenshots/Door%20To%20battle.png) |
| OU |  |  |
| Clic sur l'activation de l'étage du donjon | screenshots/Button Activate.png | ![](screenshots/Button%20Activate.png) |
| Attente et clic sur le bouton "Collect" | screenshots/Button Collect.png | ![](screenshots/Button%20Collect.png) |

### 2ème étape

|  |  |  |
| -- | -- | -- |
| Clic sur un bouton "Attack" | screenshots/Button Attack.png | ![](screenshots/Button%20Attack.png) |
| OU |  |  |
| Clic sur le bouton "Accept this fate!" | screenshots/Button Accept this fate.png | ![](screenshots/Button%20Accept%20this%20fate.png) |

Remarques :  
- Il arrive qu'il faille choisir entre deux équipes de titans, le script clic aléatoirement sur un des deux boutons.
- Si c'est le bouton "Accept this fate!" qui a été cliqué, le script reprend la boucle depuis le début.

### 3ème étape

|  |  |  |
| -- | -- | -- |
| Clic sur le bouton "To battle!" | screenshots/Button To battle.png | ![](screenshots/Button%20To%20battle.png) |
| OU |  |  |
| Clic sur le bouton "Accept this fate!" | screenshots/Button Accept this fate.png | ![](screenshots/Button%20Accept%20this%20fate.png) |

Remarque :  
- Si c'est le bouton "Accept this fate!" qui a été cliqué, le script reprend la boucle depuis le début.

### 4ème étape

|  |  |  |
| -- | -- | -- |
| Clic sur le bouton "To battle!" | screenshots/Button To battle.png | ![](screenshots/Button%20To%20battle.png) |

Remarque :
- Le combat commence après le chargement

### 5ème étape : le combat

|  |  |  |
| -- | -- | -- |
| Activation du mode "AUTO" | screenshots/Button AUTO gray.png | ![](screenshots/Button%20Auto%20gray.png) |
| Vérification du mode "AUTO" | screenshots/Button AUTO green.png | ![](screenshots/Button%20Auto%20green.png) |
| Puis... |  |  |
| Clic sur le bouton "OK" | screenshots/Button OK.png | ![](screenshots/Button%20OK.png) |

Remarque :  
- Le script reprend la boucle depuis le début.

## Adaptation des captures à votre résolution

Si le script ne trouve pas les bouton sur lesquels cliquer, c'est que les captures ne correspondent pas à votre résolution ou à la langue que vous utilisez. Vous pouvez alors remplacer les fichiers se trouvant sous le répertoire "screenshots" afin de les personnaliser selon votre configuration.

Attention : prenez bien garde de lancer le script avec la fenêtre toujours de la même taille, le plus simple étant le mode maximisé.

