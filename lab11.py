"""
Wykład: https://github.com/houp/ca-class/blob/main/slides/lecture11.pdf

zad.18
Zaimplementuj jeden z wybranych modeli prezentowanych na wykładzie: DS FFM, SIR lub GH. Jeśli to możliwe (jeśli masz
ciekawy pomysł) to wprowadź wybraną modyfikację do wybranego przez Ciebie modelu, np.:
- W modelu SIR wprowadź stan "śmierć", który osiąga się z małym prawdopodobieństwem przy infekcji i zobacz jak inne
parametry wpływają na śmiertelność epidemii.
- W modelu FFM wprowadź kierunek wiatru - tzn. prawdopodobieństwo podpalenia może być inne zależnie od tego z której
strony sąsiad się pali.
- W modelu GH - poeksperymentuj z liczbą stanów recovery i spróbuj znaleźć wartość krytycznego prawdopodobieństwa przy
których, dla zadanej liczby stanów, model istotnie zmienia swoje właściwości.

Rozwiązaniem jest program, który robi wizualizację (w pygame) oraz prezentuje w jakiejś formie wyniki eksperymentów
- opis + wykres w notebooku.
"""

import pygame
import numpy as np

# Ustawienia Pygame
pygame.init()
width, height = 500, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Model with Death")
clock = pygame.time.Clock()
cell_size = 10

# Parametry modelu
prob_infection = 0.2  # Prawdopodobieństwo infekcji
prob_death = 0.01  # Prawdopodobieństwo śmierci przy infekcji
prob_recovery = 0.05  # Prawdopodobieństwo wyzdrowienia

# Stany komórek
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
DEAD = 3

# Inicjalizacja siatki
grid_size = width // cell_size
grid = np.zeros((grid_size, grid_size), dtype=int)


# Funkcja aktualizacji stanu siatki
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == INFECTED:
                if np.random.rand() < prob_death:
                    new_grid[i, j] = DEAD
                elif np.random.rand() < prob_recovery:
                    new_grid[i, j] = RECOVERED
                else:
                    for ni in range(i - 1, i + 2):
                        for nj in range(j - 1, j + 2):
                            if 0 <= ni < grid_size and 0 <= nj < grid_size and grid[ni, nj] == SUSCEPTIBLE:
                                if np.random.rand() < prob_infection:
                                    new_grid[ni, nj] = INFECTED
    return new_grid


# Funkcja rysowania siatki
def draw_grid(win, grid):
    for i in range(grid_size):
        for j in range(grid_size):
            color = (0, 0, 255)  # Niebieski dla podatnych
            if grid[i, j] == INFECTED:
                color = (255, 0, 0)  # Czerwony dla zainfekowanych
            elif grid[i, j] == RECOVERED:
                color = (0, 255, 0)  # Zielony dla wyzdrowiałych
            elif grid[i, j] == DEAD:
                color = (0, 0, 0)  # Czarny dla martwych
            pygame.draw.rect(win, color, (i * cell_size, j * cell_size, cell_size, cell_size))


# Początkowa infekcja
grid[grid_size // 2, grid_size // 2] = INFECTED

# Główna pętla symulacji
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid = update_grid(grid)

    win.fill((0, 0, 0))
    draw_grid(win, grid)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
