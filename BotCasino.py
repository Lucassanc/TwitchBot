from twitchio.ext import commands
import random
import subprocess
import pygame

fichas_file = 'FichasCasino.txt'

pygame.init()
pygame.mixer.init()

def obtener_fichas(user, fichas_file):
    with open(fichas_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        name, fichas = line.strip().split()
        if name.lower() == user.lower():
            return int(fichas)
    
    return None

def actualizar_fichas(usuario, nuevas_fichas, fichas_file):
    nuevas_fichas = round(nuevas_fichas)
    with open(fichas_file, 'r') as file:
        lines = file.readlines()

    with open(fichas_file, 'w') as file:
        for line in lines:
            name, fichas = line.strip().split()
            if name.lower() == usuario.lower():
                file.write(f"{name} {nuevas_fichas}\n")
            else:
                file.write(line)

CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
ACCESS_TOKEN = 'r9p9tth3uzwl9sj9u8s3q91asx0ybw'

bot = commands.Bot(
    irc_token = f'oauth:{ACCESS_TOKEN}',
    client_id = CLIENT_ID,
    nick = 'soymerlu',
    prefix = '!',
    initial_channels = ['soymerlu'],
)

cosas = [ "oso de peluche", "reloj", "oro", "caca", "carbon", "waifu", "la novia de cesur", "la mama de santi", "masitas", "nada", "lentes", "boleto dorado a la fabrica", "vandal", "celular", "nariz michael jackson", "manos de peron", "ganas de vivir", "nft", "bitcoin", "mate", "droga", "las piernas de maradona", "rei chiquita", "una novia", "un abrazo", "descuento en penes de goma", "jamon crudo", "papas fritas", "un ventilador liliana", "un cafecito de Moni Argento", "una gorreada", "la locura impredecible de Jinx", "a Batman", "muñeco inflable de Henry Cavill", "cabeza de Exodia", "brazo derecho de Exodia", "brazo izquierdo de Exodia", "pierna derecha de Exodia", "pierna izquierda de Exodia", "dragon de ojos azules", "la esfera del dragon 1", "la esfera del dragon 2", "la esfera del dragon 3", "la esfera del dragon 4", "la esfera del dragon 5", "la esfera del dragon 6", "la esfera del dragon 7", "las Islas Malvinas", "la tortuga de Buscando a Nemo", "a Calamardo", "una pata de palo", "1kg de helado de Cesur", "un depto en New York", "un depto en Once", "un Martin Fierro", "una pata de conejo", "un conejo sin una pata", "a Pepinillo Rick", "un alfajor de Malphite", "un Dementor", "un Demogorgon", "a Charmander", "a Bulbasaur", "a Squirtle", "la Copa del Mundial", "un gorrito de Eve", "un insulto de Eve", "un insulto de Cesur", "un timeout de 60s", "una loli", "una estrella para Boca", "un vino en carton", "una cumbiancha", "25g de merca", "un porrito",  "un mouse gaming", "un teclado mecanico", "un ban por 15 minutos", "una trompada", "un bife con papas", "el amor de tus padres", "una foto teta", "una nude", "una lofi girl estudiosa", "un objeto que no era pastel", "un pastel que no era objeto", "una referencia de Jojo", "una pc gamer", "una bolinet", "la tercera ☆☆☆", "una pala", "un follow en Instagram", "un follow en Twitter", "un follow en Twitch", "un gato", "un perro", "un game de lol conmigo", "un game de valorant conmigo", "un game de cs conmigo", "un game del juego que quieras conmigo", "un sombrero vaquero", "una cita con bts", "una rtx 4090", "una billetera vacia", "una billetera con plata", "una latita de coca", "1 dolar", "una enfermedad terminal", "la cura de una enfermedad terminal", "a Messi Chiquito", "una Pizza con Piña", "una Empanada de Carne Con Pasas", "la Empanada de tu Vieja", "el Choripan de tu Viejo", "un Sugar Daddy", "una Sugar Mommy", "un Beso", 'la Patagonia', 'una Coca Cola', 'un Ibuprofeno', 'el cadaver de la novia', 'un partido de fubol', 'a Messi Chiquito', 'un ticket para ver un video', 'un ticker para ver una peli', 'un viaje a Europa', 'un viaje a Africa', 'un viaje a Japon', 'un viaje a la concha de tu heraman', 'un raid', 'un insulto gratis a Merlu', 'un puchito con coquita', 'un barquito', 'un bombardeo gratis', 'el Monumental', 'la Bombonera', 'el Cilindro de Avellaneda', 'el Libertadores de America', 'un golpe militar', 'un ticket para agregar un item a la maquinita', 'un ticket para chuparme un huevo', 'GTA 6', 'a Elon Musk', 'el pajarito de Twitter', 'a Javier Milei', 'a Ricardo Fort', 'a Luis Miguel', 'un evento canonico', 'un evento no canonico', 'un ticket para mostrar tu talento', 'un ticket para contarme un chiste']
galletitas = ['9 de oro', 'don satur', 'oreo', 'terrabusi', 'surtidas', 'sonrisas', 'diversion', 'pepitos', 'opera', 'macuca', 'club social', 'pitusas', 'rex', 'saladix', 'fauna', 'criollitas', 'coquitas', 'mana', 'rumba', 'formis', 'chocolinas', 'macucas']
numeros = ['1','2','3','4','5','6']
caras = ['cara', 'cruz']
multiplicadores = {
    "cereza": 1.2,
    "uva": 1.5,
    "sandia": 2,
    "campana": 5,
    "bar": 10,
    "siete": 20,
    "diamante": 100
}

@bot.event
async def event_ready():
    print(f'Tragamonedas listo.')

def leer_fichas():
    fichas = {}
    with open(fichas_file, 'r') as archivo:
        for linea in archivo:
            usuario, cantidad = linea.strip().split()
            fichas[usuario] = int(cantidad)
    return fichas

def guardar_fichas(fichas):
    with open(fichas_file, 'w') as archivo:
        for usuario, cantidad in fichas.items():
            archivo.write(f"{usuario} {cantidad}\n")

def reproducir_audio():
    archivo_audio = "fichas.mp3"
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()

def manejar_recompensa(usuario, cantidad_fichas):
    fichas = leer_fichas()
    if usuario in fichas:
        fichas[usuario] += cantidad_fichas
    else:
        fichas[usuario] = cantidad_fichas
    guardar_fichas(fichas)

@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)

    if "custom-reward-id=01820b0c-0534-4ee5-be70-a2ca7ee3e9f0" in ctx.raw_data:
        reproducir_audio()
        usuario = ctx.author.name
        cantidad_fichas = 1000
        manejar_recompensa(usuario, cantidad_fichas)
        fichas = leer_fichas()
        await ctx.channel.send(f"{usuario}, se han añadido {cantidad_fichas} Merlumonedas a tu cuenta. En total tenes {fichas[usuario]} Merlumonedas.")
    
    if "custom-reward-id=e3c3eab5-e7c9-4cb0-a6d8-0ffcdfbd956e" in ctx.raw_data:
        reproducir_audio()
        usuario = ctx.author.name
        cantidad_fichas = 5000
        manejar_recompensa(usuario, cantidad_fichas)
        fichas = leer_fichas()
        await ctx.channel.send(f"{usuario}, se han añadido {cantidad_fichas} Merlumonedas a tu cuenta. En total tenes {fichas[usuario]} Merlumonedas.")
    
    if "custom-reward-id=8c359347-df98-452c-ae0b-d7001dd7a779" in ctx.raw_data:
        reproducir_audio()
        usuario = ctx.author.name
        cantidad_fichas = 10000
        manejar_recompensa(usuario, cantidad_fichas)
        fichas = leer_fichas()
        await ctx.channel.send(f"{usuario}, se han añadido {cantidad_fichas} Merlumonedas a tu cuenta. En total tenes {fichas[usuario]} Merlumonedas.")

    if "custom-reward-id=5e12af84-bd3c-4c6a-b63a-93b95017ecfe" in ctx.raw_data:
        reproducir_audio()
        usuario = ctx.author.name
        cantidad_fichas = 50000
        manejar_recompensa(usuario, cantidad_fichas)
        fichas = leer_fichas()
        await ctx.channel.send(f"{usuario}, se han añadido {cantidad_fichas} Merlumonedas a tu cuenta. En total tenes {fichas[usuario]} Merlumonedas.")

