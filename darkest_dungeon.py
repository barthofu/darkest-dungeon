# coding: utf-8
#==================================================================================#
#====================================== MODULES ===================================#
#==================================================================================#
import pygame
from random import *
from math import * 
from copy import deepcopy #Ce module sert à simplifier la copie indépendante d'une liste
from time import * #Pour instaurer des délais durant certaines actions
import os
dirpath = os.getcwd()
print("==================================\n\n"+dirpath+"\n\n==================================")
#Vérifie l'utilisation de python 3
import sys
if sys.version_info[0] < 3:
    raise Exception("\n=====================================\n\nVous devez utiliser python 3 pour éxecuter ce programme\nGuide d'installation dans le README\n\n=====================================")

#==================================================================================#
#============================= DÉFINITION DES VARIABLES ===========================#
#==================================================================================#
c_x = [15, 25, 55] #nombre de cases en longueur en fonction de la difficulté
c_y = [11, 19, 41] #nombre de cases en largeur en fonction de la difficulté
sizes = [58, 37, 17] #taille en pixel des cases en fonction de la difficulté
diff = 1 #niveau de difficulté (1 = Easy, 2 = Medium, 3 = Hard)

display_mode = 2 #Sert à switcher entre affichage dans le noir avec les effets de lumière et affichage normal qui montre l'entierté du labyrinthe
around_check = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1], [-2, 0], [2, 0], [0, -2], [0, 2]] #Liste servant à l'algorithme qui affiche les cases autour du joueur de manière graduelle. Elle contient la différence de coordonnées entre celles de l'emplacement du joueur et celles des cases à checker
path = 0 #Variable activant ou non l'animation de la capacité 'Montre la Voie !'

#==================================================================================#
#======================== DÉFINITION DES VARIABLES DE PYGAME ======================#
#==================================================================================#
pygame.init() #Initialisation du module PyGame
pygame.font.init() #Initialisation des polices d'écritures 
myfont = pygame.font.SysFont('Comic Sans MS', 27)
text_munitions = myfont.render("Munitions", True, (255, 255, 255))
text_temps = myfont.render("Temps", True, (255, 255, 255))
text_niveau = myfont.render("Niveau", True, (255,255,255))

window = pygame.display.set_mode((1280,720)) #Définition de la fenêtre (1280*720)
pygame.display.set_caption("MAZE") 
font = pygame.font.SysFont("comic sans ms", 64) #Définition de la police d'écriture
clock = pygame.time.Clock() #Création de la clock qui permettra de régler le nombre d'images par secondes (FPS)
#Importation de toutes les images :
wall_background = pygame.image.load("assets/wall_background.png")
wall = pygame.image.load("assets/wall.png")
wall_dark = pygame.image.load("assets/wall_dark.png")
floor_s = pygame.image.load("assets/floor.png")
floor_dark_s = pygame.image.load("assets/floor_dark.png")
end_point = pygame.image.load("assets/end_point.png")
end_point_dark = pygame.image.load("assets/end_point_dark.png")
start_point = pygame.image.load("assets/start_point.png")
start_point_dark = pygame.image.load("assets/start_point_dark.png")
lantern = pygame.image.load("assets/lantern.png")
ennemy = pygame.image.load("assets/ennemy.png")
ennemy_dark = pygame.image.load("assets/ennemy_dark.png")
temple = pygame.image.load("assets/temple.png")
temple_dark = pygame.image.load("assets/temple_dark.png")
vitesse_down = pygame.image.load("assets/vitesse_down.png")
vitesse_up = pygame.image.load("assets/vitesse_up.png")
path_finder = pygame.image.load("assets/path_finder.png")
path_finder_ball = pygame.image.load("assets/path_finder_ball.png")
tir = pygame.image.load("assets/tir.png")
teleport = pygame.image.load("assets/teleport.png")
main_menu_background = pygame.image.load("assets/main_menu_background.png")
main_menu_jouer = pygame.image.load("assets/main_menu_jouer.png")
main_menu_jouer_big = pygame.transform.scale(main_menu_jouer, (int(main_menu_jouer.get_size()[0]*1.3), int(main_menu_jouer.get_size()[1]*1.3)))
main_menu_quitter = pygame.image.load("assets/main_menu_quitter.png")
main_menu_quitter_big = pygame.transform.scale(main_menu_quitter, (int(main_menu_quitter.get_size()[0]*1.3), int(main_menu_quitter.get_size()[1]*1.3)))
main_menu_quitter_little = pygame.transform.scale(main_menu_quitter, (int(main_menu_quitter.get_size()[0]*0.36), int(main_menu_quitter.get_size()[1]*0.5)))
teleport = pygame.image.load("assets/teleport.png")
bravo = pygame.image.load("assets/bravo.png")
explications = pygame.image.load("assets/explications.png")
game_over = pygame.image.load("assets/game_over.png")

