import pygame
from const import *
from complex import complexNumber
import numpy as np
import pickle

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
    # with open('123.txt', 'wb') as file:
    #     pickle.dump(set, file, protocol=pickle.HIGHEST_PROTOCOL)

    with open('123.txt', 'w') as file:
        file.writelines([repr(s[0]) + ',' + str(s[1]) + ',' + str(int(s[2])) + "\n" for s in set])
        

def read_data():
    # with open('123.txt', 'rb') as file:
    #     return pickle.load(file)

    data = []
    with open('123.txt', 'r') as file:
        for line in file.readlines():
            line = line[:-1].split(',')
            r = float(line[0])
            i = float(line[1])
            cycle = int(line[2])
            looped = bool(int(line[3]))
            data.append((complexNumber(r, i), cycle, looped))
    return data

def fractal_to_surface(fractal, zoom, x_offset, y_offset):
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(MIN_COLOR)

    for c, cycle, looped in fractal:
        x = int(c.r*((WIDTH/4)*zoom))+x_offset
        y = int(c.i*((HEIGHT/4)*zoom))+y_offset
        if 0 < x < WIDTH and 0 < y < HEIGHT:
            cycle_pct = cycle/MAX_ITER
            if looped or cycle == MAX_ITER-1:
                color = LOOPED_COLOR
            else:
                color = [min(255, MIN_COLOR[ch]+int(CYCLE_COLOR[ch]*cycle_pct)) for ch in range(0, 3, 1)]

            pygame.draw.rect(surface, color, (x, y, zoom, zoom))

    return surface

def redrawGameWindow(screen, fractal_image):
    screen.fill((255, 255, 255))

    screen.blit(fractal_image, (0, 0))

    pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2, HEIGHT/2), 1)

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

    zoom = 1
    x_offset = WIDTH/2
    y_offset = HEIGHT/2
    fractal_image = fractal_to_surface(fractal, zoom, x_offset, y_offset)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Set")
    clock = pygame.time.Clock()

    x_drag = 0
    y_drag = 0
    dragged = False

    running = True
    while running:
        clock.tick(FPS)

        refractal = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if zoom < MAX_ZOOM:
                        zoom += ZOOM_INCREMENT
                        refractal = True
                if keys[pygame.K_DOWN]:
                    if zoom > MIN_ZOOM:
                        zoom -= ZOOM_INCREMENT
                        refractal = True

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_rel = pygame.mouse.get_rel()
        if mouse_buttons[0]:
            if dragged == False:
                dragged = True

            x_drag += mouse_rel[0]
            y_drag += mouse_rel[1]
        else:
            if dragged:
                x_offset += x_drag
                y_offset += y_drag
                x_drag = 0
                y_drag = 0

                dragged = False
                refractal = True

        if refractal:
            fractal_image = fractal_to_surface(fractal, zoom, x_offset, y_offset)

        redrawGameWindow(screen, fractal_image)
    pygame.quit()

if __name__ == "__main__":
    main()