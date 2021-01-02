import discord 
from discord.ext import commands 
import datetime
import asyncio
import config, os
import time
    
#Bot (our bot)
bot = commands.Bot(command_prefix=['a!', 'A!']) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')


@bot.event
async def on_ready():
    #Message that will be sent when the bot is online.
    print('Bot started succesfully')
    general_channel = bot.get_channel(config.Channels.botChannel)
    await general_channel.send('Hi, I am online again.')
    #Status
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f'a!help | {len(bot.guilds)} guilds', type=1))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{config.Emojis.noEntry} Command not found, use `a!help` {config.Emojis.noEntry}')
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send(f'{config.Emojis.warning} Only bot owners can use the `{ctx.command}` command {config.Emojis.warning}')
        return
    


####################################################################################################
####################################################################################################
#Help Commnad

@bot.command()
async def help(ctx, arg = None):
    if arg == 'moderation':
        embed = discord.Embed(title='Moderation Commands.', description='Use this commands to moderate your server!', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name='Commands: ', value='```ban, kick, mute, purge, unban, unmute ``` ')
        await ctx.send(embed=embed)
    if arg == 'utility':
        embed = discord.Embed(title='Utility Commands.', description='Commands related to the bot and utility commands!', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name='Commands: ', value='```avatar, id, invite, suggest```')
        await ctx.send(embed=embed)
    if arg == 'owner':
        embed = discord.Embed(title='Bot owner commands.', description='These commands are only available for the bot owner!', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name='Commands: ', value='```save, say```')
        await ctx.send(embed=embed)
    if arg == None:
        embed = discord.Embed(title=f'Help Command | Prefix: `{ctx.prefix}`', description= 'Get a list of all available commands here!', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name='Utility Commands ', value=f'Use `{ctx.prefix}help utility` to get the list of utility  commands')
        embed.add_field(name='Moderation Commands ', value=f'Use `{ctx.prefix}help moderation` to get the list of Moderation commands', inline=False)
        embed.add_field(name='Owner Commands ', value=f'`{ctx.prefix}help owner` | Only owners can use them.')
        await ctx.message.channel.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{ctx.command.aliases}` ', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
        embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
        await ctx.send(embed=embed)




####################################################################################################
####################################################################################################
##Utility Commands


@bot.command(name='avatar', aliases=['av'])
async def avatar(ctx, member: discord.Member = None): 
    if member == None:
        member = ctx.author
    embed = discord.Embed(title = f'Avatar of user {member}', colour=config.Colors.green, timestamp=ctx.message.created_at)
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)



suggestion = ''
listSuggestions = ''
@bot.command(name='suggest')
async def suggest(ctx, *, new_suggestion):  
    global suggestion
    suggestion =  new_suggestion
    description = suggestion 
    embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description = f'Suggestion: **{description}** \nUser ID: {ctx.author.id} ', colour=config.Colors.green, timestamp=ctx.message.created_at)
    await ctx.send(f'**{ctx.author}**, your suggestion **`{suggestion}`** has been submited!')

    suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
    message = await suggestions_channel.send(embed=embed)
    await message.add_reaction(config.Emojis.ballotBoxWithCheck)
    await message.add_reaction(config.Emojis.x)
    print('New suggestions | ' + suggestion)


@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You need to add a message for the suggestion!')



@bot.command(name='id')
async def id(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await ctx.send(member.id)



@bot.command(name='invite')
async def invite(ctx):
    embed = discord.Embed(title='Invite the bot to your server!', colour=config.Colors.darkGreen)
    embed.add_field(name='Invite links.', value='[Admin permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=8)')
    embed.add_field(name='Join our Discord server!', value='[Al3xis Bot Server](https://discord.gg/AAJPHqNXUy)', inline=False)
    await ctx.send(embed=embed)




####################################################################################################
####################################################################################################
##Moderation commands.


@bot.command(name='kick', pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.guild_permissions.kick_members:
                try:
                    time.sleep(0.5)
                    await ctx.send(f'User {member.mention} was kicked | `{reason}`.')
                    await member.send(f'You were kicked from {guild.name} | `{reason}`.')
                    await member.kick(reason=reason)
                    print(f'User {ctx.author} kicked {member} in server {guild.name}| {reason}')
                    logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                    logEmbed.add_field(name='User', value=member.mention)
                    logEmbed.add_field(name='Reason', value=reason) 
                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                    logChannel=bot.get_channel(config.Channels.logChannel)
                    await logChannel.send(embed=logEmbed)       
                except Exception:
                    await ctx.send('An error ocurred while runnining the command.') 
            else:
                await ctx.send(f"{ctx.author.mention} You don't have permissions to kick **{member}**!")
                return
        else: 
            await ctx.send(f"{ctx.author.mention} You don't have permissions to kick me!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You can't kick yourself!")
        return


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify an user to do that!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have permissions to use the `{ctx.command}` command!")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.guild_permissions.ban_members:
                try:
                    time.sleep(0.5)    
                    await ctx.send(f'User {member.mention} was banned | `{reason}`.')
                    await member.send(f'You were banned from {guild.name} | `{reason}`.')
                    await member.ban(reason=reason)
                    print(f'User {ctx.author} banned {member} | {reason}')
                    logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                    logEmbed.add_field(name='User', value=member.mention)
                    logEmbed.add_field(name='Reason', value=reason) 
                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                    logChannel=bot.get_channel(config.Channels.logChannel)
                    await logChannel.send(embed=logEmbed)     
                except Exception:
                    await ctx.send('An error ocurred while runnining the command.')
                    return
            else:
                await ctx.send(f"{ctx.author.mention} You don't have permissions to ban **{member}**!")
                return
        else: 
            await ctx.send(f"{ctx.author.mention} You don't have permissions to ban me!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You can't ban yourself!")
        return
    

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify an user to do that!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='unban') 
@commands.has_permissions(ban_members=True)
async def unban(ctx, UserID: int, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    member = await bot.fetch_user(UserID)
    if member != ctx.author:
        if member != ctx.me:
            try:
                time.sleep(0.5)
                await ctx.guild.unban(member)
                await ctx.send(f'User {member.mention} was unbanned | `{reason}`.')
                await member.send(f'You were unbanned from {guild.name} | `{reason}`.')
                print(f'User {ctx.author} unbanned {member} from {guild.name} | {reason}')
                logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.red, timestamp=ctx.message.created_at)
                logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                logEmbed.add_field(name='User', value=member.mention)
                logEmbed.add_field(name='Reason', value=reason) 
                logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                logChannel=bot.get_channel(config.Channels.logChannel)
                await logChannel.send(embed=logEmbed)     
            except Exception:
                await ctx.send('An error ocurred while running the command.')
                return
        else:
            await ctx.send(f"{ctx.author.mention} You can't unban me if I'm not banned!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You are not banned!")
        return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify an user to do that!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='mute')
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.guild_permissions.kick_members:
                    if not mutedRole in member.roles:
                        try:
                            time.sleep(0.5)
                            await member.add_roles(mutedRole, reason= reason)
                            await ctx.send(f'{member.mention} was muted | `{reason}`')
                            await member.send(f'You were muted in {guild.name} | `{reason}`')
                            print(f'User {ctx.author} muted {member} in server {guild.name} | {reason}')
                            logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                            logEmbed.add_field(name='User', value=member.mention)
                            logEmbed.add_field(name='Reason', value=reason) 
                            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                            logChannel=bot.get_channel(config.Channels.logChannel)
                            await logChannel.send(embed=logEmbed)     
                        except Exception:
                            await ctx.send('An error ocurred while running the command.')
                            return
                    else:
                        await ctx.send(f"**{member}** is already muted!")
                        return
                else:
                    await ctx.send(f"{ctx.author.mention} You don't have permissions to mute **{member}**!")
                    return
            else:
                await ctx.send(f"{ctx.author.mention} You can't mute me!")
                return
        else:
            await ctx.send(f"{ctx.author.mention} You can't mute yourself!")
            return
    else:   
        await ctx.send("This server doesn't have a muted role. Please create one with the name `Muted`.")
        return     


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify an user to do that!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='unmute')
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if mutedRole in member.roles:
                    try:
                        time.sleep(0.5)
                        await member.remove_roles(mutedRole)
                        await ctx.send(f'{member.mention} was unmuted | `{reason}`')
                        await member.send(f'You were unmuted in {guild.name} | `{reason}`')
                        print(f'User {ctx.author} unmuted {member} in server {guild.name} | {reason}')
                        logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception:
                        await ctx.send('An error ocurred while running the command.')
                        return
                else:
                    await ctx.send(f"**{member}** is not muted!")
                    return
            else:
                await ctx.send(f"{ctx.author.mention} I'm not muted!")
                return
        else:
            await ctx.send("You are not muted!")
            return
    else:
        await ctx.send("This server doesn't have a muted role so nobody is muted.")
        return


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify an user to do that!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 0):
    guild = ctx.guild
    if amount <= 500:
        if amount >=1:
            await ctx.channel.purge(limit=amount)
            logEmbed = discord.Embed(title=f'Command: {ctx.command}', colour=config.Colors.orange, timestamp=ctx.message.created_at)
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
        await ctx.send('Select an amount of messages that should be purged!')


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to purge messages!')
        return



####################################################################################################
####################################################################################################
##Bot Owner
savedMessage = ''
@bot.command(name='save')
@commands.is_owner()
async def save(ctx,*, new_msg=None):
    global savedMessage
    savedMessage = new_msg
    if new_msg == None:
        await ctx.send('Please provide a message to save!')
        return
    else:
        try:
            await ctx.send(f'**{ctx.author}** Your message has been saved!')
            embed = discord.Embed(title=f'{ctx.author} saved a new message.', description=savedMessage, colour=config.Colors.green, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Guild: {ctx.guild}')
            savedMessagesChannel = bot.get_channel(config.Channels.ownerChannel)
            await savedMessagesChannel.send(embed=embed)
            await ctx.message.delete()
            print(f'New message saved sent by {ctx.author} | {savedMessage}')
        except Exception:
            await ctx.send('An error ocurred while running the command.')
            return



@bot.command(name='say')
@commands.is_owner()
async def say(ctx):
    embed = discord.Embed(title='Hi!', description=savedMessage, colour=config.Colors.blue)
    await ctx.send(embed=embed)
    await ctx.message.delete()
####################################################################################################
####################################################################################################
#Run the bot on the server
bot.run(os.environ['discordToken'])


