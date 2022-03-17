
# Intro

## Libertés prises :
* Ajout d'une classe GameObject pour factoriser le code commun à plusieurs classes

* Ajout d'explosions

* Au lieu de pouvoir tirer aussi vite que l'on veut avec une limite projectile, maintenant on peut en tirer autant que l'on veut mais avec un interval minimum de rechargement entre 2 tirs.



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

Gère la fenêtre et la boucle principale.

Rq : récupérer la taille du canvas n'est pas fiable (toujours de 1,1 au début), pour éviter d'avoir à donner des arguments supplémentaires dans chaque méthode, une MÉTHODE est AJOUTÉE à canvas pour retourner la taille définie dans l'instance de SpaceInvader :

self.canvas.width  = lambda : self.width
self.canvas.height = lambda : self.height

puis appel avec self.canvas.get_width()


## Structure :
* width, height : taille voulue de la zone graphique
* canvas : instance de Canvas (fenêtre)
* frameRate : fréquence de rafraichissement voulue
* running : indique si l'application (la boucle principale) est active
* game : instance de Game


## Responsabilités :
* calcul du temps écoulé entre deux itérations de la boucle principale
* bridage de la boucle pour ne pas dépasser la fréquence de rafraichissement voulue
* mise à jour et (ré)initialiser game lorsqu'il a terminé (cf Game.done)
* mise à jour de la fenêtre



# Canvas

Dépend de tk.Tk, wrapper pour la fenêtre et l'audio.

## Structure :
* tkcanvas : widget tk pour le dessin
* width, height : dimensions demandées

## Responsabilités :
* partage de l'accès à la fenêtre et à l'audio
* transmissions des messages tk vers le membre tkcanvas


# Game

Logique principale du jeu.


## Structure :
* player : instance de Defender
* fleet : instance de Fleet
* explosions : une collection d'instances d'Explosion
* game_over_text / replay_text / score_text : tag d'objet canvas pour le texte
* leftKey, rightKey, fireKey : booléens indiquant si les touches de déplacement et de tire sont pressées
* game_over : booléen indiquant que le jeu est sur l'écran de game over
* done : booléen indiquant que le jeu est terminé et que l'instance est prête à être détruite pour une autre partie ou bien pour arrêter (l'écran game over s'est affiché et le joueur a appuyé sur espace pour rejouer)
* player_name : nom du joueur dans la liste des scores
* current_score : nombre de points gagnés lors de la partie
* scores : dictionnaire liant un nom de joueur à son meilleur score
* canvas : instance de Canvas 

## Responsabilités :
* contrôles propres au jeu : mise à jour des variables leftKey, rightKey et fireKey  
* mise à jour de player et fleet
* mise à jour de explosions et destruction des explosion "mortes"/dissipées
* comptabilisation des points et mise à jour du fichier avec les meilleurs scores
* collision entre les projectiles du joueur et la flotte : explosion et destruction de l'alien et gain de points
* collision entre les projectiles de la flotte et le joueur : explosion et perte d'une vie du joueur
* détection de fin de partie/game over/win : le joueur n'a plus de vies, les aliens ont atteint le bas de l'écran (ligne grise "finish_line") ou tous les aliens sont détruits
* affichage de l'écran game over
 



# GameObject

Classe générique pour les objets qui ont une position, une vitesse et un sprite. 

## Structure :
* x, y : position en pixels
* vx, vy : vitesse en pixels par seconde
* alive : booléen 
* sprite : tag d'object image sur le canvas
* width, height : taille en pixel du sprite
* canvas : instance de Canvas 

## Responsabilités :
* calcul de collision entre deux objets ou avec les bords de l'écran
* raffraichissement/destruction du sprite à l'écran
* mettre à jour sa position en fonction de sa vitesse et du temps écoulé depuis la denière mise à jour (dt)




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

* point_value : nombre de points que vaut l'alien

## Responsabilités :
Aucune (sauf chargement du fichier image)




# Bullet

Dépend de GameObject.

Variable de classe : image, fichier image qui est chargé lors de la première instanciation de la classe.

La classe Bullet est pratiquement vide, tout étant déjà géré par la classe parente ou bien le propriétaire des objets (Defender ou Fleet suivant les cas).


## Structure :
Vide

## Responsabilités :
Aucune (sauf chargement du fichier image)





# Explosion

Dépend de GameObject.

Variable de classe : image, fichier image qui est chargé lors de la première instanciation de la classe.

## Structure :
* timer : temps restant avant que l'explosion de se dissipe

## Responsabilités :
* "tuer"/dissper l'explosion et la retirer du canvas lorsque le temps est écoulé




