```python
def PROJET_ISN(nom, classe, année, collègue):
  print("\nBienvenue sur mon compte rendu personnel du Projet d'ISN !\n")
  
PROJET_ISN("Bartholomé GILI", "TS3", 2020, "Tristan FAUVET")
```

***

<div style="text-align: center; color: red;font-weight: bold; font-size: 16px"; href="https://www.w3schools.com/html/html_links.asp">Cliquez sur le logo ci-dessous pour télécharger le projet</div>

***



### [![logo_darkest_dungeon](/Users/bartholome/Downloads/logo_darkest_dungeon.png)](https://mega.nz/file/3cZWSYZb#c3HAtwbVHVeGvs78VkyNyVeANkkbuSRVounKcPBDz7Y)





Lors de la recherche d'idée, le concept de **génération** et de **résolution** d'un **labyrinthe** nous a rapidement interpellé. Nous avons donc décidé de nous mettre au défi d'imaginer un algorithme de génération pour le labyrinthe, puis d'aller voir les différents algorithmes connus sur internet. Une fois établis, nous nous sommes rendu compte qu'il s'approchait pas mal de l'algorithme dit de **Recursive Backtracking** (ou "retour en arrière récursif"). 

Vint ensuite la phase de réalisation. Ayant déjà fait quelques projets en **Python** avec le module **pygame**, cela m'a paru le meilleur être le meilleur choix puisque j'y suis relativement habitué, et que je pouvais l'expliquer facilement à mon collègue, Tristan.

Nous avons donc réalisé un premier programme nommé `labyrinthe.py` (disponible dans le fichier `autres` du projet) qui met en oeuvre nos algorithmes de génération et de résolution avec pygame. Cependant, le script avait été rapide à coder et nous ne voulions pas nous arrêter là. Nous avons donc décidé d'aller plus loin en créant un **jeu** basé sur cette génération de labyrinthe, le pré-nommé : **Darkest Dungeon**

Voici la liste des tâches dont je me suis occupé durant le développement :

- Génération et affichage du labyrinthe
- Génération, déplacement et comportement des ennemis
- Temples et leurs pouvoirs (sauf le Path Finder, étant donné qu'il était basé sur l'algorithme de résolution que Tristan avait préalablement établis sur le script prototype, il était normal qu'il s'en occupe)
- Création des assets (images en jeux) sur Photoshop



### 1. Structure globale du code

***

Voici la structure globale du code, très grossière et sans détails. Elle permet de voir et de comprendre rapidement le fonctionnement global du programme.

```python
#Importation de tous les modules nécessaires

#Définition des variables

#Définition des variables de Pygame

#–––––––––––––––––––––––––– Fonctions ––––––––––––––––––––––––––#
def gen_all():
  #Cette fonction permet la génération de toute la partie, que ce soit la matrice, l'emplacement des ennemis ou encore la vitesse de déplacement, le tout en fonction du niveau de difficulté du labyrinthe (entre 1 et 3)
  #Elle va appeler de nombreuses autres fonctions pour générer tout cela, ces dernières sont situées ci-dessous
  
def lab():
  #Permet la génération du labyrinthe ou la résolution du chemin le plus court entre un point A et un point B en fonction des arguments qui lui sont passé.
  #la fonction lab() va appeller la fonction check() :
  check()
  
def check():
  #Petite fonction permettant de définir la prochaine case dans l'algorithme de génération du labyrinthe (détaillée dans le grand 2. du compte rendu)
  
def emplacement_aleat():
  #Retourne un emplacement aléatoire viable dans le labyrinthe. Utilisée pour :
  #- emplacement de départ/d'arrivée des ennemis
  #- emplacement des temples
  #- pouvoir de téléportation des temples

def lab_eclaire():
  #Permet l'affichage complet du labyrinthe
  
def lab_noir():
  #Permet l'affichage dans la pénombre du labyrinthe
  
def show_path():
  #Fonction exclusive au pouvoir "Path Finder" des temples
  
#–––––––––––––––––––––––––– JEU ––––––––––––––––––––––––––#
gen_all()

while True:
  if mode_jeu == "game":
    #Partie
    >  lab_noir() #ou lab_eclairé() en fonction du mode

    >  if pos du joueur == case arrivée or pos du joueur == ennemi:
        #action

    >	 #tir

    >  #déplacement des ennemis

    >  #déplacement joueur

    >  #temples
  
  elif mode_jeu == "explication":
    #Affichage des règles
    > if touche pressée == "Entrer":
      	mode_jeu = "game"
        
  elif mode_jeu == "main_menu":
    #Affichage de l'écran titre
    > if clic gauche in bouton "jouer":
      	mode_jeu = "explication"
      elif clic gauche in bouton "quitter":
        pygame.quit()

```



