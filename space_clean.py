import sys, pygame
from pygame.constants import *
import time, serial
import random

ser=serial.Serial(port='COM5', baudrate=115200)
#/dev/ttyACM0
xVel=0
button=1
val=""
def joy():
    global xVel, button, val
    data = ser.read()
    if (data==b''):
        pass
    elif (data==b'\n' or data==b'\r'):

        if val != "":
            num = int(val)
            if 0 <= num <= 1:
                button = num
            else:
                xVel = (num/512)-1
            val = ""
    else:
        val += str(int(data, 16))

def starto():
    pygame.init()
    dis = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Space shooter')
    score_f = pygame.font.SysFont("bahnschrift", 25)
    back=pygame.transform.scale(pygame.image.load('background1.jpg'),(1200, 800))
    player=pygame.transform.scale(pygame.image.load('p1.png'),(80,60))
    enemy=pygame.transform.scale(pygame.image.load('enemy2.png'),(90,70))
    explosion=pygame.image.load('explosion.png')
    shot=pygame.transform.scale(pygame.image.load('bullet.png'),(135,105))
    go=pygame.transform.scale(pygame.image.load('game_over.png'),(600,400))
    disparox=-1
    disparoy=-1
    playerpos=560
    naves=[(300, -70), (1000, -70)]
    explotado = []
    keep = True
    intro=pygame.transform.scale(pygame.image.load('intro.png'),(1200,800))
    while True:
        dis.blit(intro,(0,0))
        joy()
        if button == 0:
            break
        pygame.display.update()

    while keep:
        pygame.display.update()
        joy()
        dis.blit(back,(0,0))
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
        playerpos += xVel * 12
        for i in range(100):
            pygame.draw.line(dis, (43, 58, 103), (i*12,650), ((12*i)+8,650), 3)
        if(button == 0):
            disparox=playerpos+12.5
            disparoy=700
        if (disparox!=-1):
            dis.blit(shot,(disparox,disparoy))
            disparoy-=8
        if (disparoy <= 0):
            disparoy=-1
            disparox=-1
        dis.blit(player,(playerpos,700))
        for nave in range(len(naves)):
            alien = naves[nave]
            pos_x, pos_y = alien
            if pos_y <= disparoy <= pos_y+70 and pos_x-35 <= disparox <= pos_x+90:
                explotado.append((alien, 0))
                naves.pop(nave)
                disparox = -1
                naves.append((random.randint(50, 1050), -70))
                if random.randint(0,3) == 3:
                    naves.append((random.randint(50, 1050), -170))
                break
            else:
                naves[nave] = (pos_x, pos_y+1)
                dis.blit(enemy, (pos_x, pos_y))
                if(pos_y+1 >= 615):
                    while keep:
                        joy()
                        if button == 0:
                            keep = False
                        dis.fill((0,0,0))
                        dis.blit(go, (300, 200))
                        pygame.display.update()
        explotados = len(explotado)
        dis.blit(score_f.render("score: "+str(explotados), True, (255,255,255)), [1050, 25])
        for alien in range(explotados):
            alienExplotado = explotado[alien]
            pos, frame = alienExplotado
            if frame < 40:
                frame += 1
                explotado[alien] = (pos, frame)
                explotacion = pygame.transform.scale(explosion,(3*frame, 2*frame))
                pos_x, pos_y = pos
                pos_x += 60 - 1.5*frame
                pos_y += 40 - 1*frame
                dis.blit(explotacion, (pos_x, pos_y))

if __name__ == "__main__":
    while True:
        starto()
