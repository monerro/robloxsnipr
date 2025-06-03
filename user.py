

import discord
from discord.ext import commands
import random
import string
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

running = False  

def generate_name(length, include_numbers=True):

    chars = string.ascii_lowercase  
    if include_numbers:
        chars += string.digits  
    return ''.join(random.choice(chars) for _ in range(length))

async def check_name(name):
    async with aiohttp.ClientSession() as session:
        url = f"https://auth.roblox.com/v1/usernames/validate?request.username={name}&request.birthday=10.20.1999&request.context=Unknown"
        async with session.get(url) as resp:
            if resp.status != 200:
                return -1
            data = await resp.json()
            return data.get("code", -1)

@bot.command()
async def search(ctx, tries: int = 100, length: int = 4, numbers: bool = True):

    global running
    if running:
        await ctx.send("name check is already running.")
        return
    running = True

    await ctx.send(f" starting search for {tries} {length}-character names "
                   f"(numbers {'enabled' if numbers else 'disabled'})")

    found = []
    for _ in range(tries):
        if not running:
            await ctx.send(" search stopped.")
            break

        name = generate_name(length, include_numbers=numbers)
        code = await check_name(name)
        await asyncio.sleep(0.25)  

        if code == 0:
            found.append(name)
            await ctx.send(name)  

    running = False

@bot.command()
async def stop(ctx):

    global running
    running = False
    await ctx.send("stopping the name search")

bot.run("bot token here :)")
