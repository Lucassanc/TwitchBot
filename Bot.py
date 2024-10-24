from twitchio.ext import commands
import json
import subprocess
import asyncio
import os
import requests

directorio_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(directorio_actual)

apuestas_file = 'Ruleta/apuestas.txt'
fichas_file = 'FichasCasino.txt'
ganadores_file = 'Ruleta/ganadores.txt'
apuestas_archivo = 'Ruleta/apuestas_guardadas.json'

def extraer_codigo(url):
    if "https://static-cdn.jtvnw.net/jtv_user_pictures/" in url:
        return url.split("/")[-1]
    return None

def cargar_apuestas_guardadas():
    if os.path.exists(apuestas_archivo):
        with open(apuestas_archivo, 'r') as file:
            return json.load(file)
    else:
        return {}

def guardar_apuestas_guardadas(apuestas_guardadas):
    with open(apuestas_archivo, 'w') as file:
        json.dump(apuestas_guardadas, file, indent=4)

apuestas_actuales = {}

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

    await bot._ws.send_privmsg('SoyMerlu', f"El número ganador es: {numero} {color}.")

    with open(apuestas_file, 'r') as file:
        apuestas = file.readlines()

    await bot._ws.send_privmsg('SoyMerlu', f"Repartiendo premios...")
    for apuesta in apuestas:
        user, cantidad_str, tipo_apuesta = apuesta.strip().split(',')
        cantidad = int(cantidad_str)

        user_fichas = obtener_fichas(user, fichas_file)
        

        if tipo_apuesta.isdigit() and int(tipo_apuesta) in range(37):
            if numero == tipo_apuesta:
                ganancia = cantidad * 36
                user_fichas += ganancia
        elif tipo_apuesta.lower() in ["rojo", "negro"]:
            if color.lower() == tipo_apuesta:
                ganancia = cantidad * 2
                user_fichas += ganancia

        actualizar_fichas(user, user_fichas, fichas_file)

    await bot._ws.send_privmsg('SoyMerlu', f"Premios repartidos")
    with open(apuestas_file, 'w') as file:
        file.write("")

def guardar_apuesta(user, cantidad, apuesta, foto_perfil):
    with open(apuestas_file, 'a') as file:
        file.write(f"{user},{cantidad},{apuesta},{foto_perfil}\n")

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
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TOKEN= 'bgndnm67gp1m8czmq8i01jcxhoajyj'
REFRESH_TOKEN = '720hsds8o76ckn912okrsk6re7kjbt33erqux3vktivo7f3811'
CLIENT_SECRET = 'e9ja811yft2iban1xuqdvyxepbc85v'
ACCESS_TOKEN = 'r9p9tth3uzwl9sj9u8s3q91asx0ybw'

bot = commands.Bot(
    irc_token = f'oauth:{ACCESS_TOKEN}',
    client_id = CLIENT_ID,
    nick = 'soymerlu',
    prefix = '!',
    initial_channels = ['soymerlu'],
)

def obtener_foto_perfil(username):
    url = 'https://api.twitch.tv/helix/users'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Client-Id': CLIENT_ID
    }
    params = {'login': username}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        user_data = response.json()
        
        if 'data' in user_data and user_data['data']:
            return user_data['data'][0]['profile_image_url']
        else:
            return 'No se encontró la información del usuario.'
    else:
        return f"Error en la solicitud: {response.status_code} - {response.text}"

async def girar_ruleta_periodicamente():
    while True:
        await asyncio.sleep(120)
        await procesar_apuestas()

@bot.event
async def event_ready():
    bot.loop.create_task(girar_ruleta_periodicamente())
    subprocess.Popen(['python', 'Ruleta\\tablero.py'])
    print(f'Ruleta lista.')

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

    foto_perfil = obtener_foto_perfil(user)
    foto_perfil = extraer_codigo(foto_perfil)

    if user not in apuestas_actuales:
        apuestas_actuales[user] = []

    apuestas_actuales[user].append({
        'cantidad': cantidad,
        'apuesta': apuesta,
        'tipo_apuesta': tipo_apuesta,
        'foto_perfil': foto_perfil
    })

    guardar_apuesta(user, cantidad, apuesta, foto_perfil)
    await ctx.send(f"Apuesta registrada de {user}. Te quedan {user_fichas} Merlumonedas.")

