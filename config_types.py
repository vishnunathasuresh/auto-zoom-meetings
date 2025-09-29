from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "start_time": 9,
    "end_time": 17,
    "weekend": False,
    "join_minutes_before": 5,
    "breaks": {"duration": 1, "times": [13]},
    "regular": {
        "special": False,
        "time": {},
        "duration": 1,
        "link": os.getenv("REGULAR"),
    },
    "labs": {
        "special": True,
        "time": {"mon": [11], "tue": [15], "wed": [10, 15]},
        "duration": 2,
        "link": os.getenv("LABS"),
    },
    "electives": {
        "special": True,
        "time": {"thu": [12], "fri": [9]},
        "duration": 1,
        "link": os.getenv("ELECTIVES"),
    },
}

@dataclass
class Breaks:
    duration: int
    times: list[int]

    def __init__(self, duration: int = 1, times: list[int] = None):
        self.duration = duration
        self.times = times if times is not None else [13]


@dataclass
class ClassType:
    special: bool
    time: dict[str, list[int]]
    duration: int
    link: str

    def __init__(
        self,
        special: bool = False,
        time: dict[str, list[int]] = None,
        duration: int = 1,
        link: str = "",
    ):
        self.special = special
        self.time = time if time is not None else {}
        self.duration = duration
        self.link = link


@dataclass
class Config:
    start_time: int
    end_time: int
    weekend: bool
    join_minutes_before: int
    breaks: Breaks
    regular: ClassType
    labs: ClassType
    electives: ClassType

    def __init__(self, config: dict = CONFIG):
        self.start_time = config["start_time"]
        self.end_time = config["end_time"]
        self.weekend = config["weekend"]
        self.join_minutes_before = config["join_minutes_before"]
        breaks_config = config["breaks"]
        self.breaks = Breaks(
            duration=breaks_config["duration"], times=breaks_config["times"]
        )
        regular_config = config["regular"]
        self.regular = ClassType(
            special=regular_config["special"],
            time=regular_config["time"],
            duration=regular_config["duration"],
            link=regular_config["link"],
        )
        labs_config = config["labs"]
        self.labs = ClassType(
            special=labs_config["special"],
            time=labs_config["time"],
            duration=labs_config["duration"],
            link=labs_config["link"],
        )
        electives_config = config["electives"]
        self.electives = ClassType(
            special=electives_config["special"],
            time=electives_config["time"],
            duration=electives_config["duration"],
            link=electives_config["link"],
        )


@dataclass
class Meeting:
    join_time: datetime
    meeting_type: str
    link: str

    def __init__(self, join_time: datetime, meeting_type: str = "regular", link: str = ""):
        self.join_time = join_time
        self.meeting_type = meeting_type
        self.link = link
    
    def __repr__(self):
        return f"Meeting(join_time={self.join_time}, meeting_type={self.meeting_type}, link={self.link})"
