from random import randint, random

import pygame
from math import sin, cos, floor, sqrt, radians


PHEROMONE_EVAPORATION = 5
PHEROMONE_PLACEMENT = 15
PHEROMONE_MIN = 0
PHEROMONE_MAX = 400


SPEED_DEVIATION = 0.1
AGENTS_COUNT = 1000
ANGLE = randint(10, 90) # 45
DISTANCE = randint(10, 30) / 10 # 1.5
ROTATION_SPEED = randint(1, 100) / 100 # 0.3
SPEED = randint(1, 10) / 10 # 0.1
RADIUS = 3 # 2

MAP_X, MAP_Y = 80, 48 # 180 120
WINDOW_X, WINDOW_Y = 720, 480
SCALE_X, SCALE_Y = WINDOW_X / MAP_X, WINDOW_Y / MAP_Y

FPS = 999

GRAY_COLOR = (50, 50, 50)

MUST_SHOW_AGENTS = True

AGENTS = []



def make_properties():
    global ANGLE, DISTANCE, SPEED, ROTATION_SPEED, AGENTS, RADIUS


    ANGLE = randint(10, 90)  # 45
    DISTANCE = randint(10, 30) / 10  # 1.5
    ROTATION_SPEED = randint(1, 100) / 100  # 0.3
    SPEED = randint(1, 10) / 10  # 0.1
    RADIUS = 3  # 2

    text = \
        f"ANGLE = {ANGLE} \
        DISTANCE = {DISTANCE} \
        ROTATION_SPEED = {ROTATION_SPEED} \
        SPEED = {SPEED} (+-{SPEED_DEVIATION})  \
        RADIUS = {RADIUS} "
    print(text)


    for agent in AGENTS:
        agent.dist = DISTANCE
        agent.azim = RADIUS
        agent.angle = ANGLE
        agent.speed = SPEED
        agent.rot_speed = ROTATION_SPEED
        agent.radius = RADIUS


make_properties()



MAP = [[0 for _ in range(MAP_Y)] for _ in range(MAP_X)]
WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y), ) # pygame.FULLSCREEN
AGENTS = []

from math import radians

def get_signal(x, y, d, az, a):
    """
    Calculate the left and right sensor positions relative to the agent's direction.
    x, y: Agent's current position
    d: Distance from the agent to the sensors
    az: Agent's current azimuth (heading direction in degrees)
    a: Angle between the forward direction and each sensor
    """
    # Convert azimuth and angle to radians
    az_radians = radians(az)

    # Left sensor is at angle + a
    left_azimuth = az_radians + radians(a)
    left_signal_x = x + d * cos(left_azimuth)
    left_signal_y = y + d * sin(left_azimuth)

    # Right sensor is at angle - a
    right_azimuth = az_radians - radians(a)
    right_signal_x = x + d * cos(right_azimuth)
    right_signal_y = y + d * sin(right_azimuth)

    forward_signal = az_radians
    forward_signal_x = x + d * cos(forward_signal)
    forward_signal_y = y + d * sin(forward_signal)


    return (left_signal_x, left_signal_y), (right_signal_x, right_signal_y), (forward_signal_x, forward_signal_y)

def get_pheromone_gradient(x, y, radius):
    """
    Calculate the average pheromone level in a neighborhood around (x, y).
    """
    total_pheromone = 0
    count = 0

    # Iterate over a square area with side length 2*radius centered at (x, y)
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            # Check if the point is within the circle of given radius
            if sqrt(i ** 2 + j ** 2) <= radius:
                # Use modulo to handle the map's wrap-around edges
                nx = (x + i) % MAP_X
                ny = (y + j) % MAP_Y
                total_pheromone += MAP[nx][ny]
                count += 1

    # Return the average pheromone level in the neighborhood
    return total_pheromone / count if count > 0 else 0


class Agent:
    def __init__(self, x, y, azimuth, angle, dist, rotation_speed, speed, radius):
        self.x = x
        self.y = y
        self.azim = azimuth
        self.angle = angle
        self.dist = dist
        self.rot_speed = rotation_speed
        self.speed = speed
        self.signals = (-1, -1, -1, -1)
        self.radius = radius

    def step(self):
        # Get left and right signal positions based on agent's orientation
        left_signal, right_signal, forward_signal = get_signal(self.x, self.y, self.dist, self.azim, self.angle)

        # Apply modulo for wrap-around behavior
        left_signal = left_signal[0] % MAP_X, left_signal[1] % MAP_Y
        right_signal = right_signal[0] % MAP_X, right_signal[1] % MAP_Y
        forward_signal = forward_signal[0] % MAP_X, forward_signal[1] % MAP_Y

        # Convert to integer grid positions
        lx, ly = floor(left_signal[0]), floor(left_signal[1])
        rx, ry = floor(right_signal[0]), floor(right_signal[1])
        fx, fy = floor(forward_signal[0]), floor(forward_signal[1])

        # Define a radius for gradient calculation (e.g., 2 cells)
        radius = self.radius

        # Calculate pheromone gradients at both the left and right signal points
        left_gradient = get_pheromone_gradient(lx, ly, radius)
        right_gradient = get_pheromone_gradient(rx, ry, radius)
        forward_gradient = get_pheromone_gradient(fx, fy, radius)

        # Adjust the agent's direction based on the pheromone gradient
        if max(forward_gradient, left_gradient, right_gradient) == forward_gradient:
            pass
        elif max(left_gradient, right_gradient) == left_gradient:
            self.azim += self.rot_speed
        elif max(left_gradient, right_gradient) == right_gradient:
            self.azim -= self.rot_speed


        # Update agent position based on the azimuth
        self.x = (self.x + self.speed * cos(radians(self.azim))) % MAP_X
        self.y = (self.y + self.speed * sin(radians(self.azim))) % MAP_Y

        # Add pheromone to the map at the agent's current position
        existing_pheromone = MAP[floor(self.x)][floor(self.y)]
        if existing_pheromone > 0:
            MAP[floor(self.x)][floor(self.y)] += PHEROMONE_PLACEMENT * 1.5  # Reinforce
        else:
            MAP[floor(self.x)][floor(self.y)] += PHEROMONE_PLACEMENT


        # Store the signal positions for visualization purposes
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

    PHEROMONE_THRESHOLD = 1  # Minimum pheromone level to continue diffusing

    def diffuse_pheromones():
        diffusion_rate = 0.134
        decay_factor = 0.95  # Decay by 5% during each diffusion step
        global MAP
        new_MAP = [[0 for _ in range(MAP_Y)] for _ in range(MAP_X)]  # New map to hold diffused pheromones

        for x in range(MAP_X):
            for y in range(MAP_Y):
                pheromone = MAP[x][y] * decay_factor  # Apply decay

                # If the pheromone level is below the threshold, stop diffusion
                if pheromone < PHEROMONE_THRESHOLD:
                    continue

                # Diffuse to neighbors
                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1),
                             (x, y + 1)]  # Neighboring cells (up, down, left, right)
                for nx, ny in neighbors:
                    nx, ny = nx % MAP_X, ny % MAP_Y  # Handle wrap-around
                    new_MAP[nx][ny] += diffusion_rate * pheromone  # Spread to neighbors
                new_MAP[x][y] += pheromone / len(neighbors) * 2  # Retain some pheromone in the original cell

        MAP = new_MAP  # Update the map with diffused pheromones

    # diffuse_pheromones()

def check_events():

    global MUST_SHOW_AGENTS

    if pygame.mouse.get_pressed()[0]:
        RADIUS = 2

        # Get mouse position and map it to the grid
        x, y = pygame.mouse.get_pos()
        x = floor(x / SCALE_X) % MAP_X
        y = floor(y / SCALE_Y) % MAP_Y
        # Iterate over a square that contains the sphere (circle)
        for i in range(-RADIUS, RADIUS + 1):
            for j in range(-RADIUS, RADIUS + 1):
                # Calculate the distance from the center (x, y)
                if sqrt(i ** 2 + j ** 2) <= RADIUS:
                    # Use modulo to wrap around the map edges
                    map_x = (x + i) % MAP_X
                    map_y = (y + j) % MAP_Y

                    # Add the pheromone to the current point
                    MAP[map_x][map_y] += PHEROMONE_PLACEMENT * 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_q:
                exit()
            if key == pygame.K_SPACE:
                make_properties()
            if key == pygame.K_1:
                MUST_SHOW_AGENTS = True
            if key == pygame.K_2:
                MUST_SHOW_AGENTS = False



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
                r = max(0, min(255, floor(50 - 50 * level)))
                g = max(0, min(255, floor(level * 255)))
                b = max(0, min(255, floor(50 - 50 * level)))
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

    if MUST_SHOW_AGENTS:
        draw_agents()

def draw_text():
    pass


def start(count):
    for i in range(count):
        x, y = randint(0, MAP_X - 1), randint(0, MAP_Y - 1)
        azimuth = randint(0, 360)
        agent = Agent(x, y, azimuth, ANGLE, DISTANCE, ROTATION_SPEED, SPEED + SPEED_DEVIATION * (random() * -1 if random() > 0.5 else random()), RADIUS)
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