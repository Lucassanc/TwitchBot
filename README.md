# Twitch Bot

Este es un bot de Twitch programado en Python utilizando la librería [TwitchIO](https://twitchio.dev/). El bot está diseñado para interactuar con los usuarios en un canal de Twitch, respondiendo a comandos y manejando recompensas de canal.

## Características

- Responde a comandos personalizados en el chat.
- Gestiona recompensas de canal, sumando o restando fichas a los usuarios.
- Fácil de configurar y personalizar.

## Requisitos

Asegúrate de tener instalados los siguientes requisitos antes de ejecutar el bot:

- Python 3.10 o superior
- [TwitchIO](https://twitchio.dev/) (puedes instalarlo ejecutando `pip install twitchio`)

## Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/Lucassanc/TwitchBot.git
2. Navega al directorio del bot:
   cd TwitchBot
3. Instala las dependencias necesarias:
   pip install -r requirements.txt
4. Configura tus credenciales de Twitch creando un archivo .env con el siguiente formato:
   TWITCH_TOKEN=<tu_token_de_acceso_de_twitch>
   TWITCH_CLIENT_ID=<tu_client_id>
   TWITCH_CLIENT_SECRET=<tu_client_secret>
   TWITCH_BOT_USERNAME=<nombre_de_usuario_del_bot>
   TWITCH_CHANNEL=<nombre_del_canal_donde_estará_activo_el_bot>

Uso
Para ejecutar el bot, simplemente utiliza el siguiente comando:
  python Bot.py
Una vez iniciado, el bot se conectará a Twitch y comenzará a escuchar los mensajes del canal configurado.

Comandos
Aquí hay algunos ejemplos de comandos personalizados que puedes añadir al bot:

!comando - Descripción del comando.
!fichas - Muestra las fichas del usuario.
!ruleta - Gira la ruleta y devuelve un número aleatorio.
Personalización
Puedes personalizar los comandos y las interacciones del bot editando el archivo Bot.py. Solo asegúrate de que el bot está registrado en tu cuenta de Twitch y que tiene acceso a tu canal.

Ejecutar en un Servidor 24/7
Este bot está diseñado para ejecutarse de forma continua. Algunas opciones para mantenerlo activo 24/7 incluyen:

Usar un servidor VPS (por ejemplo, DigitalOcean, AWS).
Implementarlo en plataformas como Heroku, Railway, o Replit.
Contribuciones
¡Las contribuciones son bienvenidas! Si deseas colaborar, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Este `README.md` incluye:

- **Descripción del bot**: Breve resumen de lo que hace.
- **Requisitos**: Las herramientas necesarias para que el bot funcione.
- **Instalación**: Guía paso a paso sobre cómo clonar el repositorio y configurar el bot.
- **Uso**: Cómo ejecutar el bot y ejemplos de comandos.
- **Ejecutar 24/7**: Recomendaciones sobre cómo mantener el bot funcionando de manera continua.
- **Contribuciones y licencia**.

Puedes copiar este texto directamente en el archivo `README.md` de tu repositorio. Si necesitas alguna modificación o más detalles, ¡solo avísame!
