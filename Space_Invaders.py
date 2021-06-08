import pygame
from pygame import mixer
import random
import math

pygame.init()

# Create the screen

screen = pygame.display.set_mode((1000, 800))

# Background
background = pygame.image.load('space.png')

# Background Music

mixer.music.load('time.mp3')
mixer.music.play(- 1)

# Title and Icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('extraterrestrial.png')
pygame.display.set_icon(icon)

# Player

playerImg = pygame.image.load('space-invaders.png')
playerX = 460
playerY = 650
playerX_Change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('evil (1).png'))
    enemyX.append(random.randint(20, 736))
    enemyY.append(random.randint(0, 170))
    enemyX_Change.append(0.5)
    enemyY_Change.append(40)

# Bullet

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 650
bulletX_Change = 0
bulletY_Change = 4
bullet_state = "ready"

# Score

score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over :" + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (280, 330))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((250, 250, 250))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = - 1.5
            if event.key == pygame.K_RIGHT:
                playerX_Change = + 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    # Enemy Movement
    for i in range(num_of_enemies):

        # GAME OVER
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 1.1
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 936:
            enemyX_Change[i] = - 1.1
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()
            bulletY = 650
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(20, 736)
            enemyY[i] = random.randint(0, 170)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 5:
        bulletY = 650
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
