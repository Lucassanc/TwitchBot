from twitchio.ext import commands
import random

BROADCASTER_ID = '153299663'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TOKEN= 'bgndnm67gp1m8czmq8i01jcxhoajyj'
REFRESH_TOKEN = 'fso06nysheb9yjlcqp1tuga9s80hrcq3b6xaj554uivu0y0chv'
CLIENT_SECRET = 'e9ja811yft2iban1xuqdvyxepbc85v'
ACCESS_TOKEN = 'w2kquwqfon3730122hc2cl3zuc1jgb'

bot = commands.Bot(
    irc_token = f'oauth:{ACCESS_TOKEN}',
    client_id = CLIENT_ID,
    nick = 'soymerlu',
    prefix = '!',
    initial_channels = ['soymerlu'],
)

palabra = ['parada', 'dormida']

@bot.event
async def event_ready():
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

@bot.command(name='emotes')
async def emotes(ctx):
    await ctx.send(f'Si no puedes ver FeelsDankMan ni RareParrot y solo ves oalabras es porque no tienes la extensión de 7tv. La puedes descargar desde aquí: https://7tv.app AYAYA')

@bot.command(name='opgg')
async def comandos(ctx):
    await ctx.send(f'Opgg main: https://www.op.gg/summoners/kr/Hide%20on%20bush-KR1')

@bot.command(name='comandos')
async def comandos(ctx):
    await ctx.send(f'Los comandos son: !casino, !ruleta, !reembolso, !memide, !pajin, !simp, !facha, !tontito, !redes, !dc, !emotes, !opgg')

bot.run()