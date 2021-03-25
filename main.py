import discord, datetime, time, random # Imports discord.py, datetime, time and random libraries
from discord.ext import commands # Import the extension for discord.py - discord.ext command
from discord import Member # import discord member, used in warning
import json # import the json library
import os

from math import sqrt, cos, sin # import more math functions

prefix = "m/" # Set the prefix. e.g "!sb "
bot = commands.Bot(command_prefix=prefix) # Define what bot is
bot.remove_command('help') # Remove the default help command from the Discord.py commands lib.
botver = "1.0 [beta]" # Set the bot version number.
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
    await ctx.send("""Minimal | By Cob:web Development 
m/help                   - Shows this message
m/about                  - Shows the bot statistics and ping
m/calculate              - Calculate basic math. +-/*sqrt()sin()cos()
m/warn <memberMention>   - Warn a member
m/unwarn <memberMention> - Unwarn a member
m/status <memberMention> - get warning status of member""")

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
    await ctx.send(f'About Minimal: \n\n Ping: {latency}ms \n Uptime: {botuptime} \n Version: {botver} \n\n Minimal is serving {guilds} servers. \n This bot was created by Adam Salt \n Made with discord.py `Created by Cob:web Development:` \n https://cob-web.xyz/discord/') # Shows all the output for the about command

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

    await ctx.send("the answer is: " + str(eval(command)))

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def warn(ctx, user: Member): # warning a member
    role_names = map(lambda role : role.name, ctx.message.author.roles) # get user roles to a list
    WarnMem = ctx.message.mentions[0]
    try:
        warnings[str(WarnMem.id)] += 1
    except KeyError:
        warnings[str(WarnMem.id)] = 1
    open("./.botmem/warnings.json", "w+").write(json.dumps(warnings))
    await ctx.send("user {} has {} warning(s)".format(WarnMem, warnings[str(WarnMem.id)]))
@warn.error
async def warn_error(ctx, user: Member):
    await ctx.send("missing permissions")

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unwarn(ctx, user: Member): # unwarning a member 
    role_names = map(lambda role : role.name, ctx.message.author.roles) # get user roles to a list
    WarnMem = ctx.message.mentions[0]
    try:
        warnings[str(WarnMem.id)] -= 1
    except KeyError:
        await ctx.send("user {} has 0 warnings".format(WarnMem))
        return
    open("./.botmem/warnings.json", "w+").write(json.dumps(warnings))
    await ctx.send("user {} has {} warning(s)".format(WarnMem, warnings[str(WarnMem.id)]))
@unwarn.error
async def unwarn_error(ctx, user: Member):
    await ctx.send("missing permissions")

@bot.command(pass_context=True) 
async def status(ctx, user: Member): # warning status of member
    WarnMem = ctx.message.mentions[0]
    try:
        await ctx.send("user {} has {} warning(s)".format(WarnMem, warnings[str(WarnMem.id)]))
    except:
        await ctx.send("user {} has 0 warnings".format(WarnMem))
@bot.event # When there is a message sent
async def on_message(message):
    await bot.process_commands(message) # Process the message into a command

bot.run('') # The bot "password", this is needed to connect to the account.
