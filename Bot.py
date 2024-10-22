from twitchio.ext import commands
import random
import json
import subprocess
import asyncio
import os
import pygame

pygame.mixer.init()

apuestas_file = 'Ruleta/apuestas.txt'
fichas_file = 'FichasCasino.txt'
ganadores_file = 'Ruleta/ganadores.txt'

async def procesar_apuestas():
    if not os.path.exists(apuestas_file) or os.stat(apuestas_file).st_size == 0:
        return
    await bot._ws.send_privmsg('SoyMerlu', "Se cierran las apuestas, Girando la ruleta...")
    subprocess.run(['python', 'Ruleta\\ruleta.py'])


    with open(ganadores_file, 'r') as file:
        last_line = file.readlines()[-1].strip()
        parts = last_line.split(',')
        if len(parts) < 2:
            await bot._ws.send_privmsg('SoyMerlu', "Formato de ganador inválido.")
            return
        numero = parts[0].strip()
        color = parts[1].strip()

    await bot._ws.send_privmsg('tu_canal', f"El número ganador es: {numero} y el color ganador es: {color}.")

    with open(apuestas_file, 'r') as file:
        apuestas = file.readlines()

    for apuesta in apuestas:
        user, cantidad_str, tipo_apuesta = apuesta.strip().split(',')
        cantidad = int(cantidad_str)

        user_fichas = obtener_fichas(user, fichas_file)
        if user_fichas is None:
            await bot._ws.send_privmsg('SoyMerlu', f"Usuario {user} no encontrado en el archivo de fichas.")
            continue

        if tipo_apuesta.isdigit() and int(tipo_apuesta) in range(37):
            if numero == tipo_apuesta:
                ganancia = cantidad * 36
                user_fichas += ganancia
                await bot._ws.send_privmsg('SoyMerlu', f"¡Felicidades {user}! Ganaste {ganancia} fichas apostando al número {tipo_apuesta}.")
            else:
                await bot._ws.send_privmsg('SoyMerlu', f"Lo siento {user}, perdiste {cantidad} fichas apostando al número {tipo_apuesta}.")
        elif tipo_apuesta.lower() in ["rojo", "negro"]:
            if color.lower() == tipo_apuesta:
                ganancia = cantidad * 2
                user_fichas += ganancia
                await bot._ws.send_privmsg('SoyMerlu', f"¡Felicidades {user}! Ganaste {ganancia} fichas apostando al color {tipo_apuesta}.")
            else:
                await bot._ws.send_privmsg('SoyMerlu', f"Lo siento {user}, perdiste {cantidad} fichas apostando al color {tipo_apuesta}.")

        actualizar_fichas(user, user_fichas, fichas_file)

    with open(apuestas_file, 'w') as file:
        file.write("")

async def girar_ruleta_periodicamente():
    while True:
        await asyncio.sleep(120)
        await procesar_apuestas()
        
def reproducir_audio():
    archivo_audio = "fichas.mp3"
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()

def guardar_apuesta(user, cantidad, apuesta):
    with open(apuestas_file, 'a') as file:
        file.write(f"{user},{cantidad},{apuesta}\n")

