# zadanie numeryczne 10

import sys
import numpy as np
import math
import random
import pygame as pg

#inicjalizacja PyGame
pg.init()
WIDTH, HEIGHT = 800, 650
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fraktale - zadanie numeryczne 10")
font = pg.font.SysFont("Arial", 20)
# kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
BLUE = (50, 150, 255)
DARK_BLUE = (100, 100, 100)
# przyciski GUI
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pg.Rect(x, y, w, h)
        self.callback = callback
        self.pressed = False

    def draw(self, screen):
        color = BLUE if self.pressed else DARK_BLUE
        pg.draw.rect(screen, color, self.rect, border_radius=8)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.pressed = True
            self.callback()
        elif event.type == pg.MOUSEBUTTONUP and self.pressed:
            self.pressed = False

# fraktale
def draw_barnsley():
    screen.fill(BLACK)
    x, y = 0, 0
    for _ in range(10_000):
        r = random.random()
        if r < 0.01:
            x, y = 0, 0.16 * y
        elif r < 0.86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        px = int(WIDTH / 2 + x * 60)
        py = int(HEIGHT - y * 60)
        if 0 <= px < WIDTH and 0 <= py < HEIGHT - 50:
            screen.set_at((px, py), GREEN)
    pg.display.flip()

def mandelbrot(c):
    z = 0
    for n in range(80):
        if abs(z) > 2:
            return n
        z = z * z + c
    return 80

def draw_mandelbrot():
    screen.fill(BLACK)
    ZOOM = 200
    for x in range(WIDTH):
        for y in range(HEIGHT - 50):
            zx = (x - WIDTH / 2) / ZOOM
            zy = (y - HEIGHT / 2 + 25) / ZOOM
            c = complex(zx, zy)
            m = mandelbrot(c)
            color = (m % 8 * 32, m % 16 * 16, m % 32 * 8)
            screen.set_at((x, y), color)
    pg.display.flip()

def tree(x, y, angle, length, depth):
    if depth == 0 or length < 1:
        return
    x2 = x + length * math.cos(angle)
    y2 = y - length * math.sin(angle)
    pg.draw.line(screen, BROWN, (int(x), int(y)), (int(x2), int(y2)), max(1, depth))
    tree(x2, y2, angle - math.pi / 6, length * 0.7, depth - 1)
    tree(x2, y2, angle + math.pi / 6, length * 0.7, depth - 1)

def draw_tree():
    screen.fill(BLACK)
    tree(WIDTH // 2, HEIGHT - 60, math.pi / 2, 100, 9)
    pg.display.flip()

def exit():
    pg.quit()
    sys.exit()
# tworzenie przycisków
buttons = [
    Button("Paproć Barnsleya", 20, HEIGHT - 40, 180, 30, draw_barnsley),
    Button("Fraktal Mandelbrota", 220, HEIGHT - 40, 180, 30, draw_mandelbrot),
    Button("Fraktal drzewo", 420, HEIGHT - 40, 160, 30, draw_tree),
    Button("Zakończ", 600, HEIGHT - 40, 160, 30, exit)
]

# główna pętla
running = True
screen.fill(BLACK)
pg.display.flip()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for btn in buttons:
            btn.click(event)
    for btn in buttons:
        btn.draw(screen)

    pg.display.update()