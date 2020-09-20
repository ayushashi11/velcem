import os
import re
import ipa
import ai_m2
import discord
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("TOKEN2")
GUILD=int(os.getenv("GUILD"))
NCID=int(os.getenv("NCID"))
MID=int(os.getenv("MID"))
RID=int(os.getenv("RID"))
client = discord.Client()
o = True
st = re.compile(r"o<(\w)+>")
st_x = re.compile(r"x\/(\S)+\/")
guild = None
channel = None
id = 757192072208842773
roleg = {}
reportc = None

def get_role(guild, name):
    tc = discord.utils.find(lambda g: g.name==name, guild.roles)
    return tc

@client.event
async def on_ready():
    global o, guild, channel, roleg, reportc
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
    roleg = {
        "♂️":get_role(guild, "Pronouns:- he/him"),
        "♀️":get_role(guild, "Pronouns:- she/her"),
        "♐":get_role(guild, "Pronouns:- they/them"),
        "🅾️":get_role(guild, "Pronouns:- ask me/others"),
        "💻":get_role(guild, "Coder"),
        "🅰️":get_role(guild, "Linguist"),
        "🎼":get_role(guild, "Ezkenikqi")
    }
    for reportc in guild.channels:
        if reportc.id == RID:
            print("...")
            break
    else: raise RuntimeError("channel not found")
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    if not o:
        await channel.send("aadib kěwağaj!!")
        o = True
    members = '\n - '.join([member.name for member in guild.members])
    roles = '\n - '.join([role.name for role in guild.roles])
    print(f'Guild Members:\n - {members} \n \n{roles}')
    cs = '\n - '.join([channel.name+" "+str(channel.id) for channel in guild.channels])
    print(f"Channels:\n - {cs}")

@client.event
async def on_raw_reaction_add(reaction):
    print(reaction)
    if reaction.message_id != id:
        if reaction.emoji.name != "😠":
            return
        chan = discord.utils.find(lambda g: g.id==reaction.channel_id, guild.channels)
        message = discord.utils.find(lambda g: g.id==reaction.message_id, await chan.history(limit=25).flatten())
        ln=(discord.utils.find(lambda r: r.emoji == "😠", message.reactions)).count
        if ln>=3:
            await reportc.send(f"The message ||{message.content}|| by {message.author.mention} was flagged offensive.")
            await message.delete()
        return
    await reaction.member.add_roles(roleg[reaction.emoji.name])

@client.event
async def on_raw_reaction_remove(reaction):
    print(reaction)
    user = discord.utils.find(lambda g: g.id==reaction.user_id, guild.members)
    if reaction.message_id != id:
        return
    await user.remove_roles(roleg[reaction.emoji.name])

@client.event
async def on_member_join(member):
    for guild in client.guilds:
        if guild.id == GUILD:
            break
    for channel in guild.channels:
        if channel.id == NCID:
            break
    #await channel.send(f'{member.mention}, aadib and welcome!')
    embedVar = discord.Embed(title="Aadib noowědyoone!", description=f"{member.name} joined the sever", color=0x00ff00)
    print(member.avatar_url)
    embedVar.set_author(name="solcěm")
    embedVar.set_thumbnail(url=member.avatar_url)
    embedVar.add_field(name="Welcome", value="You can start by going to `#start`.\nAlso dont forget to write your introduction in this channel.", inline=False)
    await channel.send(embed=embedVar)
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
