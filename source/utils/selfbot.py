import discord, random

from discord.ext import commands
from utils.useful import get_account_settings, create_guild_directory, create_member_file, download_pfp, Logger

bot = commands.Bot(
  command_prefix = "!",
  self_bot = True
)
data = get_account_settings()
logger = Logger(bot)

async def scrape(guild : discord.Guild):
  logger.scraper(text = 'Starting...')
  members = await guild.fetch_members([random.choice(guild.channels)])
  logger.success(text = 'Fetched members successfully')
  return members

@bot.listen("on_ready")
async def ready():
  logger.scraper(f"Logged in as {bot.user}")
  guild_id = data['guild_id']
  # guild = await bot.fetch_guild(int(guild_id))
  guild = bot.get_guild(int(guild_id))
  create_guild_directory(guild)
  members = await scrape(guild)
  member : discord.Member
  for member in members:
    create_member_file(member)
    await download_pfp(member)