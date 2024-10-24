import pygame
import time

pygame.init()
pygame.mixer.init()

# Variables
apuestas_file = 'Ruleta/apuestas.txt'
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Tablero Ruleta")

# Cargar imágenes
tablero_image = pygame.image.load("Ruleta/tableroruleta.png")
tablero_rect = tablero_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

ficha_image = pygame.image.load("Ruleta/ficha.png")
ficha_image = pygame.transform.scale(ficha_image, (15, 15))

# Temporizador en minutos
TIEMPO_INICIAL = 2 * 60  # 5 minutos en segundos
tiempo_restante = TIEMPO_INICIAL
fuente_tiempo = pygame.font.SysFont(None, 30)  # Fuente para mostrar el tiempo

def leer_apuestas():
    apuestas = []
    with open(apuestas_file, "r") as file:
        for line in file:
            jugador, cantidad, numero = line.strip().split(",")
            apuestas.append((numero.strip(), int(cantidad)))  
    return apuestas

def obtener_posicion_ficha(opcion):
    posiciones = {
        '00': (45, 40),
        '0': (45, 95),
        '1': (70, 105),
        '2': (70, 70),
        '3': (70, 35),
        '4': (92, 105),
        '5': (92, 70),
        '6': (92, 35),
        '7': (114, 105),
        '8': (114, 70),
        '9': (114, 35),
        '10': (136, 105),
        '11': (136, 70),
        '12': (136, 35),
        '13': (158, 105),
        '14': (158, 70),
        '15': (158, 35),
        '16': (182, 105),
        '17': (182, 70),
        '18': (182, 35),
        '19': (204, 105),
        '20': (204, 70),
        '21': (204, 35),
        '22': (228, 105),
        '23': (228, 70),
        '24': (228, 35),
        '25': (250, 105),
        '26': (250, 70),
        '27': (250, 35),
        '28': (274, 105),
        '29': (274, 70),
        '30': (274, 35),
        '31': (296, 105),
        '32': (296, 70),
        '33': (296, 35),
        '34': (318, 105),
        '35': (318, 70),
        '36': (318, 35),
        'rojo': (171, 168),
        'negro': (218, 168),
    }
    return posiciones.get(opcion, (0, 0))

def mostrar_tiempo_restante(tiempo):
    minutos = tiempo // 60
    segundos = tiempo % 60
    texto_tiempo = f"{minutos:02}:{segundos:02}"
    texto_extra = "Tiempo restante:"

    render_texto_extra = fuente_tiempo.render(texto_extra, True, (255, 255, 255))
    render_tiempo = fuente_tiempo.render(texto_tiempo, True, (255, 255, 255))
    screen.blit(render_texto_extra, (WIDTH - 400, 0))
    screen.blit(render_tiempo, (WIDTH - 225, 0))  # Mostrar en la esquina superior derecha

# Bucle principal
running = True
ultimo_tiempo = time.time()

while running:
    # Calcular el tiempo transcurrido para actualizar el temporizador
    tiempo_actual = time.time()
    delta_tiempo = tiempo_actual - ultimo_tiempo
    ultimo_tiempo = tiempo_actual
    tiempo_restante -= delta_tiempo

    if tiempo_restante <= 0:
        tiempo_restante = TIEMPO_INICIAL  # Reiniciar el temporizador

    # Dibujar el fondo y el tablero
    screen.fill((0, 0, 0))
    screen.blit(tablero_image, tablero_rect.topleft)

    # Dibujar las fichas en las posiciones correctas
    apuestas = leer_apuestas()
    for opcion, cantidad in apuestas:
        pos_x, pos_y = obtener_posicion_ficha(opcion)
        screen.blit(ficha_image, (pos_x, pos_y))

    # Mostrar el tiempo restante en pantalla
    mostrar_tiempo_restante(int(tiempo_restante))

    # Actualizar la pantalla
    pygame.display.flip()

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
