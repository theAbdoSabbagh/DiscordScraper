import json, os, discord, string

from rich import print
from functools import cache

header = """[bold white]██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                [/]"""
info = """[bold black]🏴 Made by Sxvxge.
[bold yellow]🚀 Star the repo: https://github.com/Sxvxgee/Discord-Scraper
[bold green]✅ Follow me: https://github.com/Sxvxgee/ [/]"""

default_data = """{
  "guild_id": 0,
  "token": "",
  "format": "png"
}
"""

@cache
def show_header():
  print(f"{header}\n{info}\n")

@cache
def check_config_file():
  # If the config file doesn't exist
  if not os.path.isfile('config.json'):
    with open('config.json', 'w+') as file:
      file.write(json.dumps(json.loads(default_data), indent = 2, sort_keys = False))

  # Validating the JSON file, adding keys if they don't exist in it
  data = json.loads(default_data)
  with open('config.json', 'r') as file:
    file_data = json.loads(file.read())
  
  for default_key, default_value in data.items():
    if default_key not in file_data.keys():
      file_data[default_key] = default_value

  with open('config.json', 'w+') as file:
    file.write(json.dumps(file_data, indent = 2, sort_keys = False))

class Logger():
  def __init__(self, bot : discord.Client) -> None:
    self.bot = bot

  def scraper(self, /, text : str):
    print(f"[bold white][Scraper] {text} [/]")

  def success(self, /, text : str):
    print(f"[bold green][Success] {text} [/]")

  def error(self, /, text : str):
    print(f"[bold red][Error] {text} [/]")

  def custom(self, /, text : str, header : str, color : str):
    print(f"[bold {color}][{header}] {text} [/]")

@cache
def get_account_settings():
  with open('config.json', 'r') as file:
    file_data = json.loads(file.read())
  
  return file_data

@cache
def create_guild_directory(guild : discord.Guild):
  if not os.path.isdir(f'DataScraped/{guild.name}'):
    return os.makedirs(f'DataScraped/{guild.name}')

  for filename in os.listdir(f'DataScraped/{guild.name}'):
    file_path = os.path.join(f'DataScraped', guild.name, filename)
    if os.path.isfile(file_path):
      os.remove(file_path)

@cache
async def create_member_file(member : discord.Member):
  if member.bot:
    return
  try:
    username = "".join(x for x in member.name if x in string.printable)
    profile = await member.guild.fetch_member_profile(member.id)
    bio = "".join(x for x in profile.bio if x in string.printable) if profile.bio is not None else "User doesn't have a bio."
    with open(f'DataScraped/{member.guild.name}/{member.id}.txt', 'w+') as file:
      file.write(f'Username: {username}\nAccount ID: {member.id}\nBio: {bio}\nDiscriminator: #{member.discriminator}\n\n\nScraped by Discord-Scraper: https://github.com/Sxvxgee/Discord-Scraper/ \nFollow Sxvxge: https://github.com/Sxvxgee/')
  except Exception as e:
    print(f"[bold red][Error] Failed to write the data of the account \"{member}\": {e} [/]")

@cache
async def download_pfp(member : discord.Member):
  if member.bot or member.avatar is None:
    return
  try:
    data = get_account_settings()
    await member.avatar.save(f'DataScraped/{member.guild.name}/{member.id}.{data["format"]}')
  except Exception as e:
    print(f"[bold red][Error] Failed to save the profile picture of the account \"{member}\": {e} [/]")