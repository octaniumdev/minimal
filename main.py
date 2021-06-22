import discord
import datetime
import time
import random
import json
import os
# Import the extension for discord.py - discord.ext command
from discord.ext import commands
# import discord member, used in warning -- import Embed to polish messages
from discord import Member, Embed
from math import sqrt, cos, sin  # import more math functions

bot_warnings_file = "./.botmem/warnings.json"
about_embed = "./embeds/about.json"
help_embed = "./embeds/help.json"

prefix = "m/"  # Set the prefix. e.g "!sb "
bot = commands.Bot(command_prefix=prefix)  # Define what bot is
# Remove the default help command from the Discord.py commands lib.
bot.remove_command('help')
botver = "1.3.1 [beta]"  # Set the bot version number.
functions = ['+', '-', '*', '/', 'sqrt', 'cos', 'sin']  # math functions

start_time = time.time()  # Starts the timer for the uptime of the bot.


# create bot memory structure
if not os.path.isdir("./.botmem"):
    os.mkdir("./.botmem")
if not os.path.exists(bot_warnings_file):
    open(bot_warnings_file, "w+")
if open(bot_warnings_file, "r").read() == "":
    warnings = {}
else:
    warnings = json.loads(open(bot_warnings_file).read())
##############################


@bot.event  # When the bot first loads up
async def on_ready():
    bot.add_cog(Music(bot))
    print(""" _______
||  _  ||
|| | | || version {} """.format(botver))
    print('The bot has logged in as {0.user}'.format(
        bot))  # Say that [bot name] is logged on in the terminal
    # Change the bot activity
    await bot.change_presence(activity=discord.Game(name=f"m/help - {botver}"))


@bot.command()  # Help command. This will give you all of the commands
async def help(ctx):
    e = Embed(title="help", description="help command", name="helpCommands")
    for field in json.loads(open(help_embed).read()):
        e.add_field(name=field[name], value=field[value])
    await ctx.send(embed=e)


# About command. This includes; Bot latency, Bot guild number, Bot uptime, Bot version.
@bot.command()
async def about(ctx):
    # Get the latency of the bot
    # round rounds a decimal number into the nearest whole number. bot.latency is given as a decimal. (bot.latency x 100) = the time in ms.
    latency = round(bot.latency * 100)

    # Get the number of guilds the bot is in
    guilds = len(bot.guilds)  # Where len is length of the array for bot.guilds

    # Get the bot uptime
    current_time = time.time()  # Sets current time to the time.
    # Takes away the current time from the start time (rounded)
    difference = int(round(current_time - start_time))
    # Calculates the bot uptime and displays the difference.
    botuptime = str(datetime.timedelta(seconds=difference))

    # Send all the about statistics to the user
    e = Embed(title="About",
              description="About and statistics\n About Minimal:", name="aboutCommand")
    for field in json.loads(open(about_embed).read()):
        e.add_field(name=eval(field[name]), value=eval(field[value]))
    e.add_field(name="Ping", value=f"Ping: {latency}ms ")
    e.add_field(name="Uptime", value=f"Uptime: {botuptime}")
    e.add_field(name="Version", value=f"Version: {botver}")
    e.add_field(name="Serving", value=f"Minimal is serving {guilds} servers")
    e.add_field(name="Credits",
                value="Made with discord.py Created by Cob:web Development: \n https://cob-web.xyz/discord/'")
    await ctx.send(embed=e)  # Shows all the output for the about command


@bot.command()  # calculate command
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
        except Exception as e:
            e = Embed(title="Error", name="error")
            e.add_field(name="Calculation Error:", value=e)
            ctx.send(embed=e)
            break
    e = Embed(title="Calculation", name="calculateCommand")
    e.add_field(name="Answer", value=str(eval(command)))
    await ctx.send(embed=e)


@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def warn(ctx, user: Member):  # warning a member
    warn_mem = ctx.message.mentions[0]
    server_id = ctx.message.guild.id
    try:
        warnings[str(server_id)]
    except KeyError:
        warnings[str(server_id)] = {}
    try:
        warnings[str(server_id)][str(warn_mem.id)] += 1
    except KeyError:
        warnings[str(server_id)][str(warn_mem.id)] = 1
    open(bot_warnings_file, "w+").write(json.dumps(warnings))
    e = Embed(title="Warning", name="warnCommand")
    e.add_field(
        name="Warn", value=f"User {warn_mem} has {warnings[str(server_id)][str(warn_mem.id)]} warning(s)")
    await ctx.send(embed=e)