### 2. Génération et affichage du labyrinthe

***

On génère d'abord une **matrice** de -1 et 1 alternés pour former un tableau représentant le labyrinthe :

<img src="/Users/bartholome/Downloads/yes.png" width="150px" /> 

avec la ligne de commande suivante :

```python
matrice = [[1 if i%2==1 else -1 for i in range (c_x[diff-1])] if y%2==0 else [1 for i in range (c_x[diff-1])] for y in range(c_y[diff-1])]
```

Les **0** (qui sont en fait des -1 dans le code) représentes les cases "sol" et les **1** représentes les cases "murs". Nous avons donc ici un labyrinthe totalement fermé de tout part, où chaque cellule est isolée. Le but est maintenant d'appliquer à cette matrice un algorithme qui va ouvrir certains murs entre certaines cases pour créer le labyrinthe.



<u>**Explication logique de l'algorithme de génération :**</u>

- nous partons de la toute première case, celle en haut à gauche qui est donc à la position `matrice[0][0]`

- définition des cases possibles qui n'ont jamais été visitées, qui ne sont pas des murs et qui se situent à 2 de distance avec la case actuelle :

  ```python
      possibilites = []
      try:
          if matrice[l+dist][c] == non_visitee and matrice[l+1][c] == mur and l+dist<=c_y[diff-1]-1: 
              possibilites.append([l+dist, c])
      except:
          pass
      try:
          if matrice[l-dist][c] == non_visitee and matrice[l-1][c] == mur and l-dist>=0:
              possibilites.append([l-dist, c])
      except:
          pass
      try:
          if matrice[l][c+dist] == non_visitee and matrice[l][c+1] == mur and c+dist<=c_x[diff-1]-1:
              possibilites.append([l, c+dist])
      except:
          pass
      try:
          if matrice[l][c-dist] == non_visitee and matrice[l][c-1] == mur and c-dist>=0:
              possibilites.append([l, c-dist])
      except:
          pass
  ```

  *Les blocs `try:   except: pass` permettent de passer la condition si les valeurs renseignée ne sont pas incluses dans les listes (exemple : si la case avec laquelle on appelle cette fonction est en [y=0, x=0] alors la case au dessus (y-1) sera égale à -1 et n'est donc pas incluse dans la liste. De même pour la case de gauche).*

- nous choisissons ensuite une case aléatoirement dans cette liste de possibilités :

  ```python
  if len(possibilites) != 0:
      go = possibilites[randint(0,len(possibilites)-1)]
  else:
      go = None
  ```

- si la cas n'est pas dans la liste `hist`, qui est l'historique des cases visitées, alors nous l'y ajoutons :

  ```python
  if [pos[0], pos[1]] not in hist:
  		hist.append([pos[0], pos[1]]) 
  ```

- si la variable `go` a la valeur `None`, cela veut dire qu'aucune case n'est disponible autour de la case actuelle. Dans ce cas là, nous allons revenir en arrière, à la dernière case visitées grace à l'historique (`hist` pour rappel) tout en supprimant la case actuelle dans l'historique :

  ```python
  if go == None:
  		hist.pop() #suppression de la case actuelle dans l'historique
  		try:
  				pos = [hist[len(hist)-1][0], hist[len(hist)-1][1]] #nouvelle case
  		except:
  				gen_all(diff)
  				break
  ```

  puis nous répétons tout le schéma vu jusqu'à maintenant.

- en revanche, si la variable `go` est valide, nous allons changer la valeur de la nouvelle case contenue dans `go` (-1 -> 0) et cette même case va devenir la case actuelle, avec laquelle nous allons répéter tout le schéma vu jusqu'à maintenant.

Ainsi, nous arrêtons cet boucle de répétition lorsque la case actuelle est de nouveau la case de départ (`[0][0]`), puisque cela veut dire que toutes les cases du labyrinthe on été visitées et que l'algorithme est revenu en arrière dans l'historique jusqu'au tout début.

Nous obtenons ainsi un labyrinthe relativement classique et il ne reste plus qu'à l'afficher...

[Voici une petite illustration du comportement de l'algorithme.](https://upload.wikimedia.org/wikipedia/commons/b/b3/Yl_maze_ani_algo2.gif)



**<u>Affichage du labyrinthe :</u>**

L'affichage s'opère grace à pygame.

Nous avons une fenêtre de 1280x720 pixels :

```python
window = pygame.display.set_mode((1280,720)) #Définition de la fenêtre (1280*720)
```

ainsi qu'une marge x et une marge y pour que le labyrinthe soit centré  :

```python
padx = int(140 + size)
pady = int((720 - size*c_y[diff-1])/2)
```

de plus, toutes les images que l'on va utiliser dans le programme sont chargées au début de celui-ci. Celles qui le nécessite sont également redimensionnées en fonction de la taille du labyrinthe dans la fonction `gen_all()`.

Il ne nous reste donc plus qu'à convertir les index de position de chaque case de la matrice en réelles position x et y en pixel et d'afficher un **mur** lorsque la case correspondant dans la matrice est un `1` et à l'inverse d'afficher un **sol** lorsque c'est un `0`.

Cependant, cette méthode plutôt simple ne marche que pour l'affichage basique du labyrinthe. Or dans Darkest Dungeon, le labyrinthe est plongé dans la pénombre. J'ai donc recréé un pseudo effet de lumière autour du joueur grâce à la fonction `lab_noir()`. 

Elle consiste à vérifier les "états" (mur, sol, temple, ennemi, case de départ, case d'arrivée) des cases alentours et en fonction de leur distance avec le jouer d'y afficher une version pleinement éclairée de l'image correspondant à l'état, ou une version plus sombre pour donner cet effet de dégradé.



### 3. Ennemis

***

Les ennemis se déplacent de case en case en faisant des allers-retours suivant un chemin défini aléatoirement lors de leur génération. La partie s'arrête si un ennemi nous touche. Il y en a autant d'ennemis que de temples et ce nombre change en fonction de la taille du labyrinthe[^1]

**<u>Génération des ennemis :</u>** 

Pour définir le chemin que chaque entité suivra, j'ai procédé de cette manière :

```python
pos_start_ennemies = emplacement_aleat(nb_ennemies)
pos_end_ennemies =  emplacement_aleat(nb_ennemies)
hist_ennemies = []
state_ennemies = []
xy_ennemies = []
for i in range (0, nb_ennemies):
		hist_ennemies.append(lab('path', matrice, pos_start_ennemies[i], pos_end_ennemies[i]))
    state_ennemies.append(1)
    xy_ennemies.append([pady+pos_start_ennemies[i][0]*size,padx+pos_start_ennemies[i][1]*size])
```

Tout d'abord nous définissons un point de départ et un point d'arrivée aléatoirement pour chaque entité, ainsi que 3 listes :

- `hist_ennemies` : une liste contenant les sous listes de l'historique de déplacement de chaque entité
- `state_ennemies ` : une liste contenant "l'état" de chaque ennemi (si ils sont à l'allé que l'on doit donc parcourir la liste dans le bon sens pour récupérer le prochaine case ou si ils sont sur le retour et qu'on doit parcourir la liste à contre-sens pour avoir la case suivante)
- `xy_ennemies` : la position de chaque entité

Tout le contenu de ces listes est défini dans la boucle `for` .

Petite aparté sur la définition de l'historique de chaque ennemis avec la ligne :

```python
		hist_ennemies.append(lab('path', matrice, pos_start_ennemies[i], pos_end_ennemies[i]))
```

Elle appelle en fait la fonction `lab()` qui, lorsqu'on y passe le premier argument **path** au lieu de **generation**, va retourner l'historique du chemin chemin le plus court entre un point A et un point B (au lieu de tout simplement générer le labyrinthe)



<u>**Déplacement des ennemis :**</u>

Le déplacement s'effectue avec ce bloc de code dans la partie principale du code, le `while` qui contient tout le déroulement de la partie de jeu :

```python
n_e+=1 
if n_e == 60:
    n_e = 0
    for i in range (0, nb_ennemies):
        hist_e = hist_ennemies[i]
        state_e = state_ennemies[i]
        pos_e = pos_ennemies[i]
        
        xy_ennemies[i][0] = hist_e[hist_e.index(pos_e)+state_e][0]*size+pady
        xy_ennemies[i][1] = hist_e[hist_e.index(pos_e)+state_e][1]*size+padx
        
        pos_ennemies[i] = [ hist_e[hist_e.index(pos_e)+state_e][0], hist_e[hist_e.index(pos_e)+state_e][1] ]
        
        if hist_e.index(pos_ennemies[i]) == len(hist_e)-1 or hist_e.index(pos_ennemies[i]) == 0:
            state_ennemies[i] = -state_ennemies[i]     
```

La variable `n_e` permet une temporisation entre 2 déplacements. Il faudra donc que la boucle `while` régissant l'entièreté de la partie effectue 60 itérations entre chaque déplacement.

Ensuite nous entrons tout simplement dans une boucle `for` qui va s'itérer autant de fois qu'il y a d'ennemis, et pour chaque ennemi va définir sa position suivante en fonction de son historique. 

Si jamais la position actuelle de l'ennemi est sa position de départ ou d'arrivée, l'état de l'ennemi va s'inverser (-1 -> 1 ou 1 -> -1) et il va donc parcourir la liste dans l'autre sens dès lors, ce qui permet le système de vas et viens de l'entité.

Les ennemis sont finalement affichés en même temps que les murs/sols/temples/etc dans la fonction `lab_noir()`.

[^1]: Niveau 1 -> 2 | Niveau 2 -> 4 | Niveau 3 -> 6

### 4. Temples et Pouvoirs

***

Les temples sont des bâtiments disséminé de par et d'autres dans le labyrinthe. Il y en a autant qu'il y a d'ennemis[^1]

Ils confèrent un bonus ou un malus aléatoire quand on les touche :

- <img src="/Volumes/Onee-sama/BARTHO/Code/Python/ISN/Projet/Darkest Dungeon/assets/vitesse_up.png" width="50px" />  <u>**Augmentation de la vitesse**</u>

  ***

  Simple incrémentation de la variable `vit` :

  ```python
  #Augmente la vitesse du joueur (80% de chance)
  window.blit(vitesse_up, ((1280-300)/2, (720-300)/2))
  pygame.display.flip()
  sleep(time_sleep)
  vit+=2
  ```

  

- <img src="/Volumes/Onee-sama/BARTHO/Code/Python/ISN/Projet/Darkest Dungeon/assets/vitesse_down.png" width="50px" />  **<u>Réduction de la vitesse</u>**

  ***

  Simple décrémentation de la variable `vit` :

  ```python
  #Diminue la vitesse du joueur (20% de chance)
  window.blit(vitesse_down, ((1280-300)/2, (720-300)/2))
  pygame.display.flip()
  sleep(time_sleep)
  vit-=2
  if vit <= 0: #Vérifie bien que la vitesse soit supérieure à 0
      vit = 1
  ```

  

- <img src="/Volumes/Onee-sama/BARTHO/Code/Python/ISN/Projet/Darkest Dungeon/assets/teleport.png" width="50px" />  **<u>Téléportation dans un emplacement aléatoire du labyrinthe</u>**

  ***

  J'utilise ici la fonction `emplacement_aleat()` qui permet retourne un emplacement aléatoire **valide** dans la le labyrinthe :

  ```python
  window.blit(teleport, ((1280-300)/2, (720-300)/2))
  pygame.display.flip()
  sleep(time_sleep)
  pos_temp = emplacement_aleat(1)[0]
  x = ceil(padx+ceil(size*0.25)+ceil(pos_temp[1]*size))
  y = ceil(pady+(ceil(size*0.25)*(39/66))+ceil(pos_temp[0]*size))
  ```

  

- <img src="/Volumes/Onee-sama/BARTHO/Code/Python/ISN/Projet/Darkest Dungeon/assets/path_finder.png" width="50px" />  <u>**Montre pendant quelques instants la route à suivre pour arriver à l'arrivée**</u>

  ***

  Partie réalisée et expliquée dans le compte rendue de *Tristan FAUVET*.

  

  

  

  



