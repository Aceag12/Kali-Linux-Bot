import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import colorsys
import random
import platform
from discord import Game, Embed, Color, Status, ChannelType
import os
import functools
import time
import datetime
import requests
import json
import aiohttp
from discord.utils import get
from discord.voice_client import VoiceClient
from random import choice, shuffle

commandprefix = "="

client = commands.Bot(command_prefix=commandprefix)
client.remove_command('help')


async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='with ' + str(len(set(client.get_all_members())))+' members'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='in ' + str(len(client.servers))+' servers'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name="for =help"))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name="in LINUX"), status=discord.Status("idle"))
        await asyncio.sleep(5)

@client.event
async def on_ready():
    ...
    client.loop.create_task(status_task())   
    print('BOT_IS_ONLINE')

@client.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            embed.title = "{} just twitted: {}".format(usernamename, txt)
            await client.say(embed=embed)

@client.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member=None, *, nickname=None):
    member = user.name
    if user is None:
      await client.say('Please tag a person to change nickname. Example- `` =setnick @user/all <new nickname>``')
      return
    else:
      await client.change_nickname(user, nickname)
      await client.delete_message(ctx.message)

@client.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_nicknames=True)     
async def resetnick(ctx, user: discord.Member=None):
    member = user.name
    if user is None:
      await client.say('Please tag a person to reset nickname. Example- ``=resetnick @user/all``')
      return
    else:
      nick = user.name
      await client.change_nickname(user, nick)
      await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def hack(ctx,user: discord.Member=None,*,hack=None):
    nome = ctx.message.author
    if not hack:
        hack = 'KALI'
    else:
        hack = hack.replace(' ','_')
    channel = ctx.message.channel
    x = await client.send_message(channel, '``[▓▓▓                    ] / {}-Starting Hacking Tool.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-Starting Hacking Tool..``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {}-Hacking Tool Started...``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-Starting to hack user.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-Searching fb password of user..``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-Searching discord password of user.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {}-Antivirus Detected in users system...``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] \ {}-Blocking Antivirus in users system....``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Hacking Done {}- Discord Hacker``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Downloading Files  |``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Downloading Files..  /``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Files Downloaded... -``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Showing Results....\``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``check your DMs``')
    await client.delete_message(x)
    await client.delete_message(ctx.message)
        
    if user:
        await client.send_message(nome, 'I Found This:-\n FB password- iamgoodboi576 \n Discord password- discorddontsuckatall525 \n '.format(hack,user.name))
        await client.send_message(user,'**Alert!**\n``You may have been hacked. Change your passwords now.``'.format(hack))
    else:
        await client.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
        await client.send_message(name,'**Alert!**\n``You are hacked. Change your passwords right now.``'.format(hack))

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setupserver(ctx):
    author = ctx.message.author
    server = ctx.message.server
    mod_perms = discord.Permissions(manage_messages=True, kick_members=True, manage_nicknames =True,mute_members=True)
    admin_perms = discord.Permissions(ADMINISTRATOR=True)
    await client.delete_message(ctx.message)
    await client.create_role(author.server, name="Owner", permissions=admin_perms)
    await client.create_role(author.server, name="Head Admin", permissions=admin_perms)
    await client.create_role(author.server, name="Admins", permissions=mod_perms)
    await client.create_role(author.server, name="YouTubers")
    await client.create_role(author.server, name="Moderators", permissions=mod_perms)
    await client.create_role(author.server, name="Muted")
    await client.create_role(author.server, name="Friends")
    await client.create_role(author.server, name="Members")
    await client.create_role(author.server, name="Bots", permissions=admin_perms)
    await client.say('Roles were created successfully!')
    
    everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    user_perms = discord.PermissionOverwrite(read_messages=True)
    user = discord.ChannelPermissions(target=server.default_role, overwrite=user_perms)
    private_perms = discord.PermissionOverwrite(read_messages=False)
    private = discord.ChannelPermissions(target=server.default_role, overwrite=private_perms)
    await client.create_channel(server, '★彡-welcome-bye彡★',everyone)
    await client.create_channel(server, '〚📜〛rules',everyone)
    await client.create_channel(server, '〚📣〛announcements',everyone)
    await client.create_channel(server, '〚📃〛info',everyone)
    await client.create_channel(server, '〚🎁〛giveaways',everyone)
    await client.create_channel(server, '〚🎥〛uploads',everyone)
    await client.create_channel(server, '〚💭〛chit-chat',user)
    await client.create_channel(server, '〚🌏〛foreign-chat',user)
    await client.create_channel(server, '〚🤖〛bot-commands',user)
    await client.create_channel(server, '〚💻〛media-chat',user)
    await client.create_channel(server, '〚😂〛memes',user)
    await client.create_channel(server, '〚🌐〛self-promotion',user)
    await client.create_channel(server, '〚🎶〛music-zone',user)
    await client.create_channel(server, '🎧music-1', type=discord.ChannelType.voice)
    await client.create_channel(server, '🎧music-2', type=discord.ChannelType.voice)
    await client.create_channel(server, '〚💭〛chat-for-staffs',private)
    await client.create_channel(server, '〚📑〛server-logs',private)
    await client.say('I have done setup!')

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def serverinfo(ctx):

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: 
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Server Owner__', value = str(server.owner) + "\n **__Owner's ID__**  " + server.owner.id);
    join.add_field(name = '__Server ID__', value = str(server.id))
    join.add_field(name = '__Members Count Of This Server__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels in this server__', value = str(channelz));
    join.add_field(name = '__Available Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Server was Created on: %s'%time);

    return await client.say(embed = join);

