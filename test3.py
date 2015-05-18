import pygame
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1000, 840))

#Chargement et collage du fond
fond = pygame.image.load("fond noir.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = pygame.image.load("Happy.png").convert_alpha()
position_perso = perso.get_rect()
fenetre.blit(perso, (0,0))

#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_DOWN: #Si "flèche bas"
                #On descend le perso
                position_perso = position_perso.move(0,3)
            elif event.key == K_UP:
                position_perso = position_perso.move(0,-3)
            elif event.key == K_LEFT:
                position_perso = position_perso.move(-3,0)
            elif event.key == K_RIGHT:
                position_perso = position_perso.move(3,0)
    
    #Re-collage
    fenetre.blit(fond, (0,0))   
    fenetre.blit(perso, position_perso)
    #Rafraichissement
    pygame.display.flip()

class Level:
    def __init__(self, fichier):
        self.fichier = fichier
        self.forme =  0

    def generer(self):
        with open(self.fichier, 'r') as fichier:
            forme_level = []
            for ligne in fichier:
                ligne_level = []
                for lettre in ligne:
                    if lettre != '\n':
                        ligne_level.append(lettre)
                forme_level.append(ligne_level)
            self.forme = forme_level

    def affichage(self, fenetre):
	    mur = pygame.image.load(image_mur).convert()
	    depart = pygame.image.load(image_depart).convert()
	    arrivee = pygame.image.load(image_arrivee).convert()
	    num_ligne = 0
	    for ligne in self.structure:
                num_case = 0
		    x = num_case * taille.lettre
		    y = num_ligne * taille.lettre
		    if lettre == "d":
			    fenetre.blit(depart,(x,y))
                elif lettre == "a":
			    fenetre.blit(arrivee,(x,y))
                elif lettre == "m":
			    fenetre.blit(mur,(x,y))
                    num_case += 1
          num_ligne += 1


nb_sprite_cote = 9
taille_sprite = 25
cote_fenetre = nb_sprite_cote * taille_sprite

fond_accueil = "accueil.png"
decor = "mur.jpeg"
depart = "départ.jpeg"
arrivee = "nemo.jpeg"
    

pygame.quit()    
