import os
import re
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
st = re.compile(r"o\/(\w)+\/")
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
    await channel.send(f'{member.name}, aadib and welcome!')
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_invite_create(invite):
    nm=invite.inviter.name
    await invite.channel.send(f"{nm} created an invite ")

@client.event
async def on_message(message):
    if message.author.id == client.id:
        return
    ret = ""
    cont = message.content
    for m in re.finditer(st,cont):
        ret+="\n"+cont[m.start:m.end]
    if not len(ret):
        await message.channel.send(ret)

client.run(TOKEN)
