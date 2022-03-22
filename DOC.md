
# Intro

## Libertés prises :
* Ajout d'une classe GameObject pour factoriser le code commun à presque toutes les classes

* Ajout d'explosions

* Au lieu de pouvoir tirer aussi vite que l'on veut avec une limite projectile, maintenant on peut en tirer autant que l'on veut mais avec un interval minimum de rechargement entre 2 tirs.

## Remmarques :
* Les scores sont stockés dans le fichier texte `scores` sous le format dictionnaire Pyton `{JOUEUR : SCORE}` pour pouvoir être manipulé facilement avec `str` et `eval`.


## Problèmes :

* tableau des scores non implémentés : il faudrait pouvoir 
insérer son nom et afficher dans l'ordre les scores des autres joueurs, le code permet déjà de sauvegarder les scores de plusieurs joueurs.

* Redondance de code entre Defender et Fleet pour le tir de projectiles

* canvas/tk pas adapté à ce type d'application

* pas d'audio facilement portable sans utiliser un module tier. Solution actuelle non testée sous windows, pas d'implémentation pour mac, pour linux il faut avoir le paquet ffmpeg/ffplay (assez commun). 

* trop facile d'avoir le score maximal (16000pts) : ajouter des points bonus/malus pour les vies qu'il reste (si victoire), le nombre de balles ratées, la hauteur minimal des aliens au cours de la partie, ordre de destruction des aliens...


## Index des classes

* SpaceInvaders
* Canvas
* Game
* GameObject :
	* Defender
	* Fleet
	* Alien
	* Bullet
	* Explosion




# SpaceInvaders

Gère la fenêtre et la boucle principale de l'application.


## Structure :
* canvas : instance de Canvas (fenêtre)
* running : indique si l'application est active
* game : instance de Game


## Responsabilités :s
* calcul du temps écoulé entre deux itérations de la "boucle" principale
* mise à jour de game
* (ré)initialiser game lorsqu'il a terminé



# Canvas

Dépend de tk.Tk, wrapper pour la fenêtre et pour l'audio.

## Structure :
* tkcanvas : widget tk pour le dessin
* tkframe  : widget tk qui contient le canvas
* width, height : dimensions demandées

## Responsabilités :
* partage de l'accès à la fenêtre et à l'audio
* gestion des messages tk vers la fenêtre/le canvas


# Game

Logique principale du jeu.


## Structure :
* player : instance de Defender
* fleet : instance de Fleet
* explosions : une collection d'instances d'Explosion
* game_over_text / replay_text / score_text : tag d'objet canvas pour le texte
* keys : booléens indiquant si les touches de déplacement et de tire sont enfoncées
* game_over : booléen indiquant que le jeu est sur l'écran de game over
* done : booléen indiquant que le jeu est terminé (l'écran game over s'est affiché et le joueur a appuyé sur espace pour rejouer/quitter)
* player_name : nom du joueur
* current_score : nombre de points gagnés lors de la partie
* scores : dictionnaire liant un nom de joueur à son meilleur score
* canvas : instance de Canvas 

## Responsabilités :
* contrôles propres au jeu : mise à jour des variables leftKey, rightKey et fireKey  
* mise à jour de player, fleet et des explosion
* comptabilisation des points et mise à jour du fichier avec les highscores
* collision entre les projectiles du joueur et la flotte : explosion, destruction de l'alien et gain de points
* collision entre les projectiles de la flotte et le joueur : explosion et perte d'une vie
* détection de fin de partie : le joueur n'a plus de vies, les aliens ont atteint le bas de l'écran ou bien tous les aliens sont détruits
* affichage de l'écran game over
 



# GameObject

Classe générique pour les objets qui ont une position, une vitesse et un sprite. 

Variables de classe : sound_lose/sound_win les fichiers audio joués à la fin de la partie.

## Structure :
* x, y : position en pixels
* vx, vy : vitesse en pixels par seconde
* alive : booléen 
* sprite : tag d'object image sur le canvas
* width, height : taille en pixel du sprite
* canvas : instance de Canvas 

## Responsabilités :
* calcul de collision avec un autre GameObject
* calcul de collision avec les bords de l'écran
* raffraichissement du sprite à l'écran
* mettre à jour sa position en fonction de sa vitesse et du temps écoulé depuis la denière mise à jour (x = intégration de vx en fonction de dt)




# Defender

Dépend de GameObject.

Variable de classe : image, le fichier image qui est chargé lors de la première instanciation de la classe.

Le joueur en contrôle une instance.

Rq : certains aspects de Defender sont dupliqués de Fleet

## Structure :
* lives : liste d'objets canvas qui représente à la fois le nombre de vies restantes (longueur de la liste) et les icones à afficher qui correspondent au nombre de vies.
* bullets : list des balles tirés par le joueur
* interval : temps qu'il faut pour recharger le canon
* timer : temps restant avant que le canon soit rechargé, si < 0 alors le canon peut tirer à nouveau.
* reload_bar : rectangle sur le canvas qui indique le temps de rechargement du canon

## Responsabilités :
* décrémenter timer
* mettre à jour la taille de la barre de rechargement
* projectiles tirés par le joueur, leur création et destruction lorsqu'ils sortent de l'écran
* les sprites qui indiquent les vies restantes 
* se déplacer/tirer en fonction des touches pressées



# Fleet

Dépend de GameObject.
Gère les aliens.

Rq : c'est la classe Fleet qui s'occupe de tirer les projectiles des aliens, à interval régulier un alien est tiré au hasard pour tirer.


## Structure :
* aliens : liste d'instances d'Alien
* bullets : liste des projectiles tirés par les aliens
* interval : temps entre deux tirs d'alien
* timer : temps restant avant le prochain tir d'alien

## Responsabilités :
* décrémenter
* projectiles tirés par les aliens, leur création à interval régulier et destruction lorsqu'ils sortent de l'écran  
* initialiser/déplacer la formation d'aliens : changement de sens, descente et accélération lorsqu'un alien entre en collision avec les bords de l'écrans





# Alien

Dépend de GameObject.

Variable de classe : images, liste de fichiers image qui sont chargés lors de la première instanciation de la classe.

La classe Alien est pratiquement vide, tout étant déjà géré par la classe parente GameObject ou bien par la classe Fleet.

## Structure :
* type : indique quel image utiliser pour le sprite (indice dans la liste), pourra éventuellement indiquer le nombre de points que vaut l'alien.

## Responsabilités :

* calculer le nombre de points que vaut l'alien au moment
de sa destruction





# Bullet

Dépend de GameObject.

Variable de classe : image, fichier image qui est chargé lors de la première instanciation de la classe.

Variable de classe : sounds, liste des fichiers audio joués lorsqu'un projectile est tiré/instancié.

La classe Bullet est pratiquement vide, tout étant déjà géré par la classe parente ou bien le propriétaire des objets (Defender ou Fleet suivant les cas).


## Structure :
Vide

## Responsabilités :
Aucune (sauf chargement du fichier image)





# Explosion

Dépend de GameObject.

Variable de classe : image, fichier image qui est chargé lors de la première instanciation de la classe.

Variable de classe : sounds, liste des fichiers audio joués lorsqu'une explosion se produit / est instanciée.

## Structure :
* timer : temps restant avant que l'explosion de se dissipe

## Responsabilités :
* se retirer du canvas lorsque le temps est écoulé (et mettre self.alive à False)
