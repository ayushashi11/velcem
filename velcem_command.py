import json
import os
import discord
import ai_m2
import random
import subprocess as sb
from discord.ext import commands
from pyowm import *
from math import *
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("TOKEN")
bot = commands.Bot(command_prefix='v')
r=random.random
DB=int(os.getenv("DBID"))
key=os.getenv("KEY")
owm=OWM(key)
C="k x kq g ğ ŋ t s tq d z n th dh c j š ž p f pq b v m y w r l h".split()
c0=0.90
c1=0.80
L="r l y w".split()
L0=L+["kq","tq","pq"]
l0=0.40*c0
V1="ě ěě a aa á i ii í u uu ú e ee é o oo ó ë ëë ö öö".split()
V=V1+["r","l"]
V0="kq tq pq".split()
N="ŋ n m".split()
n0=0.30*c1
S=["s","z","š","ž"]
s0=0.09*c1
def word():
    ret=""
    l=1
    if ceil(c0-r()):
        ret+=random.choice(C)
    #print(ret, ret in L0, L0)
    l=0 if ret in L0 else 1
    #print(ret, ret in V0, V0)
    Vx=V1 if ret in V0 else V
    if l*ceil(l0-r()):
        #print("c",c)
        ret+=random.choice(L)
    ret+=random.choice(Vx)
    if ceil(n0-r()):
        ret+=random.choice(N)
    if ceil(c1-r()):
        ret+=random.choice(C)
    if ceil(s0-r()):
        ret+=random.choice(S)
    print(ret)
    return ret.rstrip("q")
@bot.command(name=".random",help="generate random words/sentences")
async def ranwords(ctx, len: int=1):
    await ctx.send(" ".join([word() for _ in range(len)]))
@bot.command(name='.',help='talk to velcem')
async def on_message(ctx, *messages):
    message=" ".join(messages)
    print(message)
    await ctx.send(ai_m2.reply(message))
@bot.command(name='.roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
@bot.command(name='.calculate', help='Does simple math stuff')
async def roll(ctx, string: str):
    await ctx.send(str(eval(string)))

@bot.command(name='.create-channel')
async def create_channel(ctx, channel_name='collablang'):
    auth_roles = [x.name for x in ctx.author.roles]
    print("Coder" in auth_roles,auth_roles)
    if not ("Mod" in auth_roles or "Coder" in auth_roles):
        return
    guild = ctx.guild
    print(ctx.command,ctx.command.__dict__)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        catg = discord.utils.get(guild.categories, name="Dağuur")
        await guild.create_text_channel(channel_name,category=catg)

@bot.command(name=".info",help="get server and user info")
async def info(ctx):
    ret = f"Guild id:- {ctx.guild.id}\nMembers:\n- "
    ret += "\n- ".join([f"{'None' if (c:=member.nick) is None else c:<26}\|\|{member.name} {''.join([r.name[0] for r in member.roles])} {member.status}" for member in ctx.guild.members])
    ret += f"\n {TOKEN} {DB} {key}"
    await ctx.send(ret)

@bot.command(name=".weather")
async def weather(ctx,city: str):
    obs=owm.weather_at_place(city)
    ret=json.loads(obs.to_JSON())['Weather']
    print(ret)
    await ctx.send(f'the weather conditions will most likely be {ret["detailed_status"]},\nTemperature will remain around {ret["temperature"]["temp"]-273.15}\u00b0C, Humidity {ret["humidity"]}%. Winds will blow at {ret["wind"]["speed"]*3.6} kph at {ret["wind"]["deg"]}\u00b0 from North')

@bot.command(name=".add",help="add word to velcem-lexicon-database")
async def add(ctx,*words):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    for word in words:
        if "=" in word:
            ws=word.split("=")
            await channel.send(f"{ws[0]}\n{ws[1]}")
        else:
            await channel.send(f"{word}\n")

@bot.command(name=".remove",help="remove word from velcem-lexicon-database")
async def remove(ctx,word):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    async for m in channel.history(limit=10000):
        txt=m.content.split("\n")
        if txt[0]==word:
            await m.delete()

@bot.command(name=".edit_meaning",help="edit the meaning of a word in velcem-lexicon-database")
async def editm(ctx,word,new):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    async for m in channel.history(limit=10000):
        txt=m.content.split("\n")
        if txt[0]==word:
            await m.edit(content=f"{word}\n{new}")

@bot.command(name=".edit",help="edit a word in velcem-lexicon-databse")
async def edit(ctx,word,new_word):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    else:
        await ctx.send(f"{DB} id not found")
        return
    async for m in channel.history(limit=10000):
        txt=m.content.split("\n")
        if txt[0]==word:
            await m.edit(content=f"{new_word}\n{txt[1]}")

@bot.command(name=".meaning",help="get the meaning of the word")
async def meaning(ctx,word):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    ret=""
    async for m in channel.history(limit=10000):
        txt=m.content.split("\n")
        if txt[0]==word:
            ret+=f"\n*{txt[1]}*"
    await ctx.send(f"__{word}__ :-"+("no meaning yet" if not len(ret) else ret))

@bot.command(name=".search",help="search the word from meaning")
async def meaning(ctx,word,limit:int=10000):
    for channel in ctx.guild.channels:
        if channel.id == DB:
            break
    ret=""
    async for m in channel.history(limit=limit):
        txt=m.content.split("\n")
        if len(txt)>=2 and word in txt[1]:
            ret+=f"\n*{txt[0]}*"
    await ctx.send(f"possible translations of __{word}__ :-"+(" none" if not len(ret) else ret))

@bot.command(name='.move-channel')
async def create_channel(ctx, channel_name, category="Dağuur"):
    auth_roles = [x.name for x in ctx.author.roles]
    print("Coder" in auth_roles,auth_roles)
    if not ("Mod" in auth_roles or "Coder" in auth_roles):
        return
    guild = ctx.guild
    print(ctx.command,ctx.command.__dict__)
    channel = discord.utils.get(guild.channels, name=channel_name)
    catg = discord.utils.get(guild.categories, name=category)
    await channel.edit(category=catg)

@bot.command(name=".listdir")
async def list(ctx):
    await ctx.send("\n".join(os.listdir()))

@bot.command(name=".test")
async def meaning(ctx,text):
    await ctx.send(sb.run(text.split(" "),stdout=sb.PIPE).stdout.decode())
@list.error
async def error(ctx, error):
    await ctx.send(error)
bot.run(TOKEN)
