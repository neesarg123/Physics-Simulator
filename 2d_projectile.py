import pygame
from pygame import *
import tkinter as tk
import math
from decimal import Decimal
import itertools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# initializing pygame
pygame.init()

# FINALS
TK_INPUT_WIN_H = 250
TK_INPUT_WIN_W = 250
TK_INPUT_BG = '#575353'
TK_INPUT_SUB_BTN = '#fc4949'
PYGAME_H = 600
PYGAME_W = 900
PYGAME_BG = (137, 199, 190)
BALL_COLOR = (66, 136, 212)
BALL_RADIUS = 20
GROUND_COLOR = (92, 191, 78)
STAND_COLOR = (104, 108, 115)
X_VEL_VECTOR_COLOR = (255, 18, 133)
Y_VEL_VECTOR_COLOR = (200, 18, 255)
TRAJECTORY_LINE_COLOR = (255, 0, 0)
CANVAS_H = 600
CANVAS_W = 900
FONT_STYLE = 'freesansbold.ttf'
FONT_SIZE = 20
FONT = pygame.font.Font(FONT_STYLE, FONT_SIZE)
FONT_COLOR = (255, 255, 255)
PLOT_TK_WINDOW_FRAME_BG = '#454647'
LABEL_FONT = ('Courier', 25, 'bold')
LABEL_FONT_COLOR = '#ffffff'
FPS = 60

run_next_window_cycle = itertools.cycle('ft')
ball_height_angle_initial_vel = []


def toggle_next_window(win, h, a, i):
    next(run_next_window_cycle)
    ball_height_angle_initial_vel.extend([h, a, i])
    win.destroy()


# setting up tkinter window that will take in height, angle and initial velocity inputs
root_tk_in = tk.Tk()
root_tk_in.title("Inputs")
canvas_in = tk.Canvas(root_tk_in, height=TK_INPUT_WIN_H, width=TK_INPUT_WIN_W, bg=TK_INPUT_BG)
canvas_in.pack()
# labels
angle_label = tk.Label(root_tk_in, text="Angle")
angle_label.place(relx=0.05, rely=0.1, relheight=0.15, relwidth=0.3)

init_vel_label = tk.Label(root_tk_in, text="Initial Vel.")
init_vel_label.place(relx=0.05, rely=0.3, relheight=0.15, relwidth=0.3)

height_label = tk.Label(root_tk_in, text='Height')
height_label.place(relx=0.05, rely=0.5, relheight=0.15, relwidth=0.3)

# entries
angle_entry = tk.Entry(root_tk_in)
angle_entry.place(relx=0.4, rely=0.1, relheight=0.15, relwidth=0.3)

init_vel_entry = tk.Entry(root_tk_in)
init_vel_entry.place(relx=0.4, rely=0.3, relheight=0.15, relwidth=0.3)

height_entry = tk.Entry(root_tk_in)
height_entry.place(relx=0.4, rely=0.5, relheight=0.15, relwidth=0.3)
# submit button
submit_btn = tk.Button(root_tk_in, text='Submit', command=lambda: toggle_next_window(root_tk_in,
                                                                                     int(height_entry.get()),
                                                                                     int(angle_entry.get()),
                                                                                     Decimal(init_vel_entry.get())),
                       bg=TK_INPUT_SUB_BTN)
submit_btn.place(relx=0.4, rely=0.75, relheight=0.15, relwidth=0.3)
# mainloop
root_tk_in.mainloop()


class Ball:
    def __init__(self, pos_y=500, angle=0, initial_vel=Decimal(0.0)):
        self.pos_x = 50
        self.pos_y = pos_y
        self.vel_x = Decimal(0.0)
        self.vel_y = Decimal(0.0)
        self.acc_x = Decimal(0.0)
        self.acc_y = Decimal(-9.81)

        self.angle = angle
        self.initial_vel = initial_vel

    def draw(self):
        pygame.draw.circle(display, BALL_COLOR, (self.pos_x, self.pos_y), BALL_RADIUS)

    def update_vel_x(self):
        self.vel_x = Decimal(self.initial_vel * Decimal(math.cos((self.angle / 360) * (2 * math.pi))))

    def update_pos_x(self, secs):
        self.pos_x = 50 + Decimal(self.vel_x * Decimal(secs))

    def update_vel_y(self, secs):
        self.vel_y = Decimal(self.initial_vel * Decimal(math.sin((self.angle / 360) * (2 * math.pi)))
                             + Decimal(self.acc_y * Decimal(secs)))

    def update_pos_y(self, height, secs):
        self.pos_y = height - Decimal(self.vel_y * Decimal(secs)) + Decimal(0.5) * self.acc_y * \
                     Decimal(math.pow(secs, 2))


