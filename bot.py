import discord
from discord.ext import commands 
import datetime
import asyncio
import config, os
import time, random, math
    
#Bot (our bot)
intents=discord.Intents.default()
intents.members=True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('a!', 'A!'), intents=intents) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')


@bot.event
async def on_ready():
    #Message that will be sent when the bot is online.
    print('Bot started succesfully')
    general_channel = bot.get_channel(config.Channels.botChannel)
    await general_channel.send('Hi, I am online again.')
    #Status
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        embed = discord.Embed(description='**Error!** I cannot find that user.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.ChannelNotFound):
        embed = discord.Embed(description='**Error!** I cannot find that channel.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.RoleNotFound):
        embed = discord.Embed(description=f'**Error!** I cannot find that role.', colour=config.Colors.red)
        await ctx.reply(embed=embed, mention_author=False)
        return
    if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.BotMissingPermissions) or isinstance(error, commands.errors.CommandNotFound) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError):
        pass  
    else:
        embed = discord.Embed(description='**Error!** '+str(error), colour=config.Colors.red)
        await ctx.send(embed=embed)

@bot.event
async def on_command(ctx):
    try:
        channel = bot.get_channel(config.Channels.logCommandsChannel)
        embed = discord.Embed(description=f'{ctx.guild.name} - {ctx.author} | {ctx.message.clean_content}', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)
    except Exception:
        pass 

@bot.event
async def on_message(message):
    if message.content == '<@!768309916112650321>':
        descriptionMsg = f'Hi!, my prefixes are `a!` and `A!`'
        infoEmbed = discord.Embed(description=descriptionMsg, colour=config.Colors.blue)
        await message.reply(embed=infoEmbed, mention_author=False)
        return
    if message.content == '<@768309916112650321>':
        descriptionMsg = f'Hi!, my prefixes are `a!` and `A!`'
        infoEmbed = discord.Embed(description=descriptionMsg, colour=config.Colors.blue)
        await message.reply(embed=infoEmbed, mention_author=False)
        return
    if message.guild == bot.get_guild(793987455149408309):
        for word in config.BadWords:
            if word in message.content.lower():
                embed = discord.Embed(description=f"{config.Emojis.noEntry} {message.author.mention} your message includes words that are not allowed here. {config.Emojis.noEntry}", colour=config.Colors.red)
                await message.delete()
                botMsg = await message.channel.send(embed=embed)
                logEmbed = discord.Embed(title=f'Message in #{message.channel} was deleted.', description=f'{message.content}\n __**Reason**: Message includes words that are not allowed here.__', colour=config.Colors.red, timestamp=message.created_at)
                logEmbed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
                logChannel = bot.get_channel(config.Channels.logChannel)
                await logChannel.send(embed=logEmbed)
                await asyncio.sleep(4)
                await botMsg.delete()

    if isinstance(message.channel, discord.channel.DMChannel):
        if not message.author.bot:                
            channel = bot.get_channel(config.Channels.DMsChannel)
            embed = discord.Embed(title=f'{message.author.name} sent a DM!', description=message.content, colour=config.Colors.orange, timestamp=message.created_at)
            embed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
            await channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.guild == bot.get_guild(793987455149408309):
        if not message.author.bot:
            logEmbed = discord.Embed(title=f'Message in #{message.channel} was deleted.', description=f'{message.content}', colour=config.Colors.red, timestamp=message.created_at)
            logEmbed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
            logChannel = bot.get_channel(config.Channels.logChannel)
            await logChannel.send(embed=logEmbed)

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(config.Channels.joinsleavesChannel)
    embed = discord.Embed(title='Al3xis was added to a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {guild.member_count}', colour=config.Colors.green)
    embed.set_footer(text=f'{len(bot.guilds)} guilds now', icon_url=guild.icon_url)
    await channel.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(config.Channels.joinsleavesChannel)
    embed = discord.Embed(title='Al3xis was removed from a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {guild.member_count}', colour=config.Colors.green)
    embed.set_footer(text=f'{len(bot.guilds)} guilds now', icon_url=guild.icon_url)
    await channel.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event
async def on_member_join(member):
    if member.guild == bot.get_guild(793987455149408309):
        memberRole = discord.utils.get(member.guild.roles, id=829793629236494417)
        await member.add_roles(memberRole, reason='Member Join Event')
        chatChannel = bot.get_channel(config.Channels.chatChannel)
        randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen, config.Colors.gray]
        embed = discord.Embed(description=f'Welcome {member.mention} to the **Alex\'s bots** server!', colour=random.choice(randomColors))
        await chatChannel.send(embed=embed)
        return
    else:
        return

@bot.event
async def on_member_remove(member):
    if member.guild == bot.get_guild(793987455149408309):
        chatChannel = bot.get_channel(config.Channels.chatChannel)
        randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen, config.Colors.gray]
        embed = discord.Embed(description=f'{member.mention} left the server.', colour=random.choice(randomColors))
        await chatChannel.send(embed=embed)
        return
    else:
        return

####################################################################################################
####################################################################################################
##Info Commands

