import pygame
import sys
from controller import Arduino

# Inicializar pygame

deg_to_px = 640/(360*5)

pygame.init()
# ard = Arduino(port="COM11")
ard = None
# Crear la ventana
ancho, alto = 640,480

# real_window_size = (512, 384)
real_window_size = 200, 200
virtual_surface = pygame.Surface((ancho, alto))

pantalla = pygame.display.set_mode((real_window_size))

pygame.display.set_caption("Animación con Pygame")

fondo = pygame.image.load("fondo.png")

fondo_rect = fondo.get_rect()
fondo_rect.center = (ancho // 2, alto // 2)  # empezar en el medio

# Cargar la imagen
imagen = pygame.image.load("desfile.png")
imagen_rect = imagen.get_rect()
imagen_rect.center = (ancho // 2, alto // 2)  # empezar en el medio

velocidad = 10

# Bucle pricle principal
clock = pygame.time.Clock()

key_input = True
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas presionadas
  
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_ESCAPE]:
        pygame.quit()
        ard.close()
        sys.exit()

    if teclas[pygame.K_LEFT]:
        imagen_rect.x -= velocidad
    if teclas[pygame.K_RIGHT]:
        imagen_rect.x += velocidad
    if teclas[pygame.K_UP]:
        imagen_rect.y -= velocidad
    if teclas[pygame.K_DOWN]:
        imagen_rect.y += velocidad
    
    if ard is not None:
        data = ard.get_data()
        if data is None:
            pass
        else:
            if data == "OK": 
                pass
            else:
                try:
                    steps = int(data)
                    print(f"moving {steps}")
                    imagen_rect.x += int(steps * deg_to_px)

                except TypeError:
                    print(data, "is not a number")

    # Dibujar
    
    virtual_surface.blit(fondo, fondo_rect)
    virtual_surface.blit(imagen, imagen_rect)
    
    pantalla.blit(pygame.transform.smoothscale(virtual_surface, real_window_size), (0,0))
    pygame.display.flip()

    # Controlar FPS
    clock.tick(60)