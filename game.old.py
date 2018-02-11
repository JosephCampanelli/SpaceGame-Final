import pygame
import os
import sys
import math
import random

random.seed()

pygame.init()

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Game')

obstacles = []

i = 0

while i < 3:

    if random.randint(0, 1) % 2 == 0:
        start_val = (random.randint(100, 650), random.randint(0, 400))

        obstacles.append(pygame.Rect(start_val, (20,200)))
    else:
        start_val = (random.randint(100, 450), random.randint(100, 500))

        obstacles.append(pygame.Rect(start_val, (200,20)))

    i += 1

clock = pygame.time.Clock()

rotation1 = 270.0
rotation2 = 90.0

ship_width = 40
ship_height = 40

bullet_width = 16
bullet_height = 16

p_width = 32
p_height = 32

global ship1lives
global ship2lives
global boost_timer1
global boost_timer2
global firerate_timer1
global firerate_timer2
global powerups

bulletImg = pygame.image.load('bullet.png').convert_alpha()
ship1Img = pygame.image.load('ship1.png').convert_alpha()
ship2Img = pygame.image.load('ship2.png').convert_alpha()
trueShip1Img = pygame.transform.rotate(ship1Img, rotation1)
trueShip2Img = pygame.transform.rotate(ship2Img, rotation2)
life = pygame.image.load('life.png').convert_alpha()
p1 = pygame.image.load('boost.png').convert_alpha()
p2 = pygame.image.load('firerate.png').convert_alpha()
p3 = pygame.image.load('hp.png').convert_alpha()

class Bullet:
    def __init__(self, newXPos, newYPos, newXMomentum, newYMomentum):
        self.xPos = newXPos
        self.yPos = newYPos
        self.xMomentum = newXMomentum
        self.yMomentum = newYMomentum

bullets1 = []
bullets2 = []

def shoot(xPos, yPos, xMom, yMom, bullets):
    bullets.append(Bullet(xPos+(ship_width/2)-(bullet_width/2), yPos+(ship_height/2)-(bullet_height/2), xMom, yMom))

def ship1(x,y):
    gameDisplay.blit(trueShip1Img,(x1,y1))
    if(ship1lives >= 1):
        gameDisplay.blit(life,(x1-5,y1+42))
    if(ship1lives >= 2):
        gameDisplay.blit(life,(x1+11,y1+42))
    if(ship1lives == 3):
        gameDisplay.blit(life,(x1+29,y1+42))

def ship2(x,y):
    gameDisplay.blit(trueShip2Img,(x2,y2))
    if(ship2lives >= 1):
        gameDisplay.blit(life,(x2-5,y2+42))
    if(ship2lives >= 2):
        gameDisplay.blit(life,(x2+11,y2+42))
    if(ship2lives == 3):
        gameDisplay.blit(life,(x2+29,y2+42))

ship1lives = 3
ship2lives = 3

global x1
global x2
global y1
global y2

x1 = 50+(ship_width/2)
y1 = 300+(ship_height/2)

x2 = 750-(ship_width/2)
y2 = 300+(ship_height/2)

momentum1_flag = False
x1Momentum = 0.0
y1Momentum = 0.0
x1MomentumMax = 5
x1MomentumMin = -5
y1MomentumMax = 5
y1MomentumMin = -5

momentum2_flag = False
x2Momentum = 0.0
y2Momentum = 0.0
x2MomentumMax = 5
x2MomentumMin = -5
y2MomentumMax = 5
y2MomentumMin = -5

cooldown1 = 0
cooldown2 = 0

redWin = False
blueWin = False

pygame.key.set_repeat(1, 10)

#POWERUPS
powerups = []

class Powerup:
    def __init__(self):
        self.xPos = random.randint(100, 700)
        self.yPos = random.randint(100, 500)
        self.pType = random.randint(1, 3)

boost_timer1 = 0
firerate_timer1 = 0

boost_timer2 = 0
firerate_timer2 = 0


