#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import json
from pygame.draw import *
from random import randint

pygame.init()

FPS = 15
screen = pygame.display.set_mode((900, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

BORDER_EDGES = [900, 600]
N = 10
L = 0
end = 0
count = 0
Name = ""
pool = []



f = pygame.font.Font(None,36) 
end_text = f.render('Выход', True, (178, 103, 49))
name_text = f.render('Напишите ваше имя', True, CYAN)

class Ball:
    def __init__(self, coord, velocity, color, r, randmove, direction):
        """
        Задает все начальные значения для шарика
        coord - координаты [x, y]
        velocity - скорость [v_x, v_y]
        color - цвет шарика
        r - радиус шарика
        randmove - дополнение к движению (ускорение,
        направленное к какой либо из стенок
        (зависящее от начальных скоростей шарика))
        """
        self.coord = coord
        self.color = color
        self.velocity = velocity
        self.r = r
        self.flag = True 
        self.randmove = randmove
        self.vx_dir, self.vy_dir = direction
        if self.randmove == 1:
            if self.vx_dir == 1 and self.vy_dir == 1:
                self.acc_x = -1
                self.acc_y = 0
            if self.vx_dir == 1 and self.vy_dir == -1:
                self.acc_x = 0
                self.acc_y = 1
            if self.vx_dir == -1 and self.vy_dir == 1:
                self.acc_x = 0
                self.acc_y = -1
            if self.vx_dir == -1 and self.vy_dir == -1:
                self.acc_x = 1
                self.acc_y = 0
        else:
            self.acc_x = 0
            self.acc_y = 0


    def move(self):
            """
            функция движения шарика, которая в том числе и рисует его
            два типа движения, которые отличаются наличием randmove:
            -прямолинейное движение, просто по начальным V_x и V_y
            -движение под силой гравитации (наличие притяжения у одной из стенок)
            """
            circle(screen, self.color, self.coord, self.r)
            v0_x, v0_y = self.velocity
            self.coord[0] += v0_x
            self.coord[1] += v0_y
            
    #         self.velocity[0] += self.acc_x
    #         self.velocity[1] += self.acc_y


    def collisions(self):
            """
            функция сдерживающая шарики в клетке
            """
            if self.coord[0] <= self.r or self.coord[0] >= BORDER_EDGES[0]- self.r:
                self.velocity[0] *= (-1)
    #             if self.randmove == 1:
    #                 self.velocity[0] = (-1)**int(self.velocity[0] > 0) * randint(6, 10)
    #                 self.velocity[1] = (-1)**randint(0, 1) * randint(6, 10)
            if self.coord[1] <= self.r or self.coord[1] >= BORDER_EDGES[1]- self.r:
                self.velocity[1] *= -1
    #             if self.randmove == 1:
    #                 self.velocity[0] = (-1)**randint(0, 1) * randint(6, 10)
    #                 self.velocity[1] = (-1)**int(self.velocity[0] > 0) * randint(6, 10)
            if self.coord[0] <= self.r:
                self.coord[0] = self.r+5
            if self.coord[1] <= self.r:
                self.coord[1] = self.r+5
            if self.coord[0] >= (BORDER_EDGES[0] - self.r):
                self.coord[0] = (BORDER_EDGES[0] - self.r-5)
            if self.coord[1] >= (BORDER_EDGES[1] - self.r):
                self.coord[1] = (BORDER_EDGES[1] - self.r-5)
    
            

    def event(self):
            """
            функция, срабатывающая при клике мышки, проверяет попадание по шарику
            при попадании помечает шарик, впоследствии он уничтожается
            """
            if (X_m - self.coord[0])**2 + (Y_m - self.coord[1])**2 <= (self.r)**2:
                self.flag = False

def new_usual_ball():
        x = randint(100,750)
        y = randint(100, 550)
        vx_dir = randint(0, 1)
        vx_dir = vx_dir*2 - 1
        vy_dir = randint(0, 1)
        vy_dir = vy_dir*2 - 1
        V_x = randint(6, 10)*vx_dir
        V_y = randint(6, 10)*vy_dir
        r = randint(25, 40)
        randmove = 0
        color = COLORS[randint(1, 5)]
        pool.append(Ball([x, y], [V_x, V_y], color, r, randmove, [vx_dir, vy_dir]))

def new_unusual_ball():
        x = randint(50,750)
        y = randint(50, 550)
        vx_dir = randint(0, 2)
        vx_dir = vx_dir*2 - 1
        vy_dir = randint(0, 1)
        vy_dir = vy_dir*2 - 1
        V_x = randint(6, 10)*vx_dir
        V_y = randint(6, 10)*vy_dir
        r = randint(10, 20)
        randmove = 1
        color = 'RED'
        pool.append(Ball([x, y], [V_x, V_y], color, r, randmove, [vx_dir, vy_dir]))

for _ in range (N):
    new_usual_ball()
    new_unusual_ball()    

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            X_m, Y_m = event.pos
            for ball in pool:
                ball.event()
            if end >= 15:
                if 450 < X_m < 600 and 300 < Y_m < 350:
                    pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if end >= 10 and end < 15 and event.key != 8 and event.key != 13:
                Name = Name + event.unicode

            if end >= 10 and end < 15 and event.key == 8:
                Name = Name[:-1]

            if end >= 10 and end < 15 and event.key == 13:
                with open('Results.JSON', 'r') as h:
                    loaded = json.load(h)
                loaded["results"].append({"name": Name, "points": count})
                with open('Results.JSON', 'w') as h:
                    json.dump(loaded, h)
                h.close()
                end += 10

                
    for ball in pool:
        ball.move()
        ball.collisions()
        if ball.flag == False:
            if ball.color != 'RED':
                count += 5
            if ball.color == 'RED':
                count += 15
            if ball.color == 'RED' and ball.r <= 15:
                count += 10
            pool.remove(ball)
            end += 1
            new_usual_ball()

    text = f.render('Счет: ' + str(count), True, (255, 255, 255))
    if end < 10:
        screen.blit(text, (10, 10))

    if end >= 10 and end <= 15:
        for ball in pool:
            pool.remove(ball)
        screen.blit(text, (450, 100))
        screen.blit(name_text, (400, 200))
        name_name_text = f.render(Name, True, CYAN)
        screen.blit(name_name_text, (450, 300))
        
    if end >= 15:
        with open('Results.JSON', 'r') as h:
            loaded = json.load(h)
        h.close()
        res = loaded["results"]
        table = []
        names = []
        for i in res:
            table.append(i["points"])
            names.append(i["name"])
        A = len(table)
        for i in range(A-1):
            for j in range(A-i-1):
                if table[j] > table[j+1]:
                    table[j], table[j+1] = table[j+1], table[j]
                    names[j], names[j+1] = names[j+1], names[j]

        z = len(table) - 1
        while z >= 0:
            for i in res:
                i["points"] = table[z]
                i["name"] = names[z]
                z += -1

        leaderboard = f.render('Leaderboard', True, RED)
        screen.blit(text, (450, 100))
        screen.blit(name_name_text, (400, 200))
        screen.blit(end_text, (450, 300))
        screen.blit(leaderboard, (350, 325))

        c = 0
        for i in res:
            man = f.render(i["name"] + " " + str(i["points"]), True, GREEN)
            screen.blit(man, (350, 350 + c*25))
            c += 1

    pygame.display.update()
    screen.fill(BLACK)





pygame.quit()


# In[ ]:




