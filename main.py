from random import randint
import pygame


MAP_X, MAP_Y = 1080, 720
MAP = [[-1 for i in range(MAP_X)] for i in range(MAP_Y)]

class Agent():
    pass


def start():
    pass

def clear():
    pygame.display.flip()

clock = pygame.time.Clock()


def agents_step():
    pass


def check_events():
    pass



def draw_objects():
    pass


def draw_text():
    pass


while True:
    agents_step()
    check_events()
    draw_objects()
    draw_text()
    clear()
    clock.tick(FPS)