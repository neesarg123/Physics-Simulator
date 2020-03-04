import pygame
from pygame import *
from decimal import Decimal, ROUND_HALF_UP

# global vars
fps = 10
g = -1
m1 = -1
m2 = -1
while g < 0:
    g = Decimal(input("Enter a positive value for gravity: "))
while m1 < 0:
    m1 = int(input("Enter a positive value for mass 1 (should be lower than mass 2: "))
while m2 < 0 and m2 < m1:
        m2 = int(input("Enter a positive value for mass 2 (should be higher than mass 1: "))

# initializing pygame
pygame.init()

# initializing a screen
display = pygame.display.set_mode((1000, 600))
display.fill((59, 88, 107))

# title
pygame.display.set_caption("Ideal Pulley System Simulator")

# pygame clock
clock = pygame.time.Clock()


# draw ground
def ground():
    pygame.draw.line(display, (0, 180, 0), (0, 540), (1000, 540), 1)


# draw pulley
def pulley():
    # base
    pygame.draw.rect(display, (117, 116, 113), [480, 530, 40, 10], 0)
    # rod
    pygame.draw.rect(display, (117, 116, 113), [495, 530, 10, -375], 0)
    # wheel
    pygame.draw.circle(display, (99, 16, 7), (500, 150), 60, 0)
    pygame.draw.circle(display, (214, 43, 24), (500, 150), 5, 0)
    pygame.draw.circle(display, (214, 43, 24), (500, 150), 60, 5)
    # arc rope
    pygame.draw.arc(display, (0, 0, 0), [435, 85, 130, 125], 2 * 3.14, 3 * 3.14, 5)


# draw rope and mass 1
def rope_and_mass_1(rp_length):
    # rope
    pygame.draw.rect(display, (0, 0, 0), [435, 145, 5, 100 + rp_length], 0)
    # mass block
    pygame.draw.rect(display, (87, 65, 7), [400, 245 + rp_length, 75, 75], 0)


# draw rope and mass 2
def rope_and_mass_2(rp_length):
    # rope
    pygame.draw.rect(display, (0, 0, 0), [560, 145, 5, 100 - rp_length], 0)
    # mass block
    pygame.draw.rect(display, (87, 65, 7), [525, 245 - rp_length, 75, 75], 0)


# drawing weight vectors
def weight_vector_1(mass1, rp_length):
    weight = mass1 * g
    pygame.draw.rect(display, (194, 0, 178), [435, 277.5 + rp_length, 5, weight / (2 * g)], 0)


def weight_vector_2(mass2, rp_length):
    weight = mass2 * g
    pygame.draw.rect(display, (194, 0, 178), [560, 277.5 - rp_length, 5, weight / (2 * g)], 0)


# calculating magnitude of acceleration
def acceleration(mass1, mass2):
    f_net = g * (mass2 - mass1)
    total_mass = mass1 + mass2
    return f_net / total_mass


# drawing tension vectors
def tension_vector_1(mass1, accel, rp_length):
    tension_force = mass1 * (g + accel)
    pygame.draw.rect(display, (227, 213, 20), [435, 277.5 + rp_length, 5, -(tension_force / (2 * g))], 0)


def tension_vector_2(mass2, accel, rp_length):
    tension_force = mass2 * (g - accel)
    pygame.draw.rect(display, (227, 213, 20), [560, 277.5 - rp_length, 5, -(tension_force / (2 * g))], 0)


def display_text(mass1, mass2, accel):
    font = pygame.font.Font('freesansbold.ttf', 20)
    mass1_text = font.render("Mass Block 1: " + str(mass1) + " kg", True, (255, 255, 255), (59, 88, 107))
    text_rect = mass1_text.get_rect()
    text_rect.center = (200, 100)
    display.blit(mass1_text, text_rect)

    mass2_text = font.render("Mass Block 2: " + str(mass2) + " kg", True, (255, 255, 255), (59, 88, 107))
    text_rect = mass2_text.get_rect()
    text_rect.center = (200, 150)
    display.blit(mass2_text, text_rect)

    accel_text = font.render("Mag. of Acceleration: " + str(accel) + " m/s^2", True, (255, 255, 255), (59, 88, 107))
    text_rect = accel_text.get_rect()
    text_rect.center = (200, 200)
    display.blit(accel_text, text_rect)


# acceleration to pixels
a = Decimal(round(acceleration(m1, m2), 5)).to_integral_value()
# height of mass2 and mass1 from ground
height_m2 = 300
rp_length = -(540 - 145 - 75 - height_m2 - 100)
height_m1 = 540 - (245 + rp_length + 75)
print(height_m1)
change_in_rp_length = 0
print(acceleration(m1, m2), a)

pygame.mouse.set_visible(True)

# mainloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    change_in_rp_length = int(a)
    rp_length -= change_in_rp_length
    height_m2 -= change_in_rp_length
    height_m1 += change_in_rp_length

    display.fill((59, 88, 107))
    ground()
    pulley()
    rope_and_mass_1(rp_length)
    rope_and_mass_2(rp_length)
    weight_vector_1(m1, rp_length)
    weight_vector_2(m2, rp_length)
    tension_vector_1(m1, acceleration(m1, m2), rp_length)
    tension_vector_2(m2, acceleration(m1, m2), rp_length)
    display_text(m1, m2, a)

    print(pygame.mouse.get_pos())

    # stop and restart when block gets to the top of pulley
    if height_m2 <= 0:
        running = False

    if height_m1 >= 320:
        height_m2 = 300
        rp_length = -(540 - 145 - 75 - height_m2 - 100)
        height_m1 = 540 - (245 + rp_length + 75)

    # fps
    pygame.display.update()
    clock.tick(fps)
