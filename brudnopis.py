# pip install imageio[ffmpeg]

import pygame
import numpy as np
import imageio

# Ustawienia Pygame
pygame.init()
width, height = 500, 500  # 50 komórek * 10 pikseli na komórkę
win = pygame.display.set_mode((width, height))
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
grid_size = 50  # Upewnij się, że grid_size jest zgodny z analizą
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
            color = (255, 255, 255)  # Biały dla podatnych
            if grid[i, j] == INFECTED:
                color = (255, 0, 0)  # Czerwony dla zainfekowanych
            elif grid[i, j] == RECOVERED:
                color = (0, 255, 0)  # Zielony dla wyzdrowiałych
            elif grid[i, j] == DEAD:
                color = (0, 0, 0)  # Czarny dla martwych
            pygame.draw.rect(win, color, (i * cell_size, j * cell_size, cell_size, cell_size))


# Początkowa infekcja
grid[grid_size // 2, grid_size // 2] = INFECTED

# Lista do przechowywania klatek dla gif
frames = []

# Główna pętla symulacji
steps = 200
for step in range(steps):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    grid = update_grid(grid)

    win.fill((0, 0, 0))
    draw_grid(win, grid)
    pygame.display.flip()

    # Zapisanie klatki do listy frames
    frame = pygame.surfarray.array3d(win)
    frames.append(frame)

    clock.tick(10)

pygame.quit()

# Zapisanie gif
imageio.mimsave('sir_model_with_death.gif', frames, fps=10)
