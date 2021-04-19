import discord, datetime, time, random # Imports discord.py, datetime, time and random libraries
from discord.ext import commands # Import the extension for discord.py - discord.ext command
from discord import Member, Embed # import discord member, used in warning -- import Embed to polish messages
import json # import the json library
import os

from math import sqrt, cos, sin # import more math functions

prefix = "m/" # Set the prefix. e.g "!sb "
bot = commands.Bot(command_prefix=prefix) # Define what bot is
bot.remove_command('help') # Remove the default help command from the Discord.py commands lib.
botver = "1.2.1 [beta]" # Set the bot version number.
functions = ['+', '-', '*', '/', 'sqrt', 'cos', 'sin'] # math functions

start_time = time.time() # Starts the timer for the uptime of the bot.


# create bot memory structure
if not os.path.isdir("./.botmem"): os.mkdir("./.botmem") 
if not os.path.exists("./.botmem/warnings.json"): open("./.botmem/warnings.json", "w+")
if open("./.botmem/warnings.json", "r").read() == "":
    warnings = {}
else:
    warnings = json.loads(open("./.botmem/warnings.json").read())
##############################

@bot.event # When the bot first loads up
async def on_ready():
    print(""" _______
||  _  ||
|| | | || version {} """.format(botver))
    print('The bot has logged in as {0.user}'.format(bot)) # Say that [bot name] is logged on in the terminal
    await bot.change_presence(activity=discord.Game(name=f"m/help - {botver}")) # Change the bot activity

@bot.command() # Help command. This will give you all of the commands
async def help(ctx):
    e = Embed(title="help", description="help command", name="helpCommands")
    e.add_field(name="help", value="m/help                   - Shows this message")
    e.add_field(name="about", value="m/about                  - Shows the bot statistics and ping")
    e.add_field(name="calculate", value="m/calculate              - Calculate basic math. +-/*sqrt()sin()cos()")
    e.add_field(name="warn", value="m/warn <memberMention>   - Warn a member")
    e.add_field(name="unwarn", value="m/unwarn <memberMention> - Unwarn a member")
    e.add_field(name="status", value="m/status <memberMention> - get warning status of member""")
    e.add_field(name="join", value="m/join - join the voice call you are currently in""")
    e.add_field(name="leave", value="m/leave - leave the voice call you are currently in""")
    e.add_field(name="play", value="m/play - play a song in the voice call you are currently in""")
    await ctx.send(embed=e)

@bot.command() # About command. This includes; Bot latency, Bot guild number, Bot uptime, Bot version.
async def about(ctx):
    # Get the latency of the bot
    latency = round(bot.latency * 100)  # round rounds a decimal number into the nearest whole number. bot.latency is given as a decimal. (bot.latency x 100) = the time in ms. 
    
    # Get the number of guilds the bot is in
    guilds = len(bot.guilds) # Where len is length of the array for bot.guilds
    
    # Get the bot uptime
    current_time = time.time() # Sets current time to the time.
    difference = int(round(current_time - start_time)) # Takes away the current time from the start time (rounded)
    botuptime = str(datetime.timedelta(seconds=difference)) # Calculates the bot uptime and displays the difference.
    
    # Send all the about statistics to the user
    e = Embed(title="About", description="About and statistics\n About Minimal:", name="aboutCommand")
    e.add_field(name="Ping", value=f"Ping: {latency}ms ")
    e.add_field(name="Uptime", value=f"Uptime: {botuptime}")
    e.add_field(name="Version", value=f"Version: {botver}")
    e.add_field(name="Serving", value=f"Minimal is serving {guilds} servers")
    e.add_field(name="Credits", value=f"Made with discord.py Created by Cob:web Development: \n https://cob-web.xyz/discord/'")
    await ctx.send(embed=e) # Shows all the output for the about command

@bot.command() # calculate command
async def calculate(ctx, *args):
    command = ""
    cont = False
    for i in args:
        for j in functions:
            if j in i:
                command += i
                cont = True
        if cont: 
            cont = False
            continue

        try:
            float(i)
            command += i
        except:
            print("syntax error")
            break
    e = Embed(title="Calculation", name="calculateCommand")
    e.add_field(name="Answer", value=str(eval(command)))
    await ctx.send(embed=e)

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def warn(ctx, user: Member): # warning a member
    WarnMem = ctx.message.mentions[0]
    serverId = ctx.message.guild.id
    try:
        warnings[str(serverId)]
    except KeyError: 
        warnings[str(serverId)] = {}
    try:
        warnings[str(serverId)][str(WarnMem.id)] += 1
    except KeyError:
        warnings[str(serverId)][str(WarnMem.id)] = 1
    open("./.botmem/warnings.json", "w+").write(json.dumps(warnings))
    e = Embed(title="Warning", name="warnCommand")
    e.add_field(name="Warn", value="User {} has {} warning(s)".format(WarnMem, warnings[str(serverId)][str(WarnMem.id)]))
    await ctx.send(embed=e)
@warn.error
async def warn_error(ctx, user: Member):
    await ctx.send("missing permissions")

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unwarn(ctx, user: Member): # unwarning a member 
    WarnMem = ctx.message.mentions[0]
    serverId = ctx.message.guild.id
    try: warnings[str(serverId)]
    except KeyError: warnings[str(serverId)] = {}
    try:
        warnings[str(serverId)][str(WarnMem.id)] -= 1
    except KeyError:
        e = Embed(title="Unwarning", name="unwarnCommand")
        e.add_field(name="Unwarn", value="User {} has 0 warnings".format(WarnMem))
        await ctx.send(embed=e)
        return
    open("./.botmem/warnings.json", "w+").write(json.dumps(warnings))
    e = Embed(title="Unwarning", name="unwarnCommand")
    e.add_field(name="Unwarn", value="User {} has {} warning(s)".format(WarnMem, warnings[str(serverId)][str(WarnMem.id)]))
    await ctx.send(embed=e)
@unwarn.error
async def unwarn_error(ctx, user: Member):
    await ctx.send("missing permissions")

@bot.command(pass_context=True) 
async def status(ctx, user: Member): # warning status of member
    WarnMem = ctx.message.mentions[0]
    serverId = ctx.message.guild.id
    try:
        warnings[str(serverId)]
        e = Embed(title="Status of user", description="Status", name="statusCommand")
        e.add_field(name="Status", value="User {} has {} warning(s)".format(WarnMem, warnings[str(serverId)][str(WarnMem.id)]))
        await ctx.send(embed=e)
    except KeyError as e:
        e = Embed(title="Status of user", description="Status", name="statusCommand")
        e.add_field(name="Status", value="User {} has 0 warnings".format(WarnMem))
        await ctx.send(embed=e)

@bot.command(name="join")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    try:
        server = ctx.message.guild.voice_client
        await server.disconnect()
    except:
        pass

@bot.command(pass_context=True) # TODO: skip, queues, etc
async def play(ctx, url):
    from discord.utils import get
    from discord import FFmpegPCMAudio
    from youtube_dl import YoutubeDL

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = ctx.voice_client

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        
        # info
        e = Embed(title="Video Playing", description="", name="playCommand")
        e.add_field(name="title", value=info["title"])
        await ctx.send(embed=e)

        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("Already playing song")
        return
@bot.event # When there is a message sent
async def on_message(message):
    await bot.process_commands(message) # Process the message into a command

bot.run('ODIyMzM3NDI4ODE5MDE3NzM5.YFQzaQ.Nhh9d_fHg4rFV5aTr3FxLoyJ7Zw') # The bot "password", this is needed to connect to the account.