@bot.command(name='about', aliases=['info'])
async def about(ctx):
    try:
        embedI = discord.Embed(title=f'Information about Al3xis#4614', colour=config.Colors.blue, timestamp=ctx.message.created_at)
        embedI.add_field(name='Owner', value='`Alex22#7756`')
        embedI.add_field(name='Current Version', value='__[v1.4.0](https://github.com/Alex0622/Al3xis-Bot-dev/releases/tag/v1.4.0)__')
        embedI.add_field(name='Guilds', value=f'`{len(bot.guilds)}`')
        embedI.add_field(name='Prefix', value='`a!`, `A!`')
        embedI.add_field(name='Developed since', value='`21/10/2020`')
        embedI.add_field(name='Developed with', value='`Python`')
        embedI.add_field(name='Useful links', value=f'[GitHub]({config.General.githubURL}) | [Support Server]({config.General.supportServerURL})) | [Top.gg](https://top.gg/bot/768309916112650321) | [Discord Bot List](https://discord.ly/al3xis)')
        embedI.add_field(name='Latest updates', value="New commands: say, embed, serverinfo, roleinfo, addrole, removerole.", inline=False)
        embedI.set_thumbnail(url=ctx.me.avatar_url)
        embedI.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embedI, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `about` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='help', aliases=['h'])
