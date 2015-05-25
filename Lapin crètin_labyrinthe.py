import pygame

from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre pygame
nb_sprite_cote = 15
taille_sprite = 30
cote_fenetre = nb_sprite_cote * taille_sprite

fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))

icone = pygame.image.load("LP_droite.jpg")
pygame.display.set_icon(icone)

pygame.display.set_caption("Lapin Crètin")

class Niveau:
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generateur(self):
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    if sprite != '\n':
                        ligne_niveau.append(sprite)
                structure_niveau.append(ligne_niveau)
            self.structure = structure_niveau

    def affichage(self, fenetre):
        mur = pygame.image.load("mur.jpeg").convert()
        depart = pygame.image.load("debut.jpeg").convert()
        arrivee = pygame.image.load("gateau.jpg").convert_alpha()

        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite == 'd':
                    fenetre.blit(depart, (x,y))
                elif sprite == 'm':
                    fenetre.blit(mur, (x,y))
                elif sprite == 'a':
                    fenetre.blit(arrivee, (x,y))

                num_case += 1
            num_ligne +=1


class Personnage:

    def __init__(self, droite, gauche, haut, bas, level):
        self.droite = pygame.image.load(droite).convert_alpha()
        self.gauche = pygame.image.load(gauche).convert_alpha()
        self.haut = pygame.image.load(haut).convert_alpha()
        self.bas = pygame.image.load(bas).convert_alpha()
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        self.direction = self.droite
        self.niveau = niveau

    def deplacement(self, direction):
        if direction == 'droite':
            if self.case_x < (nb_sprite_cote - 1):
                if self.niveau.structure[self.case_y][self.case_x +1] != 'm':
                    self.case_x += 1
                    self.x = self.case_x * taille_sprite
            self.direction = self.droite

        if direction == 'gauche':
            if self.case_x > 0:
                if self.niveau.structure[self.case_y][self.case_x - 1] != 'm':
                    self.case_x -= 1
                    self.x = self.case_x * taille_sprite
            self.direction = self.gauche


        if direction == 'haut':
            if self.case_y > 0:
                if self.niveau.structure[self.case_y - 1][self.case_x] != 'm':
                    self.case_y -= 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.haut


        if direction == 'bas':
            if self.case_y < (nb_sprite_cote - 1):
                if self.niveau.structure[self.case_y + 1][self.case_x] != 'm':
                    self.case_y +=1
                    self.y = self.case_y * taille_sprite
            self.direction = self.bas
                    
                    



    
        
#Boucle principale
continuer = 1
while continuer:
    presentation = pygame.image.load("accueil_1.jpg").convert()
    fenetre.blit(presentation, (0,0))


    pygame.display.flip()

    continuer_game = 1
    continuer_presentation = 1


    while continuer_presentation :
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and  event.key ==  K_ESCAPE :
                continuer_presentation = 0
                continuer_game = 0
                continuer = 0
                choix = 0
            elif event.type == KEYDOWN:
                if event.key == K_F1:  
                    continuer_presentation = 0
                    choix = 'niveau_1'
                elif event.key == K_F2:
                    continuer_presentation = 0
                    choix = 'niveau_2'


    if choix != 0:

        fond = pygame.image.load("fond noir.png").convert()
        niveau = Niveau(choix)
        niveau.generateur()
        niveau.affichage(fenetre)

        lapin_cretin = Personnage("LP_droite.jpg", "LP_gauche.jpg", "LP_haut.jpg", "LP_bas.jpg", niveau)

    while continuer_game:
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():

            if event.type == QUIT:
                
                continuer_game = 0
                continuer = 0
                
            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    continuer_game = 0

                elif event.key == K_RIGHT:
                    lapin_cretin.deplacement('droite')
                    
                            
                elif event.key == K_LEFT:
                    lapin_cretin.deplacement('gauche')
                   
                elif event.key == K_UP:
                    lapin_cretin.deplacement('haut')
        
                elif event.key == K_DOWN:
                    lapin_cretin.deplacement('bas')
                    


        fenetre.blit(fond, (0,0))
        niveau.affichage(fenetre)
        fenetre.blit(lapin_cretin.direction, (lapin_cretin.x, lapin_cretin.y))
        pygame.display.flip()

        if niveau.structure[lapin_cretin.case_y][lapin_cretin.case_x] == 'a':
            continuer_game = 0



pygame.quit()
                

    
        
    

        
        

