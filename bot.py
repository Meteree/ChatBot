import discord
import aiohttp  # HTTP istekleri için gerekli
from config import token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Kullanıcı girişini algılamak için gerekli

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f' {client.user} sunucuya atmosferi delerek iniş yaptı')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="genel")  
    if channel:
        profile_picture_url = member.avatar.url if member.avatar else member.default_avatar.url

        async with aiohttp.ClientSession() as session:
            async with session.get(profile_picture_url) as response:
                if response.status == 200:
                    avatar_data = await response.read()
                    with open("avatar.png", "wb") as f:
                        f.write(avatar_data)

                    await channel.send(
                        f'Hoş geldin {member.mention}!', 
                        file=discord.File("avatar.png")
                    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run(token)
