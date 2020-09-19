import os
import re
import ipa
import ai_m2
import discord
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("TOKEN")
GUILD=int(os.getenv("GUILD"))
NCID=int(os.getenv("NCID"))
MID=int(os.getenv("MID"))
client = discord.Client()
o = False
st = re.compile(r"o<(\w)+>")
st_x = re.compile(r"x\/(\S)+\/")
@client.event
async def on_ready():
    global o
    for guild in client.guilds:
        if guild.id == GUILD:
            print(".")
            break
    else: raise RuntimeError("guild not found")
    for channel in guild.channels:
        if channel.id == MID:
            print("..")
            break
    else: raise RuntimeError("channel not found")
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await channel.send("aadib kěwaxyooc!!" if not o else "")
    o = True
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    cs = '\n - '.join([channel.name+" "+str(channel.id) for channel in guild.channels])
    print(f"Channels:\n - {cs}")

@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.id == GUILD:
            break
    for channel in guild.channels:
        if channel.id == NCID:
            break
    await channel.send(f'{member.mention}, aadib and welcome!')
    await member.create_dm()

@client.event
async def on_invite_create(invite):
    nm=invite.inviter.name
    await invite.channel.send(f"{nm} created an invite ")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ret = ""
    cont = message.content
    for m in re.finditer(st,cont):
        print(m)
        ret+="\n"+(cont[m.start():m.end()][2:-1].replace("e1","ë")
                                                .replace("a1","ě")
                                                .replace("o1","ö")
                                                .replace("g1","ğ")
                                                .replace("s1","š")
                                                .replace("z1","ž")
                                                .replace("2","\u0301"))
    for m in re.finditer(st_x,cont):
        print(m)
        ret+="\n"+ipa.xsampa2ipa(cont[m.start():m.end()][2:-1],"")
    if len(ret):
        await message.channel.send(ret)
    if message.content.startswith('!hello'):
        embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)
        await message.channel.send(embed=embedVar)

@client.event
async def on_member_remove(member):
    for guild in client.guilds:
        if guild.id == GUILD:
            break
    for channel in guild.channels:
        if channel.id == NCID:
            break
    await channel.send(f'{member.mention}, aader!')

client.run(TOKEN)