@bot.command(name='repetir')
async def repetir(ctx):
    user = ctx.author.name
    apuestas_guardadas = cargar_apuestas_guardadas()
    
    if user not in apuestas_guardadas:
        await ctx.send("No tienes ninguna apuesta anterior registrada.")
        return

    ultimas_apuestas = apuestas_guardadas[user]

    user_fichas = obtener_fichas(user, fichas_file)
    if user_fichas is None:
        await ctx.send("Usuario no encontrado en el archivo de fichas.")
        return

    # Calcular el total de fichas que se necesitan para repetir las apuestas
    total_apuestas = sum(int(apuesta.split(',')[1]) for apuesta in ultimas_apuestas)  # Cantidad de fichas apostadas

    if total_apuestas > user_fichas:
        await ctx.send(f"No tienes suficientes fichas para repetir todas tus apuestas. Te faltan {total_apuestas - user_fichas} fichas.")
        return

    user_fichas -= total_apuestas
    actualizar_fichas(user, user_fichas, fichas_file)

    if user not in apuestas_actuales:
        apuestas_actuales[user] = []

    for apuesta_str in ultimas_apuestas:
        # Dividir la apuesta y obtener los datos
        partes = apuesta_str.split(',')
        cantidad = int(partes[1])  # La cantidad apostada
        apuesta = partes[2]  # La apuesta (rojo, negro, número, etc.)
        foto_perfil = partes[4]  # La foto de perfil

        # Agregar la apuesta a las apuestas actuales
        apuestas_actuales[user].append({
            'cantidad': cantidad,
            'apuesta': apuesta,
            'foto_perfil': foto_perfil
        })

        # Llamar a la función para guardar la apuesta (esto puede variar según tu implementación)
        guardar_apuesta(user, cantidad, apuesta, foto_perfil)

    await ctx.send(f"{user}, repetiste tus {len(ultimas_apuestas)} apuestas guardadas. Gastaste {total_apuestas} fichas, te quedan {user_fichas} Merlumonedas.")

@bot.command(name='guardar')
async def guardar(ctx):
    user = ctx.author.name
    apuestas_guardadas = cargar_apuestas_guardadas()  # Cargar apuestas guardadas

    # Verificar si el usuario tiene apuestas actuales
    if user not in apuestas_actuales or len(apuestas_actuales[user]) == 0:
        await ctx.send("No tienes apuestas actuales para guardar.")
        return

    # Obtener el código de la foto del perfil desde la última apuesta actual
    codigo_foto_perfil = None
    for apuesta in apuestas_actuales[user]:
        if 'foto_perfil' in apuesta:
            codigo_foto_perfil = apuesta['foto_perfil'].split('/')[-1]  # Obtener solo el código de la foto
            break  # Solo necesitamos el código una vez

    # Guardar las apuestas del usuario
    if user not in apuestas_guardadas:
        apuestas_guardadas[user] = []

    for apuesta in apuestas_actuales[user]:
        # Formatear la apuesta para guardarla en el JSON
        apuesta_str = f"{user},{apuesta['cantidad']},{apuesta['apuesta']},{apuesta['tipo_apuesta']},{codigo_foto_perfil}"
        apuestas_guardadas[user].append(apuesta_str)

    # Guardar en el archivo JSON
    guardar_apuestas_guardadas(apuestas_guardadas)

    await ctx.send(f"Tus {len(apuestas_actuales[user])} apuestas han sido guardadas.")

    # Limpiar las apuestas actuales después de guardarlas
    apuestas_actuales[user] = []

@bot.command(name='misapuestas')
async def misapuestas(ctx):
    user = ctx.author.name
    apuestas_guardadas = cargar_apuestas_guardadas()

    if user not in apuestas_guardadas:
        await ctx.send("No tienes apuestas guardadas.")
        return

    apuestas = apuestas_guardadas[user]
    mensaje = f"Tienes {len(apuestas)} apuestas guardadas: " + ", ".join([f"{a['cantidad']} al {a['apuesta']}" for a in apuestas])
    
    await ctx.send(mensaje)
                   
bot.run()