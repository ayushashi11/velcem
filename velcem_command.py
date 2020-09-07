import os
import discord
import ai_m2
import random
from discord.ext import commands
from math import *
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("TOKEN")
bot = commands.Bot(command_prefix='v')
r=random.random
C="k x kq g ğ ŋ t s tq d z n th dh c ż š ž p f pq b v m j w r l h".split()
c0=0.90
c1=0.80
L="r l j w".split()
L0=L+["kq","tq","pq"]
l0=0.40*c0
V1="y ý a á ă i í ĭ u ú ŭ o ó ŏ e é ĕ ai aí au aú".split()
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
        await guild.create_text_channel(channel_name)
bot.run(TOKEN)
