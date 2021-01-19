import pygame
import random
import math

# Intialize the pygame
pygame.init()

# Create the screen               w     h
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Wallpaper.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('planet.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(0.3)
    enemyY_Change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_Change = 2
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 35)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 69)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (217, 130, 181))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER :(", True, (217, 130, 181))
    screen.blit(over_text, (150, 250))


font2 = pygame.font.Font("freesansbold.ttf", 10)

name_Value = 0
nameX = 625
nameY = 570


def show_Name(x, y):
    name = font2.render("Created by Hannah Ghassabeh", True, (255, 255, 255))
    screen.blit(name, (x, y))


# drawing player image onto the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# drawing enemy image onto the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 20))


# Bullet and enemy collison
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB         R   G   B        (0-255)
    screen.fill((0, 128, 128))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if right or left
        if event.type == pygame.KEYDOWN:  # pressing key
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.5
            # firing bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # letting go of the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # checking for boundaries of spaceship
    # doesn't go out of the screen bounds
    playerX += playerX_Change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 0.3
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -0.3
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    show_score(textX, textY)

    show_Name(nameX, nameY)

    player(playerX, playerY)

    # update display
    pygame.display.update()
