import discord
from discord.ext import commands 
import datetime
import asyncio
import config, os, util
import time, random, math
    
#Bot (our bot)
intents=discord.Intents.default()
intents.members=True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('a!', 'A!'), intents=intents) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')

#Global Blacklist check
@bot.check(util.isNotBlacklisted)

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
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.BotMissingPermissions) or isinstance(error, commands.errors.CommandNotFound) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError) or isinstance(error, commands.errors.CheckFailure):
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
        await message.reply(embed=infoEmbed)
        return
    if message.content == '<@768309916112650321>':
        descriptionMsg = f'Hi!, my prefixes are `a!` and `A!`'
        infoEmbed = discord.Embed(description=descriptionMsg, colour=config.Colors.blue)
        await message.reply(embed=infoEmbed)
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
    embed = discord.Embed(title='Al3xis was added to a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {len(guild.members)}', colour=config.Colors.green)
    embed.set_footer(text=f'{len(bot.guilds)} guilds now', icon_url=guild.icon_url)
    await channel.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(config.Channels.joinsleavesChannel)
    embed = discord.Embed(title='Al3xis was removed from a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {len(guild.members)}', colour=config.Colors.green)
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
        embed = discord.Embed(description=f'Welcome **{member}** to the **Alex\'s bots** server!', colour=random.choice(randomColors))
        embed.set_footer(text=member.id, icon_url=member.avatar_url)
        await chatChannel.send(embed=embed)
        return
    else:
        return

@bot.event
async def on_member_remove(member):
    if member.guild == bot.get_guild(793987455149408309):
        chatChannel = bot.get_channel(config.Channels.chatChannel)
        randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen, config.Colors.gray]
        embed = discord.Embed(description=f'**{member}** left the server.', colour=random.choice(randomColors))
        embed.set_footer(text=member.id, icon_url=member.avatar_url)
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
        embedI.add_field(name='Current Version', value='__[v1.4.2](https://github.com/Alex22-SV/Al3xis-Bot-dev/releases/tag/v1.4.2)__')
        embedI.add_field(name='Guilds', value=f'`{len(bot.guilds)}`')
        embedI.add_field(name='Prefix', value='`a!`, `A!`')
        embedI.add_field(name='Developed since', value='`21/10/2020`')
        embedI.add_field(name='Developed with', value='`Python`')
        embedI.add_field(name='Useful links', value=f'[GitHub]({config.General.githubURL}) | [Support Server]({config.General.supportServerURL}) | [Privacy Policy]({config.General.privacyPolicyURL}) | [Terms of Use]({config.General.termsOfUseURL})')
        embedI.add_field(name='Latest updates', value=f"Added [Privacy Policy]({config.General.privacyPolicyURL}) and [Terms of Use]({config.General.termsOfUseURL})", inline=False)
        embedI.set_thumbnail(url=ctx.me.avatar_url)
        embedI.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embedI)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `about` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@about.error
