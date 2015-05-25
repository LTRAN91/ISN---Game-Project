import pygame

import time

import sys

from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre pygame
nb_sprite_cote = 15
taille_sprite = 30
cote_fenetre = nb_sprite_cote * taille_sprite
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))

icone = pygame.image.load("LP_droite.jpg")
pygame.display.set_icon(icone)

# Nom de la fenêtre
pygame.display.set_caption("Lapin Crétin")

class Niveau: # classe Niveau pour créer la structure du labyrinthe
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generateur(self):
        with open(self.fichier, "r") as fichier: # lecture du fichier
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    if sprite != '\n': # on ignore les '\n'
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
    #Réglage des déplacements du personnage
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
continuer = True
while continuer:
    presentation = pygame.image.load("accueil_1.jpg").convert()
    fenetre.blit(presentation, (0,0))


    pygame.display.flip() # Méthode permettant le rafraichissement

    continuer_game = True
    continuer_presentation = True


    while continuer_presentation :
        clock = pygame.time.Clock() #méthode permettant de limiter la vitesse
        clock.tick(30)

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and  event.key ==  K_ESCAPE :
                continuer_presentation = False
                continuer_game = False
                continuer = False
                choix = False
            elif event.type == KEYDOWN:
                if event.key == K_F1:  
                    continuer_presentation = False
                    choix = 'niveau_1'
                elif event.key == K_F2:
                    continuer_presentation = False
                    choix = 'niveau_2'


    if choix != False:

        fond = pygame.image.load("fond noir.png").convert()
        niveau = Niveau(choix)
        niveau.generateur()
        niveau.affichage(fenetre)
        
        #Appel de la classe Personnage
        lapin_cretin = Personnage("LP_droite.jpg", "LP_gauche.jpg", "LP_haut.jpg", "LP_bas.jpg", niveau)

    while continuer_game:
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():

            if event.type == QUIT:
                
                continuer_game = False
                continuer = False
                
            elif event.type == KEYDOWN: # si l'évènement est enfoncement d'une touche

                if event.key == K_ESCAPE: 
                    continuer_game = False

                elif event.key == K_RIGHT:
                    lapin_cretin.deplacement('droite')
                    
                            
                elif event.key == K_LEFT:
                    lapin_cretin.deplacement('gauche')
                   
                elif event.key == K_UP:
                    lapin_cretin.deplacement('haut')
        
                elif event.key == K_DOWN:
                    lapin_cretin.deplacement('bas')
                    


        fenetre.blit(fond, (0,0)) #collage de l'image sur l'écran
        niveau.affichage(fenetre)
        fenetre.blit(lapin_cretin.direction, (lapin_cretin.x, lapin_cretin.y))
        pygame.display.flip()

        
        # 2 fonctions pour l'affichage de fin : image + écriture
        def Gagné(x,y,image):
            fenetre.blit(image, (x,y))
        gagné = pygame.image.load("bingo.jpg").convert_alpha()

        font = pygame.font.SysFont('showcard gothic', 50) #module pour la police du texte + la taille

        def message(m, couleur):
            screen_text = font.render(m, False, couleur)
            fenetre.blit(screen_text, [cote_fenetre/2 , cote_fenetre/2])

        noir = (0,0,0) # code couleur selon le codage (rouge,vert,bleu)
            

        if niveau.structure[lapin_cretin.case_y][lapin_cretin.case_x] == 'a':
            bleu = (113,177,227)
            
            fenetre.fill(bleu) #méthode permettant d'afficher la couleur
            x = 0
            y = 10
            Gagné(x,y,gagné) #appel fonction Gagné
            message("Gagné !", noir) # appel fonction message
            pygame.display.flip()
            time.sleep(2) # module permettant d'arreter le temps 
            clock = pygame.time.Clock()
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    continuer_game = False



pygame.quit()
quit()
                
    
        
    

        
        

