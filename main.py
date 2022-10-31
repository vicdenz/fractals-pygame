import pygame
from const import *
from complex import complexNumber
import numpy as np
import pickle

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Set")

def random(z, c):
    z_div = (z - 1).cubed().divide((c.squared() * 3))
    if not z_div:
        return None
    return z - z_div + c

def burning_ship(z, c):
    return z.abs().squared() + c

def mandelbrot(z, c):
    return z.squared() + c

def solve_fractal(f):
    fractal = []

    for r in np.linspace(-2, 2, ITER_DEPTH):
        for i in np.linspace(-2, 2, ITER_DEPTH):

            z = complexNumber(0, 0)
            c = complexNumber(r, i)

            looped = False
            cycle = 0
            for iter in range(MAX_ITER):
                if not looped:
                    cycle = iter
                
                z = f(z, c)

                if cycle != 0 and z == c:
                    looped = True
                    break

                if not z or z.length() > 2:
                    break
            fractal.append((c, cycle, looped))
    
    return fractal

def save_data(set):
    with open(FILENAME, 'wb') as file:
        pickle.dump(set, file, protocol=pickle.HIGHEST_PROTOCOL)

def read_data():
    with open(FILENAME, 'rb') as file:
        return pickle.load(file)

def fractal_to_surface(fractal, x_offset, y_offset):
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((255, 255, 255))

    for c, cycle, looped in fractal:
        cycle_pct = cycle/MAX_ITER
        if looped or cycle == MAX_ITER-1:
            color = LOOPED_COLOR
        else:
            color = [min(255, MIN_COLOR[ch]+int(CYCLE_COLOR[ch]*cycle_pct)) for ch in range(0, 3, 1)]
        
        pygame.draw.rect(surface, color, (int(c.r*(WIDTH/4))+x_offset, int(c.i*(HEIGHT/4))+y_offset, 1, 1))

    return surface

def redrawGameWindow(fractal_image):
    screen.fill((255, 0, 0))

    screen.blit(fractal_image, (0, 0))

    pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2, HEIGHT/2, 1, 1))

    pygame.display.update()

def main():
    oper = input("Enter operation(\"s\" for solve_fractal, \"r\" for read_data): ")
    fractal = []

    if oper == "s":
        fractal = solve_fractal(mandelbrot)
        save_data(fractal)
        print('Done solving fractal...')
    else:
        fractal = read_data()
        print('Done reading fractal...')

    fractal_image = fractal_to_surface(fractal, WIDTH/2, HEIGHT/2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        redrawGameWindow(fractal_image)
    pygame.quit()

if __name__ == "__main__":
    main()