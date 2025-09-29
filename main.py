from bot import ZoomMeetingBot
from logging import (
    basicConfig,
    INFO,
    DEBUG,
    FileHandler,
    StreamHandler,
    error,
    info,
)
from yaml import safe_load
from dataclasses import dataclass

basicConfig(
    level=DEBUG,
    format="%(asctime)s - %(levelname)s -->  %(message)s",
    datefmt="%I:%M:%S %p",
    handlers=[FileHandler("meeting_bot.log"), StreamHandler()],
)


@dataclass
class Config:
    start_time: str
    end_time: str
    repeat: bool
    weekend: bool
    lunch_hour: int
    meeting_types: dict

    def __init__(self, config_file: str = "config.yaml"):
        with open(config_file, "r") as file:
            config = safe_load(file)
        self.start_time = config.get("start_time", "09:00")
        self.end_time = config.get("end_time", "17:00")
        self.repeat = config.get("repeat", True)
        self.weekend = config.get("weekend", False)
        self.meeting_types = config.get("type", {})
        self.lunch_hour = config.get("lunch_hour", 13)
        self.end_time = config.get("end_time", "17:00")


def main():
    config = Config()
    info("Configuration loaded successfully")

    bot = ZoomMeetingBot(config)
    info("Starting Zoom Meeting Bot...")
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error(f"Error occurred: {str(e)}")