@client.command(pass_context = True)
async def deletechannel(ctx, channel: discord.Channel=None):
    if channel is None:
        await client.delete_channel(ctx.message.channel)
        await client.send_message(ctx.message.author, "{} channel has been deleted in {}".format(ctx.message.channel.name, ctx.message.server.name))
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            await client.delete_channel(channel)
            await client.say("{} channel has been deleted.".format(channel.name))

        
@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!") 
    
@client.command(pass_context = True)
async def roll(ctx):
    choices = ['1', '2', '3', '4', '5', '6', 'Nothing']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='You Rolled', description=random.choice(choices))
    em.set_thumbnail(url='https://media.giphy.com/media/3oGRFlpAW4sIHA02NW/giphy.gif')
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)
@client.command(pass_context = True)
async def charliecharlie(ctx):
    choices = ['Yes!', 'No!']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Charlie Charlie answer', description=random.choice(choices))
    em.set_thumbnail(url='https://media.giphy.com/media/YARUMKaGd8cRG/giphy.gif')
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)    
@client.command(pass_context = True)
async def howgay(ctx):
    choices = ['10%', '20%', '30%', '40%', '50%', '60%', '70%','80%', '90%', '100%', 'You Are Not Gay!']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Gay Percentage', description=random.choice(choices))
    em.set_thumbnail(url='https://media.giphy.com/media/GjqgnbGhNPx0A/giphy.gif')
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)    
@client.command(pass_context = True)
async def toss(ctx):
    choices = ['Head', 'Tail', 'Nothing']
    color = discord.Color(value=0x00ff00)
    em=discord.Embed(color=color, title='You Just Flipped a coin!')
    em.description = random.choice(choices)
    em.set_thumbnail(url='https://media.giphy.com/media/4Hkd9l8OqFd61s1OfG/giphy.gif')
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)
@client.command(pass_context = True)
async def addchannel(ctx, channel: str=None):
    server = ctx.message.server
    if channel is None:
        await client.say("Please specify a channel name")
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**Sorry! You do not have permission to use this command**')
            return
        else:
            everyone_perms = discord.PermissionOverwrite(send_messages=None, read_messages=None)
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
            await client.create_channel(server, channel, everyone)
            await client.say("{} channel has been created.".format(channel))
@client.command(pass_context = True)
async def dmsall(ctx, *, msg: str):
    for server_member in ctx.message.server.members:
      await client.send_message(server_member, msg)
      await client.delete_message(ctx.message)
@client.command(pass_context = True)
async def lock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await client.say("Channel locked by: {}".format(ctx.message.author))
    else:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("Channel was locked by: {}".format(ctx.message.author))
@client.command(pass_context = True)
async def setupwelcome(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, '★彡-welcome-bye彡★',everyone)	
@client.command(pass_context = True)
async def unlock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=None, read_messages=True)
    if not channelname:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
            await client.say("Channel was unlocked by: {}".format(ctx.message.author))
    else:
        if ctx.message.author.server_permissions.kick_members == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("Channel was unlocked by: {}".format(ctx.message.author))
