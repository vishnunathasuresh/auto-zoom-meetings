from datetime import datetime
from logging import (
    basicConfig,
    INFO,
    FileHandler,
    StreamHandler,
    error,
    info,
)
from json import load
from os import makedirs
from traceback import format_exc
from jsonschema import validate

from bot import Bot
from config_types import Config, CONFIG_SCHEMA


makedirs("./logs", exist_ok=True)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s -->  %(message)s",
    datefmt="%I:%M:%S %p",
    handlers=[
        FileHandler(f"./logs/bot - {datetime.now().strftime('%Y-%m-%d')}.log"),
        StreamHandler(),
    ],
)


def load_config():
    with open("config.json", "r") as file:
        config_data = load(file)
    return config_data


def main():
    config_data = load_config()
    validate(config_data, CONFIG_SCHEMA)
    bot = Bot(Config(config_data))
    info("Starting Zoom Meeting Bot...")
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error("Exception occurred in main():\n" + format_exc())