#Définition de différentes variables de couleur (au format RGB):
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
FOND_1 = (54,57,63)
FOND_2 = (80,83,90)

#==================================================================================#
#============================= DÉFINITION DES FONCTIONS ===========================#
#==================================================================================#

def gen_all(diff):
    global matrice, end, size, vit, pos, nb_temple, nb_ennemies, x, y, munitions, copied_hist, pos_temple, pos_start_ennemies, pos_end_ennemies, hist_ennemies, state_ennemies, xy_ennemies, pos_ennemies, n, n_e, n_tir, last_key, key_sens, pos_temp, tir_state, sens, tir_cooldown, wall, wall_dark, floor_s, floor_dark_s, end_point,end_point_dark, start_point, start_point_dark, lantern, ennemy, ennemy_dark, temple, temple_dark, path_finder_ball, tir_hori, tir_vert, tir_diag, pady, padx
    
    matrice = [[1 if i%2==1 else -1 for i in range (c_x[diff-1])] if y%2==0 else [1 for i in range (c_x[diff-1])] for y in range(c_y[diff-1])] #Création d'une "matrice" content c_y[diff-1] listes chacunes contenant c_x[diff-1] éléments
    #Schématisation de la matrice que l'on crée (extrait):
    #(Les 1 représentent les murs et les 0 les sols)
    '''
    [[0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],]
    '''

    pos = [0,0] #Position de départ
    end = False #Variable servant à mettre fin à l'algorithme de génération du labyrinthe lorsque celui-ci a terminé
    matrice, copied_hist = lab('generation', matrice, pos, [0,0]) #GÉNÉRATION DU LABYRINTHE
    #matrice -> nouvelle matrice modifiée contenant les différents chemins du labyrinthe
    #copied_hist -> ici sera copiée indépendamment (grâce au module "copy") la liste 'hist' au moment où cette dernière atteindra la case d'arrivée durant l'éxecution de l'algorithme de génération du labyrinthe. Nous aurons donc une liste contenant toutes les positions du chemin pour aller au point d'arrivé 
    size = sizes[diff-1] #Séléction de la taille des futurs images qui seront utilisées afin de modéliser le labyrinthe, le personnage, etc. en fonction de la taille du labyrinthe (un labyrinthe plus petit demandera des cases plus grandes pour remplir tout l'écran qu'un labyinthe plus massif)

    vit = 8-diff*2

    nb_temple = diff*2 #Nombre de temples disposés dans le labyrinthe
    nb_ennemies = diff*2 #Nombre d'ennemis dans le labyrinthe
    
    padx = int(140 + size)  #Décalage en pixels du labyrinthe sur l'axe des abscisses pour pouvoir le centrer au centre de l'écran
    pady = int((720 - size*c_y[diff-1])/2) #Décalage en pixels du labyrinthe sur l'axe des ordonnées pour pouvoir le centrer au centre de l'écran
    
    x = ceil(padx+ceil(size*0.25)) #Coordonnées de départ sur l'axe des abscisses 
    y = ceil(pady+(ceil(size*0.25)*(39/66))) #Coordonnées de départ sur l'axe des ordonnées 
    munitions = 3 #Nombre de munitions au début d'une partie
    
    
    #Génération des temples:
    pos_temple = emplacement_aleat(nb_temple)

    #Génération des ennemis :
    pos_start_ennemies = emplacement_aleat(nb_ennemies)
    pos_end_ennemies =  emplacement_aleat(nb_ennemies)
    hist_ennemies = []
    state_ennemies = []
    xy_ennemies = []
    for i in range (0, nb_ennemies):
        hist_ennemies.append(lab('path', matrice, pos_start_ennemies[i], pos_end_ennemies[i]))
        state_ennemies.append(1)
        xy_ennemies.append([pady+pos_start_ennemies[i][0]*size,padx+pos_start_ennemies[i][1]*size])
    pos_ennemies = deepcopy(pos_start_ennemies)
    
    n = 0
    n_e = 0
    n_tir = 0
    
    last_key = "bas"
    key_sens = {
        "bas": [1, 0],
        "haut": [-1, 0],
        "droite": [0, 1],
        "gauche": [0, -1]
    }
    pos_temp = None
    tir_state = 0
    sens = None
    tir_cooldown = 0
    
    wall = pygame.transform.scale(wall, (size, size))
    wall_dark = pygame.transform.scale(wall_dark, (size, size))
    floor_s = pygame.transform.scale(floor_s, (size, size))
    floor_dark_s = pygame.transform.scale(floor_dark_s, (size, size))
    end_point = pygame.transform.scale(end_point, (size, size))
    end_point_dark = pygame.transform.scale(end_point_dark, (size, size))
    start_point = pygame.transform.scale(start_point, (size, size))
    start_point_dark = pygame.transform.scale(start_point_dark, (size, size))
    lantern = pygame.transform.scale(lantern, (int(ceil(ceil(size*0.75)*(39/66))), int(ceil(size*0.75))))
    ennemy = pygame.transform.scale(ennemy, (size, size))
    ennemy_dark = pygame.transform.scale(ennemy_dark, (size, size))
    temple = pygame.transform.scale(temple, (size, size))
    temple_dark = pygame.transform.scale(temple_dark, (size, size))
    path_finder_ball = pygame.transform.scale(path_finder_ball, (int(ceil(ceil(size*0.75)*(39/66))), int(ceil(size*0.75))))
    tir_hori = pygame.transform.scale(tir, (size, size))
    tir_vert = pygame.transform.rotate(tir_hori, 90)
    tir_diag = pygame.transform.scale(tir, (50, 50))
    tir_diag = pygame.transform.rotate(tir_diag, 45)


