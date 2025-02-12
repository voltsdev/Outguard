import discord
from discord.ext import commands
import json
import os

# -> All intents and prefix command.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

async def get_prefix(bot, message):
    if not message.guild:
        return ">"
        
    prefix_cog = bot.get_cog('SetPrefix')
    if prefix_cog:
        return prefix_cog.get_prefix(message.guild.id)
    return ">"

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# -> Asynchronous function to load cogs from JSON
async def laad_cogs_van_json(json_file):
    with open(os.path.join(os.path.dirname(__file__), json_file), "r") as file:
        data = json.load(file)
        for cog in data["cogs"]:
            await bot.load_extension(cog)  # Await load_extension because it is asynchronous


# -> Loads all cogs in the 'cogs' folder!
async def load_extensions():
    try:
        await laad_cogs_van_json("cogs.json")
        print("Successfully loaded cogs.")
    except Exception as e:
        print(f"One or more cogs failed to load: {e}")


# -> Registers when the bot is online.
@bot.event
async def on_ready():
    total_users = sum(guild.member_count for guild in bot.guilds)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{total_users} users"))
    try:
        await bot.tree.sync()  # Sync slash commands globally
        print("Slash commands have been synced.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

    print(f"Bot is online as user: {bot.user}")


# -> Main entry point to load extensions and start the bot.
async def main():
    await load_extensions()  # Load all cogs
    async with bot:
        await bot.start("LOL no")


# -> Run the bot.
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())