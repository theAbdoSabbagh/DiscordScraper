import discord, random

from rich.progress import track
from discord.ext import commands
from utils.useful import get_account_settings, create_guild_directory, create_member_file, download_pfp, Logger

bot = commands.Bot(
  command_prefix = "!",
  self_bot = True,
  chunk_guilds_at_startup = False
)
data = get_account_settings()
logger = Logger(bot)

async def scrape(guild : discord.Guild):
  logger.scraper(text = 'Starting...')
  members = await guild.fetch_members([random.choice(guild.channels)])
  members = [member for member in members if not member.bot]
  logger.success(text = 'Fetched members successfully')
  return members

@bot.listen("on_ready")
async def ready():
  logger.scraper(f"Logged in as {bot.user}")
  guild_id = data['guild_id']
  guild = bot.get_guild(int(guild_id))
  create_guild_directory(guild)
  members = await scrape(guild)
  member : discord.Member; members : list
  
  for member in track(members, description = '[bold white][Scraper] Scraping profiles...[/]', refresh_per_second = 100000):
    await create_member_file(member)
    await download_pfp(member)

  logger.success("Finished scraping members profiles and data.\n")
  logger.scraper(text = "Don't forget to star the repo and follow Sxvxgee on github!")