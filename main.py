from random import randint, random

import pygame
from math import sin, cos


PHEROMONE_EVAPORATION = 0.1
PHEROMONE_PLACEMENT = 15
PHEROMONE_MIN = 0
PHEROMONE_MAX = 200

AGENTS_COUNT = 3

ANGLE = 30
DISTANCE = 5
ROTATION_SPEED = 0.1
SPEED = 0.2

MAP_X, MAP_Y = 60, 40 # 180 120
WINDOW_X, WINDOW_Y = 720, 480
SCALE_X, SCALE_Y = WINDOW_X / MAP_X, WINDOW_Y / MAP_Y

MAP = [[0 for _ in range(MAP_Y)] for _ in range(MAP_X)]
WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y), ) # pygame.FULLSCREEN
AGENTS = []

FPS = 999

GRAY_COLOR = (50, 50, 50)

def get_signal(x, y, d, az, a):
    # return (x + 1, y + 1), (x + 1, y - 1)
    Ax, Ay = x + d * cos(a) * cos(az) - d * sin(a) * sin(az), y + d * cos(a) * sin(az) + d * sin(a) * cos(az)
    Bx, By = x + d * cos(a) * cos(az) + d * sin(a) * sin(az), y + d * cos(a) * sin(az) - d * sin(a) * cos(az)
    return (Ax, Ay), (Bx, By)


class Agent:
    def __init__(self, x, y, azimuth, angle, dist, rotation_speed, speed):
        self.x = x
        self.y = y
        self.azim = azimuth
        self.angle = angle
        self.dist = dist
        self.rot_speed = rotation_speed
        self.speed = speed
        self.signals = (-1, -1, -1, -1)


    def step(self):
        left_signal, right_signal = get_signal(self.x, self.y, self.dist, self.azim, self.angle)
        left_signal = left_signal[0] % MAP_X, left_signal[1] % MAP_Y
        right_signal = right_signal[0] % MAP_X, right_signal[1] % MAP_Y

        if left_signal > right_signal:
            self.azim -= self.rot_speed
        if left_signal < right_signal:
            self.azim += self.rot_speed


        self.x = self.x + self.speed * cos(self.azim) + random() / 5
        self.y = self.y + self.speed * sin(self.azim) + random() / 5
        self.x = self.x % MAP_X
        self.y = self.y % MAP_Y
        MAP[int(self.x)][int(self.y)] += PHEROMONE_PLACEMENT

        self.signals = left_signal, right_signal

def start():
    pass

def clear():
    pygame.display.flip()

# clock = pygame.time.Clock()


def agents_step():
    for agent in AGENTS:
        agent.step()

    for y in range(MAP_Y):
        for x in range(MAP_X):
            # pass
            MAP[x][y] -= PHEROMONE_EVAPORATION
            MAP[x][y] = max(0, min(PHEROMONE_MAX, MAP[x][y]))

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_q:
                exit()



def draw_objects():
    def draw_grid():
        for y in range(MAP_Y):
            for x in range(MAP_X):
                # Calculate the position and size of each square
                rect_x = x * SCALE_X
                rect_y = y * SCALE_Y
                rect_width = SCALE_X
                rect_height = SCALE_Y
                # print(x, y)
                pheromone = MAP[x][y]
                level = pheromone / PHEROMONE_MAX
                r = max(0, min(255, int(50 - 50 * level)))
                g = max(0, min(255, int(level * 255)))
                b = max(0, min(255, int(50 - 50 * level)))
                color = r, g, b
                # Draw the square
                pygame.draw.rect(WINDOW, color, (rect_x, rect_y, rect_width, rect_height))

                # Draw grid lines (optional, remove this block if you don't want lines)
                # pygame.draw.rect(WINDOW, (100, 100, 100), (rect_x, rect_y, rect_width, rect_height), 1)
    def draw_agents():
        for agent in AGENTS:
            pygame.draw.circle(WINDOW, (255, 0, 0), (agent.x * SCALE_X, agent.y * SCALE_Y), 4)
            s1, s2 = agent.signals
            x1, y1, x2, y2 = s1[0] * SCALE_X, s1[1] * SCALE_Y, s2[0] * SCALE_X, s2[1] * SCALE_Y
            pygame.draw.circle(WINDOW, (200, 200, 200), (x1, y1), 4)
            pygame.draw.circle(WINDOW, (200, 200, 200), (x2, y2), 4)
    draw_grid()
    draw_agents()

def draw_text():
    pass


def start(count):
    for i in range(count):
        x, y = randint(0, MAP_X - 1), randint(0, MAP_Y - 1)
        azimuth = randint(0, 360)
        agent = Agent(x, y, azimuth, ANGLE, DISTANCE, ROTATION_SPEED, SPEED)
        AGENTS.append(agent)

stage = 0
start(AGENTS_COUNT)
while True:
    stage += 1
    agents_step()
    check_events()
    draw_objects()
    draw_text()
    clear()
    # clock.tick(FPS)
    # print(MAP[randint(0, MAP_X-1)][randint(0, MAP_Y-1)])