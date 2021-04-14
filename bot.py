import discord 
from discord.ext import commands 
import datetime
import asyncio
import config, os
import time, random, math

    
#Bot (our bot)
bot = commands.Bot(command_prefix=commands.when_mentioned_or('a!', 'A!')) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')


@bot.event
async def on_ready():
    #Message that will be sent when the bot is online.
    print('Bot started succesfully')
    general_channel = bot.get_channel(config.Channels.botChannel)
    await general_channel.send('Hi, I am online again.')
    #Status
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers', emoji=None, type=discord.ActivityType.listening))


@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.BotMissingPermissions) or isinstance(error, commands.CommandNotFound) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError):
        pass
    else:
        embed = discord.Embed(description='**Error!** '+str(error), colour=config.Colors.red)
        await ctx.send(embed=embed)

@bot.event
async def on_command(ctx):
    channel = bot.get_channel(config.Channels.logCommandsChannel)
    embed = discord.Embed(description=f'{ctx.guild.name} - {ctx.author} | {ctx.message.clean_content}', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await channel.send(embed=embed) 


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel):
        if not message.author.bot:                
            channel = bot.get_channel(config.Channels.DMsChannel)
            embed = discord.Embed(title=f'{message.author.name} sent a DM!', description=message.content, colour=config.Colors.orange, timestamp=message.created_at)
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            await channel.send(embed=embed)
    await bot.process_commands(message)


####################################################################################################
####################################################################################################
##Info Commands



@bot.command(name='announce', aliases=['announcement', 'ann'])
@commands.has_permissions(administrator=True)
async def announce(ctx, channelA: discord.TextChannel=None):
    if channelA:
        try:
            botMsg = await ctx.send('Please provide the title for your announcement!')
            await ctx.message.delete()
            newTitle = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=120)
            await newTitle.delete()

            if newTitle.content == 'a!none':
                await botMsg.edit(content='Now provide the message or description of your announcement!')

                newContent = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=200)
                await newContent.delete()

                if newContent.content == 'a!none':
                    embed = discord.Embed(description='**Error!** You cannot make an announcement without a title and description.', colour=config.Colors.red)
                    await botMsg.edit(content='', embed=embed)
                    return

                if newContent.content == 'a!cancel':
                    await botMsg.edit(content='Announcement cancelled succesfully.')
                    return
                else:
                    await botMsg.edit(content='Preparing to make the announcement...')
                    
                    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
                    aEmbed = discord.Embed(description=newContent.content, colour=random.choice(randomColors)) 
                    print(f'Preparing announcement... Description: {newContent.content}, Channel: {channelA.id}')
                    aChannel = bot.get_channel(channelA.id)
                    await asyncio.sleep(2)
                    await aChannel.send(embed=aEmbed)
                    await botMsg.edit(content='Announcement sent succesfully.')
                    await botMsg.add_reaction(config.Emojis.whiteCheckMark)
                    return

            if newTitle.content == 'a!cancel':
                await botMsg.edit(content='Announcement cancelled succesfully.')
                return

            else:      
                await botMsg.edit(content='Now provide the message or description of your announcement!')

                newContent = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=200)
                await newContent.delete()

                if newContent.content == 'a!none':

                    await botMsg.edit(content='Preparing to make the announcement...')
                    
                    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
                    aEmbed = discord.Embed(title=newTitle.content, colour=random.choice(randomColors)) 
                    print(f'Preparing announcement... Title: {newTitle.content}, Channel: {channelA.id}')
                    aChannel = bot.get_channel(channelA.id)
                    await asyncio.sleep(2)
                    await aChannel.send(embed=aEmbed)
                    await botMsg.edit(content='Announcement sent succesfully.')
                    await botMsg.add_reaction(config.Emojis.whiteCheckMark)
                    return

                if newContent.content == 'a!cancel':
                    await botMsg.edit(content='Announcement cancelled succesfully.')
                    return

                else:

                    await botMsg.edit(content='Preparing to make the announcement...')
                    
                    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
                    aEmbed = discord.Embed(title=newTitle.content, description=newContent.content, colour=random.choice(randomColors)) 
                    print(f'Preparing announcement... Title: {newTitle.content}, Description: {newContent.content}, Channel: {channelA.id}')
                    aChannel = bot.get_channel(channelA.id)
                    await asyncio.sleep(2)
                    await aChannel.send(embed=aEmbed)
                    await botMsg.edit(content='Announcement sent succesfully.')
                    await botMsg.add_reaction(config.Emojis.whiteCheckMark)
                    return


        except asyncio.TimeoutError:
            print('Timeout in announce command')
            await botMsg.edit(content="You didn't send your message in time, please try again!")
            return
        
        except Exception:
            await botMsg.edit(content='An error ocurred while running the command.')
            await botMsg.add_reaction(config.Emojis.noEntry)
            return 
    else:
        await ctx.send('Please specify a channel!')
        return