def leer_ganadores(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    numeros = []
    colores = []
    
    for linea in lineas:
        linea = linea.strip().rstrip(',')
        partes = [parte.strip() for parte in linea.split(',') if parte.strip()]
        
        if len(partes) == 2:
            try:
                numero = int(partes[0])
                color = partes[1]
                numeros.append(numero)
                colores.append(color)
            except ValueError:
                continue
        else:
            continue
    
    return numeros, colores

def calcular_estadisticas(colores):
    total = len(colores)
    conteo_colores = {}

    for color in colores:
        if color in conteo_colores:
            conteo_colores[color] += 1
        else:
            conteo_colores[color] = 1
    
    porcentajes = {color: (count / total) * 100 for color, count in conteo_colores.items()}
    return porcentajes

def mostrar_ultimos_numeros(numeros, colores, n=10):
    return list(zip(numeros[-n:], colores[-n:]))

def obtener_estadisticas():
    archivo = 'Ruleta/ganadores.txt'
    try:
        numeros, colores = leer_ganadores(archivo)
        
        if not numeros or not colores:
            return "No hay ganadores registrados o el archivo está vacío."
        
        porcentajes = calcular_estadisticas(colores)
        mensaje = "Porcentaje de colores:\n"
        for color, porcentaje in porcentajes.items():
            mensaje += f"{color}: {porcentaje:.2f}%\n"
        
        ultimos_numeros = mostrar_ultimos_numeros(numeros, colores)
        mensaje += "\nÚltimos 10 números:\n"
        for numero in ultimos_numeros:
            mensaje += f"{numero}\n"
        
        ultimo_numero = numeros[-1]
        ultimo_color = colores[-1]
        mensaje += f"\nÚltimo ganador: Número {ultimo_numero}, Color {ultimo_color}"
        
        return mensaje
    
    except FileNotFoundError:
        return f"El archivo '{archivo}' no fue encontrado. Asegúrate de que esté en la ubicación correcta."
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

def leer_fichas():
    fichas = {}
    with open(RUTA_ARCHIVO, 'r') as archivo:
        for linea in archivo:
            usuario, cantidad = linea.strip().split()
            fichas[usuario] = int(cantidad)
    return fichas

def guardar_fichas(fichas):
    with open(RUTA_ARCHIVO, 'w') as archivo:
        for usuario, cantidad in fichas.items():
            archivo.write(f"{usuario} {cantidad}\n")

def manejar_recompensa(usuario, cantidad_fichas):
    fichas = leer_fichas()
    if usuario in fichas:
        fichas[usuario] += cantidad_fichas
        print(f"Se sumaron {cantidad_fichas} fichas a {usuario}. Total: {fichas[usuario]}")
    else:
        fichas[usuario] = cantidad_fichas
        print(f"Se creó el usuario {usuario} con {cantidad_fichas} Merlumonedas.")
    guardar_fichas(fichas)

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

BROADCASTER_ID = '153299663'
CLIENT_ID = 'xz9qt95r34bwb2kel4fkm7fuhwvppw'
TOKEN= 'bgndnm67gp1m8czmq8i01jcxhoajyj'
CLIENT_SECRET = 'exlnw27fjmubuj0zggaix3tv1zqjqv'

bot = commands.Bot(
    irc_token = 'oauth:77vdufk8u5z2dehk0a1dhqi8c2v8in',
    client_id = 'xz9qt95r34bwb2kel4fkm7fuhwvppw',
    nick = 'soymerlu',
    prefix = '!',
    initial_channels = ['soymerlu'],
)

cosas = [ "oso de peluche", "reloj", "oro", "caca", "carbon", "waifu", "la novia de cesur", "la mama de santi", "masitas", "nada", "lentes", "boleto dorado a la fabrica", "vandal", "celular", "nariz michael jackson", "manos de peron", "ganas de vivir", "nft", "bitcoin", "mate", "droga", "las piernas de maradona", "rei chiquita", "una novia", "un abrazo", "descuento en penes de goma", "jamon crudo", "papas fritas", "un ventilador liliana", "un cafecito de Moni Argento", "una gorreada", "la locura impredecible de Jinx", "a Batman", "muñeco inflable de Henry Cavill", "cabeza de Exodia", "brazo derecho de Exodia", "brazo izquierdo de Exodia", "pierna derecha de Exodia", "pierna izquierda de Exodia", "dragon de ojos azules", "la esfera del dragon 1", "la esfera del dragon 2", "la esfera del dragon 3", "la esfera del dragon 4", "la esfera del dragon 5", "la esfera del dragon 6", "la esfera del dragon 7", "las Islas Malvinas", "la tortuga de Buscando a Nemo", "a Calamardo", "una pata de palo", "1kg de helado de Cesur", "un depto en New York", "un depto en Once", "un Martin Fierro", "una pata de conejo", "un conejo sin una pata", "a Pepinillo Rick", "un alfajor de Malphite", "un Dementor", "un Demogorgon", "a Charmander", "a Bulbasaur", "a Squirtle", "la Copa del Mundial", "un gorrito de Eve", "un insulto de Eve", "un insulto de Cesur", "un timeout de 60s", "una loli", "una estrella para Boca", "un vino en carton", "una cumbiancha", "25g de merca", "un porrito",  "un mouse gaming", "un teclado mecanico", "un ban por 15 minutos", "una trompada", "un bife con papas", "el amor de tus padres", "una foto teta", "una nude", "una lofi girl estudiosa", "un objeto que no era pastel", "un pastel que no era objeto", "una referencia de Jojo", "una pc gamer", "una bolinet", "la tercera ☆☆☆", "una pala", "un follow en Instagram", "un follow en Twitter", "un follow en Twitch", "un gato", "un perro", "un game de lol conmigo", "un game de valorant conmigo", "un game de cs conmigo", "un game del juego que quieras conmigo", "un sombrero vaquero", "una cita con bts", "una rtx 4090", "una billetera vacia", "una billetera con plata", "una latita de coca", "1 dolar", "una enfermedad terminal", "la cura de una enfermedad terminal", "a Messi Chiquito", "una Pizza con Piña", "una Empanada de Carne Con Pasas", "la Empanada de tu Vieja", "el Choripan de tu Viejo", "un Sugar Daddy", "una Sugar Mommy", "un Beso", 'la Patagonia', 'una Coca Cola', 'un Ibuprofeno', 'el cadaver de la novia', 'un partido de fubol', 'a Messi Chiquito', 'un ticket para ver un video', 'un ticker para ver una peli', 'un viaje a Europa', 'un viaje a Africa', 'un viaje a Japon', 'un viaje a la concha de tu heraman', 'un raid', 'un insulto gratis a Merlu', 'un puchito con coquita', 'un barquito', 'un bombardeo gratis', 'el Monumental', 'la Bombonera', 'el Cilindro de Avellaneda', 'el Libertadores de America', 'un golpe militar', 'un ticket para agregar un item a la maquinita', 'un ticket para chuparme un huevo', 'GTA 6', 'a Elon Musk', 'el pajarito de Twitter', 'a Javier Milei', 'a Ricardo Fort', 'a Luis Miguel', 'un evento canonico', 'un evento no canonico', 'un ticket para mostrar tu talento', 'un ticket para contarme un chiste']
palabra = ['parada', 'dormida']
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

RUTA_ARCHIVO = 'FichasCasino.txt'
RECOMPENSA_OBJETIVO = 'Cargar Casino'

@bot.event
async def event_ready():
    bot.loop.create_task(girar_ruleta_periodicamente())
    print(f'{bot.nick} está listo para girar la ruleta.')
    print('Estamos listos')

@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)

    print(ctx.raw_data)

    if 'hola' in ctx.content.lower():
        await ctx.channel.send(f'Hola {ctx.author.name}, gracias por pasarte por el directo bienvenid@ 🎉')

    if 'todas' == ctx.content.lower():
         await ctx.channel.send(f'PUTAS')

    if 'todos' == ctx.content.lower():
         await ctx.channel.send(f'FACHA EZWink')

    if 'terere' in ctx.content.lower():
        await ctx.channel.send(f'{ctx.author.name} Terere? Sos trolo?')

    if 'masitas' in ctx.content.lower():
        await ctx.channel.send(f'{ctx.author.name} Se dice GA LLE TI TAS')

    if 'ahi lo tenes' in ctx.content.lower():
        await ctx.channel.send(f'Al pelotudo')

    if 'pedilo' in ctx.content.lower():
        await ctx.channel.send(f'⠀⠀⢸⡿⠿⣷⡄⣿⠿⠿⠟⢰⣿⠿⢷⣆⢰⡇⢰⡇⠀⠀⠀⣴⠿⠷⣦⠀⠀⠀ ⠀⠀⢸⣧⣤⡿⠃⣿⡶⠶⠆⢸⣿⠀⠀⣿⢸⡇⢸⡇⠀⠀⢸⡏⠀⠀⣿⡇⠀⠀ ⠀⠀⢸⡇⠀⠀⠀⣿⣤⣤⣤⢸⣿⣤⣴⠟⢸⡇⢸⣧⣤⣤⠈⢿⣤⣴⡿⠁')
    
    if 'en la primera' in ctx.content.lower():
        await ctx.channel.send(f'En la primera Era, en la primera batalla, la primera vez que las sombras se alargaron, alguien resistió. Consumido por las ascuas del armagedón. Su alma ardió en los fuegos del infierno y, demasiado corrupto para la ascensión, escogió la senda del tormento perpetuo, No halló la paz en su voraz odio y, con su sangre hirviendo,')
        await ctx.channel.send(f'recorrio las llanuras del Umbral para vengarse de los señores oscuros que tanto daño le hicieron. Portaba la corona de los Centinelas de la noche. Y los que probaron su espada le llamaron...Asesino de la Muerte.')

    if 'crazy?' in ctx.content.lower():
        await ctx.channel.send(f'Crazy? I Was Crazy Once. They Locked Me In A Room. A Rubber Room. A Rubber Room With Rats. And Rats Make Me Crazy.')
    
    if 'es confuso verdad?' in ctx.content.lower():
        await ctx.channel.send(f'sin embargo sabes perfectamente cuando estás mal, todo tu cuerpo física y mentalmente te lo hace saber, te notas flojo con pensamientos fatalistas esa sensación que todo está perdido, qué ya nada será como antes, te torturas recordando una vivencia pasada aleatoria en aquel momento ni siquiera parecía un buen momento pero comparado como te sientes ahora podría incluso decirse que... Fuiste feliz sin saberlo')
    
    if 'belico' in ctx.content.lower():
        await ctx.channel.send(f'BELICO: De la guerra o relacionado con la lucha armada.')

    if 'nashe' in ctx.content.lower():
        await ctx.channel.send(f' ⣿⣧⡈⠙⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢹⠿⣿ ⣿⣿⣿⣷⣶⡀⠿⠿⣿⣿⣿⣿⣿⣿⡇⠐⠂⢒⡢ ⣿⣿⣿⣿⣿⣿⣆⠀⠈⢻⣿⣿⣿⣿⣿⡆⢈⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠙⠻⢻⢿⣿⠷⢠⢽⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠁⠀⢘⣱⣍⠿⣾⢿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⢉⢷⣌⠳ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠋⠽⠶ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⡀⠀⠀⠀⠐ ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠏⠁⠀⠈⠀⠅⠶⠲.')
    
    if 'ks' in ctx.content.lower():
        await ctx.channel.send(f'Nuestra Kill. ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣀⣀⣀⠀⠻⣷⣄ ⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠋⠀⠀⠀⠹⣿⣦⡀ ⠀⠀⢀⣴⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⠀⢹⣿⣧ ⠀⠀⠙⢿⣿⡿⠋⠻⣿⣿⣦⡀⠀⠀⠀⢸⣿⣿⡆ ⠀⠀⠀⠀⠉⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⢸⣿⣿⡇ ⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠈⠻⣿⣿⣶⣿⣿⣿⠁ ⠀⠀⠀⣠⣿⣿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⡁ ⢠⣶⣿⣿⠋⠀⠀⠉⠛⠿⠿⠿⠿⠿⠛⠻⣿⣿⣦⡀ ⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿')

    if 'el mas grande' in ctx.content.lower():
        await ctx.channel.send(f' ⠀⠀⠀⣠⡾⠛⠶⠦⣤⣄⣀⣀⣀⣀⣀⣀⣀⣠⣤⠴⠶⡛⢷⣄⠀⠀⠀ ⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠈⠉⠉⢉⣭⣭⣥⣴⣶⣶⣿⣿⣦⡙⢷⣄⠀ ⣴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠝⣦ ⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⡛⣛⣛⡛⠿⢿⣿⣿⣿⣿⣿⣿⠃⣰⠃ ⠀⢹⡄⠀⠀⠀⠀⠀⢀⣴⡾⠿⡃⣿⡟⣿⡆⣦⡙⢿⣿⣿⣿⠃⢀⡏⠀ ⠀⠘⣷⠀⠀⠀⠀⣰⡿⢋⣴⣿⡇⣿⡇⣿⡇⣿⣿⣆⠹⡿⠁⠀⣼⠃⠀ ⠀⠀⢿⠀⠀⠀⢰⣿⢡⣿⠋⢸⡇⣿⡇⣿⡇⣿⡏⣿⡆⠁⠀⠀⡿⠀⠀ ⠀⠀⢸⡀⠀⠀⢸⣿⢸⣿⠿⢿⡇⣿⡇⣿⡇⣿⡇⣿⡇⠀⠀⠀⡇⠀⠀ ⠀⠀⢸⡇⠀⢠⠈⣿⡜⢿⡆⢸⡇⣿⣷⣿⠇⣿⣷⡿⠁⠀⠀⢸⡇⠀⠀ ⠀⠀⠈⣇⢠⣿⣷⡘⢿⣮⡃⠸⠇⣿⡿⣷⡀⣿⡏⠀⠀⠀⠀⢸⠁⠀⠀ ⠀⠀⠀⢿⠘⣿⣿⣿⣦⣙⠻⠷⡆⣿⡇⠻⠗⠋⠀⠀⠀⠀⠀⡿⠀⠀⠀ ⠀⠀⠀⠸⣧⢹⣿⣿⣿⣿⣷⣶⣶⣤⡶⠂⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀ ⠀⠀⠀⠀⠹⣆⢿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠹⣆⠻⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⣠⠏⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠘⢷⡙⢿⣿⡟⠁⠀⠀⠀⠀⠀⢀⡼⠃⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠛⢦⣍⠀⠀⠀⠀⠀⣀⡴⠛⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⢦⣤⡴⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')

    if 'pecho frio' in ctx.content.lower():
        await ctx.channel.send(f' ⠀⠀⠀⠀⡀⠐⢀⣤⣀⠁⠂⠠⢀⣀⣀⣀⡀⠄⠐⠈⣀⣤⡀⠂⢀⠀⠀⠀⠀ ⠀⢀⠀⠀⣠⣴⣿⣟⣿⣿⣶⣦⣤⣤⣤⣤⣤⣴⣶⣿⣿⣻⣿⣦⣄⠀⠀⡀⠀ ⡌⢀⣤⣿⣫⣿⣟⣿⣟⣻⣿⣻⣿⣛⣿⣛⣿⣟⣿⣟⣻⣿⣻⣿⣝⣿⣤⡈⢡ ⡇⢸⣿⣙⣿⣏⣿⣏⣿⣟⣹⣿⣻⣿⣛⣿⣟⣿⣟⣻⣿⣹⣿⣹⣿⣋⣿⡇⠸ ⠀⠸⣿⣏⣿⣏⣽⣯⣻⣿⣹⣿⣩⣿⣉⣿⣍⣿⣏⣿⣿⣽⣿⣻⣿⣙⣿⠇⠀ ⢀⠀⣿⣿⠟⠉⡉⠙⢿⣿⣏⠉⠉⢹⣿⣟⠉⠉⠉⠻⣿⣿⡏⠉⠉⣿⣿⠀⠀ ⠘⡀⢻⣿⠀⠀⣿⣶⣾⣿⠇⢠⡀⠸⣿⣿⠀⠘⠃⠠⣿⣿⣿⠀⢸⣿⡿⢀⠇ ⠀⠁⠘⣿⡀⠀⠛⠀⣸⡏⠀⢴⣶⠀⠻⡟⠀⠘⠃⢀⣇⠀⠙⠀⣸⣿⠃⠘⠀ ⠀⠘⠀⢻⣿⣿⣿⣿⢿⣿⡿⣿⣿⢿⣿⡿⣿⣿⢿⣿⡿⣿⣿⢿⣿⡟⠀⠃⠀ ⠀⠀⠠⠀⢿⣿⢿⣿⣿⢿⣿⡿⣿⣿⠿⣿⣿⢿⣿⡿⣿⣿⡿⣿⡿⠀⡔⠀⠀ ⠀⠀⠀⢀⠈⢿⣾⡿⣿⣿⢿⣿⣟⣻⣿⣟⣻⣿⡿⣿⣿⢿⣷⡿⠁⡠⠀⠀⠀ ⠀⠀⠀⠀⠂⠈⢿⣿⣟⣿⣿⣟⣿⣿⣿⣿⣿⣻⣿⣿⣻⣿⡿⠁⠐⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠻⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⠟⠀⠔⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⢄⠘⢻⣿⣧⣿⢿⣶⡿⢿⣽⣿⡟⠃⠠⠂⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠁⠄⠘⠻⣿⣿⣛⣿⣿⠟⠃⠠⠈⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠠⠈⠙⠿⠋⢁⠄⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')

    if 'puedo jugar' in ctx.content.lower():
        await ctx.channel.send(f'Merlu solo juega con sus amigos')
    
    if 'warhammer' in ctx.content.lower():
        await ctx.channel.send(f'Warhammer 40k es una franquicia de ciencia ficción y fantasía oscura para adultos o grimdark como suele ser referido, fundada en el año 1987 creada por la compañía británica Games Workshop. Esta inicio como una adaptación de otro gran título de Games Workshop Warhammer Fantasy')

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