def test_for_powerup():
    global x1
    global x2
    global y1
    global y2
    global ship1lives
    global ship2lives
    global boost_timer1
    global boost_timer2
    global firerate_timer1
    global firerate_timer2
    global powerups


    for p in powerups:
        if x1+ship_width > p.xPos and x1 < p.xPos+p_width and y1+ship_height > p.yPos and y1 < p.yPos+p_height:
            if p.pType == 1:
                boost_timer1 = 1000
            if p.pType == 2:
                firerate_timer1 = 500
            else:
                if ship1lives < 3:
                    ship1lives += 1

    new_powerups = []

    for p in powerups:
        if not(x1+ship_width > p.xPos and x1 < p.xPos+p_width and y1+ship_height > p.yPos and y1 < p.yPos+p_height):
            new_powerups.append(p)

    powerups = new_powerups

    for p in powerups:
        if x2+ship_width > p.xPos and x2 < p.xPos+p_width and y2+ship_height > p.yPos and y2 < p.yPos+p_height:
            if p.pType == 1:
                boost_timer2 = 1000
            if p.pType == 2:
                firerate_timer2 = 500
            else:
                if ship2lives < 3:
                    ship2lives += 1

    new_powerups = []

    for p in powerups:
        if not(x2+ship_width > p.xPos and x2 < p.xPos+p_width and y2+ship_height > p.yPos and y2 < p.yPos+p_height):
            new_powerups.append(p)

    powerups = new_powerups

def test_collision(obstacles):
    global x1
    global x2
    global y1
    global y2
    global bullets1
    global bullets2

    for ob in obstacles:
        if x1+ship_width > ob.left and x1 < ob.left+ob.width and y1+ship_height > ob.top and y1 < ob.top+ob.height:

            diff1 = (x1+ship_width) - ob.left
            diff2 = x1 - (ob.left+ob.width)
            diff3 = (y1+ship_height) - ob.top
            diff4 = y1 - (ob.top+ob.height)

            if math.fabs(diff1) < math.fabs(diff2) and math.fabs(diff1) < math.fabs(diff3) and math.fabs(diff1) < math.fabs(diff4):
                x1 = ob.left-ship_width

            elif math.fabs(diff2) < math.fabs(diff1) and math.fabs(diff2) < math.fabs(diff3) and math.fabs(diff2) < math.fabs(diff4):
                x1 = ob.left+ob.width

            elif math.fabs(diff3) < math.fabs(diff1) and math.fabs(diff3) < math.fabs(diff2) and math.fabs(diff3) < math.fabs(diff4):
                y1 = ob.top-ship_height

            elif math.fabs(diff4) < math.fabs(diff1) and math.fabs(diff4) < math.fabs(diff2) and math.fabs(diff4) < math.fabs(diff3):
                y1 = ob.top+ob.height

        if x2+ship_width > ob.left and x2 < ob.left+ob.width and y2+ship_height > ob.top and y2 < ob.top+ob.height:

            diff1 = (x2+ship_width) - ob.left
            diff2 = x2 - (ob.left+ob.width)
            diff3 = (y2+ship_height) - ob.top
            diff4 = y2 - (ob.top+ob.height)

            if math.fabs(diff1) < math.fabs(diff2) and math.fabs(diff1) < math.fabs(diff3) and math.fabs(diff1) < math.fabs(diff4):
                x2 = ob.left-ship_width

            elif math.fabs(diff2) < math.fabs(diff1) and math.fabs(diff2) < math.fabs(diff3) and math.fabs(diff2) < math.fabs(diff4):
                x2 = ob.left+ob.width

            elif math.fabs(diff3) < math.fabs(diff1) and math.fabs(diff3) < math.fabs(diff2) and math.fabs(diff3) < math.fabs(diff4):
                y2 = ob.top-ship_height

            elif math.fabs(diff4) < math.fabs(diff1) and math.fabs(diff4) < math.fabs(diff2) and math.fabs(diff4) < math.fabs(diff3):
                y2 = ob.top+ob.height

        new_bullets = []

        for b in bullets1:
            if not (b.xPos+bullet_width > ob.left and b.xPos < ob.left+ob.width and b.yPos+bullet_height > ob.top and b.yPos < ob.top+ob.height):
                new_bullets.append(b)
        bullets1 = new_bullets

        new_bullets = []

        for b in bullets2:
            if not (b.xPos+bullet_width > ob.left and b.xPos < ob.left+ob.width and b.yPos+bullet_height > ob.top and b.yPos < ob.top+ob.height):
                new_bullets.append(b)
        bullets2 = new_bullets

