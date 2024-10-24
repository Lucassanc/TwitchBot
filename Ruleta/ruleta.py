import pygame
import random
import math

pygame.init()

pygame.mixer.init()

sonido_giro = pygame.mixer.Sound("Ruleta/ruleta.mp3")
sonido_giro.set_volume(0.5)

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Ruleta de Casino")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ruleta_image = pygame.image.load("Ruleta/ruleta.png")
ruleta_image.set_colorkey((0, 0, 0))
ruleta_image = pygame.transform.scale(ruleta_image, (500, 500))
center = (WIDTH // 2, HEIGHT // 2)

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

n_numbers = len(NUMBERS)
angle_offset = 360 / n_numbers

font = pygame.font.Font(None, 36)

giro_en_curso = True
angle_ruleta = random.randint(0, 360)
bola_angle = random.randint(0, 360)
bola_speed = 5
giro_duracion = 6500
start_time = pygame.time.get_ticks()
final_bola_angle = 0

desfase_correccion = 100

resultado_visible = False
resultado_color = BLACK
numero_ganador = None

sonido_giro.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0, 0))

    rotated_image = pygame.transform.rotate(ruleta_image, angle_ruleta)
    rotated_rect = rotated_image.get_rect(center=center)
    screen.blit(rotated_image, rotated_rect.topleft)

    if giro_en_curso:
        angle_ruleta -= 10

        bola_angle += bola_speed * (pygame.time.get_ticks() - start_time) / 1000

        if pygame.time.get_ticks() - start_time >= giro_duracion:
            giro_en_curso = False
            
            final_bola_angle = bola_angle % 360

            resultado = int((final_bola_angle + angle_ruleta + desfase_correccion) % 360 // angle_offset) % n_numbers
            numero_ganador = list(NUMBERS.keys())[resultado]
            resultado_color = NUMBERS[numero_ganador]

            with open("Ruleta/ganadores.txt", "a") as f:
                color_nombre = "Verde" if resultado_color == (0, 128, 0) else "Rojo" if resultado_color == (255, 0, 0) else "Negro"
                f.write(f"{numero_ganador}, {color_nombre},\n")

            resultado_visible = True
            start_time_resultado = pygame.time.get_ticks()

            bola_angle = final_bola_angle
        else:
            distance_from_center = 180
            bola_x = center[0] + distance_from_center * math.cos(math.radians(bola_angle))
            bola_y = center[1] + distance_from_center * math.sin(math.radians(bola_angle))
            pygame.draw.circle(screen, WHITE, (int(bola_x), int(bola_y)), 10)

    if not giro_en_curso:
        distance_from_center = 180
        bola_x = center[0] + distance_from_center * math.cos(math.radians(bola_angle))
        bola_y = center[1] + distance_from_center * math.sin(math.radians(bola_angle))
        pygame.draw.circle(screen, WHITE, (int(bola_x), int(bola_y)), 10)


    if resultado_visible:
        current_time = pygame.time.get_ticks()
        if current_time - start_time_resultado <= 2000:
            pygame.draw.rect(screen, resultado_color, (center[0] - 30, center[1] - 20, 60, 40))
            text = font.render(str(numero_ganador), True, WHITE)
            screen.blit(text, (center[0] - text.get_width() // 2, center[1] - text.get_height() // 2))
        else:
            resultado_visible = False
            running = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