@bot.command(name='merlumonedas')
async def merlumonedas(ctx):
    fichas = leer_fichas()
    await ctx.send(f'{ctx.author.name} tenes: {fichas[ctx.author.name]} Merlumonedas.')

@bot.command(name='maquinita')
async def maquinita(ctx):
    cantidad = 1000
    user = ctx.author.name
    fichas_file = 'FichasCasino.txt'

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    if cantidad > user_fichas:
        await ctx.send("No tienes suficientes fichas para apostar.")
        return
    
    user_fichas -= cantidad
    actualizar_fichas(user, user_fichas, fichas_file)

    await ctx.send(f'{ctx.author.name} a sacado {random.choice(cosas)}')

@bot.command(name='galletita')
async def galletita(ctx):
    cantidad = 1000
    user = ctx.author.name
    fichas_file = 'FichasCasino.txt'

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    if cantidad > user_fichas:
        await ctx.send("No tienes suficientes fichas para apostar.")
        return
    
    user_fichas -= cantidad
    actualizar_fichas(user, user_fichas, fichas_file)
    await ctx.send(f'{ctx.author.name} es un paquete de {random.choice(galletitas)}')


@bot.command(name='rusa')
async def comandos(ctx):

    cantidad = 1000
    user = ctx.author.name
    fichas_file = 'FichasCasino.txt'

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    if cantidad > user_fichas:
        await ctx.send("No tienes suficientes fichas para apostar.")
        return
    
    bala = random.choice(numeros)
    if bala == '3':
        user_fichas = 0
        await ctx.send(f'Perdiste todas tus fichas')
    else:
        user_fichas += user_fichas
        await ctx.send(f'Duplicaste tus monedas')

    actualizar_fichas(user, user_fichas, fichas_file)

