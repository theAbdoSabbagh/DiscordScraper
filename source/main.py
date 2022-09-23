from internal.utils import show_header, check_config_file, get_account_settings, Logger
from internal.selfbot import client

show_header()
check_config_file()
log = Logger()
config = get_account_settings()

client.run(config["token"]) # type: ignore