quit_game = False
isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if boost_timer1 > 0:
        x1MomentumMax = 10
        x1MomentumMin = -10
        y1MomentumMax = 10
        y1MomentumMin = -10
    else:
        x1MomentumMax = 5
        x1MomentumMin = -5
        y1MomentumMax = 5
        y1MomentumMin = -5

    if boost_timer2 > 0:
        x2MomentumMax = 10
        x2MomentumMin = -10
        y2MomentumMax = 10
        y2MomentumMin = -10
    else:
        x2MomentumMax = 5
        x2MomentumMin = -5
        y2MomentumMax = 5
        y2MomentumMin = -5


    if(rotation1 > 360):
        rotation1 -= 360
    if(rotation1 < 0):
        rotation1 += 360

    if(rotation2 > 360):
        rotation2 -= 360
    if(rotation2 < 0):
        rotation2 += 360

    if cooldown1 > 10:
        cooldown1 -= 10
    else:
        cooldown1 = 0

    if cooldown2 > 10:
        cooldown2 -= 10
    else:
        cooldown2 = 0

    keys = pygame.key.get_pressed()

    if(keys[pygame.K_ESCAPE]):
        pygame.quit()
        quit()
    if(keys[pygame.K_f]):
        gameDisplay.toggle_fullscreen()
    if(keys[pygame.K_LEFT]):
        rotation1 += 3.0
    if(keys[pygame.K_RIGHT]):
        rotation1 -= 3.0
    if(keys[pygame.K_UP]):
        x1Momentum += math.cos((math.pi * (rotation1 + 90)) / 180)
        y1Momentum -= math.sin((math.pi * (rotation1 + 90)) / 180)
        if(x1Momentum > x1MomentumMax):
            x1Momentum = x1MomentumMax
        if(x1Momentum < x1MomentumMin):
            x1Momentum = x1MomentumMin
        if(y1Momentum > y1MomentumMax):
            y1Momentum = y1MomentumMax
        if(y1Momentum < y1MomentumMin):
            y1Momentum = y1MomentumMin
        momentum1_flag = True
    if(keys[pygame.K_DOWN]):
        if cooldown1 == 0:
            shoot(x1, y1, math.cos((math.pi * (rotation1 + 90)) / 180)*5, math.sin((math.pi * (rotation1 + 90)) / 180)*-5, bullets1)

            if(firerate_timer1 > 0):
                cooldown1 = 250
            else:
                cooldown1 = 500

    if(keys[pygame.K_a]):
        rotation2 += 3.0
    if(keys[pygame.K_d]):
        rotation2 -= 3.0
    if(keys[pygame.K_w]):
        x2Momentum += math.cos((math.pi * (rotation2 + 90)) / 180)
        y2Momentum -= math.sin((math.pi * (rotation2 + 90)) / 180)
        if(x2Momentum > x2MomentumMax):
            x2Momentum = x2MomentumMax
        if(x2Momentum < x2MomentumMin):
            x2Momentum = x2MomentumMin
        if(y2Momentum > y2MomentumMax):
            y2Momentum = y2MomentumMax
        if(y2Momentum < y2MomentumMin):
            y2Momentum = y2MomentumMin
        momentum2_flag = True
    if(keys[pygame.K_s]):
        if cooldown2 == 0:
            shoot(x2, y2, math.cos((math.pi * (rotation2 + 90)) / 180)*5, math.sin((math.pi * (rotation2 + 90)) / 180)*-5, bullets2)

            if(firerate_timer2 > 0):
                cooldown2 = 250
            else:
                cooldown2 = 500

    if momentum1_flag == False:
        x1Momentum *= .9
        y1Momentum *= .9
    else:
        momentum1_flag = False

    if momentum2_flag == False:
        x2Momentum *= .9
        y2Momentum *= .9
    else:
        momentum2_flag = False

    trueShip1Img = pygame.transform.rotate(ship1Img, rotation1)
    trueShip2Img = pygame.transform.rotate(ship2Img, rotation2)

    gameDisplay.fill((255,255,255))

    x1 += int(x1Momentum)
    y1 += int(y1Momentum)

    x2 += int(x2Momentum)
    y2 += int(y2Momentum)

    new_bullets = []

    for b in bullets1:

        b.xPos += b.xMomentum
        b.yPos += b.yMomentum
        gameDisplay.blit(bulletImg,(b.xPos, b.yPos))

        if not (b.xPos > 800 or b.xPos < 0 or b.yPos < 0 or b.yPos > 600):
            new_bullets.append(b)

    bullets1 = new_bullets

    new_bullets2 = []
    for b2 in bullets1:
        if not (b2.xPos+(bullet_width/2) > x2 and b2.xPos-(bullet_width/2) < x2+ship_width and b2.yPos+(bullet_height/2) > y2 and b2.yPos-(bullet_height/2) < y2+ship_height):
            new_bullets2.append(b2)
        else:
            ship2lives-=1
            if(ship2lives == 0):
                redWin = True
                isRunning = False

    bullets1 = new_bullets2

    new_bullets = []

    for b in bullets2:

        b.xPos += b.xMomentum
        b.yPos += b.yMomentum
        gameDisplay.blit(bulletImg,(b.xPos, b.yPos))

        if not (b.xPos+(bullet_width/2) > 800 or b.xPos-(bullet_width/2) < 0 or b.yPos+(bullet_height/2) < 0 or b.yPos-(bullet_height/2) > 600):
            new_bullets.append(b)

    bullets2 = new_bullets

    new_bullets2 = []
    for b2 in bullets2:
        if not (b2.xPos > x1 and b2.xPos < x1+ship_width and b2.yPos > y1 and b2.yPos < y1+ship_height):
            new_bullets2.append(b2)
        else:
            ship1lives-=1
            if(ship1lives == 0):
                blueWin = True
                isRunning = False

    bullets2 = new_bullets2

    if(x1 < 0):
        x1 = 0
        xMomentum1 = 0
    if(x1 > 750):
        x1 = 750
        xMomentum1 = 0
    if(y1 < 0):
        y1 = 0
        yMomentum1 = 0
    if(y1 > 550):
        y1 = 550
        yMomentum1 = 0

    if(x2 < 0):
        x2 = 0
        x2Momentum = 0
    if(x2 > 750):
        x2 = 750
        x2Momentum = 0
    if(y2 < 0):
        y2 = 0
        y2Momentum = 0
    if(y2 > 550):
        y2 = 550
        y2Momentum = 0

    test_collision(obstacles)

    test_for_powerup()

    if firerate_timer1 > 0:
        firerate_timer1 -= 1
    if boost_timer1 > 0:
        boost_timer1 -= 1
    if firerate_timer2 > 0:
        firerate_timer2 -= 1
    if boost_timer2 > 0:
        boost_timer2 -= 1

    if random.randint(1, 200) == 200:
        powerups.append(Powerup())

    ship1(x1,y1)
    ship2(x2,y2)

    for ob in obstacles:
        pygame.draw.rect(gameDisplay, (178,178,178), ob)

    for p in powerups:
        if p.pType == 1:
            gameDisplay.blit(p1, (p.xPos, p.yPos))
        elif p.pType == 2:
            gameDisplay.blit(p2, (p.xPos, p.yPos))
        else:
            gameDisplay.blit(p3, (p.xPos, p.yPos))

    if redWin:
        font = pygame.font.Font(None, 100)
        text = font.render("Red Wins!", True, (255,0,0))
        text_rect = text.get_rect(center=(400, 300))
        gameDisplay.blit(text, text_rect)

    if blueWin:
        font = pygame.font.Font(None, 100)
        text = font.render("Blue Wins!", True, (0,0,255))
        text_rect = text.get_rect(center=(400, 300))
        gameDisplay.blit(text, text_rect)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
########## end of while loop
while not quit_game:
    font = pygame.font.Font(None, 30)
    text = font.render("Press \"r\" to restart or \"Esc\" to quit", True, (0,0,0))
    text_rect = text.get_rect(center=(400, 350))
    gameDisplay.blit(text, text_rect)
    pygame.display.flip()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_r]):
            os.execl(sys.executable, sys.executable, *sys.argv)
        if(keys[pygame.K_ESCAPE]):
            pygame.quit()
            quit()

pygame.quit()
quit()
