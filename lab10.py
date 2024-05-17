"""
Wykład: https://github.com/houp/ca-class/blob/main/slides/lecture10.pdf

zad.17
Zaimplementuj wizualizację automatu komórkowego Gra w Życie z wykorzystaniem pygame. Zakładamy periodyczne warunki
brzegowe. Liczba komórek, rozmiar okna, rozmiar komórki na ekranie mogą być zaszyte w kodzie na sztywno. Program ma
umożliwiać:
- Wstrzymanie / wznowienie symulacji (pauza - np. przez wciśnięcie spacji na klawiaturze).
- Wylosowanie warunku początkowego (np. przy każdym naciśnięciu przycisku enter losujemy nowy warunek).
- Zwiększenie / zmniejszenie prędkości symulacji (np. przez wciśnięcie strzałki w górę / w dół na klawiaturze).

Dodatkowo program powinien umożliwiać conajmniej jedną z następujących operacji:
- Ustalanie konfiguracji początkowej przez klikanie myszką w poszczególne komórki (kliknięcie zmieni stan na przeciwny).
- Poza losowymi warunkami początkowymi, udostępnienie użytkownikowi kilku zapisanych konfiguracji - np. pokazujących
glider, glider gun, space ship.
- Możliwość zmiany reguły z tradycyjnej Game of Life na inne reguły "life-like" np. HighLife, Life without Death,
34 Life, Seeds …
- Wizualizację zmieniających się stanów - odróżnienie w wizualizacji "nowej" od "starej" 1. Czyli np. jeśli dana komórka
dopiero co przeszła z 0 na 1, to przez chwilę będzie rysowana jaśniejszym kolorem, niż komórka, która była w stanie 1
już wcześniej. (Podobnie można zrobić dla 0, czyli świeżo "umarłe" komórki zaznaczać na przykład na szaro.) W ten sposób
choć automat nadal będzie 2-stanowy, to pokażemy niejako więcej stanów ale jedynie na poziomie wizualizacji a nie reguły
CA.
"""

import pygame
import numpy as np

# Parametry
CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Kolory
COLOR_BG = (0, 0, 0)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)
COLOR_NEWBORN = (200, 200, 200)
COLOR_DIED = (100, 100, 100)

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game of Life")


# Losowanie nowej konfiguracji początkowej
def random_grid():
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))


# Ustalanie nowej konfiguracji początkowej przez kliknięcie myszką
def toggle_cell(grid, x, y):
    grid[y][x] = not grid[y][x]


# Aktualizacja stanu automatu komórkowego
def update(grid):
    new_grid = np.copy(grid)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            num_alive_neighbors = (
                    grid[(y - 1) % GRID_HEIGHT, (x - 1) % GRID_WIDTH] + grid[(y - 1) % GRID_HEIGHT, x % GRID_WIDTH] +
                    grid[(y - 1) % GRID_HEIGHT, (x + 1) % GRID_WIDTH] + grid[y % GRID_HEIGHT, (x - 1) % GRID_WIDTH] +
                    grid[y % GRID_HEIGHT, (x + 1) % GRID_WIDTH] + grid[(y + 1) % GRID_HEIGHT, (x - 1) % GRID_WIDTH] +
                    grid[(y + 1) % GRID_HEIGHT, x % GRID_WIDTH] + grid[(y + 1) % GRID_HEIGHT, (x + 1) % GRID_WIDTH]
            )
            if grid[y, x] == 1:
                if num_alive_neighbors < 2 or num_alive_neighbors > 3:
                    new_grid[y, x] = 0
            else:
                if num_alive_neighbors == 3:
                    new_grid[y, x] = 1
    return new_grid


# Rysowanie siatki
def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))


# Rysowanie komórek
def draw_cells(grid, prev_grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 1:
                if prev_grid[y, x] == 0:
                    color = COLOR_NEWBORN
                else:
                    color = COLOR_ALIVE
            else:
                if prev_grid[y, x] == 1:
                    color = COLOR_DIED
                else:
                    color = COLOR_BG
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Główna pętla
def main():
    clock = pygame.time.Clock()
    grid = random_grid()
    prev_grid = np.copy(grid)
    running = True
    paused = False
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RETURN:
                    grid = random_grid()
                elif event.key == pygame.K_UP:
                    speed = min(60, speed + 1)
                elif event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                toggle_cell(grid, x // CELL_SIZE, y // CELL_SIZE)

        if not paused:
            prev_grid = np.copy(grid)
            grid = update(grid)

        screen.fill(COLOR_BG)
        draw_cells(grid, prev_grid)
        draw_grid()
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


if __name__ == "__main__":
    main()
