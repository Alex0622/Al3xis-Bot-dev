
class InfoCommands:
    announce = 'Make announcements.'
    avatar = 'Get and post the avatar of the user/ID mentioned.'
    ban = 'Ban the user mentioned in the command. |Permanent ban.'
    id = 'Get the ID of the user given.'
    invite = 'Invite the bot to your server.'
    help = 'Display the list of commands'
    kick = 'Kick a user from the server.'
    mute = 'Mute users so they cannot send messages or join VC channels. | duration: seconds'
    ping = "Shows the bot's latency/ping."
    pmute = 'Mute a user permanently.'
    purge = 'Delete an amount of messages. | Limit of messages deleted per command: `500`.'
    save = 'Save messages to a channel.'
    say = 'Send the latest saved message in an embed.' 
    suggest = 'Make a new suggestion.'
    unban = 'Remove ban from user.'
    unmute = 'Remove `Muted` role from user.'



class UsageCommands:
    announce = '`a!announce #channel` | after this you will send the title and then description in a new channel.'
    avatar = '`a!avatar @user/ID`'
    ban = '`a!ban @user/ID (reason)`'
    id = '`a!id @user`'
    invite = '`a!invite`'
    help = '`a!help "command"` | If you do not add a command, it will show the general help command.'
    kick = '`a!kick @user/ID (reason)`'
    mute = '`a!mute @user/ID duration (reason)`'
    ping = '`a!ping`'
    pmute = '`a!pmute @user/ID (reason)`'
    purge = '`a!purge (amount of messages that will be purged)`'
    save = '`a!save (message)`' 
    say = '`a!say (message)` | if there is no message, it will send the latest messaged saved.' 
    suggest = '`a!suggest (suggestion)`'
    unban = '`a!unban ID `(reason)`'
    unmute = '`a!unmute @user/ID (reason)`'
    
    
    
class AliasesCommands:
    announce = 'announcement', 'ann'
    avatar = 'av'
    ban = 'No aliases'
    id = 'ID'
    invite = 'inv'
    help = 'h'
    kick = 'No aliases'
    mute = 'No aliases'
    ping = 'pong', 'latency'
    pmute = 'p-mute', 'pm'
    purge = 'clear'
    save = 'No aliases'
    say = 'No aliases'
    suggest = 'sug'
    unban = 'No aliases'
    unmute = 'No aliases'

    

class Channels:
    suggestionsChannel = 793989328602791946
    botChannel = 793990563682582567
    logChannel = 793990292213727262
    ownerChannel = 793989996494192692



class Colors:
    red = 0xde0707
    ligthBlue = 0x32d9cb
    green = 0x6cfd00
    blue = 0x0037fa
    yellow = 0xf1fc14 
    orange = 0xe07007
    purple = 0x8a1bba
    darkGreen = 0x156109



class Emojis:
    ballotBoxWithCheck = '☑️'
    x ='❌'
    warning = '⚠️'
    noEntry = '⛔'
    whiteCheckMark = '✅'
    octagonalSign = '🛑'
    eyes = '👀'



# User does not have permissions = blue
# User not found = green
# Missing argument = orange
# Command not found = orange
# Help command = yellow
# Avatar command = purple
# Suggestions = green
# Reaction commands = ligthBlue
# Announce commands = lightBlue
# Invite command = darkGreen
# Save command = blue
# Say command = blue

