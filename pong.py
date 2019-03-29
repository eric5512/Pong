import pygame
import random
import math


class player:
    def __init__(self, x, y, w, h, vel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = vel
        self.d = 1
        self.m = False
        self.p = 0

    def move(self):
        self.y += self.vel * self.d
        self.m = True

    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.w, self.h))
        self.m = False


class ball:
    def __init__(self, x, y, w, h, velx, vely):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.velx = velx
        self.vely = vely
        self.vel = math.sqrt(velx*velx + vely*vely)

    def move(self):
        self.x += self.velx
        self.y += self.vely

    def hit(self, wall):
        a = random.randint(30,60)
        a = 0.01745 * a
        if wall == 1:
            self.vely = math.sin(a) * self.vel
            self.velx = math.cos(a) * self.vel * self.velx / abs(self.velx)
        elif wall == 2:
            self.velx = math.cos(a) * self.vel * (-1)
            self.vely = math.sin(a) * self.vel * self.vely / abs(self.vely)
        elif wall == 3:
            self.vely = math.sin(a) * self.vel * (-1)
            self.velx = math.cos(a) * self.vel * self.velx / abs(self.velx)
        elif wall == 4:
            self.velx = math.cos(a) * self.vel
            self.vely = math.sin(a) * self.vel * self.vely / abs(self.vely)

    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.w, self.h))
            



pygame.init()

sWidth = 1250
sHeight = 750

win = pygame.display.set_mode((sWidth,sHeight))
pygame.display.set_caption("Pong")

f1 = pygame.font.SysFont("comicsans", 60)

p1 = player(50, sHeight//2-90//2, 20, 90, 4)
p2 = player(sWidth-70, sHeight//2-90//2, 20, 90, 4)

run = True
quit = False

while not (p1.p > 4 or p2.p > 4) and not quit:
    run = True
    v = random.randint(-1,1)
    while v == 0:
        v = random.randint(-1,1)
    b = ball(sWidth//2-10,sHeight//2-10,20,20,4*v,4*v)
    while run and not quit:
        pygame.time.delay(10)
        pygame.draw.rect(win, (0,0,0), (0,0,sWidth,sHeight))
        pygame.draw.rect(win, (255,255,255), (sWidth//2-2,0,2,sHeight))
        win.blit(f1.render(str(p1.p),1,(255,255,255)),(sWidth//2-50, 5))
        win.blit(f1.render(str(p2.p),1,(255,255,255)),(sWidth//2+25, 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        if b.x < 0:
            run = False
            p2.p += 1
        if b.x + b.w > sWidth:
            run = False
            p1.p += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and p1.y + p1.h < sHeight:
            p1.d = 1
            p1.move()
        if keys[pygame.K_UP] and p1.y > 0:
            p1.d = -1
            p1.move()

        if p2.y > b.y:
            p2.d = -1
            p2.move()
        elif p2.y < b.y and not p2.y + p2.h > sHeight:
            p2.d = 1
            p2.move()

        b.move()

        if b.y < 0:
            b.hit(1)
        elif b.y + b.h > sHeight:
            b.hit(3)
        elif b.x < p1.x + p1.w and (b.y + b.h > p1.y and b.y < p1.y + p1.h):
            b.hit(4)
        elif b.x + b.w > p2.x and (b.y + b.h > p2.y and b.y < p2.y + p2.h):
            b.hit(2)

        p1.draw(win)
        p2.draw(win)
        b.draw(win)

        pygame.display.update()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if p1.p > p2.p:
        win.blit(f1.render("You win",16,(255,255,255)), (10,10))
    else:
        win.blit(f1.render("You lose",16,(255,255,255)), (10,10))
    pygame.display.update()




pygame.quit()