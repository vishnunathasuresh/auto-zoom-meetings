from logging import (
    basicConfig,
    INFO,
    FileHandler,
    StreamHandler,
    error,
    info,
)

from bot import Bot
from config_types import Config

basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s -->  %(message)s",
    datefmt="%I:%M:%S %p",
    handlers=[FileHandler("meeting_bot.log"), StreamHandler()],
)



def main():
    bot = Bot(Config())
    info("Starting Zoom Meeting Bot...")
    bot.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        error("Exception occurred in main():\n" + traceback.format_exc())
        raise