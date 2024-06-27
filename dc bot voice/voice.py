# Import things
import discord, os, sys, random, datetime, time, ast, shutil, time, urllib.request, json, discord.ext, traceback, re, io

from dotenv import load_dotenv
from configparser import ConfigParser
from pathlib import Path
from traceback import format_exc

from gtts import gTTS

# Import discord things
from discord.ext import commands
from discord.commands import Option, slash_command, SlashCommandGroup
from discord.ext.commands import has_permissions, MissingPermissions
from discord.member import Member
from discord.role import Role
from discord.utils import get
from discord.ext import tasks
from discord import default_permissions
from discord import guild_only
from discord.voice_client import VoiceClient

f = open("data/bot/version.txt", "r")
version = int(f.read())+1
f.close()
f = open("data/bot/version.txt", "w")
f.write(str(version))
f.close()

filename = sys.argv[0].split('\\')[-1]

hidden = True

####################################################################################################################
####################################################################################################################
####################################################################################################################

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = [os.getenv('DISCORD_PREFIX')]

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

####################################################################################################################
##def###############################################################################################################
####################################################################################################################

def printt(text):
    try:
        print(str(text))
    except Exception:
        pass

####################################################################################################################
####################################################################################################################
####################################################################################################################

@bot.event
async def on_ready():
    printt(f"{bot.user} is now running v.{version}")
    f = open("data/bot/status.txt", "r")
    status=f.read()
    f.close()
    status=status.split(";")
    if status[0] == "Streaming":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=status[1], url=status[-1]))
    elif status[0] == "Slaying": 
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status[1]))
    elif status[0] == "Listening": 
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status[1]))
    elif status[0] == "Custom": 
        await bot.change_presence(activity=discord.CustomActivity(status[1]))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[1]))

    #print guilds
    for guild in bot.guilds:
        printt(guild.name)


####################################################################################################################
##commands##########################################################################################################
####################################################################################################################

sc_owner = bot.create_group(name="owner", description="Owner related commands", guild_only=True, guild_ids=[829873116175925269])

# stop
@sc_owner.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.defer(ephemeral=True)
    if ctx.author.id == 413683572612792320:
        await ctx.followup.send(f"Good night!")
        raise SystemExit

# status
@sc_owner.command()
@commands.is_owner()
async def status(ctx, option: Option(str, "Select a option", choices=["Custom", "Streaming", "Playing", "Watching", "Listening"], required=True), text: Option(str, "The text to be displayed", required=True), stream: Option(str, "The streamer name to be streamed", required=False)):
    await ctx.defer(ephemeral=True)

    if stream == None:
        stream = "twitch.tv/twitchrivals"
        
    if ctx.author.id == 413683572612792320:
        f = open("data/bot/status.txt", "w")
        f.write(str(option)+";"+str(text)+";"+str(stream))
        f.close()

        if option == "Streaming":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text, url=f"{stream}"))
        elif option == "Playing": 
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=text))
        elif option == "Watching": 
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text)) 
        elif option == "Listening": 
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
        elif option == "Custom": 
            await bot.change_presence(activity=discord.CustomActivity(text))
        
        await ctx.followup.send(f"{option} **{text}**")

# join VCs
@bot.command(description="Press F to pay respect")
@guild_only()
@commands.has_permissions(kick_members=True)
async def f(ctx, member: Option(Member, description="F an ...", required=True)):
    await ctx.defer(ephemeral=False)

    # lade einen zufälligen satz
    f = io.open("data/f/satz.txt", "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    satz = random.choice(lines)
    satz = satz.format(member.display_name)

    # lade eine zufällige bescheibung
    f = io.open("data/f/beschreibung.txt", "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    beschreibung = random.choice(lines)
    beschreibung = beschreibung.format(member.display_name)

    # lade ein zufälliges bild
    f = open("data/f/bild.txt", "r")
    lines = f.readlines()
    f.close()
    bild = random.choice(lines)

    # erstelle und sende das embed
    embed = discord.Embed(title=satz, colour=discord.Colour(0x7808dc), description=beschreibung)
    embed.set_image(url=bild)
    message = await ctx.followup.send(content=f"<@{member.id}>", embed=embed)
    await message.add_reaction("🇫")

    # tts generieren
    myobj = gTTS(text=satz, lang="de", slow=False)
    myobj.save("data/audio/audio.mp3")

    # tts in jedem poker channel abspielen
    for vc in ctx.guild.voice_channels:
        if str(vc.category) == "POKER":
            voice_client = await vc.connect()
            await voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="data/audio/audio.mp3"), wait_finish=True)
            await voice_client.disconnect()




####################################################################################################################
####################################################################################################################
####################################################################################################################

bot.run(token)