@bot.command(name='sorteo')
async def sorteo(ctx):
    await ctx.send(f'{ctx.author.name} no maestro, no se viene sorteo')

@bot.command(name='simp')
async def pajin(ctx):
    await ctx.send(f'Hoy {ctx.author.name} esta un {random.randint(1, 100)}% simp peepoSIMP')

@bot.command(name='pajin')
async def pajin(ctx):
    await ctx.send(f'Hoy {ctx.author.name} esta un {random.randint(1, 100)}% pajin Despairge')

@bot.command(name='facha')
async def facha(ctx):
    await ctx.send(f'Hoy {ctx.author.name} esta un {random.randint(1, 100)}% facha EZWink')

@bot.command(name='tontito')
async def tontito(ctx):
    await ctx.send(f'Hoy {ctx.author.name} está un {random.randint(1, 100)}% tontito Okayge')

@bot.command(name='reembolso')
async def reembolso(ctx):
    await ctx.send(f'No te reembolso una pija, jodete')

@bot.command(name='redes')
async def redes(ctx):
    await ctx.send(f'Ig: instagram.com/merlusoy ¬¬¬¬ Tiktok: tiktok.com/@iammerlu ¬¬¬¬ Twitter: twitter.com/MerLucassc')

@bot.command(name='dc')
async def dc(ctx):
    await ctx.send(f'Entra al server pibardo https://discord.gg/ebqPwPHyDh')

