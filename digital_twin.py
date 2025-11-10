import pygame
import sys
from controller import Arduino
from spec_generation import sample_single, apply_specs, sample_generator
from scipy.stats import binom, uniform, norm, rv_discrete
from functools import partial
import numpy as np

CAMERA_W, CAMERA_H = 640, 480
REAL_WINDOW_SIZE = (384, 288)
N_NODES = 5
TEMPLATE = np.load("TEMPLATE.npy")
com = "COM19"
key_input = False

sample_single = sample_generator(
            rng = 1,           
            ocupation_dist=binom(n=1, p=1),
            variety_dist=rv_discrete(values=([0, 1, 2], [1/2, 1/2, 0])),
            intensities=[
                rv_discrete(values=([0.5], [1])),
                rv_discrete(values=([1], [1])),
                norm(loc=0, scale=0.1)
                ],
            size_dist=uniform(loc=20, scale=5),
            rotation_dist=uniform(scale=360),)


def main(com = None, key_input = True):
    NODE_LENGTH = CAMERA_W / N_NODES
    deg_to_px = NODE_LENGTH/360

    if key_input:
        velocidad = 10
    if com: 
        ard = Arduino(port=com)
    else:
        ard = None
    
    belt = [Semilla(NODE_LENGTH*(4-i)) for i in range(5)]

    pygame.init()

    virtual_surface = pygame.Surface((CAMERA_W, CAMERA_H))

    pantalla = pygame.display.set_mode((REAL_WINDOW_SIZE))

    pygame.display.set_caption("SEEDBELT DIGITAL TWIN")

    # Cargar fondo
    fondo = pygame.image.load("fondo.png")
    fondo_rect = fondo.get_rect()
    fondo_rect.center = (CAMERA_W // 2, CAMERA_H // 2)  # empezar en el medio

    # Bucle pricle principal
    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Teclas presionadas
        if key_input:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if teclas[pygame.K_LEFT]:
                for semilla in belt:
                    semilla.update(-velocidad)
            if teclas[pygame.K_RIGHT]:
                for semilla in belt:
                    semilla.update(velocidad)
            
        # Lectura de arduino
        if ard is not None:
            step = check_for_steps(ard)
            if step is not None:    
                print("Dephasing", step, "deg")
                for semilla in belt:
                    semilla.update(step * deg_to_px)
                
        # Dibujar
        virtual_surface.blit(fondo, fondo_rect)
        for semilla in belt:    
            semilla.draw(virtual_surface)

        # Reescalar y mostrar
        pantalla.blit(pygame.transform.smoothscale(virtual_surface, REAL_WINDOW_SIZE), (0,0))
        pygame.display.flip()

        # Controlar FPS
        clock.tick(60)
        fps = clock.get_fps()
        print(fps)

class Semilla():
    def __init__(self, x):
        self.reset(x)
        
    def reset(self, x):
        self.x = x
        self.y = int(CAMERA_H/2)
        spec = sample_single()
        im = apply_specs(TEMPLATE, spec)[:,:,:]
        self.surface = pygame.image.frombuffer(im.tobytes(), im.shape[1::-1], "RGBA")

    def draw(self, surface):
        surface.blit(self.surface, dest = (self.x, self.y))
    
    def update(self, dx):
        self.x += dx
        if self.x > CAMERA_W:
            self.reset(self.x - CAMERA_W)
        



def check_for_steps(ard):
    data = ard.get_data()
    if data:
        try:
            steps = int(data)
            return steps
        except TypeError:
            print(data, "invalid step size")

if __name__ == "__main__":
    main(com, key_input)