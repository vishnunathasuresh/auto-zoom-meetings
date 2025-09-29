from logging import (
    basicConfig,
    INFO,
    FileHandler,
    StreamHandler,
    error,
    info,
)
import json
import traceback
import jsonschema

from bot import Bot
from config_types import Config, CONFIG_SCHEMA

basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s -->  %(message)s",
    datefmt="%I:%M:%S %p",
    handlers=[FileHandler("meeting_bot.log"), StreamHandler()],
)


def load_config():
    with open("config.json", "r") as file:
        config_data = json.load(file)
    return config_data


def main():
    config_data = load_config()
    jsonschema.validate(config_data, CONFIG_SCHEMA)
    bot = Bot(Config(config_data))
    info("Starting Zoom Meeting Bot...")
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error("Exception occurred in main():\n" + traceback.format_exc())