def draw_ground():
    pygame.draw.rect(display, GROUND_COLOR, [0, 520, 900, 600])


def draw_stand(height):
    pygame.draw.rect(display, STAND_COLOR, [0, 520 - height, 50, height])


def draw_vectors(vel_x, vel_y, ball_x, ball_y):
    # x-velocity vector
    pygame.draw.line(display, X_VEL_VECTOR_COLOR, (ball_x, ball_y), (ball_x + vel_x / Decimal(1.25), ball_y), 2)
    # y-velocity vector
    pygame.draw.line(display, Y_VEL_VECTOR_COLOR, (ball_x, ball_y), (ball_x, ball_y - vel_y / Decimal(1.25)), 2)


def draw_trajectory():
    for pos_x, pos_y in ball_positions:
        pygame.draw.rect(display, TRAJECTORY_LINE_COLOR, [pos_x, pos_y, 1, 1])


def display_texts(ball_vel_x, ball_vel_y, ball_dist_traveled, ball_time):
    # displaying x-velocity
    text_ball_vel_x = FONT.render("X-Velocity: " + str(ball_vel_x)[:5] + "m/s", True, FONT_COLOR, PYGAME_BG)
    text_rect = text_ball_vel_x.get_rect()
    text_rect.center = (700, 100)
    display.blit(text_ball_vel_x, text_rect)

    # displaying y-velocity
    text_ball_vel_y = FONT.render("Y-Velocity: " + str(ball_vel_y)[:5] + "m/s", True, FONT_COLOR, PYGAME_BG)
    text_rect = text_ball_vel_y.get_rect()
    text_rect.center = (700, 130)
    display.blit(text_ball_vel_y, text_rect)

    # displaying distance traveled
    text_ball_dist = FONT.render("Distance: " + str(ball_dist_traveled)[:5] + "m", True, FONT_COLOR, PYGAME_BG)
    text_rect = text_ball_dist.get_rect()
    text_rect.center = (700, 160)
    display.blit(text_ball_dist, text_rect)

    # displaying time traveled
    text_time = FONT.render("Time: " + str(ball_time)[:5] + "s", True, FONT_COLOR, PYGAME_BG)
    text_rect = text_time.get_rect()
    text_rect.center = (700, 190)
    display.blit(text_time, text_rect)


def display_position_vs_time_graphs(frame_win):
    # X-POSITION VS. TIME GRAPH
    fig = Figure(figsize=(5, 5), dpi=80)
    subplot = fig.add_subplot(111)
    subplot.set_title('X-Position vs. Time Graph')
    x_var = times
    y_var = [pos_x - 50 for pos_x, _ in ball_positions]

    # plotting the scatter graph
    subplot.scatter(x_var, y_var, color="#eb6e34")

    # displaying the bar graph onto tkinter window
    c = FigureCanvasTkAgg(fig, frame_win)
    c.draw()
    c.get_tk_widget().place(relx=0.1, rely=0.15, relheight=0.35, relwidth=0.35)

    # Y-POSITION VS. TIME GRAPH
    x_var = times
    y_var = [500 - pos_y for _, pos_y in ball_positions]

    # plotting the scatter graph
    fig = Figure(figsize=(5, 5), dpi=80)
    subplot_1 = fig.add_subplot(111)
    subplot_1.set_title('Y-Position vs. Time Graph')
    subplot_1.scatter(x_var, y_var, color="#eb6e34")

    # displaying the bar graph onto tkinter window
    c = FigureCanvasTkAgg(fig, frame_win)
    c.draw()
    c.get_tk_widget().place(relx=0.1, rely=0.5, relheight=0.35, relwidth=0.35)


