
class InfoCommands:
    av = 'Get and post the avatar of the user/ID mentioned.'
    avatar = 'Get and post the avatar of the user/ID mentioned.'
    ban = 'Ban a user given in the command. | At the moment the command is a permanent ban.'
    id = 'Get the ID of the user given.'
    invite = 'Invite the bot to your server.'
    kick = 'Kick a user from the server. they are still able to join again with an invite though.'
    mute = 'Mute users so they cannot send messages or join VC channels.'
    purge = 'Delete an amount of messages. | The limit of the bot that can be deleted at a time is 500 messages.'
    save = 'Save messages so the bot can send them in an embed with the `a!say` command.'
    say = 'Send the latest saved message in an embed.' 
    suggest = 'Make a new suggestion.'
    unban = 'Remove ban from user.'
    unmute = 'Remove `Muted` role from user.'



class UsageCommands:
    av = 'a!av @user'
    avatar = 'a!avatar @user'
    ban = 'a!ban @user/ID reason'
    id = 'a!id @user'
    invite = 'a!invite'
    kick = 'a!kick @user/ID reason'
    purge = 'a!purge (amount of messages that will be purged)'
    mute = 'a!mute @user/ID reason'
    save = 'a!save (your message)' 
    say = 'a!say' 
    suggest = 'a!suggest (suggestion)'
    unban = 'a!unban ID reason'
    unmute = 'a!unmute @user/ID reason'


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
