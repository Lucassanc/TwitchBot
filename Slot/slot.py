import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Tragamonedas")

slot_image = pygame.image.load("Slot/slot.png")
symbols = ["Slot/cereza.png", "Slot/uva.png", "Slot/sandia.png", "Slot/campana.png", "Slot/bar.png", "Slot/siete.png", "Slot/diamante.png"]
symbol_images = [pygame.image.load(sym) for sym in symbols]
symbol_dict = dict(zip(symbol_images, symbols))

symbol_probabilities = [0.4, 0.15, 0.15, 0.1, 0.09, 0.09, 0.02]

slot_sound = pygame.mixer.Sound("Slot/slot.mp3")
slot_sound.set_volume(0.1)

def select_symbol():
    return random.choices(symbol_images, weights=symbol_probabilities, k=3)

def display_symbols(symbols_to_display):
    screen.fill((0, 0, 0))
    screen.blit(slot_image, (0, 0))

    for i, symbol in enumerate(symbols_to_display):
        screen.blit(symbol, (165 * i + 90, 130))
    pygame.display.flip()

running = True
slot_sound.play()
result = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for _ in range(40):
        symbols_displayed = select_symbol()
        display_symbols(symbols_displayed)
        pygame.time.wait(100)

    if symbols_displayed[0] == symbols_displayed[1] == symbols_displayed[2]:
        print("¡Ganaste!")
        result = ("Ganaste", symbols_displayed)
    else:
        print("Perdiste.")
        result = ("Perdiste", symbols_displayed)

    with open("Slot/resultado_slot.txt", "w") as f:
        f.write(f"{result[0]}\n")
        simbolos_nombres = [symbol_dict[sym] for sym in result[1]]
        f.write(f"Simbolos: {', '.join(simbolos_nombres)}\n")

    time.sleep(2)
    running = False

pygame.quit()