def lab(objectif, matrice, pos, end_pos):
    
    if objectif == 'generation':
        matrice_temp = matrice
        non_visitee = -1
        mur = 1
        dist = 2
        typ = 1
    else:
        non_visitee = -1
        mur = -1
        dist = 1
        typ = 2
        matrice_temp = []
        for i in range (0, c_y[diff-1]):
            matrice_temp.append([])
            for j in range (0, c_x[diff-1]):
                if matrice[i][j] == 0:
                    matrice_temp[i].append(-1)
                else:
                    matrice_temp[i].append(1)
    
    hist = []
    end = False
    
    while end == False:
        go = check(pos[0], pos[1], matrice_temp, non_visitee, mur, dist, typ)
        if [pos[0], pos[1]] not in hist:
            hist.append([pos[0], pos[1]])
        if go == None:
            hist.pop()
            try:
                pos = [hist[len(hist)-1][0], hist[len(hist)-1][1]]
            except:
                gen_all(diff)
                break
        else:
            if objectif == 'generation':
                matrice_temp[pos[0]][pos[1]] = 0
                matrice_temp[int(pos[0]+(go[0]-pos[0])/2)][int(pos[1]+(go[1]-pos[1])/2)] = 0
            matrice_temp[go[0]][go[1]] = 0
            pos = [go[0], go[1]]
        if pos == end_pos:
            end = True
        elif pos == [c_y[diff-1]-1, c_x[diff-1]-1] and objectif == 'generation':
            copied_hist = deepcopy(hist)
    
    if objectif == 'generation' and end == True:
        return matrice_temp, copied_hist
    elif end == True:
        return hist
        
        
#Vérifie les cases adjacentes à la case concernée. Cette fonction prend différents paramètres qui changeront en fonction de son utilité : La génération du labyrinthe ou la simple recherche d'un chemin d'un point à un autre
def check(l, c, matrice, non_visitee, mur, dist, typ): 
    possibilites = []
    #Les blocs 'try:   except: pass' permettent de passer la condition si les valeurs renseignée ne sont pas incluses dans les listes (exemple : si la case avec laquelle on appelle cette fonction est en [y=0, x=0] alors la case au dessus (y-1) sera égale à -1 et n'est donc pas incluse dans la liste. De même pour la case de gauche)
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
    if len(possibilites) != 0:
        if typ == 1:
            go = possibilites[randint(0,len(possibilites)-1)]
        else:
            go_temp = [100, None]
            for element in possibilites:
                if (c_y[diff-1]-element[0])+(c_x[diff-1]-element[1]) < go_temp[0]:
                    go_temp = [(c_y[diff-1]-element[0])+(c_x[diff-1]-element[1]), element]
            go = go_temp[1]
    else:
        go = None
    return go