def display_velocity_vs_time_graphs(frame_win):
    # X-VELOCITY VS. TIME GRAPH
    fig = Figure(figsize=(5, 5), dpi=80)
    subplot = fig.add_subplot(111)
    subplot.set_title('X-Velocity vs. Time Graph')
    x_var = times
    y_var = [ball.vel_x] * (len(times) - 1)
    y_var.insert(0, init_vel_x)

    # plotting the scatter graph
    subplot.scatter(x_var, y_var, color="#eb6e34")

    # displaying the bar graph onto tkinter window
    c = FigureCanvasTkAgg(fig, frame_win)
    c.draw()
    c.get_tk_widget().place(relx=0.55, rely=0.15, relheight=0.35, relwidth=0.35)

    # Y-VELOCITY VS. TIME GRAPH
    fig = Figure(figsize=(5, 5), dpi=80)
    subplot = fig.add_subplot(111)
    subplot.set_title('Y-Velocity vs. Time Graph')
    x_var = times
    y_var = y_velocities

    # plotting the scatter graph
    subplot.scatter(x_var, y_var, color="#eb6e34")

    # displaying the bar graph onto tkinter window
    c = FigureCanvasTkAgg(fig, frame_win)
    c.draw()
    c.get_tk_widget().place(relx=0.55, rely=0.5, relheight=0.35, relwidth=0.35)


if next(run_next_window_cycle) == 't':
    # setting up pygame window
    display = pygame.display.set_mode((PYGAME_W, PYGAME_H))
    display.fill(PYGAME_BG)

    # setting up pygame clock
    clock = pygame.time.Clock()

    # setting up tkinter window which will display the graphs for position and velocity
    root_tk_window = tk.Tk()
    root_tk_window.title("Plots")
    canvas = tk.Canvas(root_tk_window, height=CANVAS_H, width=CANVAS_W)
    canvas.pack()

    # running loop for pygame
    running = True

    # initializing a ball
    ball = Ball(pos_y=500 - ball_height_angle_initial_vel[0], angle=ball_height_angle_initial_vel[1],
                initial_vel=ball_height_angle_initial_vel[2])

    # initializing time
    time = 0
    # keeping track of all time increments -- for future plotting
    times = [0]

    # storing ball positions
    ball_positions = [(50, 500 - ball_height_angle_initial_vel[0])]

    # storing ball y-velocities
    ball.update_vel_y(time)
    y_velocities = [ball.vel_y]

    # initial x-vel of ball
    ball.update_vel_x()
    init_vel_x = ball.vel_x

    # setting up frame for tkinter window -- plots
    frame = tk.Frame(root_tk_window, bg=PLOT_TK_WINDOW_FRAME_BG)
    frame.place(relx=0, rely=0, relheight=1, relwidth=1)
    # window title text
    title_label = tk.Label(root_tk_window, text="Analytics", bg=PLOT_TK_WINDOW_FRAME_BG, font=LABEL_FONT,
                           fg=LABEL_FONT_COLOR)
    title_label.place(relx=0.4, rely=0.05, relheight=0.1, relwidth=0.2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                display_position_vs_time_graphs(frame)
                display_velocity_vs_time_graphs(frame)
                root_tk_window.mainloop()

        try:
            display.fill(PYGAME_BG)
        except pygame.error:
            break

        if ball.pos_y <= 500:
            ball.update_vel_x()
            ball.update_pos_x(time)
            ball.update_vel_y(time)
            ball.update_pos_y(500 - ball_height_angle_initial_vel[0], time)
            ball_positions.append((ball.pos_x, ball.pos_y))
            y_velocities.append(ball.vel_y)
            # incrementing time
            time += 0.02
            times.append(time)

        draw_ground()
        ball.draw()
        draw_vectors(ball.vel_x, ball.vel_y, ball.pos_x, ball.pos_y)
        draw_trajectory()
        draw_stand(ball_height_angle_initial_vel[0])
        # distance traveled so far by ball
        distance = ball_positions[-1][0] - ball_positions[0][0]
        display_texts(ball.vel_x, ball.vel_y, distance, time)

        pygame.display.update()
        clock.tick(FPS)