async def about_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='help', aliases=['h'])
async def help(ctx, arg = None):
    try:
        if arg == None:
            helpEmbed = discord.Embed(title = 'Help | Prefix: `a!`, `A!`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            helpEmbed.add_field(name='Info', value='`about`, `help`, `invite`, `ping`, `privacy`, `report`, `source`, `suggest`, `support`, `terms`, `vote`', inline=True)
            helpEmbed.add_field(name='Math', value='`calc`, `mathrandom`, `mathsq`, `mathsqrt`', inline=True)
            helpEmbed.add_field(name='Moderation', value='`addrole`, `ban`, `bans`, `kick`, `mute`, `pmute`, `purge`, `removerole` `slowmode`, `softban`, `unban`, `unmute`, `voicemute`, `voiceunmute`', inline=True)
            helpEmbed.add_field(name='Utility', value='`announce`, `avatar`, `embed`, `id`, `membercount`, `nick`, `reminder`, `roleinfo`, `say`, `servericon`, `serverinfo`, `userinfo`', inline=False)
            helpEmbed.add_field(name='Owner', value='`DM`, `logout`, `save`, `updatereport`, `updatesuggestion`', inline=True)
            helpEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=helpEmbed)
            return
        if str(arg).lower() == 'info':
            titleEmbed = 'Info commands'
            descEmbed = f'''`about` - {config.InfoCommands.about} \n`help` - {config.InfoCommands.help} \n`invite` - {config.InfoCommands.invite} \n`ping` - {config.InfoCommands.ping} \n`privacy` - {config.InfoCommands.privacy} \n`report` - {config.InfoCommands.report} \n`source` - {config.InfoCommands.source} \n`suggest` - {config.InfoCommands.suggest} \n`support` - {config.InfoCommands.support} \n`terms` - {config.InfoCommands.terms} \n`vote` - {config.InfoCommands.vote}'''
            infoEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            infoEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=infoEmbed)
            return
        if str(arg).lower() == 'utility':
            titleEmbed = 'Utility commands'
            descEmbed = f'''`announce` - {config.InfoCommands.announce} \n`avatar` - {config.InfoCommands.avatar} \n`embed` - {config.InfoCommands.embed} \n`id` - {config.InfoCommands.id} \n`membercount` - {config.InfoCommands.membercount} \n`nick` - {config.InfoCommands.nick} \n`reminder` - {config.InfoCommands.reminder} \n`roleinfo` - {config.InfoCommands.roleinfo} \n`say` - {config.InfoCommands.say} \n`servericon` - {config.InfoCommands.servericon} \n`serverinfo` - {config.InfoCommands.serverinfo} \n`userinfo` - {config.InfoCommands.userinfo}'''
            utilityEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            utilityEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=utilityEmbed)
            return
        if str(arg).lower() == 'math':
            titleEmbed = 'Math commands'
            descEmbed = f'''`calc` - {config.InfoCommands.calc} \n`mathrandom` - {config.InfoCommands.mathrandom} \n`mathsq` - {config.InfoCommands.mathsq} \n`mathsqrt` - {config.InfoCommands.mathsqrt}'''
            mathEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            mathEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=mathEmbed)
            return
        if str(arg).lower() == 'moderation':
            titleEmbed = 'Moderation commands'
            descEmbed = f'''`addrole` - {config.InfoCommands.addrole} \n`ban` - {config.InfoCommands.ban} \n`bans` - {config.InfoCommands.bans} \n`kick`- {config.InfoCommands.kick} \n`mute` - {config.InfoCommands.mute} \n`pmute` - {config.InfoCommands.pmute} \n`purge` - {config.InfoCommands.purge} \n`removerole` - {config.InfoCommands.removerole} \n`slowmode` - {config.InfoCommands.slowmode} \n`softban` - {config.InfoCommands.softban} \n`unban` - {config.InfoCommands.unban} \n`unmute` - {config.InfoCommands.unmute} \n`voicemute` - {config.InfoCommands.voicemute} \n`voiceunmute` - {config.InfoCommands.voiceunmute}'''
            moderationEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            moderationEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=moderationEmbed)
            return
        if str(arg).lower() == 'owner':
            titleEmbed = 'Bot\'s owner commands'
            descEmbed = f'''`DM` - {config.InfoCommands.DM} \n`logout` - {config.InfoCommands.logout} \n`save` - {config.InfoCommands.save} \n`updatereport` - {config.InfoCommands.updatereport} \n`updatesuggestion` - {config.InfoCommands.updatesuggestion}'''
            ownerEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            ownerEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=ownerEmbed)
            return
        else:
            arg = str(arg).lower()
            embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{getattr(config.AliasesCommands, arg)}`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
            embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
            embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
            embed.add_field(name='Required permissions', value='`'+getattr(config.RequiredPermissions, arg)+'`', inline=False)
            embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
    except Exception as e:
        if "type object" in str(e):
            notFoundEmbed = discord.Embed(description=f"Command/Category `{arg}` not found.", colour=config.Colors.red)
            await ctx.send(embed=notFoundEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `help` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)
        
@bot.command(name='invite', aliases=['inv'])
@commands.cooldown(1, 15, type=commands.BucketType.user)
async def invite(ctx):
    try:
        embed = discord.Embed(title='Links', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
        embed.add_field(name='Join our Discord server!', value=f"[Alex's bots]({config.General.supportServerURL})", inline=False)
        embed.add_field(name='Invite the bot to your server', value=f'[Admin permissions]({config.General.botInviteURLAdmin}) \n[Required permissions]({config.General.botInviteURL})')
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `invite` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@invite.error
async def invite_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='ping', aliases=['pong', 'latency'])
async def ping(ctx):
    try:
        before = time.monotonic()
        message = await ctx.send("Pong!")
        await asyncio.sleep(2)
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"**Bot's ping:**  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `ping` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="privacy")
@commands.guild_only()
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def privacy(ctx):
    try:
        desc = f"Read our Privacy Policy [here]({config.General.privacyPolicyURL})."
        privacyEmbed = discord.Embed(description=desc, colour=config.Colors.blue)
        privacyEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=privacyEmbed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `privacy` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@privacy.error
async def privacy_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='report')
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def report(ctx, *, msg=None):
    if msg != None:
        try:
            botEmbed = discord.Embed(description=f"Saving report {config.Emojis.loading}", colour=config.Colors.gray)
            botMsg = await ctx.send(embed=botEmbed)
            await asyncio.sleep(2)
            reportsChannel = bot.get_channel(config.Channels.reportsChannel)
            embed = discord.Embed(title=f'Report made by {ctx.author}', description=msg, colour=config.Colors.purple, timestamp=ctx.message.created_at)
            embed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar_url)
            await reportsChannel.send(content='',embed=embed)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            desc = '''Thanks for your report! \nAn Admin will review your report as soon as possible. \nYou will get a respoonse in DMs when your report's status gets updated.'''
            reportedEmbed = discord.Embed(description=desc, colour=config.Colors.green)
            await botMsg.edit(embed=reportedEmbed)
        except Exception as e:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
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
@report.error
async def report_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='source')
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def source(ctx):
    try:
        embed = discord.Embed(title=f"{ctx.me.name}'s source", description=f'Hi!, you can find my source code [here]({config.General.githubURL}).', colour=config.Colors.yellow)
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `source` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@source.error
async def source_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='suggest', aliases=['sug'])
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def suggest(ctx, *, new_suggestion=None):
    if new_suggestion == None:
        embed = discord.Embed(description='Please add a suggestion in your message.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        msg = await ctx.send('Saving suggestion...')
        await asyncio.sleep(2)
        embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description=new_suggestion, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar_url)
        suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
        message = await suggestions_channel.send(f'Status: **Pending** {config.Emojis.loading}', embed=embed)
        await message.add_reaction(config.Emojis.ballotBoxWithCheck)
        await message.add_reaction(config.Emojis.x)
        desc = f'''Thanks for your suggestion **{ctx.author}**! \nYour suggestion is currently waiting for approval, make sure to join our [support server]({config.General.supportServerURL}) to know when it gets approved or denied (*You will also receive a DM when your suggestion's status gets updated.*) \n`[Suggestion:]` {new_suggestion}'''
        embed2 = discord.Embed(description=desc, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed2.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await msg.edit(content='', embed=embed2, allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
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
@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="support")
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def support(ctx):
    try:
        supportEmbed = discord.Embed(description=f"Need help with Al3xis? join our support server [here]({config.General.supportServerURL})!", colour=config.Colors.gray)
        await ctx.send(embed=supportEmbed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `support` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@support.error
async def support_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="terms")
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def terms(ctx):
    try:
        desc = f"Read our Terms of Use [here]({config.General.termsOfUseURL})."
        termsEmbed = discord.Embed(description=desc, colour=config.Colors.blue)
        termsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=termsEmbed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `terms` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@terms.error
async def terms_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='vote')
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def vote(ctx):
    try:
        voteEmbed = discord.Embed(description='''Hi, you can vote me on the following websites:
        1. [Top.gg](https://top.gg/bot/768309916112650321)
        2. [Discord Bot List](https://discordbotlist.com/bots/al3xis)
        3. [Discord Boats](https://discord.boats/bot/768309916112650321)
        4. [Discord Extreme List](https://discordextremelist.xyz/en-US/bots/768309916112650321)
        ''', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        voteEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=voteEmbed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `vote` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@vote.error
async def vote_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

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
        botMsg = await ctx.send('Do you want to send this message in an embed?')
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
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)
    
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
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `avatar` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@avatar.error 
async def avatar_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='embed')
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def embed(ctx, *, embedMsg=None):
    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
    try:
        if embedMsg == None:
            embed = discord.Embed(description="Please provide a message!", colour=config.Colors.red)
            await ctx.send(embed=embed)
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
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `embed` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='id', aliases=['ID'])
@commands.guild_only()
async def id(ctx, *, member: discord.Member = None):
    try:
        if member == None:
            member = ctx.author
        await ctx.send(member.id)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `id` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@id.error
async def id_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='membercount')
@commands.guild_only()
async def membercount(ctx):
    try:
        embed = discord.Embed(description=f'There are **{ctx.guild.member_count} members** in this server.', colour=config.Colors.lightBlue)
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `membercount` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@membercount.error
async def membercount_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='nick', aliases=['setnick'])
@commands.guild_only()
@commands.has_permissions(manage_nicknames=True)
@commands.bot_has_permissions(manage_nicknames=True)
async def nick(ctx, member:discord.Member=None, *, nickname=None):
    embed = discord.Embed(description=f"Changing/Getting nickname {config.Emojis.loading}", colour=config.Colors.gray)
    botmsg = await ctx.send(embed=embed)
    try:
        if member == None:
            notMemberEmbed = discord.Embed(description="Please provide a member to change their nickname.", colour=config.Colors.red)
            await botmsg.edit(embed=notMemberEmbed)
            return
        if nickname == None:
            gettingNickEmbed = discord.Embed(description=f"Getting {member.mention}'s nickname {config.Emojis.loading}", colour=config.Colors.gray)
            await botmsg.edit(embed=gettingNickEmbed)
            await asyncio.sleep(1)
            if member.nick == None:
                notNickEmbed = discord.Embed(description=f"{config.Emojis.x} **{member}** does not have a nickname.")
                await botmsg.edit(embed=notNickEmbed)
                return
            else:
                nickEmbed = discord.Embed(description=f"**{member}**'s nickname is: {member.nick}", colour=config.Colors.green)
                await botmsg.edit(embed=nickEmbed)
                return
        if str(nickname) == member.nick:
            sameNickEmbed = discord.Embed(description=f"{config.Emojis.x} That nickname is the same as **{member}**'s nickname.", colour=config.Colors.red)
            await botmsg.edit(embed=sameNickEmbed)
            return
        if str(nickname).lower() == "remove":
            if member.nick == None:
                notNickEmbed2 = discord.Embed(description=f"{config.Emojis.x} **{member}** does not have a nickname. Therefore, I cannot remove it.", colour=config.Colors.red)
                await botmsg.edit(embed=notNickEmbed2)
                return
            else:
                await member.edit(nick=member.name)
                removedNickEmbed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've removed **{member}**'s nickname", colour=config.Colors.green)
                await botmsg.edit(embed=removedNickEmbed)
                return
        else:
            await member.edit(nick=nickname)
            updatedNickEmbed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've changed **{member}**'s nickname to: {nickname}.", colour=config.Colors.green)
            await botmsg.edit(embed=updatedNickEmbed)
            return
    except Exception as e:
        if str(e) == "403 Forbidden (error code: 50013): Missing Permissions":
            errorEmbed = discord.Embed(description=f"**Error!** It seems like I'm missing permissions to change **{member}**'s nickname.", colour=config.Colors.red)
            await botmsg.edit(content="", embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
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
@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE NICKNAMES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE NICKNAMES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='reminder', aliases=['remind'])
async def reminder(ctx, time=None, *, msg=None):
    if not time: 
        embed = discord.Embed(description="Please provide a period of time for your reminder.", colour=config.Colors.red)
        return await ctx.send(embed=embed)
        
    if not msg:
        msg = "No description!"
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
            embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration. \n*Try: `s`, `m`, `h` or `d`.*', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return  

        await ctx.send(f"I've set a reminder of {counter}: {msg}", allowed_mentions=discord.AllowedMentions.none())
        await asyncio.sleep(seconds)
        desc = f'''`Reminder:` {msg} \n`Jump to message:` [click here]({ctx.message.jump_url})'''
        reminderEmbed = discord.Embed(description=desc, colour=config.Colors.green)
        await ctx.channel.send(f'Hey {ctx.author.mention}!', embed=reminderEmbed)
    except Exception as e:
        if str(e).startswith("could not convert string to float"):
            embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration. \n*Try: `s`, `m`, `h` or `d`.*', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `reminder` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command('roleinfo', aliases=['ri', 'role'])
@commands.guild_only()
async def roleinfo(ctx, role:discord.Role=None):
    if not role:
        embed = discord.Embed(description='Please provide a role ID.', colour=config.Colors.red)
        await ctx.send(embed=embed)
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
        members = []
        for member in role.members:
            members.append("member")
        roleinfoDesc = f'''**Role name:** {role.name} ({role.id}) \n**Created on** {role.created_at.strftime("%A %d %B %Y, %H:%M")} \n**Position:** {len(guild.roles)-role.position} \n**Is managed?** {role.managed} \n**Is hoisted?** {role.hoist} \n**Color:** {role.color} \n**Members:** {len(members)} \n**Permissions:** {', '.join(perms)}'''
        roleinfoEmbed = discord.Embed(title=roleinfoTitle, description=roleinfoDesc, colour=role.color)
        await ctx.send(embed=roleinfoEmbed)
    except Exception as e:
        if e == "'NoneType' object has no attribute 'name'":
            errorEmbed = discord.Embed(description=f'**Error!** I cannot find that role.', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `roleinfo` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@roleinfo.error
async def roleinfo_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

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
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `say` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='servericon')
@commands.guild_only()
async def servericon(ctx):
    try:
        embed = discord.Embed(title = f'Icon of {ctx.guild}', colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_image(url='{}'.format(ctx.guild.icon_url))
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `servericon` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@servericon.error
async def servericon_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='serverinfo', aliases=['si'])
@commands.guild_only()
async def serverinfo(ctx):
    try:
        guild = ctx.guild
        owner = await bot.fetch_user(guild.owner.id)
        general = f'''**Owner:** {owner} \n**Owner ID:** {owner.id} \n**Guild ID:** {guild.id} \n**Created:** {guild.created_at.strftime("%d %B %Y, %H:%M")}'''
        bots = []
        humans = []
        botperms = dict(ctx.me.guild_permissions)
        userperms = dict(ctx.author.guild_permissions)
        if botperms["ban_members"] is True:
            if userperms["ban_members"] is True:
                permsAllowed = True
                bans = len(await guild.bans())
            if userperms["ban_members"] is False:
                permsAllowed = False
        if botperms["ban_members"] is False:
            permsAllowed = False
        members = guild.members
        for member in members:
            if member.bot:
                bots.append('bot')
            if not member.bot:
                humans.append('human')
        if permsAllowed is True:
            statistics = f'''**Boosts:** `{guild.premium_subscription_count}` \n**Banned users:** `{bans}` \n**Total members:** `{guild.member_count}` \n`{len(humans)}` Humans | `{len(bots)}` Bots \n**Roles:** `{len(guild.roles)}` \n**Emojis:** `{len(guild.emojis)}` \n**Channels:** \n`{len(guild.text_channels)}` Text channels | `{len(guild.voice_channels)}` Voice channels'''
        if permsAllowed is False:
            statistics = f'''**Boosts:** `{guild.premium_subscription_count}` \n**Total members:** `{guild.member_count}` \n`{len(humans)}` Humans | `{len(bots)}` Bots \n**Roles:** `{len(guild.roles)}` \n**Emojis:** `{len(guild.emojis)}` \n**Channels:** \n`{len(guild.text_channels)}` Text channels | `{len(guild.voice_channels)}` Voice channels'''
        serverinfoEmbed = discord.Embed(title=f"{guild}'s information", colour=config.Colors.blue, timestamp=ctx.message.created_at)
        if ctx.guild.description != None:
            serverinfoEmbed.description = ctx.guild.description
        serverinfoEmbed.add_field(name='**__General__**', value=general)
        serverinfoEmbed.add_field(name='**__Statistics__**', value=statistics)
        if not guild.is_icon_animated():
            serverinfoEmbed.set_thumbnail(url=guild.icon_url_as(format="png"))
        elif guild.is_icon_animated():
            serverinfoEmbed.set_thumbnail(url=guild.icon_url_as(format="gif"))
        if guild.banner:
            serverinfoEmbed.set_image(url=guild.banner_url_as(format="png"))
        serverinfoEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=serverinfoEmbed)
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `serverinfo` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@serverinfo.error
async def serverinfo_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

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
        s = mentions
        roleS = util.listToStringComma(s)

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
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `userinfo` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

####################################################################################################
####################################################################################################
#Math commands

@bot.command(name='calc', aliases=['calculator'])
async def calc(ctx, x:float=None, arg=None, y:float=None):
    if arg != None:
        if x != None:
            if y != None:
                try:
                    if arg == '+':
                        result = util.add(x, y)
                        await ctx.send(result)
                        return
                    if arg == '-':
                        result = util.sub(x, y)
                        await ctx.send(result)
                        return
                    if arg == '*':
                        result = util.mult(x, y)
                        await ctx.send(result)
                        return
                    if arg == '/':
                        result = util.div(x, y)
                        await ctx.send(result)
                        return
                    else:
                        embed = discord.Embed(description=f'"{arg}" is not a valid option!', colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return   
                except Exception as e:
                    errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                    await ctx.send(embed=errorEmbed)
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
        await ctx.send('Math ERROR.')
        return
    if str('Converting to "float"') in str(error):
        embed = discord.Embed(description=f'Please provide a valid math equation. \nNote: Rememeber to add spaces between arguments. (e.g. `a!calc 1 + 1`)', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='mathrandom')
async def mathrandom(ctx, x=None, y=None):
    try:
        if x == None:
            embed = discord.Embed(description='You are missing the arguments "x" and "y". \nUse `a!help mathrandom` for more information.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if y == None:
            embed = discord.Embed(description='You are missing the argument "y". \nUse `a!help mathrandom` for more information.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        x = int(x)
        y = int(y)
        result = util.rando(x, y)
        await ctx.send(result) 
    except Exception as e:
        if "invalid literal" in str(e):
            notIntEmbed = discord.Embed(description=f"**Error!** Please use valid arguments (numbers) e.g. `a!mathrandom 1 5`", colour=config.Colors.red)
            await ctx.send(embed=notIntEmbed)
            return
        elif "empty range for" in str(e):
            notValid = discord.Embed(description=f"**Error!** The order of your values must be from lowest to highest. \n Note: Only use numbers, e.g. `a!mathrandom 1 5`", colour=config.Colors.red)
            await ctx.send(embed=notValid)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `mathrandom` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@mathrandom.error
async def mathrandom_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='mathsq')
async def mathsq(ctx, x=None):
    if x == None:    
        embed = discord.Embed(description='You are missing the argument "x". \nUse `a!help mathsq` for more information.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 
    else:
        try:  
            x = float(x)
            result = util.sq(x)
            await ctx.send(result)
        except Exception as e:
            if "could not convert string to float" in str(e):
                notIntEmbed = discord.Embed(description=f"**Error!** Please use a valid argument (number) e.g. `a!mathsq 2`", colour=config.Colors.red)
                await ctx.send(embed=notIntEmbed)
                return
            else:
                errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.send(embed=errorEmbed)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                description=f"""Error while using `mathsq` command:
                    `[Content]` {ctx.message.content} 
                    `[Error]` {e}"""
                logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await logErrorsChannel.send(embed=logErrorsEmbed)
                return
@mathsq.error
async def mathsq_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='mathsqrt')
async def mathsqrt(ctx, x=None):
    if x == None:    
        embed = discord.Embed(description='You are missing the argument "x". \nUse `a!help mathsqrt` for more information.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  
    else:     
        try:    
            x = float(x)
            result = util.sqrt(x)
            await ctx.send(result)
        except Exception as e:
            if "could not convert string to float" in str(e):
                notIntEmbed = discord.Embed(description=f"**Error!** Please use a valid argument (number) e.g. `a!mathsqrt 4`", colour=config.Colors.red)
                await ctx.send(embed=notIntEmbed)
                return
            else:
                errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.send(embed=errorEmbed)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
                description=f"""Error while using `mathsqrt` command:
                    `[Content]` {ctx.message.content} 
                    `[Error]` {e}"""
                logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
                logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await logErrorsChannel.send(embed=logErrorsEmbed)
                return 
@mathsqrt.error
async def mathsqrt_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

####################################################################################################
####################################################################################################
##Moderation commands

@bot.command(name='addrole')
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def addrole(ctx, role:discord.Role=None, *, member:discord.Member=None):
    if role == None:
        notRoleEmbed = discord.Embed(description="Please provided a Discord role.", colour=config.Colors.red)
        await ctx.send(embed=notRoleEmbed)
        return
    if member == None:
        notMembersEmbed = discord.Embed(description="Please provide a member that will get the role.", colour=config.Colors.red)
        await ctx.send(embed=notMembersEmbed)
        return
    try:
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot add the role to that member because they have the same role as me or their top role is above mine.", colour=role.color)
            await ctx.send(embed=embed)
            return
        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="It seems like I cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.send(embed=embed)
            return
        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            embed = discord.Embed(description="It seems like you cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.send(embed=embed)
            return
        if role in member.roles:
            embed = discord.Embed(description="That member already has that role.", colour=role.color)
            await ctx.send(embed=embed)
            return
        await member.add_roles(role, reason=f"{ctx.author} used command `addrole`.")
        embed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've successfully added the role {role.mention} to {member.mention}", colour=role.color)
        await ctx.send(embed=embed)
    except Exception as e:
        if str(e) == "403 Forbidden (error code: 50013): Missing Permissions":
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to add that role.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='ban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to ban.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        if member == ctx.me:
            embed = discord.Embed(description="I can't ban myself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member  == ctx.author:
            embed = discord.Embed(description="You can't ban yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot ban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        guild = ctx.guild 
        await member.ban(reason=f'{ctx.author}: {reason}')
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was banned | `{reason}`') 
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to ban that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `ban` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="bans")
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
@commands.cooldown(1, 60, type=commands.BucketType.user)
async def bans(ctx):
    try:
        desc = []
        guild = ctx.guild
        bans = await guild.bans()
        if len(bans) == 0:
            noBansEmbed = discord.Embed(description="This server has no banned members.", colour=config.Colors.red)
            await ctx.send(embed=noBansEmbed)
            return
        for ban in bans:
            desc.append(f"{ban.user}({ban.user.id}): {ban.reason}")
        s = desc
        desc = util.listToStringSpace(s)
        bansEmbed = discord.Embed(title=f"Server bans of {guild}", description=desc, timestamp=ctx.message.created_at, colour=config.Colors.blue)
        bansEmbed.set_author(name=f"{len(bans)} bans")
        bansEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=bansEmbed)
        return
    except Exception as e:
        if "or fewer in length" in str(e):
            tooLongBansEmbed = discord.Embed(description="The bans of this server are too long. Therefore I was unable to send an embed with the bans.", timestamp=ctx.message.created_at, colour=config.Colors.blue)
            tooLongBansEmbed.set_author(name=f"{len(bans)} bans")
            tooLongBansEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=tooLongBansEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `bans` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@bans.error
async def bans_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='kick', pass_context=True)
@commands.guild_only()
@commands.bot_has_permissions(kick_members=True)
@commands.has_permissions(ban_members=True)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        if member == ctx.me:
            embed = discord.Embed(description="I can't kick myself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member  == ctx.author:
            embed = discord.Embed(description="You can't kick yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot kick that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.kick(reason=f'{ctx.author}: {reason}')
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was kicked | `{reason}`') 
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to kick that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `kick` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='mute')
@commands.guild_only()
@commands.bot_has_permissions(manage_roles=True)
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member=None, duration=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not duration:
            embed = discord.Embed(description='Please specify a duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        if member == ctx.me:
            embed = discord.Embed(description="I can't mute myself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member  == ctx.author:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        if not mutedRole:
            embed = discord.Embed(description='I was unable to find the muted role. \n*Note: the role name should be `Muted`.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if mutedRole in member.roles:
            embed = discord.Embed(description="That user is already muted.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
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
            embed = discord.Embed(description=f'**Error!** "{duration}" is not a valid duration. \n*Try: `s`, `m`, `h` or `d`.*', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return  
        await member.add_roles(mutedRole, reason=f"{ctx.author}: {reason}")
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was muted for {counter} | `{reason}`')
        await asyncio.sleep(seconds)
        if mutedRole in member.roles:
            await member.remove_roles(mutedRole, reason="Temporary mute completed.")
        if not mutedRole in member.roles:
            return
    except Exception as e:
        if str(e).startswith("could not convert string to float"):
            embed = discord.Embed(description=f'**Error!** "{duration}" is not a valid duration. \n*Try: `s`, `m`, `h` or `d`.*', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return  
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to mute that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `mute` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CommandInvokeError):
        if str('ValueError') in str(error): 
            embed = discord.Embed(description=f'**Error!** Your message does not include a valid duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='pmute', aliases= ['pm'])
@commands.guild_only()
@commands.bot_has_permissions(manage_roles=True)
@commands.has_permissions(ban_members=True)
async def pmute(ctx, member: discord.Member=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        if member == ctx.me:
            embed = discord.Embed(description="I can't mute myself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member  == ctx.author:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        if not mutedRole:
            embed = discord.Embed(description='I was unable to find the muted role. \n*Note: the role name should be `Muted`.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if mutedRole in member.roles:
            embed = discord.Embed(description="That user is already muted.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.add_roles(mutedRole, reason=f"{ctx.author}: {reason}")
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was permanently muted | `{reason}`')
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to mute that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `pmute` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@pmute.error
async def pmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='purge', aliases=['clear'])
@commands.guild_only()
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages = True)
@commands.cooldown(3, 60, type=commands.BucketType.user)
async def purge(ctx, am=None):
    try:
        if am == None:
            amount = 15
        elif am != None:
            amount = int(am)
        if amount > 500:
            embed = discord.Embed(description=f'You can only purge **500** messages at a time and you tried to delete **{amount}**.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if amount <= 0:
            notIntEmbed = discord.Embed(description=f"**Error!** Amount of messages cannot be negative numbers or 0.", colour=config.Colors.red)
            await ctx.send(embed=notIntEmbed)
            return
        if amount <= 500:
            if amount >=1:
                await ctx.message.delete()
                await ctx.channel.purge(limit=amount)
                e = discord.Embed(description=f'Deleted {amount} message(s) {config.Emojis.loading}', colour=config.Colors.red)
                botMsg = await ctx.send(embed=e)
                await asyncio.sleep(5)
                await botMsg.delete()
    except Exception as e:
        if "invalid literal" in str(e):
            notIntEmbed = discord.Embed(description=f"**Error!** `{am}` is not valid amount of messages.", colour=config.Colors.red)
            await ctx.send(embed=notIntEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `purge` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='removerole')
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def removerole(ctx, role:discord.Role=None, *, member:discord.Member=None):
    if role == None:
        notRoleEmbed = discord.Embed(description="Please provided a Discord role.", colour=config.Colors.red)
        await ctx.send(embed=notRoleEmbed)
        return
    if member == None:
        notMembersEmbed = discord.Embed(description="Please provide a member to remove their role.", colour=config.Colors.red)
        await ctx.send(embed=notMembersEmbed)
        return
    try:
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot remove the role from that member because they have the same role as me or their top role is above mine.", colour=role.color)
            await ctx.send(embed=embed)
            return   
        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="It seems like I cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.send(embed=embed)
            return
        if role.position >= ctx.author.top_role.position and ctx.author != ctx.guild.owner:
            embed = discord.Embed(description="It seems like you cannot access that role in the role hierarchy.", colour=role.color)
            await ctx.send(embed=embed)
            return
        if not role in member.roles:
            embed = discord.Embed(description="That member does not have that role.", colour=role.color)
            await ctx.send(embed=embed)
            return
        await member.remove_roles(role, reason=f"{ctx.author} used command `removerole`.")
        embed = discord.Embed(description=f"{config.Emojis.whiteCheckMark} I've successfully removed the role {role.mention} from {member.mention}", colour=role.color)
        await ctx.send(embed=embed)
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to remove that role.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
@commands.cooldown(1, 20, type=commands.BucketType.channel)
async def slowmode(ctx, time=None):
    try:
        if not time:
            embed = discord.Embed(description="Please provide the seconds.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        seconds = 0
        if time.lower().endswith("h"):
            seconds += float(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += float(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += float(time[:-1])
            counter = f"{seconds} seconds"
        elif time.lower() == "disable":
            seconds = 0
        elif time.lower() == "0":
            seconds = 0
        else:
            embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration. \n*Try: `s`, `m`, `h` or `disable`.*', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 
        await ctx.channel.edit(slowmode_delay=seconds, reason=f"{ctx.author} used `slowmode`")
        if seconds == 0:
            await ctx.send(f"{ctx.channel.mention}'s slowmode is now disabled.")
            return
        else:
            await ctx.send(f"{ctx.channel.mention}'s slowmode is now set to **{counter}**.")
    except Exception as e:
        if "invalid literal for int" in str(e):
            errorEmbed = discord.Embed(description="**Error!** Please only provide numbers for the time (in seconds). \nExample: `a!slowmode 5`", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        if "or equal to 0" in str(e):
            errorEmbed = discord.Embed(description="**Error!** Value should be greater than or equal to 0 seconds.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        if "or equal to 21600." in str(e):
            errorEmbed = discord.Embed(description="**Error!** Value should be less than or equal to 21600 seconds.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to execute that command.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return   
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `slowmode` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE CHANNELS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE CHANNELS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='softban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def softban(ctx, member:discord.Member=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to softban.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        if member == ctx.me:
            embed = discord.Embed(description="I can't softban myself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member  == ctx.author:
            embed = discord.Embed(description="You can't softban yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot softban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.ban(reason=f'{ctx.author}: {reason}', delete_message_days=5)
        await member.unban(reason=f'{ctx.author}: softban')
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was softbanned | `{reason}`')
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to softban that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `softban` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
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
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='unban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, member, *, reason=None):
    try: 
        if not member:
            embed = discord.Embed(description='Please specify the ID of the user to unban.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not member.isdigit():
            embed = discord.Embed(description="Please provide a valid member ID.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.isdigit():    
            user = await bot.fetch_user(member)
            await ctx.guild.fetch_ban(discord.Object(id=user.id))
        if not reason:
            reason = "No reason provided."
        if user == ctx.me:
            embed = discord.Embed(description="I am not banned here.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if user  == ctx.author:
            embed = discord.Embed(description="You are not banned here.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await ctx.guild.unban(user, reason=f"{ctx.author}: {reason}")  
        await ctx.send(f"{config.Emojis.ballotBoxWithCheck} **{user}** was unbanned | `{reason}`")  
    except discord.NotFound:
        embed = discord.Embed(description='That user is not banned here.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to unban that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `unban` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='unmute')
@commands.guild_only()
@commands.bot_has_permissions(manage_roles=True)
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member=None, *, reason=None):
    try:
        if not member:
            embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not reason:
            reason = "No reason provided."
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mutedRole:
            embed = discord.Embed(description='I was unable to find the muted role. \n*Note: the role name should be `Muted`.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(description="I can't mute you.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member == ctx.me:
            embed = discord.Embed(description='I am not muted.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if not mutedRole in member.roles:
            embed = discord.Embed(description="That user is not muted.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.top_role >= ctx.me.top_role:
            embed = discord.Embed(description="I cannot unmute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.remove_roles(mutedRole, reason=f"{ctx.author}: {reason}")
        await ctx.send(f"{config.Emojis.ballotBoxWithCheck} **{member}** was unmuted | `{reason}`")     
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to unmute that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `unmute` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE ROLES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="voicemute")
@commands.guild_only()
@commands.has_guild_permissions(mute_members=True)
@commands.bot_has_guild_permissions(mute_members=True)
async def voicemute(ctx, member: discord.Member = None, *, reason=None):
    try:
        if not member:
            notMemberEmbed = discord.Embed(description="Please provide a member to mute in a voice channel.", colour=config.Colors.red)
            await ctx.send(embed=notMemberEmbed)
            return
        if not reason:
            reason = "No reason provided."
        if not member.voice:
            embed = discord.Embed(description="That member is not in a voice channel.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.voice.mute == True:
            embed = discord.Embed(description="That member is already muted.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.edit(mute=True, reason=f"{ctx.author}: {reason}")
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was voice muted | `{reason}`')
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to voice mute that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `voicemute` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@voicemute.error
async def voicemute_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MUTE MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MUTE MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="voiceunmute")
@commands.guild_only()
@commands.has_guild_permissions(mute_members=True)
@commands.bot_has_guild_permissions(mute_members=True)
async def voiceunmute(ctx, member: discord.Member = None, *, reason=None):
    try:
        if not member:
            notMemberEmbed = discord.Embed(description="Please provide a member to unmute in a voice channel.", colour=config.Colors.red)
            await ctx.send(embed=notMemberEmbed)
            return
        if not reason:
            reason = "No reason provided."
        if not member.voice:
            embed = discord.Embed(description="That member is not in a voice channel.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member == ctx.author:
            embed = discord.Embed(description="You can't unmute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if member.voice.mute == False:
            embed = discord.Embed(description="That member is not muted.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        await member.edit(mute=False, reason=f"{ctx.author}: {reason}")
        await ctx.send(f'{config.Emojis.ballotBoxWithCheck} **{member}** was voice unmuted | `{reason}`')
    except Exception as e:
        if "Missing Permissions" in str(e):
            errorEmbed = discord.Embed(description="**Error!** It seems like I'm missing permissions to voice unmute that user.", colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `voice unmute` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@voiceunmute.error
async def voiceunmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MUTE MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MUTE MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

####################################################################################################
####################################################################################################
##Owner commands
@bot.command(name='DM', aliases=['dm', 'msg'])
@commands.guild_only()
@commands.is_owner()
async def DM(ctx, memberID=None, *, message=None):
    if not memberID:
        notMemberID = discord.Embed(description="Please provide the ID of the member.", colour=config.Colors.red)
        await ctx.send(embed=notMemberID)
        return
    if not message:
        notmessage = discord.Embed(description="Please provide the message to send.", colour=config.Colors.red)
        await ctx.send(embed=notmessage)
        return
    try:
        botMsg = await ctx.send(f'DMing user {config.Emojis.loading}')
        member = await bot.fetch_user(memberID)
        await asyncio.sleep(2)
        embed = discord.Embed(description=message, colour=config.Colors.orange)
        embed.set_footer(text=f'Sent by {ctx.author}', icon_url=ctx.author.avatar_url)
        await member.send(embed=embed)
        logEmbed = discord.Embed(title=f'{ctx.author.name} has sent a DM to {member.name}', description=message, colour=config.Colors.orange, timestamp=ctx.message.created_at)
        logEmbed.set_footer(text=member, icon_url=member.avatar_url)
        DMs_channel = bot.get_channel(config.Channels.DMsChannel)
        await DMs_channel.send(embed=logEmbed)
        await botMsg.edit(content=f'DM sent successfully! {config.Emojis.whiteCheckMark}')
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
    except Exception as e:
        if "is not snowflake" and "user_id" in str(e):
            embed = discord.Embed(description="That is not a valid user ID.", colour=config.Colors.red)
            await botMsg.edit(embed=embed)
            return
        if "'ClientUser' object has no attribute 'create_dm'" in str(e):
            embed = discord.Embed(description="I can't DM myself.", colour=config.Colors.red)
            await botMsg.edit(embed=embed)
            return
        if "Cannot send messages" in str(e):
            embed = discord.Embed(description="I was unable to send a DM to that user.", colour=config.Colors.red)
            await botMsg.edit(embed=embed)
            return
        if "Unknown User" in str(e):
            embed = discord.Embed(description="That's not a valid user.", colour=config.Colors.red)
            await botMsg.edit(embed=embed)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await botMsg.edit(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `DM` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@DM.error 
async def DM_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="logout")
@commands.is_owner()
async def logout(ctx):
    try:
        await ctx.send(f"Guess it's time to say goodbye!, for now {config.Emojis.wave}")
        await bot.close()
        print(f"{ctx.author} has disconnected the bot from Discord today at {ctx.message.created_at}")
    except Exception as e:
        errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.send(embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
        description=f"""Error while using `logout` command:
            `[Content]` {ctx.message.content} 
            `[Error]` {e}"""
        logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
        logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await logErrorsChannel.send(embed=logErrorsEmbed)
        return
@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

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
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `save` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@save.error
async def save_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name="updatereport", aliases=["ur"])
@commands.guild_only()
@commands.is_owner()
async def updatereport(ctx, messageID=None, *, comment=None):
    try:
        if messageID == None:
            embed = discord.Embed(description="Please provide the message ID.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        if comment == None:
            embed = discord.Embed(description="Please provide the comment.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
        updatingEmbed = discord.Embed(description=f"Updating report {config.Emojis.loading}", colour=config.Colors.gray)
        botMsg = await ctx.send(embed=updatingEmbed)
        reportsChannel = await bot.fetch_channel(config.Channels.reportsChannel)
        reportMsg = await reportsChannel.fetch_message(messageID)
        await reportMsg.edit(content=f"Comment from {ctx.author.mention}: {comment}", allowed_mentions=discord.AllowedMentions.none())
        embeds = reportMsg.embeds
        for embed in embeds:
            user = await bot.fetch_user(embed.footer.text)
            desc = f'''Hello {user} \nThis message was sent to you because the status of your report was updated. \nReport message: {embed.description} \nComment: {comment} \nCommented by: {ctx.author}'''
            updatedReportEmbed = discord.Embed(description=desc, colour=config.Colors.purple, timestamp=ctx.message.created_at)
            try:
                await user.send(embed=updatedReportEmbed)
            except Exception:
                pass
            updatedReport = discord.Embed(description=f"The status of that report was successfully updated {config.Emojis.whiteCheckMark}", colour=config.Colors.green)
            await botMsg.edit(embed=updatedReport)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
    except Exception as e:
        if "Invalid Form Body" in str(e):
            notValidMessageID = discord.Embed(description="That is not a valid Message ID.", colour=config.Colors.red)
            await botMsg.edit(embed=notValidMessageID)
            return
        if "Unknown Message" in str(e):
            messageNotFound = discord.Embed(description="I could not find that message.", colour=config.Colors.red)
            await botMsg.edit(embed=messageNotFound)
            return
        if "Cannot edit a message authored by another user" in str(e):
            notOwnedMessage = discord.Embed(description="I am not the author of that message.", colour=config.Colors.red)
            await botMsg.edit(embed=notOwnedMessage)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await botMsg.edit(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `updatereport` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@updatereport.error
async def updatereport_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)

@bot.command(name='us', aliases=['updatesuggestion'])
@commands.guild_only()
@commands.is_owner()
async def us(ctx, msgID:int=None, type=None, *, reason=None):
    if msgID == None:
        embed = discord.Embed(description="Please provide the message ID.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if type == None:
        embed = discord.Embed(description="Please specify if the status should be accepted, denied or pending.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if reason == None:
        if str(type).lower() == 'pending':
            pass
        else:
            embed = discord.Embed(description="You need to provide a reason.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    updatingEmbed = discord.Embed(description=f"Updating suggestion {config.Emojis.loading}", colour=config.Colors.gray)
    botMsg = await ctx.send(embed=updatingEmbed)
    await asyncio.sleep(2)
    try:    
        if str(type).lower() == 'accept':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Accepted** {config.Emojis.whiteCheckMark} | Reason: {reason}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.clear_reaction(emoji1)
            await msg.clear_reaction(emoji2)

            embeds = msg.embeds
            for embed in embeds:
                user = await bot.fetch_user(embed.footer.text)
                desc = f'''Hello {user} \nThis message was sent to you because the status of your suggestion was updated. \nYour suggestion: {embed.description} \nStatus: **Accepted** \nComment: {reason} \nCommented by: {ctx.author}'''
                updatedSuggestionAcceptedEmbed = discord.Embed(description=desc, colour=config.Colors.green, timestamp=ctx.message.created_at)
                try:
                    await user.send(embed=updatedSuggestionAcceptedEmbed)
                except Exception:
                    pass
                updatedSuggestion = discord.Embed(description=f"The status of that suggestion was successfully updated {config.Emojis.whiteCheckMark}", colour=config.Colors.green)
                await botMsg.edit(embed=updatedSuggestion)
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
            
            embeds = msg.embeds
            for embed in embeds:
                user = await bot.fetch_user(embed.footer.text)
                desc = f'''Hello {user} \nThis message was sent to you because the status of your suggestion was updated. \nYour suggestion: {embed.description} \nStatus: **Denied** \nComment: {reason} \nCommented by: {ctx.author}'''
                updatedSuggestionDeniedEmbed = discord.Embed(description=desc, colour=config.Colors.green, timestamp=ctx.message.created_at)
                try:
                    await user.send(embed=updatedSuggestionDeniedEmbed)
                except Exception:
                    pass
                updatedSuggestion = discord.Embed(description=f"The status of that suggestion was successfully updated {config.Emojis.whiteCheckMark}", colour=config.Colors.green)
                await botMsg.edit(embed=updatedSuggestion)
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
            
            embeds = msg.embeds
            for embed in embeds:
                user = await bot.fetch_user(embed.footer.text)
                desc = f'''Hello {user} \nThis message was sent to you because the status of your suggestion was updated. \nYour suggestion: {embed.description} \nStatus: **Pending** \nCommented by: {ctx.author}'''
                updatedSuggestionEmbed = discord.Embed(description=desc, colour=config.Colors.green, timestamp=ctx.message.created_at)
                try:
                    await user.send(embed=updatedSuggestionEmbed)
                except Exception:
                    pass
                updatedSuggestion = discord.Embed(description=f"The status of that suggestion was successfully updated {config.Emojis.whiteCheckMark}", colour=config.Colors.green)
                await botMsg.edit(embed=updatedSuggestion)
                await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
                await asyncio.sleep(5)
                await botMsg.delete()
                return
        else:
            embed = discord.Embed(description=f"{config.Emojis.x} `{type} is not a valid option.`", colour=config.Colors.red)
            await botMsg.edit(embed=embed)
            await ctx.message.add_reaction(config.Emojis.x)
            await asyncio.sleep(5)
            await botMsg.delete()
    except Exception as e:
        if "Invalid Form Body" in str(e):
            notValidMessageID = discord.Embed(description="That is not a valid Message ID.", colour=config.Colors.red)
            await botMsg.edit(embed=notValidMessageID)
            return
        if "Unknown Message" in str(e):
            messageNotFound = discord.Embed(description="I could not find that message.", colour=config.Colors.red)
            await botMsg.edit(embed=messageNotFound)
            return
        if "Cannot edit a message authored by another user" in str(e):
            notOwnedMessage = discord.Embed(description="I am not the author of that message.", colour=config.Colors.red)
            await botMsg.edit(embed=notOwnedMessage)
            return
        else:
            errorEmbed = discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.send(embed=errorEmbed)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            logErrorsChannel = bot.get_channel(config.Channels.logErrorsChannel)
            description=f"""Error while using `updatesuggestion` command:
                `[Content]` {ctx.message.content} 
                `[Error]` {e}"""
            logErrorsEmbed = discord.Embed(description=description, colour=config.Colors.red, timestamp=ctx.message.created_at)
            logErrorsEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await logErrorsChannel.send(embed=logErrorsEmbed)
            return
@us.error
async def us_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        blacklistedEmbed = discord.Embed(description=f"You are trying to execute one of our awesome commands; unfortunately, you are blacklisted from using our commands. If you want more information about why we blacklisted you and if it's possible to get unblacklisted send a direct message to the bot to open a support ticket.", colour=config.Colors.red)
        blacklistedEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(f"Hello, {ctx.author.mention}", embed=blacklistedEmbed)
################################
####################################################################################################
####################################################################################################
#Run the bot on Discord.
bot.run(os.environ['discordToken'])