@warn.error
async def warn_error(ctx, user: Member):
    await ctx.send("missing permissions")


@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unwarn(ctx, user: Member):  # unwarning a member
    warn_mem = ctx.message.mentions[0]
    server_id = ctx.message.guild.id
    try:
        warnings[str(server_id)]
    except KeyError:
        warnings[str(server_id)] = {}
    try:
        warnings[str(server_id)][str(warn_mem.id)] -= 1
    except KeyError:
        e = Embed(title="Unwarning", name="unwarnCommand")
        e.add_field(name="Unwarn",
                    value=f"User {warn_mem} has 0 warnings")
        await ctx.send(embed=e)
        return
    open(bot_warnings_file, "w+").write(json.dumps(warnings))
    e = Embed(title="Unwarning", name="unwarnCommand")
    e.add_field(
        name="Unwarn", value=f"User {warn_mem} has {warnings[str(server_id)][str(warn_mem.id)]} warning(s)")
    await ctx.send(embed=e)


@unwarn.error
async def unwarn_error(ctx, user: Member):
    await ctx.send("missing permissions")


@bot.command(pass_context=True)
async def status(ctx, user: Member):  # warning status of member
    warn_mem = ctx.message.mentions[0]
    server_id = ctx.message.guild.id
    try:
        warnings[str(server_id)]
        e = Embed(title="Status of user",
                  description="Status", name="statusCommand")
        e.add_field(
            name="Status", value=f"User {warn_mem} has {warnings[str(server_id)][str(warn_mem.id)]} warning(s)")
        await ctx.send(embed=e)
    except KeyError as e:
        e = Embed(title="Status of user",
                  description="Status", name="statusCommand")
        e.add_field(name="Status",
                    value=f"User {warn_mem} has 0 warnings")
        await ctx.send(embed=e)


class Music(commands.Cog):
    """
    MusicPlayer
     - contains queue and ways to interact with it
    """

    def __init__(self, bot):
        self.queue = []
        self.stop = False
        self.skip = False
        self.bot = bot

  # private
    async def _waitForSong(self, expected_duration):
        # wait for song to finish and
        # check if skip was called.
        import asyncio
        st = time.time()
        while time.time() - st < expected_duration:
            if self.skip:
                return
            await asyncio.sleep(1)

  # public
    @commands.command(name="join")
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        # leave from voice channel
        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
        except RuntimeError:
            pass

    @commands.command(pass_context=True)
    async def enqueue(self, ctx, url):
        # enqueue a song to play
        self.queue.append(url)

    @commands.command()
    async def shuffle(self, ctx):
        # shuffle queue
        random.shuffle(self.queue)

    @commands.command()
    async def stop(self, ctx):
        # stop queue from playing
        self.stop = True
        ctx.voice_client.stop()

    @commands.command()
    async def skip(self, ctx):
        # skip a song
        self.skip = True
        ctx.voice_client.stop()

    @commands.command()
    async def show(self, ctx):
        await ctx.send(str(self.queue))

    @commands.command(pass_context=True)
    async def play(self, ctx):
        if not ctx.voice_client:
            # if we are not connected to a
            # voice channel, connect to
            # the author's channel.
            channel = ctx.author.voice.channel
            await channel.connect()

        from discord import FFmpegPCMAudio
        from youtube_dl import YoutubeDL

        YDL_OPTIONS = {'format': 'bestaudio',
                       'noplaylist': 'True', 'quiet': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = ctx.voice_client

        if len(self.queue) == 0:  # queue is empty
            await ctx.send("you need to enqueue a video to start playing")
        else:
            while len(self.queue) > 0:  # iterate over all queue
                # until it has nothing in it
                if self.skip:
                    # make sure we skip
                    self.skip = False
                    ctx.voice_client.stop()
                    continue
                if self.stop:
                    # make sure we stop
                    self.stop = False
                    ctx.voice_client.stop()
                    break

                url = self.queue.pop(0)
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']

                # info embed
                e = Embed(title="Video Playing",
                          description="", name="playCommand")
                e.add_field(name="title", value=info["title"])
                await ctx.send(embed=e)

                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                await self._waitForSong(info['duration'])


@bot.event  # When there is a message sent
async def on_message(message):
    await bot.process_commands(message)  # Process the message into a command

bot.run('')  # The bot "password", this is needed to connect to the account.