@announce.error
async def announce_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** Only administrators of this server can use that command!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='avatar', aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(title = f'Avatar of user {member}', colour=config.Colors.green, timestamp=ctx.message.created_at)
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)



@bot.command(name='help', aliases=['h'])
async def help(ctx, arg = None):
    if arg == None:
        helpEmbed = discord.Embed(title = 'Help | Prefix: `a!`, `A!`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        helpEmbed.add_field(name='Info commands', value='`about`, `announce`, `avatar`, `help`, `id`, `invite`, `membercount`, `ping`, `remind`, `report`, `suggest`, `userinfo`')
        helpEmbed.add_field(name='Math commands', value='`mathadd`, `mathdiv`, `mathmult`, `mathrandom`, `mathsq`, `mathsqrt`, `mathsub`')
        helpEmbed.add_field(name='Moderation commands', value='`ban`, `kick`, `mute`, `pmute`, `purge`, `unban`, `unmute`')
        helpEmbed.add_field(name='Owner commands', value='`DM`, `save`, `say`')
        helpEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=helpEmbed)
        return
    else:
        embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{getattr(config.AliasesCommands, arg)}`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
        embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
        embed.add_field(name='Required permissions', value='`'+getattr(config.RequiredPermissions, arg)+'`', inline=False)
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return



@bot.command(name='id', aliases=['ID'])
async def id(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await ctx.send(member.id)



@bot.command(name='info', aliases=['about'])
async def info(ctx):
    embedI = discord.Embed(title=f'Information about Al3xis#4614', colour=config.Colors.blue, timestamp=ctx.message.created_at)
    embedI.set_author(name='Al3xis')
    embedI.add_field(name='Owner', value='`Alex22#7756`')
    embedI.add_field(name='Current Version', value='__[v1.3.5](https://github.com/Alex0622/Al3xis-Bot-dev/releases/tag/v1.3.5)__')
    embedI.add_field(name='Guilds', value=f'`{len(bot.guilds)}`')
    embedI.add_field(name='Prefix', value='`a!`, `A!`')
    embedI.add_field(name='Developed since', value='`21/10/2020`')
    embedI.add_field(name='Developed with', value='`Python`')
    embedI.add_field(name='GitHub link', value='[here](https://github.com/Alex0622/Al3xis-Bot-dev/)')
    embedI.add_field(name='Important', value='Use `a!help` to get the list of available commands and `a!invite` to invite the bot or join our Discord server. \n If you find any bug please use `a!report` and if you have a suggestion about the bot use `a!suggest`.', inline=False)
    embedI.set_thumbnail(url=ctx.me.avatar_url)
    embedI.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embedI)



@bot.command(name='invite', aliases=['inv'])
async def invite(ctx):
    embed = discord.Embed(title='Links', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
    embed.add_field(name='Join our Discord server!', value="[Alex's bots](https://discord.gg/AAJPHqNXUy)", inline=False)
    embed.add_field(name='Invite the bot to your server', value='[Admin permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=8) \n[Required permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=2081287413)')
    embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)



@bot.command(name='membercount')
async def membercount(ctx):
    embed = discord.Embed(description=f'There are **{ctx.guild.member_count} members** in this server.', colour=config.Colors.lightBlue)
    await ctx.send(embed=embed)



