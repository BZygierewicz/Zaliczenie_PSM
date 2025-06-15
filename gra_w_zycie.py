# Gra w życie - zadanie numeryczne 4
import numpy as np
import pygame as pg
import sys

# rozmiar planszy
WIDTH, HEIGHT = 800, 650
GRID_HEIGHT = 600
CELL_SIZE = 25
# kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (40, 40, 40)
BLUE = (50, 150, 255)
DARK_BLUE = (100, 100, 100)


# inicjalizacja PyGame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Gra w zycie - zadanie numeryczne 4')
font = pg.font.SysFont('Arial', 20)
# grid
cols, rows = WIDTH // CELL_SIZE, GRID_HEIGHT // CELL_SIZE
grid = np.zeros((rows, cols), dtype=int)
running = False
clock = pg.time.Clock()
# Przyciski GUI
class Button:
    def __init__(self, text, x, y, width, height, callback, color=BLUE, pressed_color=DARK_BLUE):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.callback = callback
        self.color = color
        self.is_pressed = False
        self.pressed_color = pressed_color

    def draw(self, screen):
        current_color = self.pressed_color if self.is_pressed else self.color
        pg.draw.rect(screen, current_color, self.rect, border_radius=8)
        label = font.render(self.text, True, WHITE)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.callback()
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_pressed = False

# funkcje do przycisków
def running_handler():
    global running
    running = not running

def clear_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)

def randomize_grid():
    global grid
    grid = np.random.choice([0,1], size=(rows, cols), p=[0.85, 0.15])

def exit():
    pg.quit()
    sys.exit()
# tworzenie przycisków
buttons = [
    Button("Start / Stop", 10, GRID_HEIGHT+10, 130, 30, running_handler),
    Button("Reset", 300, GRID_HEIGHT+10, 100, 30, clear_grid),
    Button("Losuj", 410, GRID_HEIGHT+10, 100, 30, randomize_grid),
    Button("Zakończ", 670, GRID_HEIGHT+10, 100, 30, exit)
]
# rysowanie siatki
def draw_grid(screen, grid):
    screen.fill(BLACK)
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                pg.draw.rect(screen, WHITE, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # linie siatki
    for x in range(0,WIDTH,CELL_SIZE):
        pg.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
    for y in range(0,HEIGHT,CELL_SIZE):
        pg.draw.line(screen, GREY, (0, y), (WIDTH, y))

# update komórek
def update_grid(grid):
    new_grid = np.copy(grid)
    for y in range(rows):
        for x in range(cols):
            # sąsiedzi (3x3)
            neighbors = np.sum(grid[max(0, y-1) : min(rows, y+2),
                               max(0, x-1) : min(cols, x+2)]) - grid[y,x]
            if grid[y, x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[y, x] = 0
            else:
                if neighbors == 3:
                    new_grid[y, x] = 1
    return new_grid

# Główna pętla
while True:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
            for btn in buttons:
                btn.click(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()

            else:
                for bnt in buttons:
                    bnt.click(event)


    if running:
        grid = update_grid(grid)
    draw_grid(screen, grid)

    for btn in buttons:
        btn.draw(screen)

    # obsługa myszki
    mouse_buttons = pg.mouse.get_pressed()
    if mouse_buttons[0] or mouse_buttons[2]:
        mx, my = pg.mouse.get_pos()
        if my < GRID_HEIGHT:
            cell_x = mx // CELL_SIZE
            cell_y = my // CELL_SIZE
            if 0 <= cell_x < cols and 0 <= cell_y < rows:
                if mouse_buttons[0]:
                    grid[cell_y, cell_x] = 1
                elif mouse_buttons[2]:
                    grid[cell_y, cell_x] = 0

    pg.display.update()
