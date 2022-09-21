import json, os, discord, aiohttp, string, requests

from rich import print

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

def show_header():
  print(header)
  print(info)

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

def get_account_settings():
  with open('config.json', 'r') as file:
    file_data = json.loads(file.read())
  
  return file_data

def create_guild_directory(guild : discord.Guild):
  if not os.path.isdir(guild.name):
    return os.makedirs(guild.name)

  for filename in os.listdir(guild.name):
    file_path = os.path.join(guild.name, filename)
    if os.path.isfile(file_path):
      os.remove(file_path)

def create_member_file(member : discord.Member):
  if member.bot:
    return
  with open(f'{member.guild.name}/{member.name}.txt', 'w+') as file:
    file.write(f'Username: {member.name}\nAccount ID: {member.id}\nDiscriminator: {member.discriminator}\n\n\nScraped by Discord-Scraper: https://github.com/Sxvxgee/Discord-Scraper')

async def download_pfp(member : discord.Member):
  if member.bot or member.avatar is None or member.avatar.url is None:
    return
  # session : aiohttp.ClientSession
  data = get_account_settings()
  URL = member.avatar.url.replace('.webp', data['format'])
  print(URL)
  headers={
      "Authorization": data["token"],
      "content-type": "application/json"
  }
  # async with aiohttp.ClientSession(headers = headers) as session:
  #   async with session.get(URL) as response:
  #     text = await response.text()
  #     with open(f'{member.guild.name}/{member.name}.{data["format"]}', 'w+') as file:
  #       file.write(text)
  response = requests.get(URL, headers = headers)
  print(response.text, type(response.text))
  with open(f'{member.guild.name}/{member.name}.{data["format"]}', 'w+') as file:
    file.write(response.text)