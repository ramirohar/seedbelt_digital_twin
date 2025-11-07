import pygame
import sys
from controller import Arduino

def read_ard_buffer(ard):
    data = ard.get_data()
    if data is None:
        pass
    else:
        if data == "OK": 
            pass
        else:
            return(data)

def check_for_steps(ard):
    data = read_ard_buffer(ard)
    try:
        steps = int(data)
        return steps
    except TypeError:
        print(data, "invalid step size")


def main(com = None, key_input = True):

    CAMERA_W, CAMERA_H = 640, 480
    REAL_WINDOW_SIZE = (512, 384)
    deg_to_px = CAMERA_W/(360*5)

    pygame.init()

    virtual_surface = pygame.Surface((CAMERA_W, CAMERA_H))

    pantalla = pygame.display.set_mode((REAL_WINDOW_SIZE))

    pygame.display.set_caption("Seedbelt digital twin")

    # Cargar fondo
    fondo = pygame.image.load("fondo.png")
    fondo_rect = fondo.get_rect()
    fondo_rect.center = (CAMERA_W // 2, CAMERA_H // 2)  # empezar en el medio

    # Cargar imagen
    imagen = pygame.image.load("desfile.png")
    imagen_rect = imagen.get_rect()
    imagen_rect.center = (CAMERA_W // 2, CAMERA_H // 2)  # empezar en el medio

    # Bucle pricle principal
    clock = pygame.time.Clock()
    
    if key_input:
        velocidad = 10

    if com: 
        ard = Arduino(com=com)
    else:
        ard = None

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
        
        # Lectura de arduino
        if ard is not None:
            step = check_for_steps(ard)
            print("Dephasing", step, "deg")
            imagen.rect.x += step * deg_to_px
            
        # Dibujar
        virtual_surface.blit(fondo, fondo_rect)
        virtual_surface.blit(imagen, imagen_rect)
        
        # Reescalar y mostrar
        pantalla.blit(pygame.transform.smoothscale(virtual_surface, REAL_WINDOW_SIZE), (0,0))
        pygame.display.flip()

        # Controlar FPS
        clock.tick(60)

if __name__ == "__main__":
    main()