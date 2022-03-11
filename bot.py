import os
import sys
import discord

if len(sys.argv) < 3:
    sys.exit()

# Getting the token and the serv from the args
TOKEN = sys.argv[1]
GUILD = sys.argv[2]

# Connecting to Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Log that the bot is succesfully connected."""
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to {guild.name}')
    

def get_avatar(author, serv=False):
    """Return an embedded message with the avatar from a given member and original message"""
    embed = discord.Embed(title=author.name)
    if serv and author.guild_avatar != None:
        embed.set_image(url = author.guild_avatar.url)   
    else:
        embed.set_image(url = author.avatar.url)
    return embed

def get_banner(user):
    """Return an embedded message with the banner from a given user and original message"""
    if user.banner != None:
        embed = discord.Embed(title=user.name)
        embed.set_image(url = user.banner.url)   
        return embed
    return None


async def send_avatar(message, member, serv):
    """Construct an embedded avatar message and send it."""
    embedAvatar = get_avatar(member, serv)
    await message.channel.send(embed=embedAvatar)

async def send_banner(message, user):
    """Construct an embedded banner message and send it."""
    embedBanner = get_banner(user)
    if embedBanner == None:
        await message.channel.send(f'{user.name} n\'a pas de banner, pour moi...')
    else:
        await message.channel.send(embed=embedBanner)


@client.event
async def on_message(message):
    """Receipt the new message event from the server."""

    # Ignore bot messages
    if message.author == client.user:
        return

    # Getting server info
    guild = discord.utils.get(client.guilds, name=GUILD)

    cmd = message.content.split()
    if len(cmd) > 0:
        if cmd[0] == '!kiyovatar':

            # Local server avatar (nitro) or not
            serv = False
            if len(cmd) >= 2:
                serv = cmd[1] == 'serv'

            # If the command ping some users
            if len(message.mentions) > 0:
                for member in message.mentions:
                    await send_avatar(message, member, serv)

            # Else if some users are gave just by plain text
            elif (len(cmd) > 1  and not serv) or (len(cmd) > 2 and serv):
                start = 1 if serv else 2
                args = cmd[start:]
                for arg in args:
                    foundMember = guild.get_member_named(arg)
                    if foundMember != None:
                        await send_avatar(message, foundMember, serv)

            # The command is for self usage.
            else:
                await send_avatar(message, message.author, serv)

        elif cmd[0] == '!kiyobanner':
            # If the command ping some users
            if len(message.mentions) > 0:
                for member in message.mentions:
                    user = await client.fetch_user(member.id)
                    await send_banner(message, user)

            # Else if some users are gave just by plain text
            elif len(cmd) > 1:
                args = cmd[1:]
                for arg in args:
                    foundMember = guild.get_member_named(arg)
                    if foundMember != None:
                        user = await client.fetch_user(foundMember.id)
                        await send_banner(message, user)

            # The command is for self usage.
            else:
                user = await client.fetch_user(message.author.id)
                await send_banner(message, user)


client.run(TOKEN) # Run the bot