@client.command(pass_context = True)
async def say(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if ctx.message.author.bot:
        return
    if not msg: await client.say("**What Do You Want Me To Say?** eg:- `` =say <your text here>``")
    else: await client.say(msg)
    return

@client.command(pass_context = True)
async def help(ctx):
    if ctx.message.author.bot:
      return
    else:
      author = ctx.message.author
      r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
      embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
      embed.set_author(name='Help')
      embed.add_field(name = '**Help**',value ='```My Prefix is = and my Commands are as follows:-\n announce\n rank \n reminder\n coins (Note:- Coins depends upon your  level.)\n purge <1-100>(ADMIN)\n botinfo\n ban(ADMIN)\n clearwarn(ADMIN)\n warn(ADMIN)\n kick(ADMIN)\n mute(ADMIN)\n unmute(ADMIN)\n charliecharlie \n userinfo(ADMIN)\n meme \n ping \n toss \n roll \n howgay \n hack \n virus \n addrole(ADMIN)\n deleterole(ADMIN)\n addchannel(ADMIN)\n tweet \n deletechannel(ADMIN)\n setnick(ADMIN)\n resetnick(ADMIN)\n invite-For inviting me to your server\n setupwelcome-To Setup Welcomer(ADMIN)\n say\n serverinvite-Link Of my official server\n invites\n serverinfo```',inline = False)
      dmmessage = await client.send_message(author,embed=embed)
      msg = (':incoming_envelope: Check your DMs For Information')
      await client.say(msg)
      await asyncio.sleep(30)
      await client.delete_message(dmmessage)
@client.command(pass_context = True)
async def announce(ctx, channel: discord.Channel=None, *, msg: str=None):
    member = ctx.message.author
    if channel is None or msg is None:
        await client.say('Invalid Command. Use this command like ``=announce text here``')
        return
    else:
        if member.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed=discord.Embed(title="Announcement", description="{}".format(msg), color = discord.Color((r << 16) + (g << 8) + b))
            await client.send_message(channel, embed=embed)
            await client.delete_message(ctx.message)
            
@client.command(pass_context = True)
async def setupsuggestion(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, '彡suggestions彡',everyone)
@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name == '★彡-welcome-bye彡★':
            embed = discord.Embed(title=f'Welcome {member.name} to {member.server.name}', description='Do not forget to check #rules and never try to break any one of them. Thank You.', color = 0x36393E)
            embed.add_field(name='__Thanks for joining__', value='**Hope you will be active here.**', inline=True)
            embed.set_thumbnail(url='https://media.giphy.com/media/jF1oqkXJL0Mda/giphy.gif') 
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            embed.add_field(name='Time of joining', value=member.joined_at)
            await asyncio.sleep(0.4)
            await client.send_message(channel, embed=embed)
@client.command(pass_context=True)
async def embedtext(ctx, *args):
    argstr = " ".join(args)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    text = argstr
    color = discord.Color((r << 16) + (g << 8) + b)
    await client.send_message(ctx.message.channel, embed=Embed(color = color, description=text))
    await client.delete_message(ctx.message)            

@client.command(pass_context = True)
async def addrole(ctx,*, role:str=None):
    user = ctx.message.author
    if user.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    if discord.utils.get(user.server.roles, name="{}".format(role)) is None:
        await client.create_role(user.server, name="{}".format(role), permissions=discord.Permissions.none())
        await client.say("{} role has been added.".format(role))
        return
    else:
        await client.say("{} role is already exists.".format(role))
@client.command(pass_context = True)
async def roleinfo(ctx,*, role:discord.Role=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("No such role found")
        return
    if ctx.message.author.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title="{}'s info".format(role.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url = ctx.message.server.icon_url)
        embed.add_field(name="Name", value=role.name, inline=True)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Created", value=role.created_at.strftime("%d %b %Y %H:%M"))
        await client.say(embed=embed)
@client.command(pass_context = True)
async def deleterole(ctx,*, role: discord.Role = None):
    user = ctx.message.author
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("There is no role with this name in this server")
    if ctx.message.author.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    else:
        await client.delete_role(ctx.message.server, role)
        await client.say(f"{role} role has been deleted")
@client.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == '★彡-welcome-bye彡★':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f'{member.name} just left {member.server.name}', description='Bye bye! We will miss you..', color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name='__User left__', value='**Hope you will be back soon.**', inline=True)
            embed.add_field(name='Your join position was', value=member.joined_at)
            embed.set_thumbnail(url=member.avatar_url)
            await client.send_message(channel, embed=embed)        
@client.command(pass_context=True)
async def virus(ctx,user: discord.Member=None,*,hack=None):
    nome = ctx.message.author
    if not hack:
        hack = 'KALI'
    else:
        hack = hack.replace(' ','_')
    channel = ctx.message.channel
    x = await client.send_message(channel, '``[▓▓▓                    ] / {}-discordvirus.exe Packing files.``'.format(hack))
    await asyncio.sleep(1.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-discordvirus.exe Packing files..``'.format(hack))
    await asyncio.sleep(0.3)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {}-discordvirus.exe Packing files...``'.format(hack))
    await asyncio.sleep(1.2)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-discordvirus.exe is Initializing code.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-discordvirus.exe is Initializing code..``'.format(hack))
    await asyncio.sleep(1.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-discordvirus.exe Finishing.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {}-discordvirus.exe Finishing..``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Successfully downloaded {}-virus.exe``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Injecting virus.   |``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus..  /``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus... -``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus....\``')
    await client.delete_message(x)
    await client.delete_message(ctx.message)
        
    if user:
        await client.say('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
        await client.send_message(user,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
    else:
        await client.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
        await client.send_message(name,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
@client.command(pass_context = True)
async def invite(ctx):
        embed=discord.Embed(title="**GLAD TO JOIN YOUR SERVER**", description="https://discordapp.com/api/oauth2/authorize?client_id=545585329990795274&permissions=2146958591&scope=bot".format(ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)    
@client.command(pass_context = True)
async def serverinvite(ctx):
        embed=discord.Embed(title="**JOIN OUR SUPPORT SERVER**", description="https://discord.gg/aERFDKP".format(ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)	
@client.command(pass_context = True)
async def botinfo(ctx):
        embed=discord.Embed(title="**INFO**", description="**Name- KALI**\n**Creator- Allipsters**\n\n**Bot Type- Public**\n**API- Discord.py**\n**command prefix- =**\n**For help- =help**\n**invite me by- =invite**".format(ctx.message.author), color=0x7289da)
        await client.say(embed=embed)        
@client.command(pass_context = True)
async def kick(ctx, userName: discord.User):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '519122918773620747':
        await client.kick(userName)
        embed=discord.Embed(title="**User Kicked Successfully!**", description="**The User was successfully Kicked!**".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Command not accepted!", description="Sorry! You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '519122918773620747':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        embed=discord.Embed(title="**User unmuted!**", description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
     else:
        embed=discord.Embed(title="Command not accepted!", description="Sorry! You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
	
@client.command(pass_context = True)
@commands.has_permissions(manage_messages = True)
async def purge(ctx, number: int):
  purge = await client.purge_from(ctx.message.channel, limit = number+1)
@client.command(pass_context = True)
async def cleartext(ctx, number: int):
    if ctx.message.author.id == '519122918773620747':
       purge = await client.purge_from(ctx.message.channel, limit = number+1)  
    else:
        await client.say('Looks like you are noob for that!')
@client.command(pass_context = True)
async def mute(ctx, member: discord.Member=None, mutetime=None):
     if ctx.message.author.server_permissions.administrator:
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.add_roles(member, role)
        embed=discord.Embed(title="**User muted!**", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
     else:
        embed=discord.Embed(title="Command not accepted!", description="Sorry! You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
@client.command(pass_context = True)
async def userinfo(ctx, user: discord.Member=None):
    if user is None:
      await client.say('Please tag a user to get user information. Example- ``=userinfo @user``')
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.kick_members == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
      embed = discord.Embed(title="{}'s info".format(user.name), description="Here is the detail of that user.", color = discord.Color((r << 16) + (g << 8) + b))
      embed.add_field(name="Name", value=user.mention, inline=True)
      embed.add_field(name="ID", value=user.id, inline=True)
      embed.add_field(name="Status", value=user.status, inline=True)
      embed.add_field(name="Highest role", value=user.top_role)
      embed.add_field(name="Color", value=user.color)
      embed.add_field(name="Playing", value=user.game)
      embed.add_field(name="Nickname", value=user.nick)
      embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
      embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
      embed.set_thumbnail(url=user.avatar_url)
      await client.say(embed=embed)
@client.command(pass_context=True)
async def kiss(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    randomurl = ["https://media3.giphy.com/media/G3va31oEEnIkM/giphy.gif", "https://i.imgur.com/eisk88U.gif", "https://media1.tenor.com/images/e4fcb11bc3f6585ecc70276cc325aa1c/tenor.gif?itemid=7386341", "http://25.media.tumblr.com/6a0377e5cab1c8695f8f115b756187a8/tumblr_msbc5kC6uD1s9g6xgo1_500.gif"]
    if user.id == ctx.message.author.id:
        await client.say("Goodluck kissing yourself {}".format(ctx.message.author.mention))
    else:
        embed = discord.Embed(title=f"{user.name} was kissed by {ctx.message.author.name}", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(randomurl))
        await client.say(embed=embed)
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, userName: discord.User=None,*, message:str=None): 
    if userName is None:
      await client.say('Please tag a person to warn user. Example- **=warn @user <reason>**')
      return
    else:
      await client.send_message(userName, "You have been warned for: **{}**".format(message))
      await client.say("***:white_check_mark: Alright! {0} Has Been Warned for {1}.*** ".format(userName,message))
      for channel in userName.server.channels:
        if channel.name == 'action-logs':
            embed=discord.Embed(title="User Warned!", description="{0} warned by {1} for {2}".format(userName, ctx.message.author, message), color=0x0521F6)
            await client.send_message(channel, embed=embed)
        else:
            return
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def clearwarn(ctx, userName: discord.User=None,*, message:str=None):  
  if userName is None:
      await client.say('Please tag a person to warn user. Example- ``=clearwarn @user``')
      return
  else:
      await client.send_message(userName, "Your have been cleared.".format(message))
      await client.say("***Warnings of {0} Has Been Cleared successfully.*** ".format(userName,message))           
@client.command(pass_context = True)
async def dms(ctx, user: discord.Member, *, msg: str):
   if user is None or msg is None:
       await client.say('Invalid command. Use this command like: ``=dms @user message``')
   if ctx.message.author.server_permissions.kick_members == False:
       await client.say('**You do not have permission to use this command**')
       return
   else:
       await client.send_message(user, msg)
       await client.delete_message(ctx.message)          
       await client.say("Success! Your DMS is done! :white_check_mark: ")
@client.command(pass_context = True)
async def ban(ctx, userName: discord.User):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '519122918773620747':
        await client.ban(userName)
        embed=discord.Embed(title="**User Banned Successfully!**", description="**The User was successfully Banned!**".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Command not accepted!", description="Sorry! You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
async def unban(ctx, identification:str):
    user = await client.get_user_info(identification)
    await client.unban(ctx.message.server, user)
    try:
        await client.say(f'`{user}` has been unbanned from the server.')
        for channel in ctx.message.server.channels:
          if channel.name == 'action-logs':
              embed=discord.Embed(title="User unbanned!", description="**{0}** unbanned by **{1}**!".format(user, ctx.message.author), color=0x38761D)
              await client.send_message(channel, embed=embed)
    except:
        await client.say(f'Unable to unban `{user}`')
        pass
@client.command(pass_context=True)
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await client.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await client.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = [':white_check_mark:', ':negative_squared_cross_mark:']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=question, description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        react_message = await client.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await client.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await client.edit_message(react_message, embed=embed)
@client.command(pass_context = True)
async def meme(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title='Random Meme', description='Random meme from reddit :joy:', color = discord.Color((r << 16) + (g << 8) + b))
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f'This meme was requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await client.say(embed=embed)
@client.command(pass_context = True)
async def time(ctx):
    timestamp = datetime.datetime.utcnow()
    await client.say(timestamp)
@client.command(pass_context=True)
async def invites(ctx, user:discord.Member=None):
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        if user is None:
            total_uses=0
            embed=discord.Embed(title='__Invites from {}__'.format(ctx.message.author.name), color = discord.Color((r << 16) + (g << 8) + b))
            invites = await client.invites_from(ctx.message.server)
            for invite in invites:
              if invite.inviter == ctx.message.author:
                  total_uses += invite.uses
                  embed.add_field(name='Invites',value=invite.id)
                  embed.add_field(name='Invites Used',value=invite.uses)
                  embed.add_field(name='Channel',value=invite.channel)
                  embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.add_field(name='__Total Uses__',value=total_uses)
            await client.say(embed=embed)
            if total_uses >= 10:
                role = discord.utils.get(ctx.message.server.roles, name='Pico Inviter')
                if role in ctx.message.author.roles:
                    return
                else:
                    await client.add_roles(ctx.message.author, role)
                    await client.say('Congrats! You have got ``pico inviter`` role.')
            if total_uses >= 20:
                role = discord.utils.get(ctx.message.server.roles, name='Micro Inviter')
                if role in ctx.message.author.roles:
                    return
                else:
                    await client.add_roles(ctx.message.author, role)
                    await client.say('Congrats! You have got ``Micro Inviter`` role.')
            if total_uses >= 40:
                role = discord.utils.get(ctx.message.server.roles, name='Mega Inviter')
                if role in ctx.message.author.roles:
                    return
                else:
                    await client.add_roles(ctx.message.author, role)
                    await client.say('Congrats! You have got ``mega inviter`` role')
            if total_uses >= 60:
                role = discord.utils.get(ctx.message.server.roles, name='Hyper Inviter')
                if role in ctx.message.author.roles:
                    return
                else:
                    await client.add_roles(ctx.message.author, role)
                    await client.say('Congrats! You have got ``hyper inviter`` role')
        else:
            total_uses=0
            embed=discord.Embed(title='__Invites from {}__'.format(user.name), color = discord.Color((r << 16) + (g << 8) + b))
            invites = await client.invites_from(ctx.message.server)
            for invite in invites:
              if invite.inviter == user:
                  total_uses += invite.uses
                  embed.add_field(name='Invite',value=invite.id)
                  embed.add_field(name='Uses',value=invite.uses)
                  embed.add_field(name='Channel',value=invite.channel)
                  embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.add_field(name='__Total Uses__',value=total_uses)
            await client.say(embed=embed)
            if total_uses >= 10:
                role = discord.utils.get(user.server.roles, name='Pico Inviter')
                if role in user.roles:
                    return
                else:
                    await client.add_roles(user, role)
                    await client.say(f'Congrats! {user.name}, You have got Pico inviter role')
            if total_uses >= 20:
                role = discord.utils.get(user.server.roles, name='Micro Inviter')
                if role in user.roles:
                    return
                else:
                    await client.add_roles(user, role)
                    await client.say(f'Congrats! {user.name} You have got Micro Inviter role')
            if total_uses >= 40:
                role = discord.utils.get(user.server.roles, name='Mega Inviter')
                if role in user.roles:
                    return
                else:
                    await client.add_roles(user, role)
                    await client.say(f'Congrats! {user.name} You have got Mega Inviter role')
            if total_uses >= 60:
                role = discord.utils.get(user.server.roles, name='Hyper Inviter')
                if role in user.roles:
                    return
                else:
                    await client.add_roles(user, role)
                    await client.say(f'Congrats! {user.name} You have got Hyper Inviter role')
        return


@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def totalbans(ctx):
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "Here Is The List of The Banned Members/Bots Of This Server", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)
@client.command(pass_context = True)
async def rank():
    return
@client.command(pass_context = True)
async def coins():
    return
@client.command(pass_context = True)
async def mymessages():
    return
@client.command(pass_context = True)
async def daily():
    return
@client.command(pass_context = True)
async def work():
    return
@client.command(pass_context = True)
async def join():
    return
@client.command(pass_context = True)
async def play():
    return
@client.command(pass_context = True)
async def leave():
    return

@client.command(pass_context=True)
async def reminder(ctx, time=None, *,remind=None):
    time =int(time)
    time = time * 60
    output = time/60
    await client.say("I will remind {} after {} minutes for {}".format(ctx.message.author.name, output, remind))
    await asyncio.sleep(time)
    await client.say("Reminder: {} You told {}".format(ctx.message.author.mention, remind))
    await client.send_message(ctx.message.author, "Reminder:- {}".format(remind))
@client.command(pass_context=True)
async def avatar(ctx, user:discord.Member=None):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='User Avatar')
    embed.set_thumbnail(url = ctx.message.author.avatar_url)
    await client.send_message(ctx.message.channel, embed=embed)

@client.command(pass_context=True)
async def ytsearch(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={new_message}"
    await client.say(url)        


@client.command(pass_context=True, aliases=['server'])
@commands.has_permissions(kick_members=True)
async def serverstats(ctx, *args):
    if ctx.message.channel.is_private:
        await bot.delete_message(ctx.message)
        return

    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    created = str(g.created_at)
    
    em = Embed(title="Server Stats")
    em.description =    "```\n" \
                        "Total Members:   %s (%s)\n" \
                        "Total Human Users:   %s (%s)\n" \
                        "Total Bots:    %s (%s)\n" \
                        "Server Created:   %s\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await client.send_message(ctx.message.channel, embed=em)
    await client.delete_message(ctx.message)	
                      
client.run(os.getenv('token'))
