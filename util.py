import math
import random
import config

def listToStringSpace(s):
    str1 = " \n"
    return (str1.join(s))

def listToString(s):
    str1 = " "
    return (str1.join(s))

def listToStringComma(s):
    str1 = ", "
    return (str1.join(s))

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

async def isNotBlacklisted(ctx):
    return ctx.author.id not in config.General.blacklistedUsers