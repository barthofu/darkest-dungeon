from random import *
from math import *
from copy import deepcopy
from time import *
import pygame

pygame.init()
pygame.font.init()

c = 101
l = 101
matrice = [[1 if i%2==1 else -1 for i in range (c)] if y%2==0 else [1 for i in range (c)] for y in range(l)]
pos = [0,0]
hist = []
copied_hist = None
end = False



def check(l, c, matrice): 
    possibilites = []
    try:
        if matrice[l+2][c] == -1 and matrice[l+1][c] == 1:
            possibilites.append([l+2, c])
    except:
        pass
    try:
        if matrice[l-2][c] == -1 and matrice[l-1][c] == 1:
            possibilites.append([l-2, c])
    except:
        pass
    try:
        if matrice[l][c+2] == -1 and matrice[l][c+1] == 1:
            possibilites.append([l, c+2])
    except:
        pass
    try:
        if matrice[l][c-2] == -1 and matrice[l][c-1] == 1:
            possibilites.append([l, c-2])
    except:
        pass
    if len(possibilites) != 0:
        go = possibilites[randint(0,len(possibilites)-1)]
    else:
        go = None
    return go

while end == False:
    go = check(pos[0], pos[1], matrice)
    if [pos[0], pos[1]] not in hist:
        hist.append([pos[0], pos[1]])
    if go == None:
        hist.pop()
        pos = [hist[len(hist)-1][0], hist[len(hist)-1][1]]
    else:
        matrice[pos[0]][pos[1]] = 0
        matrice[int(pos[0]+(go[0]-pos[0])/2)][int(pos[1]+(go[1]-pos[1])/2)] = 0
        matrice[go[0]][go[1]] = 0
        pos = [go[0], go[1]]
    if pos == [0, 0]:
        end = True
    elif pos == [l-1, c-1]:
        copied_hist = deepcopy(hist)


'''for i in range (0,l):
    print(f"{matrice[i][0]} {matrice[i][1]} {matrice[i][2]} {matrice[i][3]} {matrice[i][4]} {matrice[i][5]} {matrice[i][6]} {matrice[i][7]} {matrice[i][8]} {matrice[i][9]} {matrice[i][10]} {matrice[i][11]} {matrice[i][12]} {matrice[i][13]} {matrice[i][14]} {matrice[i][15]} {matrice[i][16]} {matrice[i][17]} {matrice[i][18]} {matrice[i][19]} {matrice[i][20]} {matrice[i][21]} {matrice[i][22]} {matrice[i][23]} {matrice[i][24]} {matrice[i][25]} {matrice[i][26]} {matrice[i][27]} {matrice[i][28]} {matrice[i][29]}")

print(copied_hist)
'''








coeff = 700/ceil(len(matrice)/2)
padx = 290
pady = 10

window = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Pong")
font = pygame.font.SysFont("comic sans ms", 64)
clock = pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
FOND_1 = (54,57,63)
FOND_2 = (80,83,90)

window.fill(FOND_1)

pygame.draw.rect(window, FOND_2, (padx, pady, 700, 700))
pygame.draw.rect(window, BLANC, (padx, pady, 700, 700), 3)


for i in range (0, len(matrice)):
    for j in range (0, len(matrice[i])):
        if i%2==0 and j%2==0:
            #print(f"y,x = {i},{j}")
            #l = []
            try:
                if matrice[i][j+1] == 1:
                    pygame.draw.line(window, BLANC, (ceil((j+1)/2)*coeff+padx, ceil(i/2)*coeff+pady), (ceil((j+1)/2)*coeff+padx, ceil((i+1)/2)*coeff+pady))
                    #l.append("⇨")
            except:
                pass
            try:
                if matrice[i][j-1] == 1:
                    pygame.draw.line(window, BLANC, (ceil(j/2)*coeff+padx, ceil(i/2)*coeff+pady), (ceil(j/2)*coeff+padx, ceil((i+1)/2)*coeff+pady))
                    #l.append("⇦")             
            except:
                pass
            try:
                if matrice[i+1][j] == 1:
                    pygame.draw.line(window, BLANC, (ceil(j/2)*coeff+padx, ceil((i+1)/2)*coeff+pady), (ceil((j+1)/2)*coeff+padx, ceil((i+1)/2)*coeff+pady))
                    #l.append("⇩")
            except:
                pass
            try:
                if matrice[i-1][j] == 1:
                    pygame.draw.line(window, BLANC, (ceil(j/2)*coeff+padx, ceil(i/2)*coeff+pady), (ceil((j+1)/2)*coeff+padx, ceil(i/2)*coeff+pady))
                    #l.append("⇧")
            except:
                pass
            #print(" ".join(l))
            #print("===============")
            
'''
for coor in copied_hist:
    pygame.draw.rect(window, FOND_1, (ceil(coor[1]/2)*coeff+coeff/3+padx, ceil(coor[0]/2)*coeff+coeff/3+pady, coeff/3, coeff/3))
'''

def resolve():
    div = 8
    for i in range (0, len(copied_hist)+ceil(len(copied_hist)/div)+1):
        try:
            pygame.draw.rect(window, FOND_1, (ceil(copied_hist[i][1]/2)*coeff+coeff/3+padx, ceil(copied_hist[i][0]/2)*coeff+coeff/3+pady, coeff/3, coeff/3))
        except:
            pass
        if i > ceil(len(copied_hist)/div):
            pygame.draw.rect(window, FOND_2, (ceil(copied_hist[i-1-ceil(len(copied_hist)/div)][1]/2)*coeff+coeff/3+padx, ceil(copied_hist[i-1-ceil(len(copied_hist)/div)][0]/2)*coeff+coeff/3+pady, coeff/3, coeff/3))
        pygame.display.flip()
        sleep(0.04)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    touche_pressee = pygame.key.get_pressed()
    if touche_pressee[pygame.K_q]:
        resolve()
    pygame.display.update()