async def help(ctx, arg = None):
    try:
        if arg == None:
            helpEmbed = discord.Embed(title = 'Help | Prefix: `a!`, `A!`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            helpEmbed.add_field(name='Info', value='`about`, `help`, `invite`, `ping`, `report`, `source`, `suggest`, `vote`', inline=True)
            helpEmbed.add_field(name='Math', value='`calc`, `mathrandom`, `mathsq`, `mathsqrt`', inline=True)
            helpEmbed.add_field(name='Moderation', value='`addrole`, `ban`, `kick`, `mute`, `pmute`, `purge`, `removerole`, `unban`, `unmute`', inline=True)
            helpEmbed.add_field(name='Utility', value='`announce`, `avatar`, `embed`, `id`, `membercount`, `nick`, `reminder`, `roleinfo`, `say`, `servericon`, `serverinfo`, `userinfo`', inline=False)
            helpEmbed.add_field(name='Owner', value='`DM`, `logout`, `save`, `updatesuggestion`', inline=True)
            helpEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=helpEmbed, mention_author=False)
            return
        if str(arg).lower() == 'info':
            titleEmbed = 'Info commands'
            descEmbed = f'''
            `about` - {config.InfoCommands.about}
            `help` - {config.InfoCommands.help}
            `invite` - {config.InfoCommands.invite}
            `ping` - {config.InfoCommands.ping}
            `report` - {config.InfoCommands.report}
            `source` - {config.InfoCommands.source}
            `suggest` - {config.InfoCommands.suggest}
            `vote` - {config.InfoCommands.vote}'''
            infoEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            infoEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=infoEmbed, mention_author=False)
            return
        if str(arg).lower() == 'utility':
            titleEmbed = 'Utility commands'
            descEmbed = f'''
            `announce` - {config.InfoCommands.announce}
            `avatar` - {config.InfoCommands.avatar}
            `embed` - {config.InfoCommands.embed}
            `id` - {config.InfoCommands.id}
            `membercount` - {config.InfoCommands.membercount}
            `nick` - {config.InfoCommands.nick}
            `reminder` - {config.InfoCommands.reminder}
            `roleinfo` - {config.InfoCommands.roleinfo} 
            `say` - {config.InfoCommands.say}
            `servericon` - {config.InfoCommands.servericon}
            `serverinfo` - {config.InfoCommands.serverinfo}
            `userinfo`- {config.InfoCommands.userinfo}'''
            utilityEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            utilityEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=utilityEmbed, mention_author=False)
            return
        if str(arg).lower() == 'math':
            titleEmbed = 'Math commands'
            descEmbed = f'''
            `calc` - {config.InfoCommands.calc}
            `mathrandom` - {config.InfoCommands.mathrandom}
            `mathsq` - {config.InfoCommands.mathsq}
            `mathsqrt` - {config.InfoCommands.mathsqrt}'''
            mathEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            mathEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=mathEmbed, mention_author=False)
            return
        if str(arg).lower() == 'moderation':
            titleEmbed = 'Moderation commands'
            descEmbed = f'''
            `addrole` - {config.InfoCommands.addrole} 
            `ban` - {config.InfoCommands.ban}
            `kick`- {config.InfoCommands.kick}
            `mute` - {config.InfoCommands.mute}
            `pmute` - {config.InfoCommands.pmute}
            `purge` - {config.InfoCommands.purge}
            `removerole` - {config.InfoCommands.removerole}
            `unban` - {config.InfoCommands.unban}
            `unmute` - {config.InfoCommands.unmute}'''
            moderationEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            moderationEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=moderationEmbed, mention_author=False)
            return
        if str(arg).lower() == 'owner':
            titleEmbed = 'Bot\'s owner commands'
            descEmbed = f'''
            `DM` - {config.InfoCommands.DM}
            `logout` - {config.InfoCommands.logout}
            `save` - {config.InfoCommands.save}
            `updatesuggestion` - {config.InfoCommands.updatesuggestion}'''
            ownerEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            ownerEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=ownerEmbed, mention_author=False)
            return
        else:
            arg = str(arg).lower()
            embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{getattr(config.AliasesCommands, arg)}`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
            embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
            embed.add_field(name='Required permissions', value='`'+getattr(config.RequiredPermissions, arg)+'`', inline=False)
            embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `help` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
        

@bot.command(name='invite', aliases=['inv'])
async def invite(ctx):
    try:
        embed = discord.Embed(title='Links', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
        embed.add_field(name='Join our Discord server!', value=f"[Alex's bots]({config.General.supportServerURL})", inline=False)
        embed.add_field(name='Invite the bot to your server', value=f'[Admin permissions]({config.General.botInviteURLAdmin}) \n[Required permissions]({config.General.botInviteURL})')
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `invite` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='ping', aliases=['pong', 'latency'])
async def ping(ctx):
    try:
        before = time.monotonic()
        message = await ctx.reply("Pong!", mention_author=False)
        await asyncio.sleep(2)
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"**Bot's ping:**  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `ping` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='report')
async def report(ctx, *, msg=None):
    if msg != None:
        try:
            botMsg = await ctx.reply(f'Saving report {config.Emojis.loading}', mention_author=False)
            await asyncio.sleep(2)
            embed = discord.Embed(title=f'Report made by {ctx.author.name}', description=msg, colour=config.Colors.purple, timestamp=ctx.message.created_at)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            print(f'{ctx.author} reported: {msg}')
            channel = bot.get_channel(config.Channels.reportsChannel)
            await channel.send(content='',embed=embed)
            
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await botMsg.edit(content='Thanks for your report!, and Admin will review your report as soon as possible.')
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `report` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
    else:
        embed = discord.Embed(description="Please provide a description for your report.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='source')
async def source(ctx):
    try:
        embed = discord.Embed(title=f"{ctx.me.name}'s source", description='Hi!, you can find my source code [here](https://github.com/Alex0622/Al3xis-Bot-dev/).', colour=config.Colors.yellow)
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `source` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='suggest', aliases=['sug'])
async def suggest(ctx, *, new_suggestion=None):
    if new_suggestion == None:
        embed = discord.Embed(description='Please add a suggestion in your message.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        msg = await ctx.reply('Saving suggestion...', mention_author=False)
        await asyncio.sleep(2)
        embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description=new_suggestion, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar_url)
        suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
        message = await suggestions_channel.send(f'Status: **Pending** {config.Emojis.loading}', embed=embed)
        await message.add_reaction(config.Emojis.ballotBoxWithCheck)
        await message.add_reaction(config.Emojis.x)
        desc = f'''Thanks for your suggestion **{ctx.author}**!
        Your suggestion is currently waiting for approval, make sure to join our [support server](https://discord.com/invite/AAJPHqNXUy) to know when it gets approved or denied.
        `[Suggestion:]` {new_suggestion}'''
        embed2 = discord.Embed(description=desc, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed2.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await msg.edit(content='', embed=embed2, allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await msg.edit(content='', embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `suggest` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='vote')
async def vote(ctx):
    try:
        voteEmbed = discord.Embed(description='''Hi, you can vote me on the following websites:
        1. [Top.gg](https://top.gg/bot/768309916112650321)
        2. [Discord Bot List](https://discordbotlist.com/bots/al3xis)
        3. [Discord Boats](https://discord.boats/bot/768309916112650321)
        ''', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        voteEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=voteEmbed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `vote` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return

####################################################################################################
####################################################################################################
##Utility Commands

@bot.command(name='announce', aliases=['announcement', 'ann'])
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def announce(ctx, channel : discord.TextChannel=None, *, announceMsg=None):
    if not channel:
        embed = discord.Embed(description='Please provide a Discord channel for the announcement!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if not announceMsg:
        embed = discord.Embed(description='Please provide the text for the announcement!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        def check(reaction, user):
            return user.id == ctx.author.id and reaction.message.id == botMsg.id
        botMsg = await ctx.reply('Do you want to send this message in an embed?', mention_author=False)
        await botMsg.add_reaction(config.Emojis.whiteCheckMark)
        await botMsg.add_reaction(config.Emojis.x)
        react, user = await bot.wait_for('reaction_add', check=check, timeout=30)
        if str(react) == config.Emojis.whiteCheckMark:
            try:
                await botMsg.clear_reactions()
            except Exception:
                pass
            randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
            AnnounceEmbed = discord.Embed(description=announceMsg, colour=random.choice(randomColors))
            await channel.send(embed=AnnounceEmbed)
            await botMsg.edit(content='Announcement sent sucessfully.')
            return

        if str(react) == config.Emojis.x:
            try:
                await botMsg.clear_reactions()
            except Exception:
                pass
            await channel.send(announceMsg)
            await botMsg.edit(content='Announcement sent sucessfully.')
            return 
    except asyncio.TimeoutError:
        try:
            await botMsg.clear_reactions()
        except Exception:
            pass
        await botMsg.edit(content="You didn't reply in time, please try again.")
        return
    except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `announce` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return

@announce.error
async def announce_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** Only administrators of this server can use that command!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='avatar', aliases=['av'])
@commands.guild_only()
async def avatar(ctx, *, member: discord.Member = None):
    try:
        if member == None:
            member = ctx.author
        user = await bot.fetch_user(member.id)
        embed = discord.Embed(title = f'Avatar of user {user}', colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_image(url='{}'.format(user.avatar_url))
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `avatar` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='embed')
@commands.guild_only()
async def embed(ctx, *, embedMsg=None):
    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
    try:
        if embedMsg == None:
            embed = discord.Embed(description="Please provide a message!", colour=config.Colors.red)
            await ctx.reply(embed=embed, mention_author=False)
            return
        else:
            embed = discord.Embed(description=embedMsg, colour=random.choice(randomColors))
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            try:
                await ctx.message.delete()
            except Exception:
                pass
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `embed` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return

@bot.command(name='id', aliases=['ID'])
@commands.guild_only()
async def id(ctx, *, member: discord.Member = None):
    try:
        if member == None:
            member = ctx.author
        await ctx.reply(member.id, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `id` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='membercount')
@commands.guild_only()
async def membercount(ctx):
    try:
        embed = discord.Embed(description=f'There are **{ctx.guild.member_count} members** in this server.', colour=config.Colors.lightBlue)
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `membercount` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return



@bot.command(name='nick', aliases=['setnick'])
@commands.guild_only()
@commands.has_permissions(change_nickname=True)
@commands.bot_has_permissions(manage_nicknames=True)
async def nick(ctx, *, new_nick=None):
    embed = discord.Embed(description=f'Updating nick {config.Emojis.loading}', colour=config.Colors.gray)
    if new_nick:
        botmsg = await ctx.reply(embed=embed, mention_author=False)
        await asyncio.sleep(1)
        if ctx.author.top_role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="I cannot change your nickname because you have the same role as me or your top role is above mine.", colour=config.Colors.red)
            await botmsg.edit(embed=embed)
            return   
        else:      
            try:   
                if str(new_nick).lower() == 'reset':
                    if ctx.author.nick == None:
                        embedDesc = "You don't have a nickname!"
                        color = config.Colors.red
                    else:
                        await ctx.author.edit(nick=ctx.author.name)
                        embedDesc = f"{config.Emojis.whiteCheckMark} I've removed your nickname."
                        color = config.Colors.green
                    embed2 = discord.Embed(description=embedDesc, colour=color)
                    await botmsg.edit(embed=embed2)
                    return
                if new_nick == ctx.author.nick:
                    embed3 = discord.Embed(description="You already have that nickname, please select a different one!", colour=config.Colors.red)
                    await botmsg.edit(embed=embed3)
                    return
                else:
                    await ctx.author.edit(nick=new_nick)
                    embed4 = discord.Embed(description=f'{config.Emojis.whiteCheckMark} Your new nickname is: {new_nick}', colour=config.Colors.green)
                    await botmsg.edit(embed=embed4)
                    return
            except Exception as e:
                if str(e) == "403 Forbidden (error code: 50013): Missing Permissions":
                    errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to change your nickname.", colour=config.Colors.red)
                    await botmsg.edit(embed=errorEmbed)
                    return
                else:
                    errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                    await botmsg.edit(embed=errorEmbed)
                    await ctx.message.add_reaction(config.Emojis.noEntry)
                    logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                    description=f"""Error while using `nick` command:
                        `[Content]` {ctx.message.content} 
                        `[Error]` {e}"""
                    logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                    await logErrorsChannel.send(embed=logErrorsEmbed)
                    return
    else:
        if ctx.author.nick == None:
            desc = 'You don\'t have a current nickname.'
            color = config.Colors.red
        else:
            desc = f'Your current nick is: {ctx.author.nick}'
            color = config.Colors.orange
        embed = discord.Embed(description=desc, colour=color)
        await ctx.channel.send(embed=embed)
        return  

@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `CHANGE NICKNAME` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE NICKNAMES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

    
@bot.command(name='reminder', aliases=['remind'])
async def reminder(ctx, time=None, *, msg=None):
    if time != None:
        if msg != None:
            try:
                await asyncio.sleep(0.5)
                seconds = 0
                if time.lower().endswith("d"):
                    seconds += float(time[:-1]) * 60 * 60 * 24
                    counter = f"{seconds // 60 // 60 // 24} days"
                elif time.lower().endswith("h"):
                    seconds += float(time[:-1]) * 60 * 60
                    counter = f"{seconds // 60 // 60} hours"
                elif time.lower().endswith("m"):
                    seconds += float(time[:-1]) * 60
                    counter = f"{seconds // 60} minutes"
                elif time.lower().endswith("s"):
                    seconds += float(time[:-1])
                    counter = f"{seconds} seconds"
                else:
                    embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return  

                await ctx.reply(f"I've set a reminder of {counter}: {msg}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
                await asyncio.sleep(seconds)
                await ctx.reply(f'Hey! {msg}', mention_author=True, allowed_mentions=discord.AllowedMentions.none())
            except Exception as e:
                if str(e).startswith("could not convert string to float"):
                    embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                    await ctx.reply(embed=embed, mention_author=False)
                    return  
                else:
                    errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                    await ctx.reply(embed=errorEmbed, mention_author=False)
                    await ctx.message.add_reaction(config.Emojis.noEntry)
                    logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                    description=f"""Error while using `reminder` command:
                        `[Content]` {ctx.message.content} 
                        `[Error]` {e}"""
                    logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                    await logErrorsChannel.send(embed=logErrorsEmbed)
                    return
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
        if str('Unknown message') in str(error):
            await ctx.send(f"Hey {ctx.author.mention} please don't delete your message when using `{ctx.prefix}{ctx.command}`")
            return
        if str('ValueError') in str(error): 
            embed = discord.Embed(description=f'**Error!** Your message does not include a valid duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 


@bot.command('roleinfo', aliases=['ri', 'role'])
@commands.guild_only()
async def roleinfo(ctx, role:discord.Role=None):
    if not role:
        embed = discord.Embed(description='Please provide a role ID.', colour=config.Colors.red)
        await ctx.reply(embed=embed, mention_author=False)
        return
    try:
        guild = ctx.guild
        roleinfoTitle = f'About {role.name}'
        permissions = dict(role.permissions)
        perms = []
        for perm in permissions.keys():
            if permissions[perm] is True and not role.permissions.administrator:
                perms.append(perm.lower().replace('_', ' ').title())

        if role.permissions.administrator:
            perms.append("Administrator")
        roleinfoDesc = f'''
        **Role name:** {role.name} ({role.id})
        **Created on** {role.created_at.strftime("%A %d %B %Y, %H:%M")}
        **Position:** {len(guild.roles)-role.position}
        **Is managed?** {role.managed}
        **Is hoisted?** {role.hoist}
        **Color:** {role.color}
        **Permissions:** {', '.join(perms)}'''

        roleinfoEmbed = discord.Embed(title=roleinfoTitle, description=roleinfoDesc, colour=role.color)
        await ctx.reply(embed=roleinfoEmbed, mention_author=False)
    except Exception as e:
        if e == "'NoneType' object has no attribute 'name'":
            errorEmbed = discord.Embed(description=f'**Error!** I cannot find that role.', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return
        else:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `roleinfo` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return


@bot.command(name='say')
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def say(ctx, *, sayMsg=None):
    if not sayMsg:
        embed = discord.Embed(description='Please provide a message!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        try:
           await ctx.message.delete()
        except Exception:
           pass
        await ctx.send(sayMsg, allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `say` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='servericon')
@commands.guild_only()
async def servericon(ctx):
    try:
        embed = discord.Embed(title = f'Icon of {ctx.guild}', colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_image(url='{}'.format(ctx.guild.icon_url))
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `servericon` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='serverinfo', aliases=['si'])
@commands.guild_only()
async def serverinfo(ctx):
    try:
        guild = ctx.guild
        owner = await bot.fetch_user(guild.owner.id)
        general = f'''
        **Owner:** {owner}
        **Owner ID:** {owner.id}
        **Guild ID:** {guild.id}
        **Created:** {guild.created_at.strftime("%d %B %Y, %H:%M")}
        '''
        statistics = f'''
        **Members:** 
            `[{guild.member_count}]` Members
        **Roles:** 
            `[{len(guild.roles)}]` Roles
        **Channels:** 
            `[{len(guild.text_channels)}]` Text channels | `[{len(guild.voice_channels)}]` Voice channels
        '''
        serverinfoEmbed = discord.Embed(title=f"{guild}'s information", colour=config.Colors.blue, timestamp=ctx.message.created_at)
        serverinfoEmbed.add_field(name='**__General__**', value=general)
        serverinfoEmbed.add_field(name='**__Statistics__**', value=statistics)
        if not guild.is_icon_animated():
            serverinfoEmbed.set_thumbnail(url=guild.icon_url_as(format="png"))
        elif guild.is_icon_animated():
            serverinfoEmbed.set_thumbnail(url=guild.icon_url_as(format="gif"))
        if guild.banner:
            serverinfoEmbed.set_image(url=guild.banner_url_as(format="png"))
        serverinfoEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=serverinfoEmbed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `serverinfo` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return


@bot.command(name='userinfo', aliases=['user', 'ui'])
@commands.guild_only()
async def userinfo(ctx, *, member: discord.Member=None):
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
        await ctx.reply(embed=userinfoEmbed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `userinfo` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
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

@bot.command(name='calc', aliases=['calculator'])
async def calc(ctx, x:float=None, arg=None, y:float=None):
    if arg != None:
        if x != None:
            if y != None:
                try:
                    if arg == '+':
                        result = add(x, y)
                        await ctx.reply(result, mention_author=False)
                        return
                    if arg == '-':
                        result = sub(x, y)
                        await ctx.reply(result, mention_author=False)
                        return
                    if arg == '*':
                        result = mult(x, y)
                        await ctx.reply(result, mention_author=False)
                        return
                    if arg == '/':
                        result = div(x, y)
                        await ctx.reply(result, mention_author=False)
                        return
                    else:
                        embed = discord.Embed(description=f'"{arg}" is not a valid option!', colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return   
                except Exception as e:
                    errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                    await ctx.reply(embed=errorEmbed, mention_author=False)
                    await ctx.message.add_reaction(config.Emojis.noEntry)
                    logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                    description=f"""Error while using `calc` command:
                        `[Content]` {ctx.message.content} 
                        `[Error]` {e}"""
                    logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                    await logErrorsChannel.send(embed=logErrorsEmbed)
                    return
            else:
                embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
                await ctx.send(embed=embed)
                return    
        else:
            embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return      
    else:
        embed = discord.Embed(description=f'Please provide a math argument (+ - * /)', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 

@calc.error
async def calc_error(ctx, error):
    if str(error) == 'Command raised an exception: ZeroDivisionError: float division by zero':
        await ctx.reply('Math ERROR.', mention_author=False)
        return
    if str('Converting to "float"') in str(error):
        embed = discord.Embed(description=f'Please provide a valid math equation. \nNote: Rememeber to add spaces between arguments. (e.g. `a!calc 1 + 1`)', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 


@bot.command(name='mathrandom')
async def mathrandom(ctx, x:int=None, y:float=None):
    if x != None:
        if y != None:
            try:
                result = rando(x, y)
                await ctx.reply(result, mention_author=False)
            except Exception as e:
                errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.reply(embed=errorEmbed, mention_author=False)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                description=f"""Error while using `mathrandom` command:
                    `[Content]` {ctx.message.content} 
                    `[Error]` {e}"""
                logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await logErrorsChannel.send(embed=logErrorsEmbed)
                return
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
        try:  
            result = sq(x)
            await ctx.reply(result, mention_author=False)
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `mathsq` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  


@bot.command(name='mathsqrt')
async def mathsqrt(ctx, x:float=None):
    if x != None:      
        try:    
            result = sqrt(x)
            await ctx.reply(result, mention_author=False)
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `mathsqrt` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  


####################################################################################################
####################################################################################################
##Moderation commands

@bot.command(name='addrole')
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def addrole(ctx, role:discord.Role=None, *, member:discord.Member=None):
    if role == None:
        notRoleEmbed = discord.Embed(description="Please provided a Discord role.", colour=config.Colors.red)
        await ctx.reply(embed=notRoleEmbed, mention_author=False)
        return
    if member == None:
        notMembersEmbed = discord.Embed(description="Please provide a member that will get the role.", colour=config.Colors.red)
        await ctx.reply(embed=notMembersEmbed, mention_author=False)
        return
    try:
        if member.top_role > ctx.me.top_role:
            embed = discord.Embed(description="I cannot add the role to that member because they have the same role as me or their top role is above mine.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="It seems like I cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            embed = discord.Embed(description="It seems like you cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if role in member.roles:
            embed = discord.Embed(description="That member already has that role.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        await member.add_roles(role, reason=f"{ctx.author} used command `addrole`.")
        embed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've successfully added the role {role.mention} to {member.mention}", colour=role.color)
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        if str(e) == "403 Forbidden (error code: 50013): Missing Permissions":
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to access that role.", colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `addrole` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return

@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='ban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to ban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'  
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    if member.top_role > ctx.me.top_role:
                        embed = discord.Embed(description="I cannot ban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return 
                    else:
                        try:
                            await asyncio.sleep(0.5)    
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
                        except Exception as e:
                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                            await ctx.reply(embed=errorEmbed, mention_author=False)
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                            description=f"""Error while using `ban` command:
                                `[Content]` {ctx.message.content} 
                                `[Error]` {e}"""
                            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='kick', pass_context=True)
@commands.guild_only()
@commands.bot_has_permissions(kick_members=True)
@commands.has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    if member.top_role > ctx.me.top_role:
                        embed = discord.Embed(description="I cannot kick that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                    else:
                        try:
                            await asyncio.sleep(0.5)
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
                        except Exception as e:
                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                            await ctx.reply(embed=errorEmbed, mention_author=False)
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                            description=f"""Error while using `kick` command:
                                `[Content]` {ctx.message.content} 
                                `[Error]` {e}"""
                            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `KICK MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='mute')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member=None, duration=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if member.top_role > ctx.me.top_role:
                            embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return
                        else:
                            if not mutedRole in member.roles:
                                if duration:
                                    try:
                                        await asyncio.sleep(0.5)
                                        seconds = 0
                                        if duration.lower().endswith("d"):
                                            seconds += float(duration[:-1]) * 60 * 60 * 24
                                            counter = f"{seconds // 60 // 60 // 24} days"
                                        elif duration.lower().endswith("h"):
                                            seconds += float(duration[:-1]) * 60 * 60
                                            counter = f"{seconds // 60 // 60} hours"
                                        elif duration.lower().endswith("m"):
                                            seconds += float(duration[:-1]) * 60
                                            counter = f"{seconds // 60} minutes"
                                        elif duration.lower().endswith("s"):
                                            seconds += float(duration[:-1])
                                            counter = f"{seconds} seconds"
                                        else:
                                            embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                                            await ctx.send(embed=embed)
                                            return 
                                        
                                        await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                        await ctx.send(f'**{member}** was muted for {counter} | `{reason}`')
                                        try:                    
                                            await member.send(f'You were muted in server: **{guild.name}** for {counter} | `{reason}`')
                                        except Exception:
                                            pass
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
                                        if mutedRole in member.roles:
                                            await member.remove_roles(mutedRole, reason='Temporary mute completed!')
                                        if not mutedRole in member.roles:
                                            return
                                        reason = 'Temporary mute completed!'
                                        try:
                                            await member.send(f'You were unmuted in server: **{guild.name}** | `{reason}`')
                                        except Exception:
                                            pass
                                        print(f'User {member} was unmuted in server {guild.name} | {reason}')
                                        logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                        logEmbed.add_field(name='User', value=member.mention)
                                        logEmbed.add_field(name='Reason', value=reason) 
                                        logEmbed.set_footer(text=f'Guild: {guild}')
                                        logChannel=bot.get_channel(config.Channels.logChannel)
                                        await logChannel.send(embed=logEmbed)
                                        return
                                    except Exception as e:
                                        if str(e).startswith("could not convert string to float"):
                                            embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                                            await ctx.reply(embed=embed, mention_author=False)
                                            return  
                                        else:
                                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                                            await ctx.reply(embed=errorEmbed, mention_author=False)
                                            await ctx.message.add_reaction(config.Emojis.noEntry)
                                            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                                            description=f"""Error while using `mute` command:
                                                `[Content]` {ctx.message.content} 
                                                `[Error]` {e}"""
                                            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                                            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                                            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CommandInvokeError):
        if str('ValueError') in str(error): 
            embed = discord.Embed(description=f'**Error!** Your message does not include a valid duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 


@bot.command(name='pmute', aliases= ['pm'])
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def pmute(ctx, member: discord.Member=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if member.top_role > ctx.me.top_role:
                            embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return
                        else:
                            if not mutedRole in member.roles:
                                try:
                                    await asyncio.sleep(0.5)
                                    await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                    await ctx.send(f'**{member}** was permanently muted | `{reason}`')
                                    try:
                                        await member.send(f'You were permanently muted in server: **{guild.name}** | `{reason}`')
                                    except Exception:
                                        pass
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

                                except Exception as e:
                                    errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                                    await ctx.reply(embed=errorEmbed, mention_author=False)
                                    await ctx.message.add_reaction(config.Emojis.noEntry)
                                    logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                                    description=f"""Error while using `pmute` command:
                                        `[Content]` {ctx.message.content} 
                                        `[Error]` {e}"""
                                    logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                                    logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                                    await logErrorsChannel.send(embed=logErrorsEmbed)
                                    return

                            else:
                                embed = discord.Embed(description=f'{member.mention} is already muted.', colour=config.Colors.red)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** Looks like I\'m missing permissions.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='purge', aliases=['clear'])
@commands.guild_only()
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 0):
    guild = ctx.guild
    if amount <= 500:
        if amount >=1:
            try:
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
            except Exception as e:
                errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.reply(embed=errorEmbed, mention_author=False)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                description=f"""Error while using `purge` command:
                    `[Content]` {ctx.message.content} 
                    `[Error]` {e}"""
                logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await logErrorsChannel.send(embed=logErrorsEmbed)
                return
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


@bot.command(name='removerole')
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def removerole(ctx, role:discord.Role=None, *, member:discord.Member=None):
    if role == None:
        notRoleEmbed = discord.Embed(description="Please provided a Discord role.", colour=config.Colors.red)
        return
        await ctx.reply(embed=notRoleEmbed, mention_author=False)
    if member == None:
        notMembersEmbed = discord.Embed(description="Please provide a member to remove their role.", colour=config.Colors.red)
        await ctx.reply(embed=notMembersEmbed, mention_author=False)
        return
    try:
        if member.top_role > ctx.me.top_role:
            embed = discord.Embed(description="I cannot remove the role from that member because they have the same role as me or their top role is above mine.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return   
        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="It seems like I cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            embed = discord.Embed(description="It seems like you cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if not role in member.roles:
            embed = discord.Embed(description="That member does not have that role.", colour=role.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        await member.remove_roles(role, reason=f"{ctx.author} used command `removerole`.")
        embed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've successfully removed the role {role.mention} from {member.mention}", colour=role.color)
        await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        if str(e) == "403 Forbidden (error code: 50013): Missing Permissions":
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to access that role.", colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `removerole` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='softban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def softban(ctx, member:discord.Member=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    if member.top_role > ctx.me.top_role:
                        embed = discord.Embed(description="I cannot softban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                    else:
                        try:
                            await asyncio.sleep(0.5)
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
                        except Exception as e:
                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                            await ctx.reply(embed=errorEmbed, mention_author=False)
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                            description=f"""Error while using `softban` command:
                                `[Content]` {ctx.message.content} 
                                `[Error]` {e}"""
                            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='unban')
@commands.guild_only()
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
                        await asyncio.sleep(0.5)
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
                    except Exception as e:
                        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                        await ctx.reply(embed=errorEmbed, mention_author=False)
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                        description=f"""Error while using `unban` command:
                            `[Content]` {ctx.message.content} 
                            `[Error]` {e}"""
                        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                        await logErrorsChannel.send(embed=logErrorsEmbed)
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
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member=None, *, reason=None):
    if member == None:
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
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
                            await asyncio.sleep(0.5)
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
                        except Exception as e:
                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                            await ctx.reply(embed=errorEmbed, mention_author=False)
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                            description=f"""Error while using `unmute` command:
                                `[Content]` {ctx.message.content} 
                                `[Error]` {e}"""
                            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                            await logErrorsChannel.send(embed=logErrorsEmbed)
                            return
                    else:
                        embed = discord.Embed(description=f'{member.mention} is not muted.', colour=config.Colors.red)
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
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** Looks like I\'m missing permissions.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

####################################################################################################
####################################################################################################
##Owner commands

@bot.command(name='DM', aliases=['dm', 'msg'])
@commands.guild_only()
@commands.is_owner()
async def DM(ctx, member: discord.Member=None, *, msg=None):
    if member != None:
        if msg != None:
            botMsg = await ctx.send(f'DMing user {config.Emojis.loading}')
            await asyncio.sleep(2)
            embed = discord.Embed(description=msg, colour=config.Colors.orange)
            embed.set_footer(text=f'Sent by {ctx.author}', icon_url=ctx.author.avatar_url)
            try:
                await member.send(embed=embed)
                logEmbed = discord.Embed(title=f'{ctx.author.name} has sent a DM to {member.name}', description=msg, colour=config.Colors.orange, timestamp=ctx.message.created_at)
                logEmbed.set_footer(text=member, icon_url=member.avatar_url)
                DMs_channel = bot.get_channel(config.Channels.DMsChannel)
                await DMs_channel.send(embed=logEmbed)
                await botMsg.edit(content=f'DM sent successfully! {config.Emojis.whiteCheckMark}')
            except Exception as e:
                errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.reply(embed=errorEmbed, mention_author=False)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                description=f"""Error while using `DM` command:
                    `[Content]` {ctx.message.content} 
                    `[Error]` {e}"""
                logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await logErrorsChannel.send(embed=logErrorsEmbed)
                return
        
        else:
            embed = discord.Embed(description='Please provide a description for your embed.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description='Please specify a member to DM.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@bot.command(name="logout")
@commands.is_owner()
async def logout(ctx):
    try:
        await ctx.reply(f"Guess it's time to say goodbye!, for now {config.Emojis.wave}", mention_author=False)
        await bot.close()
        print(f"{ctx.author} has disconnected the bot from Discord today at {ctx.message.created_at}")
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `logout` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return

@bot.command(name='save')
@commands.guild_only()
@commands.is_owner()
async def save(ctx,*, saveMsg=None):
    if saveMsg == None:
        embed = discord.Embed(description='Please provide a description for your embed.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    else:
        try:
            firstMessage = await ctx.send('Saving message...')
            try:
                await ctx.message.delete()
            except Exception:
                pass
            await asyncio.sleep(2)
            embed = discord.Embed(title=f'{ctx.author} saved a new message.', description=saveMsg, colour=config.Colors.green, timestamp=ctx.message.created_at)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            savedMessagesChannel = bot.get_channel(config.Channels.ownerChannel)
            await savedMessagesChannel.send(embed=embed)
            await firstMessage.edit(content=f'**{ctx.author}** Your message has been saved!')
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `save` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return

@bot.command(name='us', aliases=['updatesuggestion'])
@commands.guild_only()
@commands.is_owner()
async def us(ctx, msgID:int=None, type=None, *, reason=None):
    if msgID == None:
        embed = discord.Embed(description="Please provide the message ID.", colour=config.Colors.red)
        await ctx.reply(embed=embed, mention_author=False)
        return
    if type == None:
        embed = discord.Embed(description="Please specify if the status should be accepted, denied or pending.", colour=config.Colors.red)
        await ctx.reply(embed=embed, mention_author=False)
        return
    if reason == None:
        if str(type).lower() == 'pending':
            pass
        else:
            embed = discord.Embed(description="You need to provide a reason.", colour=config.Colors.red)
            await ctx.reply(embed=embed, mention_author=False)
            return
    try:    
        if str(type).lower() == 'accept':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Accepted** {config.Emojis.whiteCheckMark} | Reason: {reason}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.clear_reaction(emoji1)
            await msg.clear_reaction(emoji2)
            botMsg = await ctx.reply(f'{config.Emojis.whiteCheckMark} Suggestion was successfully accepted.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
            return
        if str(type).lower() == 'deny':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Denied** {config.Emojis.noEntry} | Reason: {reason}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.clear_reaction(emoji1)
            await msg.clear_reaction(emoji2)
            botMsg = await ctx.reply(f'{config.Emojis.whiteCheckMark} Suggestion was successfully denied.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
            return
        if str(type).lower() == 'pending':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Pending** {config.Emojis.loading}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.add_reaction(emoji1)
            await msg.add_reaction(emoji2)
            botMsg = await ctx.reply(f'{config.Emojis.whiteCheckMark} Suggestion is now pending.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
            return
        else:
            botMsg = await ctx.reply(f'{config.Emojis.x} `{type}` is not a valid option.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.x)
            await asyncio.sleep(5)
            await botMsg.delete()
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `updatesuggestion` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return

################################
####################################################################################################
####################################################################################################
#Run the bot on Discord.
bot.run(os.environ['discordToken'])


