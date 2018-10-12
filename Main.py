# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 13:05:30 2018

@author: runni
"""
import pygame
from pygame.locals import *
import os
import sys
import math
import random 


pygame.init()

R = (255,0,0)
G = (0,255,0)
B = (0,0,255)

W, H = 1200, 500
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("SpaceGame")

bg = pygame.image.load(os.path.join("S", "bg.png"))
bgX = 0
bgX2 = bg.get_width()
clock = pygame.time.Clock()

lazers = []
ammo = 1
score = 0 
pause = 0 
"""
CLASSES
"""

class player(object):
    still = pygame.image.load(os.path.join("S", "OG.png" ))
    up = pygame.image.load(os.path.join("S", "OGU.png" ))
    down = pygame.image.load(os.path.join("S", "OGD.png" ))
    
    def __init__(self, x,y,w,h,v):
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h
        self.v = v 
        self.state = 0
        self.health = 100
        self.hitbox = (self.x, self.y, self.w+256, self.h+20)
        self.dead = False
        
    def draw(self, win):
        
        if self.state == 0: 
            win.blit(self.still, (self.x,self.y))
            self.hitbox = (self.x, self.y, self.w+256, self.h+20)
        
        elif self.state == 1 > 0:
            self.y -= self.v 
            win.blit(self.up, (self.x,self.y))
            self.hitbox = (self.x, self.y, self.w+256, self.h+20)
        
        elif self.state == -1 :
            self.y += self.v
            win.blit(self.down, (self.x,self.y))
            self.hitbox = (self.x, self.y, self.w+256, self.h+20)
            
        pygame.draw.rect(win, R, self.hitbox, 2)
        
        
        
    def collide(self,rect):
        pass
    
class projectile(object):
    
    def __init__(self,x,y,r,v,color):
        self.x = x 
        self.y = y 
        self.r = r 
        self.v = v 
        self.color = color
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 100, self.r))
#        pygame.draw.rect(win, R, self.hitbox, 2)
        
class alien(object):
    still = pygame.image.load(os.path.join("S", "A1.png" ))
    
    def __init__(self, x,y,w,h,v):
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h
        self.v = v 
        self.hp = 100
        self.hitbox = (self.x, self.y, self.w+30, self.h)
        self.heading = [W+50, random.randint(0, H-self.h), random.randint(3,5), random.randint(-1,1)]

    def remove(self):
        if self.x < -1*self.w  -50:
                return True
        
    def draw(self,win):
        self.x -= self.heading[2]
        self.y += self.heading[3]
        self.hitbox = (self.x, self.y, self.w+30, self.h)
        pygame.draw.rect(win, R, self.hitbox, 2)
        win.blit(self.still, (self.x,self.y))
            
    
class alien2(alien):
    still = pygame.image.load(os.path.join("S", "A2.png" ))
    
    def __init__(self, x,y,w,h,v):
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h
        self.v = v 
        self.health = 10
        self.hitbox = (self.x+30, self.y, self.w+30, self.h+60)
        self.heading = [W+50, random.randint(0, H-self.h), random.randint(2,4), random.randint(-1,1)]
        
    def draw(self,win):
        self.x -= self.heading[2]
        self.y += self.heading[3]
        self.hitbox = (self.x+10, self.y, self.w+30, self.h+60)
#        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
#        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((5)*(10 - self.health)), 10))
        pygame.draw.rect(win, R, self.hitbox, 2)
        win.blit(self.still, (self.x,self.y))
        
        
            

"""
SETUP
"""

def shoot(S):
    if S > 0:
        lazers.append(projectile((int(P1.x+P1.w/2)) +70, int(P1.y+P1.h/2) +15, 3, 40, B ))
        S -= 1
       
def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    
    P1.draw(win)
    
    """text"""
    
    pygame.font.init()
    scoreFont = pygame.font.SysFont("comicsans", 30, True,True)
    scoreText = scoreFont.render("Score: " + str(score), 1, R)
    win.blit(scoreText, (800, 30))
    
    """ text """
    
    
    for enemy in enemies:
        if enemy.x < -120:
            enemies.pop(enemies.index(enemy))
        else:
            enemy.draw(win)
    
    for enemy in enemies2:
        if enemy.x < -120:
            enemies2.pop(enemies2.index(enemy))
        else:
            enemy.draw(win)
            
    
    for lazor in lazers:
        if lazor.x > W + 5000:
            lazers.pop(lazers.index(lazor))
        else:
            lazor.x += lazor.v
            lazor.draw(win)
        
#    for objectt in objects:
#        objectt.draw(win)
        
    pygame.display.update()



def drawBG(s):
    global bgX, bgX2
    bgX -= s
    bgX2 -= s
    if bgX < bg.get_width()*-1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width()*-1:
        bgX2 = bg.get_width()

def controlKeys():
    keys = pygame.key.get_pressed()
    P1.state = 0 
    
    if keys[pygame.K_UP] and P1.y > 0:
        if P1.state == -1:
            P1.state = 0
        elif P1.state == 0:
            P1.state = 1 
            
    if keys[pygame.K_DOWN] and P1.y < H - P1.h:
        if P1.state == 1:
            P1.state = 0
        elif P1.state == 0:
            P1.state = -1
    
    if keys[pygame.K_SPACE]:
        shoot(ammo)

def lazerHit():
    global score
    for lazor in lazers: 
        for enemy in enemies:
            if lazor.y - lazor.r < enemy.hitbox[1] + enemy.hitbox[3] and lazor.y + lazor.r > enemy.hitbox[1]:
                if lazor.x + lazor.r > enemy.hitbox[0] and lazor.x - lazor.r < enemy.hitbox[0] + enemy.hitbox[2]:
                    lazers.pop(lazers.index(lazor))
                    enemies.pop(enemies.index(enemy))
                    score += 1 
                    
        for enemy in enemies2:
            if lazor.y - lazor.r < enemy.hitbox[1] + enemy.hitbox[3] and lazor.y + lazor.r > enemy.hitbox[1]:
                if lazor.x + lazor.r > enemy.hitbox[0] and lazor.x - lazor.r < enemy.hitbox[0] + enemy.hitbox[2]:
                    if enemy.health > 0:
#                        lazers.pop(lazers.index(lazor))
                        enemy.health -= 10
                    else:
#                        lazers.pop(lazers.index(lazor))
                        enemies2.pop(enemies2.index(enemy))
                        score += 1 
#                    lazers.pop(lazers.index(lazor))

def playerHit():
    
    for enemy in enemies2:
        if P1.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and P1.hitbox[1] + P1.hitbox[3] > enemy.hitbox[1]:
            if P1.hitbox[0] + P1.hitbox[2] > enemy.hitbox[0] and P1.hitbox[0]  < enemy.hitbox[0] + enemy.hitbox[2]:
                print("oof")
                P1.dead = True
                
    for enemy in enemies:
        if P1.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and P1.hitbox[1] + P1.hitbox[3] > enemy.hitbox[1]:
            if P1.hitbox[0] + P1.hitbox[2] > enemy.hitbox[0] and P1.hitbox[0]  < enemy.hitbox[0] + enemy.hitbox[2]:
                print("oof")
                P1.dead = True

def endScreen():
    global pause, score, enemies, lazers
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
                quit()
        
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont("comicsans", 80)
        currentScore = largeFont.render("Score: " + str(score), 1, R)
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 320))
        
        if score < 10:
            bad = largeFont.render("You're bad niBBa ", 1, R)
            win.blit(bad, (W/2 - currentScore.get_width()/2, 200))
        pygame.display.update()
        
        
        
    
"""
Init objects variables
"""

P1 = player(60, H//2, 128, 64, 5)
pygame.time.set_timer(USEREVENT+2, random.randrange(2000,3500))
pygame.time.set_timer(USEREVENT+1, 500)

#A1 = alien(1000, H//2, 128, 64,5)
speed = 30

pause = 0
fallSpeed = 0 
objects = []
enemies = []
enemies2 = []
run = True


"""
MAINLOOP
"""

while run: 
    
    drawBG(2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False 
            pygame.quit()
            quit()
    
    if event.type == USEREVENT+1:
        speed += 1
    if event.type == USEREVENT+2:
        #draw ojects here.
        r = random.randrange(0,5)
        if r == 0:
            s = random.randrange(-200,200)
            enemies.append(alien(1200, H//2 + s, 128, 64,2))
            enemies2.append(alien2(1200, H//2 + s, 128, 64,2))
        
    lazerHit()
    playerHit()
    
    controlKeys()
    
    playerHit()
    
    if P1.dead:
        endScreen()
    
    clock.tick(speed)
    redrawWindow()

    
    
    
    
    

            
            
        
        
        
    