@bot.command(name='memide')
async def memide(ctx):
    await ctx.send(f'A {ctx.author.name} le mide {random.randint(1, 45)}cm {random.choice(palabra)}')

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

@bot.command(name='emotes')
async def emotes(ctx):
    await ctx.send(f'Si no puedes ver FeelsDankMan ni RareParrot y solo ves oalabras es porque no tienes la extensión de 7tv. La puedes descargar desde aquí: https://7tv.app AYAYA')

@bot.command(name='opgg')
async def comandos(ctx):
    await ctx.send(f'Opgg main: https://www.op.gg/summoners/kr/Hide%20on%20bush-KR1')

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
        user_fichas += cantidad
        await ctx.send(f'ganaste 1000 fichas')

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

@bot.command(name='merlumonedas')
async def merlumonedas(ctx):
    fichas = leer_fichas()
    await ctx.send(f'{ctx.author.name} tenes: {fichas[ctx.author.name]} Merlumonedas.')

@bot.command(name='estadisticas')
async def estadisticas(ctx):
    stats_message = obtener_estadisticas()
    await ctx.send(stats_message)

@bot.command(name='apostar')
async def apostar(ctx):
    contenido = ctx.content.lower()
    partes = contenido.split()

    if len(partes) != 3:
        await ctx.send("Uso incorrecto. Usa: !apostar (cantidad) (número o color). Ejemplo: !apostar 120 rojo.")
        return

    cantidad_str = partes[1]
    apuesta = partes[2]

    if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
        await ctx.send("La cantidad apostada debe ser un número positivo.")
        return
    
    cantidad = int(cantidad_str)

    if apuesta.isdigit() and (0 <= int(apuesta) <= 36 or apuesta == "00"):
        tipo_apuesta = "numero"
    elif apuesta in ["rojo", "negro"]:
        tipo_apuesta = "color"
    else:
        await ctx.send("La apuesta debe ser un número entre 00 o 0 y hasta el 36 o 'rojo'/'negro'.")
        return

    user = ctx.author.name

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    if cantidad > user_fichas:
        await ctx.send("No tienes suficientes fichas para apostar.")
        return
    
    user_fichas -= cantidad
    actualizar_fichas(user, user_fichas, fichas_file)

    guardar_apuesta(user, cantidad, apuesta)
    await ctx.send(f"Apuesta registrada: {user} apostó {cantidad} fichas a {apuesta}.")

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