#Emplacements aléatoires dans le labyrinthe :
def emplacement_aleat(nb):
    pos_list = []
    for i in range (0, nb):
        pos_temp = [randint(0,c_y[diff-1]-1), randint(0,c_x[diff-1]-1)]
        while matrice[pos_temp[0]][pos_temp[1]] == 1 or (pos_temp[0] == 0 and pos_temp[1] == 0) or (pos_temp[0] == c_y[diff-1]-1 or pos_temp[1] == c_x[diff-1]-1) or ([pos_temp[0], pos_temp[1]] in pos_list):
            pos_temp = [randint(0,c_y[diff-1]-1), randint(0,c_x[diff-1]-1)] 
        pos_list.append(pos_temp)
    return pos_list

#Affiche l'entierté du labyrinthe
def lab_eclaire():
    for i in range (0, c_y[diff-1]):
        for j in range (0, c_x[diff-1]):
            if matrice[i][j] == 0:
                window.blit(floor_s, (j*size+padx, i*size+pady))
            else:
                window.blit(wall, (j*size+padx, i*size+pady))
            if i == c_y[diff-1]-1 and j == c_x[diff-1]-1:
                window.blit(end_point, (j*size+padx, i*size+pady))
            elif i == 0 and j == 0:
                window.blit(start_point, (j*size+padx, i*size+pady))
    for i in range (-2, c_y[diff-1]+2):
        window.blit(wall, (padx-size, i*size))
        window.blit(wall, (padx+(size*c_x[diff-1]), i*size))
    for i in range (-1, c_x[diff-1]):
        window.blit(wall, (padx+size+size*i, pady-size))
        window.blit(wall, (padx+size+size*i, c_y[diff-1]*size+pady))
    for coor in pos_temple:
        window.blit(temple, (padx+size*coor[1], pady+size*coor[0]))
    for coor in xy_ennemies:
        window.blit(ennemy, (coor[1], coor[0]))
        

