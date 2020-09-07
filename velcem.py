import ai_m2
import discord
TOKEN="NzUyMzYxNzI4MDM3MjI0NDQ4.X1Whdg.SWobGXljVtyul9FXxKswSSi2ciE"
GUILD=0
client = discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
