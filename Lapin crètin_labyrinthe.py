"""Jeu Lapin crétin labyrinthe.
But du jeu: déplacer le lapin jusqu'au gâteau"""

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

#Icone du jeu
icone = pygame.image.load("LP_bas.jpg")
pygame.display.set_icon(icone)

#Nom de la fenêtre
pygame.display.set_caption("Lapin Crétin")

"""Définition de la classe Niveau permettant de créer la structure du labyrinthe"""
class Niveau: 
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    """ méthode permettant de générer le niveau en fonction du fichier.
    On crée une liste contenant une liste par ligne à afficher"""
    def generateur(self):
        #Ouverture du fichier
        with open(self.fichier, "r") as fichier: 
            structure_niveau = []
            #Parcourt des lignes du fichier
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    #Ajout du sprite à la liste de la ligne
                    ligne_niveau.append(sprite)
                #Ajout de la ligne à la structure du niveau
                structure_niveau.append(ligne_niveau)
            #Sauvegarde de la structure
            self.structure = structure_niveau

    """Méthode permettant d'afficher le niveau en fonction de la liste renvoyée par generateur"""
    def affichage(self, fenetre):

        #Chargement des images
        mur = pygame.image.load("mur.jpeg").convert()
        depart = pygame.image.load("debut.jpeg").convert()
        arrivee = pygame.image.load("gateau.jpg").convert()

        #Parcourt de la iste du niveau
        num_ligne = 0
        for ligne in self.structure:  #Parcourt des listes de ligne
            num_case = 0
            for sprite in ligne:  #Calcul de la position réelle en pixels
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

"""Classe permettant de créer le personnage"""
class Personnage:

    def __init__(self, droite, gauche, haut, bas, level):  #Sprites du personnage
        self.droite = pygame.image.load(droite).convert_alpha()
        self.gauche = pygame.image.load(gauche).convert_alpha()
        self.haut = pygame.image.load(haut).convert_alpha()
        self.bas = pygame.image.load(bas).convert_alpha()
        #Position du personnage en cases et pixels
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        #Direction par défaut
        self.direction = self.droite
        #Niveau dans lequel se trouve le personnage
        self.niveau = niveau

    #Réglage des déplacements du personnage
    def deplacement(self, direction):
        if direction == 'droite':
            if self.case_x < (nb_sprite_cote - 1): #Pour ne as dépasser l'écran
                #Vérification si la case de destination n'est pas un mur
                if self.niveau.structure[self.case_y][self.case_x +1] != 'm':
                    self.case_x += 1 #Déplacement d'une case
                    self.x = self.case_x * taille_sprite #Calcul de la position
            self.direction = self.droite #Image dans la bonne direction

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

"""Définition de 2 fonctions permettant d'afficher une image de fin de partie"""                
def Gagné(x, y, image):
    fenetre.blit(image, (x,y))

def Message(m, couleur):
    screen_text = font.render(m, False, couleur)
    fenetre.blit(screen_text, [cote_fenetre / 2, cote_fenetre / 2])


#Boucle principale
continuer = True
while continuer:
    #Chargement et affichage de l'écran d'accueil
    presentation = pygame.image.load("accueil_1.jpg").convert()
    fenetre.blit(presentation, (0,0))


    pygame.display.flip() #Rafraichissement de la fenêtre

    #Variables remises à condition à chaque tour de boucle
    continuer_game = True
    continuer_presentation = True

    #Boucle d'accueil
    while continuer_presentation :
        clock = pygame.time.Clock() #Limitation de la vitesse de la boucle
        clock.tick(30)

        for event in pygame.event.get():

            #Si le joueur quitte, on ne parcourt aucune boucle
            if event.type == QUIT or event.type == KEYDOWN and  event.key ==  K_ESCAPE :
                continuer_presentation = False
                continuer_game = False
                continuer = False

                #Variable de choix du niveau
                choix = False

            elif event.type == KEYDOWN:

                #Lancement niveau 1
                if event.key == K_F1:  
                    continuer_presentation = False
                    choix = 'niveau_1'

                #Lancement niveau 2
                elif event.key == K_F2:
                    continuer_presentation = False
                    choix = 'niveau_2'

    #Vérification du choix du joueur
    if choix != False:

        #Chargement du fond principal
        fond = pygame.image.load("fond noir.png").convert()

        #On génère un niveau à partir de la classe Niveau
        niveau = Niveau(choix)
        niveau.generateur()
        niveau.affichage(fenetre)
        
        #Création du perso grâce à la classe Personnage
        lapin_cretin = Personnage("LP_droite.jpg", "LP_gauche.jpg", "LP_haut.jpg", "LP_bas.jpg", niveau)

    #Boucle de jeu
    while continuer_game:
    
        #Limitation de la vitesse de la boucle
        clock = pygame.time.Clock()
        clock.tick(30)

        for event in pygame.event.get():

            #Si le joueur quitte, on ferme la fenêtre
            if event.type == QUIT:
                continuer_game = False
                continuer = False
                
            elif event.type == KEYDOWN: # si l'évènement est enfoncement d'une touche

                #Si le joueur presse Echap, on revient à la page d'accueil
                if event.key == K_ESCAPE: 
                    continuer_game = False

                #Déplacements du personnage
                elif event.key == K_RIGHT:
                    lapin_cretin.deplacement('droite')
                                           
                elif event.key == K_LEFT:
                    lapin_cretin.deplacement('gauche')
                   
                elif event.key == K_UP:
                    lapin_cretin.deplacement('haut')
        
                elif event.key == K_DOWN:
                    lapin_cretin.deplacement('bas')

        #Chargement et affichage de l'image de fin de partie            
        gagné = pygame.image.load("bingo.jpg").convert_alpha()
        font = pygame.font.SysFont('showcard gothic', 50)  #Module pour la police et la taille
        noir = (0,0,0)  #Code couleur selon le codage rouge, vert, bleu
        
        #Affichage aux nouvelles positions
        fenetre.blit(fond, (0,0)) 
        niveau.affichage(fenetre)
        fenetre.blit(lapin_cretin.direction, (lapin_cretin.x, lapin_cretin.y))
        pygame.display.flip()  #Rafraichissement de la fenêtre

        if niveau.structure[lapin_cretin.case_y][lapin_cretin.case_x] == 'a':
            clock = pygame.time.Clock()
            clock.tick(30)

            bleu = (113,177,227)
            fenetre.fill(bleu) #méthode permettant d'afficher la couleur
            x = 0
            y = 10
            Gagné(x,y,gagné) #appel fonction Gagné
            Message("Gagné !", noir) # appel fonction Message
            pygame.display.flip()  #Rafraichissement de la fenêtre
            time.sleep(6) #Module définissant le nombre de secondes qui passent entre la fin de la partie et le retour à l'accueil

            continuer_game = False



pygame.quit()
quit()
                
    
        
    

        
        

