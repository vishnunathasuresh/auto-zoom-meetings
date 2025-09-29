from pprint import pprint
import webbrowser
from time import sleep
from datetime import datetime, date
from schedule import every, run_pending
from logging import debug, error, info
import sys

from config_types import Config, ClassType, Breaks, Meeting


class Bot:
    def __init__(self, config: Config, sleep_interval: int = 30):
        self.config = config
        self.breaks: Breaks = config.breaks
        self.regular_info: ClassType = config.regular
        self.lab_info: ClassType = config.labs
        self.elective_info: ClassType = config.electives
        self.start_time = config.start_time
        self.end_time = config.end_time
        self.minutes = config.join_minutes_before
        self.meetings: list[Meeting] = []
        self.weekend = config.weekend
        self.sleep_interval = sleep_interval  # Sleep interval in seconds

    def is_break_time(self, hour: int) -> bool:
        return hour in self.breaks.times

    def map_elective_time(self, meeting: Meeting) -> Meeting:
        meeting_hour = meeting.join_time.hour
        if self.elective_info.special:
            day = meeting.join_time.strftime("%a").lower()[:3]
            elective_today = self.elective_info.time.get(day)
            if elective_today:
                for elective_time in elective_today:
                    if meeting_hour == elective_time:
                        meeting.meeting_type = "elective"
                        meeting.link = self.elective_info.link
        return meeting

    def map_lab_time(self, meeting: Meeting) -> Meeting:
        meeting_hour = meeting.join_time.hour
        if self.lab_info.special:
            day = meeting.join_time.strftime("%a").lower()[:3]
            lab_today = self.lab_info.time.get(day)
            if lab_today:
                for lab_time in lab_today:
                    if meeting_hour == lab_time:
                        meeting.meeting_type = "lab"
                        meeting.link = self.lab_info.link
        return meeting

    def filter_redundant_meetings(self, meetings: list[Meeting]) -> list[Meeting]:
        indexes_to_remove = set()
        for index in range(len(meetings)):
            meeting = meetings[index]
            if meeting.meeting_type == "lab":
                lab_duration = self.lab_info.duration
                if lab_duration > 1:
                    for offset in range(1, lab_duration):
                        if index + offset < len(meetings):
                            indexes_to_remove.add(index + offset)

            if meeting.meeting_type == "elective":
                elective_duration = self.elective_info.duration
                if elective_duration > 1:
                    for offset in range(1, elective_duration):
                        if index + offset < len(meetings):
                            indexes_to_remove.add(index + offset)

            if self.is_break_time(meeting.join_time.hour):
                indexes_to_remove.add(index)

        # Remove meetings in reverse order to avoid indexing issues
        for index in sorted(indexes_to_remove, reverse=True):
            meetings.pop(index)

        return meetings

    def generate_schedule(self):
        # store dates in meetings
        meeting_times = list(
            datetime.strptime(f"{date.today()} {hour}:{self.minutes}", "%Y-%m-%d %H:%M")
            for hour in range(self.start_time, self.end_time)
        )

        self.meetings = [
            Meeting(
                join_time=meeting_time,
                meeting_type="regular",
                link=self.regular_info.link,
            )
            for meeting_time in meeting_times
        ]
        self.meetings = list(map(self.map_elective_time, self.meetings))
        self.meetings = list(map(self.map_lab_time, self.meetings))
        self.meetings = self.filter_redundant_meetings(self.meetings)

        if not self.weekend:
            if date.today().weekday() >= 5:
                self.meetings = []

    def join_meeting(self, meeting: Meeting):
        info(
            f"Joining {meeting.meeting_type} meeting at {meeting.join_time.strftime('%H:%M')}"
        )
        try:
            webbrowser.open(meeting.link)
        except Exception as e:
            error(f"Failed to open meeting link: {str(e)}")

    def run(self):
        """
        Schedules all meetings for the day and enters a loop to join them at the correct time.

        - Calls generate_schedule() to build today's meeting list.
        - Schedules each meeting using the 'schedule' library to run at the exact join time.
        - Checks for date change in the main loop; if the date changes, regenerates and reschedules meetings for the new day.
        - Enters an infinite loop, calling run_pending() and sleeping for self.sleep_interval seconds.
        - If the script is not running or the system is asleep at the scheduled time, the meeting will be missed (lapse).
        - The schedule library does not run missed jobs retroactively.
        - Logs all activity and errors.
        """
        import schedule
        from datetime import date

        def schedule_meetings():
            # Clear all jobs
            jobs = list(schedule.get_jobs())
            for job in jobs:
                schedule.cancel_job(job)
            self.generate_schedule()
            debug(f"Today's Meetings: {self.meetings}")
            if not self.meetings:
                info("No meetings scheduled for today.")
                return
            for meeting in self.meetings:
                schedule.every().day.at(meeting.join_time.strftime("%H:%M")).do(
                    self.join_meeting, meeting
                )
            info("Scheduler set up. Waiting to join meetings...")

        # Initial schedule
        schedule_meetings()
        current_day = date.today()

        while True:
            try:
                run_pending()
                sleep(self.sleep_interval)
                # Check for date change
                if date.today() != current_day:
                    current_day = date.today()
                    info("Date changed. Regenerating schedule for new day...")
                    schedule_meetings()
            except KeyboardInterrupt:
                info("Bot stopped by user.")
                sys.exit()
            except Exception as e:
                error(f"Unexpected error: {str(e)}")
