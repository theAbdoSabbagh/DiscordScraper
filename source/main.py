from utils.useful import show_header, check_config_file, Logger, get_account_settings
from utils.selfbot import bot

show_header(); check_config_file()
log = Logger(bot)
config = get_account_settings()

bot.run(config['token'])