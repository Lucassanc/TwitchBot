import subprocess
import os
import signal
import sys
import time

# Obtén el directorio actual donde está el archivo iniciador
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Especifica los nombres de los archivos Python que deseas ejecutar
archivos_a_ejecutar = [
    "Bot.py",
    "BotComandos.py"
]

# Crea una lista para almacenar los procesos
procesos = []

# Inicia cada bot y almacena el proceso
for archivo in archivos_a_ejecutar:
    ruta_archivo = os.path.join(directorio_actual, archivo)
    print(f"Iniciando {archivo}...")
    proceso = subprocess.Popen(["python", ruta_archivo])  # Usa "python3" si es necesario
    procesos.append(proceso)

try:
    # Mantén el script en ejecución
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Deteniendo bots...")

# Finaliza los procesos de los bots
for proceso in procesos:
    os.kill(proceso.pid, signal.SIGTERM)  # Envía señal para detener el proceso
    print(f"{proceso.pid} detenido.")

print("Todos los bots han sido detenidos.")
