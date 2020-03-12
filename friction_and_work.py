import pygame
from pygame import *
from decimal import Decimal, ROUND_HALF_UP

# initializing pygame
pygame.init()
# colors
BACKGROUND = (59, 88, 107)
GREEN = (73, 186, 71)
GRAY = (124, 125, 124)
RED = (184, 24, 24)
BROWN = (120, 80, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (247, 95, 0)
PINK = (252, 3, 136)
PURPLE = (177, 3, 252)
YELLOW = (252, 206, 3)
# setting up a display
display = pygame.display.set_mode((1000, 600))
display.fill(BACKGROUND)
# title
title = pygame.display.set_caption("Neesarg's Loop-the-Loop Simulator")
# game clock
clock = pygame.time.Clock()
# fps
fps = 20
# initial location of user cart
x = 20
y = 0
# accelerations
a_x = 2  # acceleration in x-direction of cart
g = 9.8  # gravitational acceleration in y-direction of cart
# initializing velocity of cart
v = 0
# initializing mass of cart (in kg)
m = 25
# initializing coefficient of static friction (acting on the wheels of the cart by the track)
coef_of_sf = 0.18
# calculating force of friction by track
friction_force_by_track = m * g * coef_of_sf
# calculating deceleration
deceleration = int(Decimal(friction_force_by_track / m).to_integral_exact(rounding=ROUND_HALF_UP))
# initializing x and y changes in cart's position
x_change = 0
y_change = 0
# initializing status of keys pressed (right or left)
right_moved = False
left_moved = False
# initializing status of whether the cart passed the release mark
release_mark_crossed = False

do_once = 0
v_copy = v


class Cart:
    def __init__(self, x_loc, y_loc, color_of_cart):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.color_of_cart = color_of_cart
        # cart body
        pygame.draw.rect(display, color_of_cart, [x_loc, y_loc + 455, 80, 40], 0)
        # cart wheels
        pygame.draw.circle(display, BROWN, (x_loc, y_loc + 495), 15, 0)  # wheel 1
        pygame.draw.circle(display, BLACK, (x_loc, y_loc + 495), 15, 2)  # outline wheel 1
        pygame.draw.circle(display, BROWN, (x_loc + 80, y_loc + 495), 15, 0)  # wheel 2
        pygame.draw.circle(display, BLACK, (x_loc + 80, y_loc + 495), 15, 2)  # outline wheel 2

    def get_x_loc(self):
        return self.x_loc


# drawing ground and track
def ground_and_track():
    # ground
    pygame.draw.rect(display, GREEN, [0, 520, 1200, 120])
    # track
    pygame.draw.rect(display, GRAY, [0, 510, 1200, 10])
    pygame.draw.line(display, RED, (550, 510), (550, 520), 5)  # release mark


# displaying text
def display_text(velocity, work_done, v_post_release):
    font_of_text = pygame.font.Font('freesansbold.ttf', 20)
    vel_text = font_of_text.render("Velocity: " + str(velocity) + " m/s", True, WHITE, BACKGROUND)
    text_rect = vel_text.get_rect()
    text_rect.center = (100, 100)
    display.blit(vel_text, text_rect)

    if release_mark_crossed:
        vel_p_r_text = font_of_text.render("Velocity (post release): " + str(v_post_release) + " m/s", True, WHITE,
                                           BACKGROUND)
        text_rect = vel_p_r_text.get_rect()
        text_rect.center = (175, 150)
        display.blit(vel_p_r_text, text_rect)
        if v is 0:
            work_text = font_of_text.render("Work on Cart (post release): " + "K(f) - K(i) = " +
                                            str(work_done) + " J", True, WHITE, BACKGROUND)
            text_rect = work_text.get_rect()
            text_rect.center = (270, 200)
            display.blit(work_text, text_rect)


# display vectors
def display_vectors(x_of_cart, v, mass, coef_of_friction):
    weight_force = mass * g
    weight_force_in_pixel = 475 + ((weight_force * 3) / g)  # just preferable to get integer values
    pygame.draw.line(display, PINK, (x_of_cart + 40, 475), (x_of_cart + 40, weight_force_in_pixel), 5)  # weight vector

    normal_force = weight_force  # there is no vertical acceleration, therefore the normal force = weight vector
    normal_force_in_pixel = 475 - ((normal_force * 3) / g)
    pygame.draw.line(display, PURPLE, (x_of_cart + 40, 475), (x_of_cart + 40, normal_force_in_pixel), 5)

    friction_force = normal_force * coef_of_friction

    if v > 0:
        friction_force_in_pixel = (x_of_cart + 40) - ((friction_force * 3) / g)
        pygame.draw.line(display, YELLOW, (x_of_cart + 40, 475), (friction_force_in_pixel, 475), 5)


# calculating work done on cart after release point
def work(v_after_release):
    # using the approach that change in kinetic energy is equal to the work done on cart
    # final velocity is zero as the cart comes to rest, so, K final is 0
    return -1 * (0.5 * m * v_after_release ** 2)


# main class
if __name__ == '__main__':
    # running loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if x + x_change + 95 < 550:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                left_moved = False
                right_moved = True
                x_change += v
                v += a_x

            elif keys[pygame.K_LEFT]:
                right_moved = False
                left_moved = True
                x_change -= v
                v += a_x
            else:
                if v > 0:
                    v -= deceleration
                    if right_moved:
                        x_change += v
                    else:
                        x_change -= v
        else:
            # changing status of release_mark_crossed
            release_mark_crossed = True
            # storing velocity after release
            if do_once < 1:
                v_copy = v
                do_once += 1
            # the cart should continue to decelerate
            if v > 0:
                v -= deceleration
                if right_moved:
                    x_change += v
                else:
                    x_change -= v
        display.fill(BACKGROUND)
        # drawing ground and track
        ground_and_track()
        # drawing the cart controlled by user
        cart = Cart(x_loc=x + x_change, y_loc=y - y_change, color_of_cart=RED)
        # displaying text
        display_text(v, work(v_copy), v_copy)
        # displaying vectors
        if release_mark_crossed:
            display_vectors(cart.get_x_loc(), v=v, mass=m,
                            coef_of_friction=coef_of_sf)
        # update display
        pygame.display.update()
        # tick clock
        clock.tick(fps)