@bot.command(name='moneda')
async def moneda(ctx):

    cantidad = 1000
    user = ctx.author.name
    fichas_file = 'FichasCasino.txt'

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    if cantidad > user_fichas:
        await ctx.send("No tienes suficientes fichas para apostar.")
        return
    
    cara = random.choice(caras)
    if cara == 'cara':
        user_fichas -= 1000
        await ctx.send(f'Salio Cara, Perdiste 1000 fichas')
    else:
        user_fichas += 1000
        await ctx.send(f'Salio Cruz, Ganaste 1000 fichas')

    actualizar_fichas(user, user_fichas, fichas_file)

@bot.command(name='tragamonedas')
async def tragamonedas(ctx):
    user = ctx.author.name
    fichas_file = 'FichasCasino.txt'
    user_fichas = obtener_fichas(user, fichas_file)
    
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    cantidad = 1000
    
    if user_fichas < cantidad:
        await ctx.send("No tienes suficientes fichas para jugar en la tragamonedas.")
        return

    user_fichas -= cantidad

    await ctx.send("Girando el tragamonedas...")
    subprocess.run(['python', 'Slot\\slot.py'])

    resultado_file = 'Slot/resultado_slot.txt'
    with open(resultado_file, 'r') as file:
        lines = file.readlines()

    resultado = lines[0].strip()
    simbolos_linea = lines[1].strip()

    simbolos = simbolos_linea.replace('Simbolos: ', '').split(', ')

    if simbolos[0] == simbolos[1] == simbolos[2]:
        simbolo_ganador = simbolos[0].split('/')[-1].replace('.png', '')

        ganancia = cantidad * multiplicadores.get(simbolo_ganador, 1)

        user_fichas += ganancia
        await ctx.send(f"¡Felicidades {user}! Ganaste {ganancia} fichas. Simbolo ganador: {simbolo_ganador}.")
    else:
        simbolo1 = simbolos[0].split('/')[-1].replace('.png', '')
        simbolo2 = simbolos[1].split('/')[-1].replace('.png', '')
        simbolo3 = simbolos[2].split('/')[-1].replace('.png', '')
        await ctx.send(f"Lo siento {user}, perdiste {cantidad} fichas. Resultado: {simbolo1}, {simbolo2}, {simbolo3}")


    actualizar_fichas(user, user_fichas, fichas_file)

bot.run()