#Affiche le labyrinthe dans le noir avec des effets de lumière autour de la lanterne
def lab_noir(pos, pos_temple, pos_ennemies):
    pygame.draw.rect(window, NOIR, (padx, pady, c_x[diff-1]*size, c_y[diff-1]*size))
    for i in range (-2, c_y[diff-1]+2):
        window.blit(wall, (padx-size, i*size))
        window.blit(wall, (padx+(size*c_x[diff-1]), i*size))
    for i in range (-1, c_x[diff-1]):
        window.blit(wall, (padx+size+size*i, pady-size))
        window.blit(wall, (padx+size+size*i, c_y[diff-1]*size+pady))
    for coor in around_check:
        difference = 1
        if (coor[0] == 2 or coor[1] == 2) or (coor[0] == 2 or coor[1] == -2): #or ((coor[0] == 1 or coor[0] == -1) and (coor[1] == 1 or coor[1] == -1)):
            difference = 2
        try:
            c_ase = matrice[int(pos[0]+coor[0])][int(pos[1]+coor[1])]
            if (int(pos[0]+coor[0]) >= 0 and int(pos[0]+coor[0]) <= c_y[diff-1]) and (int(pos[1]+coor[1]) >= 0 and int(pos[1]+coor[1]) <= c_x[diff-1]):
                if c_ase == 0:
                    if difference == 1:
                        window.blit(floor_s, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(floor_dark_s, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                if c_ase == 1:
                    if difference == 1:
                        window.blit(wall, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(wall_dark, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                if int(pos[0]+coor[0]) == c_y[diff-1]-1 and int(pos[1]+coor[1]) == c_x[diff-1]-1:
                    if difference == 1:
                        window.blit(end_point, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(end_point_dark, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                elif int(pos[0]+coor[0]) == 0 and int(pos[1]+coor[1]) == 0:
                    if difference == 1:
                        window.blit(start_point, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(start_point_dark, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                if [int(pos[0]+coor[0]), int(pos[1]+coor[1])] in pos_temple:
                    if difference == 1:
                        window.blit(temple, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(temple_dark, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                if [int(pos[0]+coor[0]), int(pos[1]+coor[1])] in pos_ennemies:
                    if difference == 1:
                        window.blit(ennemy, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
                    else:
                        window.blit(ennemy_dark, ((pos[1]+coor[1])*size+padx, (pos[0]+coor[0])*size+pady))
        except:
            pass

#Affiche la ligne qui mène à l'arrivée
def show_path(hist):
    for i in range (1, c_x[diff-1]+ceil(c_x[diff-1]/3)):
        try:
            window.blit(path_finder_ball, (padx+hist[i][1]*size,pady+hist[i][0]*size))
        except:
            pass
        if i == ceil(c_x[diff-1]/3):
            try:
                window.blit(floor_s, (padx+hist[i-ceil(c_x[diff-1]/3)][1]*size,pady+hist[i-ceil(c_x[diff-1]/3)][0]*size))
            except:
                pass
        elif i == ceil(c_x[diff-1]/3)+1 or i == ceil(c_x[diff-1]/3)+2:
            try:
                window.blit(floor_dark_s, (padx+hist[i-ceil(c_x[diff-1]/3)][1]*size,pady+hist[i-ceil(c_x[diff-1]/3)][0]*size))
            except:
                pass        
        else:
            try:
                pygame.draw.rect(window, NOIR, (padx+hist[i-ceil(c_x[diff-1]/3)][1]*size,pady+hist[i-ceil(c_x[diff-1]/3)][0]*size, size, size))
            except:
                pass
        pygame.display.flip()
        sleep(0.1)
        


gen_all(diff)

game = True
mode_jeu = "main_menu"

start_time = None

while game == True:
    
    if mode_jeu == "game":
        
        window.fill(FOND_1) 
        window.blit(wall_background, (0, 0))
        #window.blit(main_menu_background, (0, 0))
        window.blit(main_menu_quitter_little, (5, 660))
        window.blit(text_munitions, (10, 10))
        for i in range (1, munitions+1):
            window.blit(tir_diag, ((i-1)*30, 50))
        
        #Définition du timer
        sec = floor((pygame.time.get_ticks()-start_time)/1000)
        if sec >= 600:
            minute = str(floor(sec/60))
        elif sec >= 60:
            minute = "0{}".format(floor(sec/60))
        else:
            minute = "00"
        sec = sec%60
        if sec < 10:
            sec = "0{}".format(sec)
        time_text = myfont.render("{}:{}".format(minute, sec), True, (255, 255, 255))
        window.blit(text_temps, (1150, 10))
        window.blit(time_text, (1150, 50))
        window.blit(text_niveau, (1150, 600))
        diff_text = myfont.render(str(diff), True, (255,255,255))
        window.blit(diff_text, (1190, 650))

        pos = [int( floor( ( y-pady + (ceil(size*0.75)/2) ) / size ) ), int( floor( ( x-padx + (ceil(ceil(size*0.75)*(39/66))/2) ) / size ) )] #conversion des coordonnées x et y du joueur en positions dans la matrice
        #Affiche le labyrinthe d'une certaine façon (entièrement éclairé ou plongé dans le noir)
        if display_mode == 1:
            lab_eclaire()
        else:
            lab_noir(pos, pos_temple, pos_ennemies)

        #Arrête le programme si la fenêtre est fermée
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0 <= pygame.mouse.get_pos()[0] <= padx-size) and (660 <= pygame.mouse.get_pos()[1]):
                        mode_jeu = "main_menu"
                        diff = 1
                        gen_all(diff)
                        continue

        #Game over si on se fait toucher par un ennemi
        for coor_e in pos_ennemies:
            if pos == coor_e:
                window.blit(game_over, (0,0))
                pygame.display.flip()
                sleep(4)
                mode_jeu = "main_menu"
                diff = 1
                gen_all(diff)
                continue
            
        #Passage au niveau suivant ou affichage du message de félicitation quand on atteint la case de fin
        if pos == [len(matrice)-1, len(matrice[0])-1]:
            if diff == 3:
                window.blit(bravo, (0,0))
                pygame.display.flip()
                sleep(4)
                mode_jeu = "main_menu"
                diff = 1
                gen_all(diff)
                continue
            else:
                diff+=1
                gen_all(diff)
                continue
            
        
        if tir_state == 1:
            n_tir+=1
            if n_tir >= 15: 
                tir_state = 0
                n_tir = 0
            else:
                pos_temp2 = deepcopy(pos_temp)
                while True:
                    pos_temp2 = [pos_temp2[0]+sens[0], pos_temp2[1]+sens[1]]
                    try:
                        if matrice[pos_temp2[0]][pos_temp2[1]] == 1 or pos_temp2[0] < 0 or pos_temp2[1] < 0 or pos_temp2[0] > len(matrice)-1 or pos_temp2[1] > len(matrice[0])-1:
                            break
                    except:
                        break
                    if sens[0] != 0:
                        window.blit(tir_vert, (pos_temp2[1]*size+padx, pos_temp2[0]*size+pady))
                    else:
                        window.blit(tir_hori, (pos_temp2[1]*size+padx, pos_temp2[0]*size+pady))
                    for item in pos_ennemies:
                        if item == [pos_temp2[0], pos_temp2[1]]:
                            indice = pos_ennemies.index(item)
                            del pos_ennemies[indice]
                            del hist_ennemies[indice]
                            del state_ennemies[indice]
                            del xy_ennemies[indice]
                            nb_ennemies-=1


        #Déplacement des ennemis
        n_e+=1
        if n_e == 60:
            n_e = 0
            for i in range (0, nb_ennemies):
                hist_e = hist_ennemies[i]
                state_e = state_ennemies[i]
                #xy_e = xy_ennemies[i]
                pos_e = pos_ennemies[i]
                
                xy_ennemies[i][0] = hist_e[hist_e.index(pos_e)+state_e][0]*size+pady
                xy_ennemies[i][1] = hist_e[hist_e.index(pos_e)+state_e][1]*size+padx
                
                pos_ennemies[i] = [ hist_e[hist_e.index(pos_e)+state_e][0], hist_e[hist_e.index(pos_e)+state_e][1] ]
                
                if hist_e.index(pos_ennemies[i]) == len(hist_e)-1 or hist_e.index(pos_ennemies[i]) == 0:
                    state_ennemies[i] = -state_ennemies[i]         
                

        touche_pressee = pygame.key.get_pressed() #Récupère un touche si elle est appuyée
            



        #Les conditions à l'intérieur des blocs vérifiant la touche pressée servent à créer un système de collision avec les murs. Elles vérifient si la case adjacente adaptée (si flèche de droite appuyée -> case de droite) est un mur ou non, et si c'est le cas, annulent l'incrémentation de x ou y

        if touche_pressee[pygame.K_UP]: #Flèche du haut
            last_key = "haut"
            y-=vit
            if y < pady or matrice[int(floor((y-pady)/size))][int(floor((x-padx)/size))] == 1:
                y+=vit

        if touche_pressee[pygame.K_DOWN]: #Flèche du bas
            last_key = "bas"
            y+=vit
            if y+ceil(size*0.75) > pady+c_y[diff-1]*size or matrice[int(floor((y-pady+ceil(size*0.75))/size))][int(floor((x-padx)/size))] == 1:  #matrice[int(floor((y+ceil(size*0.75))/size))][int(floor(x/size))] == 1:
                y-=vit

        if touche_pressee[pygame.K_RIGHT]: #Flèche de droite
            last_key = "droite"
            x+=vit
            if x+ceil(ceil(size*0.75)*(39/66)) > padx+c_x[diff-1]*size or matrice[int(floor((y-pady)/size))][int(floor((x-padx+ceil(ceil(size*0.75)*(39/66)))/size))] == 1:
                x-=vit

        if touche_pressee[pygame.K_LEFT]: #Flèche de gauche
            last_key = "gauche"
            x-=vit
            if x < padx or matrice[int(floor((y-pady)/size))][int(floor((x-padx)/size))] == 1:
                x+=vit

        if touche_pressee[pygame.K_l]:
            display_mode+=1
            if display_mode >= 2:
                display_mode = 0
                
        if tir_cooldown > 0:
            tir_cooldown-=1
        
        if touche_pressee[pygame.K_a]:
            if tir_cooldown == 0:
                if (munitions > 0):
                    tir_cooldown = 60
                    munitions-=1
                    pos_temp = deepcopy(pos)
                    sens = key_sens[last_key]
                    tir_state = 1

        if path == 1:
            show_path(hist)
            path = 0
            
        #====================== TEMPLES ========================#
        if [pos[0], pos[1]] in pos_temple: #Vérifie si la position du joueur correspond à une case où se trouve un temple
            time_sleep = 2 
            del pos_temple[pos_temple.index([pos[0], pos[1]])] #Enlève le temple de la liste. Il ne sera ainsi plus pris en compte et ne sera plus affiché
            nb = randint(1,100) #Nombre aléatoire pour définir l'action que va effectuer le temple
            if nb <= 20:
                #Téléportation aléatoire dans le labyrinthe (20% de chance)
                window.blit(teleport, ((1280-300)/2, (720-300)/2))
                pygame.display.flip()
                sleep(time_sleep)
                pos_temp = emplacement_aleat(1)[0]
                x = ceil(padx+ceil(size*0.25)+ceil(pos_temp[1]*size))
                y = ceil(pady+(ceil(size*0.25)*(39/66))+ceil(pos_temp[0]*size))
            elif 20 < nb <= 60:
                #Augmente ou diminue la vitesse du joueur (40% de chance)
                nb = randint(1,100)
                if nb <= 20:
                    #Diminue la vitesse du joueur (20% de chance)
                    window.blit(vitesse_down, ((1280-300)/2, (720-300)/2))
                    pygame.display.flip()
                    sleep(time_sleep)
                    vit-=2
                    if vit <= 0: #Vérifie bien que la vitesse soit supérieure à 0
                        vit = 1
                else:
                    #Augmente la vitesse du joueur (80% de chance)
                    window.blit(vitesse_up, ((1280-300)/2, (720-300)/2))
                    pygame.display.flip()
                    sleep(time_sleep)
                    vit+=2
            else:
                #Affiche une partie du chemin menant à l'arrivée (40% de chance)
                window.blit(path_finder, ((1280-300)/2, (720-300)/2))
                pygame.display.flip()
                sleep(time_sleep)
                hist = lab('path', matrice, pos, [c_y[diff-1]-1, c_x[diff-1]-1])
                path = 1


        window.blit(lantern, (x, y))
        n+=1
    elif mode_jeu == "explications":
        window.blit(explications, (0,0))
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        
        touche_pressee = pygame.key.get_pressed()
        
        if touche_pressee[pygame.K_RETURN]:
            mode_jeu = "game"
            start_time = pygame.time.get_ticks()
                
    else:
        window.blit(main_menu_background, (0, 0))
        
        if (450 <= pygame.mouse.get_pos()[0] <= 450+main_menu_jouer.get_size()[0]) and (350 <= pygame.mouse.get_pos()[1] <= 350+main_menu_jouer.get_size()[1]):
            window.blit(main_menu_jouer_big, (int(450-((main_menu_jouer_big.get_size()[0]-main_menu_jouer.get_size()[0])/2)) , int(350-((main_menu_jouer_big.get_size()[1]-main_menu_jouer.get_size()[1])/2))))
        else:
            window.blit(main_menu_jouer, (450, 350))
        if (450 <= pygame.mouse.get_pos()[0] <= 450+main_menu_quitter.get_size()[0]) and (470 <= pygame.mouse.get_pos()[1] <= 470+main_menu_quitter.get_size()[1]):
            window.blit(main_menu_quitter_big, (int(450-((main_menu_quitter_big.get_size()[0]-main_menu_quitter.get_size()[0])/2)) , int(470-((main_menu_quitter_big.get_size()[1]-main_menu_quitter.get_size()[1])/2))))
        else:
            window.blit(main_menu_quitter, (450, 470))
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (450 <= pygame.mouse.get_pos()[0] <= 450+main_menu_jouer.get_size()[0]) and (350 <= pygame.mouse.get_pos()[1] <= 350+main_menu_jouer.get_size()[1]):
                        mode_jeu = "explications"
                    if (450 <= pygame.mouse.get_pos()[0] <= 450+main_menu_quitter.get_size()[0]) and (470 <= pygame.mouse.get_pos()[1] <= 470+main_menu_quitter.get_size()[1]):
                        pygame.quit()

                
        #Arrête le programme si la fenêtre est fermée

        

    clock.tick(60)
    pygame.display.update()