@bot.command(name='casino')
async def casino(ctx):
    await ctx.send(f'Los comandos de casino son: !merlumonedas, !estadisticas, !apostar (cantidad) (numero o Rojo/Negro) !slot(1000), !maquinita(1000), !galletita(1000), !rusa(1000), !moneda(1000)')
                   
@bot.command(name='comandos')
async def comandos(ctx):
    await ctx.send(f'Los comandos son: !casino, !reembolso, !memide, !pajin, !simp, !facha, !tontito, !redes, !dc, !emotes, !opgg')

@bot.event
async def event_reward_earned(channel, reward_id, user):
    if reward_id == "01820b0c-0534-4ee5-be70-a2ca7ee3e9f0":
        with open(RUTA_ARCHIVO, 'r') as archivo:
            datos_usuarios = json.load(archivo)
        if user.name not in datos_usuarios:
            datos_usuarios[user.name] = 0
        
        datos_usuarios[user.name] += 100
        with open(RUTA_ARCHIVO, 'w') as archivo:
            json.dump(datos_usuarios, archivo)
        await channel.send(f"@{user.name}, cargaste 100 puntos al casino")

@bot.event
async def handle_redemption(event):
    reward_name = event.reward.title
    await event.channel.send(f'¡Hola {event.author.name}! Gracias por canjear la recompensa.')

bot.run()