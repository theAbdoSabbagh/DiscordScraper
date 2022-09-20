from email.policy import default
import json, os

from rich import print

header = """[bold white]██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                [/]"""

default_data = """{
  "guild_id": 0,
  "token": "",
  "format": "png"
}
"""

def show_header():
  print(header)

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

  with open('config.json', 'w+', encoding = 'utf-8') as file:
    file.write(json.dumps(file_data, indent = 2, sort_keys = False))