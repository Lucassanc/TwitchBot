import pygame
import time
import requests
from io import BytesIO

pygame.init()
pygame.mixer.init()

apuestas_file = 'Ruleta/apuestas.txt'
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Tablero Ruleta")

tablero_image = pygame.image.load("Ruleta/tableroruleta.png")
tablero_rect = tablero_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Cargar la imagen de la ficha original
ficha_image_original = pygame.image.load("Ruleta/ficha.png")
ficha_image_original = pygame.transform.scale(ficha_image_original, (15, 15))

TIEMPO_INICIAL = 2 * 60
tiempo_restante = TIEMPO_INICIAL
fuente_tiempo = pygame.font.SysFont(None, 30)

def leer_apuestas():
    apuestas = []
    with open(apuestas_file, "r") as file:
        for line in file:
            jugador, cantidad, numero, foto_perfil = line.strip().split(",")
            apuestas.append((numero.strip(), int(cantidad), foto_perfil.strip()))  
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
        '13': (160, 105),
        '14': (160, 70),
        '15': (160, 35),
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
    screen.blit(render_tiempo, (WIDTH - 225, 0))

def cargar_imagen_perfil(codigo):
    if codigo.lower() == "none":
        return None  # Si no hay foto de perfil, retornar None
    url = f"https://static-cdn.jtvnw.net/jtv_user_pictures/{codigo}"
    response = requests.get(url)
    if response.status_code == 200:
        image = pygame.image.load(BytesIO(response.content)).convert_alpha()
        return redondear_imagen(image)
    return None

def redondear_imagen(imagen):
    # Crear una nueva superficie circular
    ancho, alto = imagen.get_size()
    circle_surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (255, 255, 255), (ancho // 2, alto // 2), ancho // 2)
    
    # Combinar la imagen con la superficie circular
    circle_surface.blit(imagen, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return pygame.transform.scale(circle_surface, (15, 15))  # Redimensionar a 15x15

running = True
ultimo_tiempo = time.time()

while running:
    tiempo_actual = time.time()
    delta_tiempo = tiempo_actual - ultimo_tiempo
    ultimo_tiempo = tiempo_actual
    tiempo_restante -= delta_tiempo

    if tiempo_restante <= 0:
        mostrar_tiempo_restante(0)
        pygame.display.flip()
        pygame.time.wait(8000)
        tiempo_restante = TIEMPO_INICIAL
        ultimo_tiempo = time.time()

    screen.fill((0, 0, 0))
    screen.blit(tablero_image, tablero_rect.topleft)

    apuestas = leer_apuestas()
    for opcion, cantidad, codigo_imagen in apuestas:
        pos_x, pos_y = obtener_posicion_ficha(opcion)
        ficha_image = cargar_imagen_perfil(codigo_imagen)

        # Usar la imagen de ficha original si no se cargó una imagen de perfil
        if ficha_image is None:
            ficha_image = ficha_image_original
            
        screen.blit(ficha_image, (pos_x, pos_y))

    mostrar_tiempo_restante(int(tiempo_restante))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
