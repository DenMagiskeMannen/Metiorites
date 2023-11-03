# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:07:33 2023

@author: teodo
"""

import pygame
import random
import time

screenie=(1280, 720)
YN=[True,False]

class meteorite():
    meteorites=[]
    score=[]
    
    def __init__(self):
        self.radius=random.randint(20,50)
        self.speed_x=random.randint(1,150)
        negative_x=random.choice(YN)
        self.speed_y=random.randint(1,150)
        negative_y=random.choice(YN)
        if self.speed_x > self.speed_y:
            if negative_x:
                self.x_pos=screenie[0]+self.radius
                self.y_pos=random.randint(0+self.radius,screenie[1]-self.radius)
            else:
                self.x_pos=0-self.radius
                self.y_pos=random.randint(0+self.radius,screenie[1]-self.radius)
        else:
            if negative_y:
                self.y_pos=screenie[1]+self.radius
                self.x_pos=random.randint(0+self.radius,screenie[0]-self.radius)
            else:
                self.y_pos=0-self.radius
                self.x_pos=random.randint(0+self.radius,screenie[0]-self.radius)
        if negative_x==True:
            self.speed_x=self.speed_x*(-1)
        if negative_y==True:
            self.speed_y=self.speed_y*(-1)
        self.pos=pygame.Vector2(self.x_pos,self.y_pos)
        self.point=self.radius*10
        if self.point<0:
            self.point = self.point*(-1)
        self.speed=[self.speed_x,self.speed_y]
        #self.speed=[0,0]
        self.color=[10,10,10]
        self.index=len(self.meteorites)
        self.meteorites.append(self)
        self.In_contanct_with_player=False
        self.x_hitbox=[self.pos.x-self.radius,self.pos.x+self.radius]
        self.y_hitbox=[self.pos.y-self.radius,self.pos.y+self.radius]
        
    
    def updata_data(self):
        self.x_hitbox=[self.pos.x-self.radius,self.pos.x+self.radius]
        self.y_hitbox=[self.pos.y-self.radius,self.pos.y+self.radius]
        if self.x_hitbox[1]<0:
            self.self_destruct()
        elif self.x_hitbox[0]>screenie[0]:
            self.self_destruct()
        if self.y_hitbox[1]<0:
            self.self_destruct()
        elif self.y_hitbox[0]>screenie[1]:
            self.self_destruct()
            
    def hit(self):
        index=0
        for each in self.meteorites:
            if each == self:
                self.meteorites.pop(index)
            else:
                index+=1
        self.score.append(self.point)
        summ=0
        for each in self.score:
            summ+=each
        #print(summ)
        del(self)
        
    def distance_player(self,player_pos,player_radius):
        #We doing triangles, not
        distance_x=self.pos.x-player_pos.x
        distance_y=self.pos.y-player_pos.y
        covered=self.radius+player_radius
        X=False
        Y=False
        if covered*(-1)<distance_x<covered or covered*(-1)>distance_x>covered:
            X=True
        if covered*(-1)<distance_y<covered or covered*(-1)>distance_y>covered:
            Y=True
        if X and Y:
            self.hit()
    
    def self_destruct(self):
        index=0
        for each in self.meteorites:
            if each == self:
                self.meteorites.pop(index)
            else:
                index+=1
        #self.meteorites.pop(index)
        del(self)
    



# pygame setup
pygame.init()
screen = pygame.display.set_mode(screenie)
clock = pygame.time.Clock()
running = True
dt = 0
latest_met=0
how_many_mets=10
points=sum(meteorite.score)



player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
print(screen.get_width())
print(screen.get_height())
x_places=[0,screen.get_width()]
y_places=[0,screen.get_height()]

#If circle
radius=20
player_x_hitbox=[None,None]
player_y_hitbox=[None,None]

player_speed=[0,0]

while running:
    current_time=time.time()
    points=sum(meteorite.score)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{points}", True, (255, 255, 255))
    mets= font.render(f"{how_many_mets}", True, (255, 255, 255))
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    while len(meteorite.meteorites)<how_many_mets:
        new_met=meteorite()
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", (player_pos.x,player_pos.y), radius)
    
    pygame.draw.circle(screen, "red", (player_pos.x+screenie[0],player_pos.y), radius)
    pygame.draw.circle(screen, "red", (player_pos.x-screenie[0],player_pos.y), radius)
    pygame.draw.circle(screen, "red", (player_pos.x,player_pos.y+screenie[1]), radius)
    pygame.draw.circle(screen, "red", (player_pos.x,player_pos.y-screenie[1]), radius)
    
    
    for meteoritt in meteorite.meteorites:
        pygame.draw.circle(screen, meteoritt.color,meteoritt.pos , meteoritt.radius)
    
    screen.blit(text,(screenie[0]-screenie[0]/8,screenie[1]-screenie[1]/8))
    screen.blit(mets,(0+screenie[0]/12,0+screenie[1]/12))
    
    player_x_hitbox[0]=(player_pos.x)-radius
    player_x_hitbox[1]=(player_pos.x)+radius
    player_y_hitbox[0]=(player_pos.y)-radius
    player_y_hitbox[1]=(player_pos.y)+radius
    
    
    #Hitbox checks
    if player_x_hitbox[0]<x_places[0]:
        player_pos.x=player_pos.x+screenie[0]
    elif player_x_hitbox[1]>x_places[1]:
        player_pos.x=player_pos.x-screenie[0]
        #player_speed[0]=player_speed[0]*(-1)
    if player_y_hitbox[0]<y_places[0]:
        player_pos.y=player_pos.y+screenie[1]
    elif player_y_hitbox[1]>y_places[1]:
        player_pos.y=player_pos.y-screenie[1]
        #player_speed[1]=player_speed[1]*(-1)
        
    for meteoritt in meteorite.meteorites:
        meteoritt.distance_player(player_pos,radius)
    
    
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_speed[1] -= 20
    if keys[pygame.K_s]:
        player_speed[1] += 20
    if keys[pygame.K_a]:
        player_speed[0] -= 20
    if keys[pygame.K_d]:
        player_speed[0] += 20
    
    if keys[pygame.K_m]:
        player_pos= pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    if keys[pygame.K_SPACE]:
        player_speed[0]=player_speed[0]*0.9
        player_speed[1]=player_speed[1]*0.9
    if keys[pygame.K_PLUS]:
        if current_time-latest_met>=0.2:
            #Newest_met=meteorite()
            how_many_mets+=1
            print(how_many_mets)
            latest_met=time.time()
    if keys[pygame.K_MINUS]:
        if len(meteorite.meteorites)>0:
            if current_time-latest_met>=0.2:
                how_many_mets-=1
                doomed=random.choice(meteorite.meteorites)
                doomed.self_destruct()
                latest_met=time.time()
            
            
    
    
    
        
    
    player_pos.x += player_speed[0]*dt
    player_pos.y += player_speed[1]*dt
    for meteoritt in meteorite.meteorites:
        meteoritt.pos.x += meteoritt.speed[0]*dt
        meteoritt.pos.y += meteoritt.speed[1]*dt
        meteoritt.updata_data()
    
    
    #print(player_pos)
    #print(player_x_hitbox,player_y_hitbox)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()