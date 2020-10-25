"""
Full Project Link : https://github.com/Saadman-Galib/Project--01-Space-Invaders-Game-with-Pygame
Author: Md. Saadman Galib Rabbi
Youtube: https://rb.gy/e6piqa
Facebook: https://rb.gy/9ckb8m
Instagram: https://rb.gy/xluody
"""

import pygame as pg
import random as rd
import math as mt
from pygame import mixer


# Intialize the pygame
pg.init()

# Create the screen
screen = pg.display.set_mode((800, 600))

# Background
background = pg.image.load('background.png ')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.2)

# Caption and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("Untitled.png")
pg.display.set_icon(icon)

# Player
PlayerImg = pg.image.load("spaceship.png")
playerX = 350
playerY = 470
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load("real enemy.png"))
    enemyX.append(rd.randint(0, 735)) # 335
    enemyY.append(rd.randint(50, 150)) # 2
    enemyX_change.append(6)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pg.image.load("bullet.png")
bulletX = 0
bulletY = 470
bulletX_change = 2
bulletY_change = 12
bullet_state = 'ready'

score = 0

# Score

score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game Over text
over_font = pg.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 41.8, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = mt.sqrt((mt.pow(enemyX-bulletX-28, 2)) + (mt.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:
    # RGB = Red, Green, Blue
    screen.fill((160, 160, 160))

    # Background Image
    screen.blit(background,(0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -5
            if event.key == pg.K_RIGHT:
                playerX_change = 5
            if event.key == pg.K_KP_ENTER:
                if bullet_state is 'ready':
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pg.K_SPACE:
                if bullet_state is 'ready':
                    # Get the current x cordinate of the spaceship
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.set_volume(0.2)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pg.KMOD_ALT or event.key == pg.K_F4:
                running = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0


    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= -30:
        playerX = -30
    elif playerX >= 715:
        playerX = 715

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 470:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.set_volume(0.15)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = rd.randint(0, 735)
            enemyY[i] = rd.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)

    pg.display.update()