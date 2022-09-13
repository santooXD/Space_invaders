# Import libreries
from cProfile import run
from cgitb import text
from pickle import GLOBAL
from re import A, X
from shutil import move
from tkinter import Widget
from turtle import distance, width
from webbrowser import get
import pygame 
import random
import math
from pygame import mixer
random.randint(0, 10)

# initializate pygame
pygame.init()

# windows size
screen_width = 800
screen_height = 600

# size variable

size = (screen_width,  screen_height)

# display window

screen = pygame.display.set_mode( size )

# Background image
ground = pygame.image.load("fondo.png")

# Titule
pygame.display.set_caption("Invaders")

#Icon
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("Player1.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy 
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

# numbers of enemies
number_enemies = 13
# Create multiple enemies
for item in range( number_enemies ):
    enemy_img.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 800))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append( 5 )
    enemy_y_change.append( 15 ) 



# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 5
bullet_state = "ready"

# Score
scrore = 1

# Font variable
score_font = pygame.font.Font("Stocky-lx5.ttf", 32)

# text position
text_x = 10
text_y = 10

# Game over text
go_font = pygame.font.Font("Stocky-lx5.ttf", 64)
go_x = 200
go_y = 250


# Game over function
def game_over(x, y):
    go_text = go_font.render("Game over :(", True,(255, 255, 255))
    screen.blit( go_text, (x, y) )
    Game_over_sound = mixer.Sound("videogame-death-sound-43894 (1).wav")
    Game_over_sound.play()
    

# text function
def show_text( x, y ):
    score_text = score_font.render(" SCORE:   " + str( scrore ), True, (255, 255, 255))
    screen.blit( score_text, (x, y) )




# Player function 
def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy function 
def enemy(x, y, item):
    screen.blit(enemy_img[item],  (x, y)) 

# fire function
def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Collision function
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt( (enemy_x - bullet_x) ** 2 + ( enemy_y - bullet_y) ** 2)

    if distance < 27:
        return True
    else:
        return False

# Bordes Izquierda
if player_x <= 0:
    player_x = 0 



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Movimientos del Personaje
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("hit-someting-6037.wav")
                    bullet_sound.play()
                    bullet_x = player_x 
                fire(player_x, bullet_y)
# Si una tecla fue levantada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change == 0

    # Color Rgb: red - green - blue
    Rgb = (0, 0 , 0)
    screen.fill(Rgb)  

    # show background image
    screen.blit( ground, (0, 0) )
   
    # Call player function 
    player_x += player_x_change
    player(player_x, player_y)




# Bordes de derecha y izquierda
    if player_x <= 0:
       player_x = 0

    elif player_x >= 736:
        player_x = 736

    # Bordes del enemigo y movimiento
    for item in range(number_enemies):
        
# game over zone
        if enemy_y[ item ] > 440:
            for j in range( number_enemies ):
                enemy_y[ j ] = 2000

            # call game over function
            game_over( go_x, go_y)

            break

        enemy_x[item] += enemy_x_change[item]
        if enemy_x[item] <= 0:
            enemy_x_change[item] = 2
            enemy_y[item] += enemy_y_change[item] 

        elif enemy_x[item] >= 736:
            enemy_x_change[item] = -2
            enemy_y[item] += enemy_y_change[item]

        # Call collision function
        collision = is_collision(enemy_x[item], enemy_y[item], bullet_x, bullet_y)
        if collision: 
            explosion_sound = mixer.Sound("monster-attack-47786.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            scrore += 1 
            #print(scrore)
            enemy_x[item] = random.randint(0, 735)
            enemy_y[item] = random.randint(50, 150)
        # Call enemy function
        enemy(enemy_x[item], enemy_y[item], item)



    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready" 

    if bullet_state == "fire":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change   
     
   # Call the text function
    show_text(text_x, text_y )

    # Update Windows
    pygame.display.update()
