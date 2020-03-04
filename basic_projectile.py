import pygame
from pygame import *
import random
import time
import math
from decimal import Decimal, ROUND_HALF_UP

vel = int(input("Enter Initial Velocity: "))
angle = float(input("Enter a Angle (0-90): "))
y = int(input("Enter Height: "))

pygame.init()

# initializing a screen
display = pygame.display.set_mode((1000, 600))
display.fill((59, 88, 107))

# title
pygame.display.set_caption("Projectile Motion Simulator")

# pygame clock
clock = pygame.time.Clock()


# draw ground
def ground():
    pygame.draw.line(display, (0, 255, 0), (0, 540), (1000, 540), 1)


# draw ball
def ball(x, y, color):
    pygame.draw.circle(display, color, (x, y), 20)


# calculate x-cord from time, initial x, given initial velocity and angle
def getX(x0, time, vel, angle):
    velx = vel * math.cos((angle / 360) * (2 * math.pi))
    return int(Decimal(round(x0 + velx * time, 1)).to_integral_value(rounding=ROUND_HALF_UP))


# calculate total time of travel given initial velocity and angle
def getTotTime(vel, angle, height):
    vely = vel * math.sin((angle / 360) * (2 * math.pi))
    d = (vely ** 2) - (4 * -4.9 * (height))
    tot_time = (-vely - math.sqrt(d)) / (2 * -4.9)
    return int(Decimal(round(tot_time, 1)).to_integral_value(rounding=ROUND_HALF_UP))


# calculate y-cord from time, initial y, given initial velocity, and angle
def getY(y0, time, vel, angle):
    vely = vel * math.sin((angle / 360) * (2 * math.pi))
    return int(Decimal(round(y0 - vely * time + 4.9 * math.pow(time, 2), 1)).to_integral_value(rounding=ROUND_HALF_UP))


# draw trajectory given the initial velocity and angle
def draw_trajectory(initX, initY, vel, angle):
    tot_time = int(Decimal(round(getTotTime(vel, angle, initY), 1)).to_integral_value(rounding=ROUND_HALF_UP))

    xcord = 0
    ycord = 0
    for i in range(0, 10 * tot_time + 1):
        xcord = getX(initX, i / 10, vel, angle)
        ycord = getY(520 - initY, i / 10, vel, angle)

        pygame.draw.line(display, (255, 0, 0), (xcord, ycord), (xcord + 1, ycord + 1), 5)

    ball(xcord, ycord, (255, 255, 255))


# draw x-directional and y-directional vectors
def drawVectors(vel, angle, x, y, y_change):
    velx = vel * math.cos((angle / 360) * (2 * math.pi))
    pygame.draw.line(display, (242, 218, 0), (x, y), (x + velx * 2, y), 3)

    vectory = pygame.draw.line(display, (242, 0, 173), (x, y), (x, y + (y_change * 15)), 3)


# displaying text
def displayText(initVel, velx, vely, distTraveled, tot_time):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text_init_vel = font.render('Initial Vel. : ' + str(initVel) + " m/s", True, (255, 255, 255), (59, 88, 107))
    text_rect = text_init_vel.get_rect()
    text_rect.center = (700, 100)
    display.blit(text_init_vel, text_rect)

    text_velx = font.render('Vel. X-Dir : ' + str(round(velx, 2)) + " m/s", True, (255, 255, 255), (59, 88, 107))
    text_rect = text_velx.get_rect()
    text_rect.center = (700, 150)
    display.blit(text_velx, text_rect)

    text_vely = font.render('Vel. Y-Dir : ' + str(round(vely, 2)) + " m/s", True, (255, 255, 255), (59, 88, 107))
    text_rect = text_vely.get_rect()
    text_rect.center = (700, 200)
    display.blit(text_vely, text_rect)

    text_dist = font.render('Distance Traveled : ' + str(distTraveled) + " m", True, (255, 255, 255), (59, 88, 107))
    text_rect = text_dist.get_rect()
    text_rect.center = (700, 250)
    display.blit(text_dist, text_rect)

    text_tot_time = font.render('Total Time : ' + str(tot_time) + " s", True, (255, 255, 255), (59, 88, 107))
    text_rect = text_tot_time.get_rect()
    text_rect.center = (700, 300)
    display.blit(text_tot_time, text_rect)


# draw platform
def draw_platform(xcord, height):
    pygame.draw.rect(display, (0, 222, 242), [xcord - 40, 520 - height + 20, xcord, height], 0)


# initial ball cords
x = 40

X_COPY = x
Y_COPY = y

# run loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(0, 10 * getTotTime(vel, angle, Y_COPY) + 1):
        xcord = getX(X_COPY, i / 10, vel, angle)
        ycord = getY(520 - Y_COPY, i / 10, vel, angle)
        x_change = xcord - x
        y_change = ycord - y

        x += x_change
        y += y_change

        display.fill((59, 88, 107))
        velx = vel * math.cos((angle / 360) * (2 * math.pi))
        vely = vel * math.sin((angle / 360) * (2 * math.pi))
        final_vely = vely - 9.8 * (i / 10)
        displayText(vel, velx, final_vely, xcord - 40, getTotTime(vel, angle, Y_COPY))
        ball(x, y, (100, 100, 100))
        draw_trajectory(X_COPY, Y_COPY, vel, angle)
        ball(X_COPY, 520 - Y_COPY, (255, 255, 255))
        ground()
        draw_platform(X_COPY, Y_COPY)
        drawVectors(vel, angle, x, y, y_change)

        pygame.display.update()
        clock.tick(20)
