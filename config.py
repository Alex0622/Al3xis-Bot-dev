
class InfoCommands:
    ann =               'Make announcements.'
    announce =          'Make announcements.'
    announcement =      'Make announcements.'
    av =                'Get and post the avatar of the member mentioned.'
    avatar =            'Get and post the avatar of the member mentioned.'
    ban =               'Ban the member mentioned in the command. | Permanent ban.'
    clear =             'Delete an amount of messages. | Limit of messages deleted per command: `500`.'
    id =                'Get the ID of the given member.'
    ID =                'Get the ID of the given member.' 
    info =              'Get information about the bot.'
    inv =               'Invite the bot to your server or join our Discord server.'
    invite =            'Invite the bot to your server or join our Discord server.'
    h =                 'Display the list of commands.'
    help =              'Display the list of commands.'
    kick =              'Kick a member from the server.'
    latency =           "Shows the bot's latency/ping."
    mute =              'Mute members so they cannot send messages or join VC channels. | Duration: seconds.'
    ping =              "Shows the bot's latency/ping."
    pm =                'Mute a member permanently.'
    pmute =             'Mute a member permanently.'
    pong =              "Shows the bot's latency/ping."
    purge =             'Delete an amount of messages. | Limit of messages deleted per command: `500`.'
    remind =            'Set a reminder. | Duration: minutes.'
    reminder =          'Set a reminder. | Duration: minutes.'
    save =              'Save messages to a channel.'
    say =               'Send the latest saved message in an embed.'
    softban =           'Ban and automatically unban a member.' 
    sug =               'Make a new suggestion for the bot.'
    suggest =           'Make a new suggestion for the bot.'
    ui =                'Get information about a member.'
    unban =             'Remove ban from member.'
    unmute =            'Remove `Muted` role from member.'
    user =              'Get information about a member.'
    userinfo =          'Get information about a member.'



class UsageCommands:
    ann =               "`a!ann #channel` | After this you will send the title (if you don't want to set a title use `None` when the bot requests a title) and then a description in a new message."
    announce =          "`a!announce #channel` | After this you will send the title (if you don't want to set a title use `None` when the bot requests a title) and then a description in a new message."
    announcement =      "`a!announcement #channel` | After this you will send the title (if you don't want to set a title use `None` when the bot requests a title) and then a description in a new message."
    av =                '`a!av (member)`'
    avatar =            '`a!avatar (member)`'
    ban =               '`a!ban (member) (reason)`'
    clear =             '`a!clear (amount of messages that will be purged)`'
    id =                '`a!id (member)`'
    ID =                '`a!ID (member)`'
    info =              '`a!info`'
    inv =               '`a!inv`'
    invite =            '`a!invite`'
    h =                 '`a!h (command)` | If you do not mention a command, it will show the general help command.'
    help =              '`a!help (command)` | If you do not mention a command, it will show the general help command.'
    kick =              '`a!kick (member) (reason)`'
    latency =           '`a!latency`'
    mute =              '`a!mute (member) (duration) (reason)`'
    ping =              '`a!ping`'
    pm =                '`a!pm (member) (reason)`'
    pmute =             '`a!pmute (member) (reason)`'
    pong =              '`a!pong`'
    purge =             '`a!purge (amount of messages that will be purged)`'
    remind =            '`a!remind (time) (message)`'
    reminder =          '`a!reminder (time) (message)`'
    save =              '`a!save (message)`' 
    say =               '`a!say (message)` | if there is no message, it will send the latest messaged saved.'
    sug =               '`a!sug (suggestion)`'
    softban =           '`a!softban (member) (reason)`' 
    suggest =           '`a!suggest (suggestion)`'
    ui =                '`a!userinfo (member)`'
    unban =             '`a!unban ID (reason)`'
    unmute =            '`a!unmute (member) (reason)`'
    user =              '`a!userinfo (member)`'
    userinfo =          '`a!userinfo (member)`'
    
    
    
class AliasesCommands:
    ann =               'announce, announcement'
    announce =          'announcement, ann'
    announcement =      'ann, announce'
    av =                'avatar'
    avatar =            'av'
    ban =               'No aliases'
    clear =             'purge'
    id =                'ID'
    ID =                'id'
    info =              'No aliases'
    inv =               'invite'
    invite =            'inv'
    h =                 'help'
    help =              'h'
    kick =              'No aliases'
    latency =           'ping, pong'
    mute =              'No aliases'
    ping =              'pong, latency'
    pm =                'pmute'
    pmute =             'pm'
    purge =             'clear'
    pong =              'ping, latency'
    remind =            'reminder'
    reminder =          'remind'
    save =              'No aliases'
    say =               'No aliases'
    softban =           'No aliases'
    sug =               'suggest'
    suggest =           'sug'
    ui =                'user, userinfo'
    unban =             'No aliases'
    unmute =            'No aliases'
    user =              'ui, userinfo'
    userinfo =          'ui, user'



class RequiredPermissions:
    ann =               'ADMINISTRATOR'
    announce =          'ADMINISTRATOR'
    announcement =      'ADMINISTRATOR'
    av =                'NO REQUIRED PERMISSION'
    avatar =            'NO REQUIRED PERMISSION'
    ban =               'BAN MEMBERS'
    clear =             'MANAGE MESSAGES'
    id =                'NO REQUIRED PERMISSION'
    ID =                'NO REQUIRED PERMISSION'
    info =              'NO REQUIRED PERMISSION'
    inv =               'NO REQUIRED PERMISSION'
    invite =            'NO REQUIRED PERMISSION'
    h =                 'NO REQUIRED PERMISSION'
    help =              'NO REQUIRED PERMISSION'
    kick =              'BAN MEMBERS'
    latency =           'NO REQUIRED PERMISSION'
    mute =              'BAN MEMBERS'
    ping =              'NO REQUIRED PERMISSION'
    pm =                'BAN MEMBERS'
    pmute =             'BAN MEMBERS'
    purge =             'MANAGE MESSAGES'
    pong =              'NO REQUIRED PERMISSION'
    remind =            'NO REQUIRED PERMISSION'
    reminder =          'NO REQUIRED PERMISSION'
    save =              "BOT'S OWNER"
    say =               "BOT'S OWNER"
    softban =           'BAN MEMBERS'
    sug =               'NO REQUIRED PERMISSION'
    suggest =           'NO REQUIRED PERMISSION'
    ui =                'NO REQUIRED PERMISSION'
    unban =             'BAN MEMBERS'
    unmute =            'BAN MEMBERS'
    user =              'NO REQUIRED PERMISSION'
    userinfo =          'NO REQUIRED PERMISSION'


    
class Channels:
    suggestionsChannel = 793989328602791946
    botChannel = 793989024879476767
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
    loading = '<a:loading:823701755946074142>'
