import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Inicialización del mezclador de sonido
pygame.mixer.init()

# Cargar el efecto de sonido
sonido_giro = pygame.mixer.Sound("Ruleta/ruleta.mp3")
sonido_giro.set_volume(0.5)

# Dimensiones de la pantalla
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Ruleta de Casino")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cargar la imagen de la ruleta con fondo transparente
ruleta_image = pygame.image.load("Ruleta/ruleta.png")  # Asegúrate de que el archivo esté en la misma carpeta
ruleta_image.set_colorkey((0, 0, 0))  # Ajusta el color clave para hacer el fondo transparente
ruleta_image = pygame.transform.scale(ruleta_image, (500, 500))  # Cambia el tamaño si es necesario
center = (WIDTH // 2, HEIGHT // 2)

# Números de la ruleta y colores asociados
NUMBERS = {
    0: (0, 128, 0),
    28: (0, 0, 0), 9: (255, 0, 0), 26: (0, 0, 0), 30: (255, 0, 0),
    11: (0, 0, 0), 7: (255, 0, 0), 20: (0, 0, 0), 32: (255, 0, 0),
    17: (0, 0, 0), 5: (255, 0, 0), 22: (0, 0, 0),  34: (255, 0, 0),
    15: (0, 0, 0), 3: (255, 0, 0), 24: (0, 0, 0), 36: (255, 0, 0),
    13: (0, 0, 0), 1: (255, 0, 0), 00: (0, 128, 0), 27: (255, 0, 0),
    10: (0, 0, 0), 25: (255, 0, 0), 29: (0, 0, 0), 12: (255, 0, 0),
    8: (0, 0, 0), 19: (255, 0, 0), 31: (0, 0, 0), 18: (255, 0, 0),
    6: (0, 0, 0), 21: (255, 0, 0), 33: (0, 0, 0), 16: (255, 0, 0),
    4: (0, 0, 0), 23: (255, 0, 0), 35: (0, 0, 0), 14: (255, 0, 0),
    2: (0, 0, 0)
}

# Variables de la ruleta
n_numbers = len(NUMBERS)  # Números de 0 a 36
angle_offset = 360 / n_numbers

# Configuración de la fuente
font = pygame.font.Font(None, 36)

# Variables para controlar el giro
giro_en_curso = True  # Iniciar automáticamente el giro
angle_ruleta = random.randint(0, 360)  # Posición inicial aleatoria para la ruleta
bola_angle = random.randint(0, 360)  # Ángulo de la bola
bola_speed = 5  # Velocidad de la bola
giro_duracion = 6500  # Duración fija del giro en milisegundos (8 segundos)
start_time = pygame.time.get_ticks()  # Obtener el tiempo actual
final_bola_angle = 0  # Inicializa final_angle para evitar el NameError

# Desfase de corrección
desfase_correccion = 100

# Variables para mostrar el resultado
resultado_visible = False
resultado_color = BLACK
numero_ganador = None

# Reproduce el sonido al iniciar el giro
sonido_giro.play()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar pantalla
    screen.fill((0, 0, 0, 0))

    # Rotar la imagen de la ruleta
    rotated_image = pygame.transform.rotate(ruleta_image, angle_ruleta)
    rotated_rect = rotated_image.get_rect(center=center)
    screen.blit(rotated_image, rotated_rect.topleft)

    # Realizar el giro
    if giro_en_curso:
        angle_ruleta -= 10  # Controlar la velocidad del giro

        # Gira la bola en sentido contrario
        bola_angle += bola_speed * (pygame.time.get_ticks() - start_time) / 1000  # Gira en el tiempo actual

        # Comprobar si ha pasado el tiempo de giro
        if pygame.time.get_ticks() - start_time >= giro_duracion:
            giro_en_curso = False
            
            # Calcular el número en el que cayó la bola
            final_bola_angle = bola_angle % 360  # Asegura que el ángulo esté en el rango [0, 360]

            # Ajustar el cálculo del número ganador
            resultado = int((final_bola_angle + angle_ruleta + desfase_correccion) % 360 // angle_offset) % n_numbers
            numero_ganador = list(NUMBERS.keys())[resultado]  # Obtener el número ganador
            resultado_color = NUMBERS[numero_ganador]  # Obtener el color ganador
            
            # Guardar el resultado en el archivo ganadores.txt
            with open("Ruleta/ganadores.txt", "a") as f:
                color_nombre = "Verde" if resultado_color == (0, 128, 0) else "Rojo" if resultado_color == (255, 0, 0) else "Negro"
                f.write(f"{numero_ganador}, {color_nombre},\n")
            
            # Mostrar el resultado durante 2 segundos
            resultado_visible = True
            start_time_resultado = pygame.time.get_ticks()

            # Dibuja la bola en la posición final
            bola_angle = final_bola_angle  # Actualiza el ángulo de la bola a la posición final
        else:
            # Dibujar la bola durante el giro
            distance_from_center = 180  # Ajusta este valor según lo que necesites
            bola_x = center[0] + distance_from_center * math.cos(math.radians(bola_angle))
            bola_y = center[1] + distance_from_center * math.sin(math.radians(bola_angle))
            pygame.draw.circle(screen, WHITE, (int(bola_x), int(bola_y)), 10)

    # Si la ruleta ha terminado de girar, dibujar la bola en la posición final
    if not giro_en_curso:
        distance_from_center = 180  # Ajusta este valor según lo que necesites
        bola_x = center[0] + distance_from_center * math.cos(math.radians(bola_angle))
        bola_y = center[1] + distance_from_center * math.sin(math.radians(bola_angle))
        pygame.draw.circle(screen, WHITE, (int(bola_x), int(bola_y)), 10)

    # Mostrar el resultado en un cuadro pequeño
    if resultado_visible:
        current_time = pygame.time.get_ticks()
        if current_time - start_time_resultado <= 2000:  # Mostrar por 2 segundos
            # Dibuja un cuadrado con el color del número ganador
            pygame.draw.rect(screen, resultado_color, (center[0] - 30, center[1] - 20, 60, 40))
            # Renderiza el texto del número ganador
            text = font.render(str(numero_ganador), True, WHITE)
            screen.blit(text, (center[0] - text.get_width() // 2, center[1] - text.get_height() // 2))
        else:
            resultado_visible = False  # Oculta el resultado después de 2 segundos
            running = False  # Cerrar el programa después de mostrar el resultado

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
