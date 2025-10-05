import pygame
import sys

# Inicializar pygame
pygame.init()

# Crear la ventana
ancho, alto = 1080,960
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Animación con Pygame")

fondo = pygame.image.load("fondo.png")

fondo_rect = fondo.get_rect()
fondo_rect.center = (ancho // 2, alto // 2)  # empezar en el medio

# Cargar la imagen
imagen = pygame.image.load("desfile.png")
imagen_rect = imagen.get_rect()
imagen_rect.center = (ancho // 2, alto // 2)  # empezar en el medio

velocidad = 5

# Bucle pricle principal
clock = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    if teclas[pygame.K_LEFT]:
        imagen_rect.x -= velocidad
    if teclas[pygame.K_RIGHT]:
        imagen_rect.x += velocidad
    if teclas[pygame.K_UP]:
        imagen_rect.y -= velocidad
    if teclas[pygame.K_DOWN]:
        imagen_rect.y += velocidad


    # Dibujar
    pantalla.fill((30, 30, 30))  # fondo gris oscuro
    pantalla.blit(fondo, fondo_rect)
    pantalla.blit(imagen, imagen_rect)
    pygame.display.flip()

    # Controlar FPS
    clock.tick(60)