@bot.command(name='ping', aliases=['pong', 'latency'])
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    time.sleep(2)
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**Bot's ping:**  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


    
@bot.command(name='reminder', aliases=['remind'])
async def reminder(ctx, time=None, *, msg=None):
    if time != None:
        if msg != None:
            await asyncio.sleep(0.5)
            seconds = 0
            if time.lower().endswith("d"):
                seconds += int(time[:-1]) * 60 * 60 * 24
                counter = f"{seconds // 60 // 60 // 24} days"
            elif time.lower().endswith("h"):
                seconds += int(time[:-1]) * 60 * 60
                counter = f"{seconds // 60 // 60} hours"
            elif time.lower().endswith("m"):
                seconds += int(time[:-1]) * 60
                counter = f"{seconds // 60} minutes"
            elif time.lower().endswith("s"):
                seconds += int(time[:-1])
                counter = f"{seconds} seconds"
            else:
                embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                await ctx.send(embed=embed)
                return  

            await ctx.send(f"I've set a reminder of {counter}: {msg}", allowed_mentions=discord.AllowedMentions.none())
            await asyncio.sleep(seconds)
            await ctx.reply(f'Hey! {msg}', mention_author=True, allowed_mentions=discord.AllowedMentions.none())
        else: 
            embed = discord.Embed(description="Please provide a message for your reminder.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="Please provide a period of time for your reminder.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@reminder.error
async def reminder_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(description=f"You set a reminder but probably deleted your message so I can't reply to it.", colour=config.Colors.red)
        await ctx.send(str(f'Hi {ctx.author.mention}!'),embed=embed)
        return



@bot.command(name='report')
async def report(ctx, *, msg=None):
    if msg != None:
        botMsg = await ctx.send(f'Saving report {config.Emojis.loading}')
        await asyncio.sleep(2)
        embed = discord.Embed(title=f'Report made by {ctx.author.name}', description=msg, colour=config.Colors.purple, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        print(f'{ctx.author} reported: {msg}')
        channel = bot.get_channel(config.Channels.reportsChannel)
        await channel.send(embed=embed)
        
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await botMsg.edit(content='Your report has been sent successfully!')

    else:
        embed = discord.Embed(description="Please provide a description for your report.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



suggestion = ''
listSuggestions = ''
@bot.command(name='suggest', aliases=['sug'])
async def suggest(ctx, *, new_suggestion):
    try:
        global suggestion
        suggestion =  new_suggestion
        description = suggestion 
        msg = await ctx.send('Saving suggestion...')

        time.sleep(2)
        embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description=description, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id)
        suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
        message = await suggestions_channel.send(embed=embed)
        await message.add_reaction(config.Emojis.ballotBoxWithCheck)
        await message.add_reaction(config.Emojis.x)
        print('New suggestions | ' + suggestion)
        
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await msg.edit(content=f'**{ctx.author}**, your suggestion has been submited: {suggestion}', allowed_mentions=discord.AllowedMentions.none())
    except Exception:
        await ctx.send('An error ocurred while running the command.')
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return

@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please add a suggestion in your message.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='userinfo', aliases=['user', 'ui'])
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    try:
        mentions = []
        for role in member.roles:
            if role.name != "@everyone":
                mentions.append(role.mention)
        roleS = ", ".join(mentions)

        if roleS == '':
            ROLES = f'No roles to show here {config.Emojis.eyes}'
        else:
            ROLES = roleS

        if member.bot:
            isBotMsg = 'Yes'
        else:
            isBotMsg = 'No'

        userinfoEmbed = discord.Embed(title=str(member), description=f'__**Information about**__ {member.mention} \n**User ID**: {member.id} \n**Created at** {member.created_at.strftime("%A %d %B %Y, %H:%M")} \n**Joined at** {member.joined_at.strftime("%A %d %B %Y, %H:%M")} \n **Bot?**: {isBotMsg}', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
        userinfoEmbed.set_thumbnail(url=member.avatar_url)
        userinfoEmbed.add_field(name='**Roles**', value=ROLES)
        await ctx.send(embed=userinfoEmbed)
    except Exception:
        await ctx.send('An error ocurred while executing the command.')
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return



####################################################################################################
####################################################################################################
#Math commands


def add(x:float, y:float):
    return x + y
def sub(x:float, y:float):
    return x - y
def mult(x:float, y:float):
    return x * y
def div(x:float, y:float):
    return x / y
def rando(x:int, y:int):
    return random.randint(x, y)
def sqrt(x:float):
    return math.sqrt(x)
def sq(x:float):
    return x * x


@bot.command(name='mathadd')
async def mathadd(ctx, x:float=None, y:float=None):
    if x != None:
        if y != None:
            result = add(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return    



@bot.command(name='mathdiv')
async def mathdiv(ctx, x:float=None, y:float=None):
    if x != None:
        if y != None:
            result = div(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 
   



@bot.command(name='mathmult')
async def mathmult(ctx, x:float=None, y:float=None):
    if x != None:
        if y != None:
            result = mult(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return    




@bot.command(name='mathrandom')
async def mathrandom(ctx, x:int=None, y:float=None):
    if x != None:
        if y != None:
            result = rando(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 


@mathrandom.error
async def mathrandom_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(description='The order of your values must be from lowest to highest. \n Note: Only use numbers.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  



@bot.command(name='mathsq')
async def mathsq(ctx, x:float=None):
    if x != None:      
        result = sq(x)
        await ctx.reply(result, mention_author=False)
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  



@bot.command(name='mathsqrt')
async def mathsqrt(ctx, x:float=None):
    if x != None:          
        result = sqrt(x)
        await ctx.reply(result, mention_author=False)
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  



@bot.command(name='mathsub')
async def mathsub(ctx, x:float=None, y:float=None):
    if x != None:
        if y != None:
            result = sub(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 



####################################################################################################
####################################################################################################
##Moderation commands


@bot.command(name='ban')
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)    
                        await ctx.send(f'**{member}** was banned | `{reason}`')
                        try:
                            await member.send(f'You were banned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.ban(reason=f'{ctx.author}: {reason}')
                        print(f'User {ctx.author} banned {member} | {reason}')
                        logEmbed = discord.Embed(title=f'Case: `ban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception:
                        await ctx.send('An error ocurred while runnining the command.')
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to ban that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't ban me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't ban yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to ban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='kick', pass_context=True)
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)
                        await ctx.send(f'**{member}** was kicked | `{reason}`')
                        try:
                            await member.send(f'You were kicked from server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.kick(reason=f'{ctx.author}: {reason}')
                        print(f'User {ctx.author} kicked {member} in server {guild.name}| {reason}')
                        logEmbed = discord.Embed(title=f'Case: `kick`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel = bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)       
                    except Exception:
                        await ctx.send('An error ocurred while runnining the command.') 
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to kick that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't kick me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't kick yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='mute')
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member, duration=None, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if not mutedRole in member.roles:
                            if duration:

                                try:
                                    time.sleep(0.5)
                                    seconds = 0
                                    if duration.lower().endswith("d"):
                                        seconds += int(duration[:-1]) * 60 * 60 * 24
                                        counter = f"{seconds // 60 // 60 // 24} days"
                                    elif duration.lower().endswith("h"):
                                        seconds += int(duration[:-1]) * 60 * 60
                                        counter = f"{seconds // 60 // 60} hours"
                                    elif duration.lower().endswith("m"):
                                        seconds += int(duration[:-1]) * 60
                                        counter = f"{seconds // 60} minutes"
                                    elif duration.lower().endswith("s"):
                                        seconds += int(duration[:-1])
                                        counter = f"{seconds} seconds"
                                    else:
                                        embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                                        await ctx.send(embed=embed)
                                        return 

                                    
                                    await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                    try:                    
                                        await ctx.send(f'**{member}** was muted for {counter} | `{reason}`')
                                    except Exception:
                                        pass
                                    await member.send(f'You were muted in server: **{guild.name}** for {counter} | `{reason}`')
                                    print(f'User {ctx.author} muted {member} in server {guild.name} for {counter} | {reason}')
                                    logEmbed = discord.Embed(title=f'Case: `mute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                    logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                                    logEmbed.add_field(name='User', value=member.mention)   
                                    logEmbed.add_field(name='Reason', value=reason) 
                                    logEmbed.add_field(name='Duration', value=counter)
                                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                    logChannel=bot.get_channel(config.Channels.logChannel)
                                    await logChannel.send(embed=logEmbed)   

                                    await asyncio.sleep(seconds) 

                                    
                                    await member.remove_roles(mutedRole, reason='Temporary mute completed!')
                                    reason = 'Temporary mute completed!'
                                    try:
                                        await member.send(f'You were unmuted in server: **{guild.name}** | `{reason}`')
                                    except Exception:
                                        pass
                                    print(f'User {member} was unmuted in server {guild.name} | {reason}')
                                    logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                    logEmbed.add_field(name='User', value=member.mention)
                                    logEmbed.add_field(name='Reason', value=reason) 
                                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                    logChannel=bot.get_channel(config.Channels.logChannel)
                                    await logChannel.send(embed=logEmbed)
                                    return
                                
                                except Exception:
                                    await ctx.send('An error ocurred while running the command.')
                                    await ctx.message.add_reaction(config.Emojis.noEntry)
                                    return
                            else:
                                embed = discord.Embed(description='Please specify an amount of time to mute that member.', colour=config.Colors.red)
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(description=f'**{member}** is already muted.', colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return
                    else:
                        embed = discord.Embed(description="**Error!** You don't have permissions to mute that member.", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="You can't mute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:   
        embed = discord.Embed(description='**Error!** This server does not have a Muted role. Please make one named `Muted`.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 



@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='pmute', aliases= ['pm'])
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def pmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'

    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if not mutedRole in member.roles:
                            try:
                                time.sleep(0.5)
                                await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                try:
                                    await ctx.send(f'**{member}** was permanently muted | `{reason}`')
                                except Exception:
                                    pass
                                await member.send(f'You were permanently muted in server: **{guild.name}** | `{reason}`')
                                print(f'User {ctx.author} permanently muted {member} in server {guild.name} | {reason}')
                                logEmbed = discord.Embed(title=f'Case: `mute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                                logEmbed.add_field(name='User', value=member.mention)
                                logEmbed.add_field(name='Reason', value=reason) 
                                logEmbed.add_field(name='Duration', value=f'Permanently')
                                logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                logChannel=bot.get_channel(config.Channels.logChannel)
                                await logChannel.send(embed=logEmbed)  
                                return

                            except Exception:
                                await ctx.send('An error ocurred while running the command.')
                                await ctx.message.add_reaction(config.Emojis.noEntry)
                                return

                        else:
                            embed = discord.Embed(description=f'**{member}** is already muted.', colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return 
                    else:
                        embed = discord.Embed(description=f"**Error!** You don't have permissions to mute that member!", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="You can't mute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:   
        embed = discord.Embed(description='**Error!** This server does not have a Muted role. Please make one named `Muted`.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return   


@pmute.error
async def pmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='purge', aliases=['clear'])
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 0):
    guild = ctx.guild
    if amount <= 500:
        if amount >=1:
            await ctx.channel.purge(limit=amount)
            e = discord.Embed(description=f'Deleted {amount} messages {config.Emojis.loading}', colour=config.Colors.red)
            botMsg = await ctx.send(embed=e)
            await asyncio.sleep(5)
            await botMsg.delete()
            logEmbed = discord.Embed(title=f'Case: `purge`', colour=config.Colors.orange, timestamp=ctx.message.created_at)
            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
            logEmbed.add_field(name='Channel', value=ctx.message.channel.mention)
            logEmbed.add_field(name='Deleted messages', value=f'{amount} message(s).')
            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
            logChannel=bot.get_channel(config.Channels.logChannel)
            await logChannel.send(embed=logEmbed)
            print(f'{ctx.message.author} deleted {amount} messages using the purge command in server {guild.name}.')
    if amount > 500:
        await ctx.send(f'You can only purge **500** messages at a time and you tried to delete **{amount}**.')
        print(f'{ctx.message.author} tried to delete {amount} messages with the purge command in server {guild.name}.')
        return
    if amount == 0:
        embed = discord.Embed(description='Select an amount of messages to purge.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE MESSAGES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE MESSAGES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='softban')
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def softban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)
                        await ctx.send(f'**{member}** was softbanned | `{reason}`')
                        try:
                            await member.send(f'You were softbanned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.ban(reason=f'{ctx.author}: {reason}', delete_message_days=5)
                        await member.unban(reason=f'{ctx.author}: softban')
                        print(f'User {ctx.author} softbanned {member} in server {guild.name}| {reason}')
                        logEmbed = discord.Embed(title=f'Case: `softban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel = bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)       
                    except Exception:
                        await ctx.send('An error ocurred while runnining the command.') 
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to softban that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't softban me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't softban yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@softban.error
async def softban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to softban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



@bot.command(name='unban') 
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, UserID: int, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    member = await bot.fetch_user(UserID)
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                try:
                    await ctx.guild.fetch_ban(discord.Object(id=member.id))
                    try:
                        time.sleep(0.5)
                        await ctx.guild.unban(member, reason=f'{ctx.author}: {reason}')
                        await ctx.send(f'**{member}** was unbanned | `{reason}`')
                        try:
                            await member.send(f'You were unbanned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        print(f'User {ctx.author} unbanned {member} from {guild.name} | {reason}')
                        logEmbed = discord.Embed(title=f'Case: `unban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception:
                        await ctx.send('An error ocurred while running the command.')
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                except discord.NotFound:
                    embed = discord.Embed(description='That user is not banned here.', colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return     
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="I'm not banned...", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You are not banned here...", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to unban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return




@bot.command(name='unmute')
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if mutedRole in member.roles:
                        try:
                            time.sleep(0.5)
                            await member.remove_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                            await ctx.send(f'**{member}** was unmuted | `{reason}`')
                            try:
                                await member.send(f'You were unmuted in server: **{guild.name}** | `{reason}`')
                            except Exception:
                                pass
                            print(f'User {ctx.author} unmuted {member} in server {guild.name} | {reason}')
                            logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                            logEmbed.add_field(name='User', value=member.mention)
                            logEmbed.add_field(name='Reason', value=reason) 
                            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                            logChannel=bot.get_channel(config.Channels.logChannel)
                            await logChannel.send(embed=logEmbed)     
                        except Exception:
                            await ctx.send('An error ocurred while running the command.')
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            return
                    else:
                        embed = discord.Embed(description=f'**{member}** is not muted.', colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return 
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else: 
                embed = discord.Embed(description="You can't unmute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't unmute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        await ctx.send("I can't find any muted role here. Guess nobody is muted.")
        return
 

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to unmute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return



####################################################################################################
####################################################################################################
##Owner commands



@bot.command(name='DM', aliases=['dm', 'msg'])
@commands.is_owner()
async def DM(ctx, member: discord.Member=None, *, msg=None):
    if member != None:
        if msg != None:
            botMsg = await ctx.send(f'DMing user {config.Emojis.loading}')
            await asyncio.sleep(2)
            embed = discord.Embed(description=msg, colour=config.Colors.orange)
            try:
                await member.send(embed=embed)
                logEmbed = discord.Embed(title=f'{ctx.author.name} has sent a DM to {member.name}', description=msg, colour=config.Colors.orange, timestamp=ctx.message.created_at)
                logEmbed.set_footer(text=member, icon_url=member.avatar_url)
                DMs_channel = bot.get_channel(config.Channels.DMsChannel)
                await DMs_channel.send(embed=logEmbed)
                await botMsg.edit(content=f'DM sent successfully! {config.Emojis.whiteCheckMark}')
            except Exception:
                errorEmbed = discord.Embed(description=f'**Error!** I could not send a DM to {member.name}.', colour=config.Colors.red)
                await botMsg.edit(content='', embed=errorEmbed)
                return
        
        else:
            embed = discord.Embed(description='Please provide a description for your embed.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description='Please specify a member to DM.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return




savedMessageSave = ''
@bot.command(name='save')
@commands.is_owner()
async def save(ctx,*, saveMsg=None):
    global savedMessageSave
    savedMessageSave = saveMsg
    if saveMsg == None:
        await ctx.send('Please provide a message to save!')
        return
    else:
        try:
            firstMessage = await ctx.send('Saving message...')
            await ctx.message.delete()
            time.sleep(3)
            embed = discord.Embed(title=f'{ctx.author} saved a new message.', description=savedMessageSave, colour=config.Colors.green, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Guild: {ctx.guild}')
            savedMessagesChannel = bot.get_channel(config.Channels.ownerChannel)
            await savedMessagesChannel.send(embed=embed)
            print(f'New message saved sent by {ctx.author} | {savedMessageSave}')
            await firstMessage.edit(content=f'**{ctx.author}** Your message has been saved!')
        except Exception:
            await ctx.send('An error ocurred while running the command.')
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return



@bot.command(name='say')
@commands.is_owner()
async def say(ctx, *, sayMsg=None):
    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
    if sayMsg == None:
        embed = discord.Embed(description=savedMessageSave, colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    else:
        embed = discord.Embed(description=sayMsg, colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return

    
  
################################
####################################################################################################
####################################################################################################
#Run the bot on Discord.
bot.run(os.environ['discordToken'])


