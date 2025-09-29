import webbrowser
from time import sleep
from datetime import datetime
from schedule import every, run_pending
from logging import error, info, debug, warning


class ZoomMeetingBot:
    def __init__(self, config):
        self.config = config
        self.meeting_types = config.meeting_types
        self.regular_info = self.meeting_types.get("regular", {})
        self.lab_info = self.meeting_types.get("lab", {})
        self.elective_info = self.meeting_types.get("elective", {})
        self.lab_times = self.lab_info.get("time", {})
        self.elective_times = self.elective_info.get("time", {})
        self.lab_duration = int(self.lab_info.get("duration", "2 hours").split()[0])
        self.start_hour = int(config.start_time.split(":")[0])
        self.end_hour = int(config.end_time.split(":")[0])
        self.lunch_hour = config.lunch_hour
        self.weekend = config.weekend
        self.last_meeting = None
        self.lab_end_time = None

    def join_meeting(self, url, meeting_type):
        try:
            info(
                f"Joining {meeting_type} meeting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            # TODO: Add a way to close previous meeting if still open
            # TODO: Add a way to close previous meeting browser if still open
            webbrowser.open(url)
            info(f"{meeting_type.capitalize()} meeting opened successfully in browser")
            self.last_meeting = meeting_type
        except Exception as e:
            error(f"Failed to open {meeting_type} meeting: {str(e)}")

    def is_weekday(self) -> bool:
        if self.weekend:
            return True
        return datetime.now().weekday() < 5

    def get_current_meeting(self):
        """
        Determines which meeting (lab, elective, or regular) should be joined at the current time.
        
        Returns:
            tuple: (meeting_url, meeting_type) if a meeting should be joined, otherwise (None, None).

        Logic:
        - Skips weekends if not allowed by config.
        - Skips lunch hour.
        - Only triggers at 5 minutes past the hour within allowed hours.
        - If a lab is scheduled now, returns lab meeting and blocks other meetings for the lab duration.
        - If an elective is scheduled now, returns elective meeting.
        - Otherwise, returns regular meeting if scheduled.
        - Returns (None, None) if no meeting should be joined at this time.
        """
        """
        
        """
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        weekday = now.strftime("%a").lower()[:3]

        if self.lab_end_time and now < self.lab_end_time:
            info("Currently in a lab session, skipping other meetings.")
            return None, None

        if not self.is_weekday():
            info("Skipping meeting - weekend")
            return None, None

        if hour == self.lunch_hour:
            info("Skipping meeting - lunch break")
            return None, None

        if minute != 5 and self.last_meeting:
            return None, None

        if hour < self.start_hour or hour >= self.end_hour:
            return None, None

        if self.lab_times:
            lab_today = self.lab_times.get(weekday)
            if lab_today:
                if isinstance(lab_today, list):
                    for lab_time in lab_today:
                        if hour == int(lab_time.split(":")[0]):
                            self.lab_end_time = now.replace(
                                hour=hour + self.lab_duration,
                                minute=0,
                                second=0,
                                microsecond=0,
                            )
                            return self.lab_info.get("link", ""), "lab"
                else:
                    if hour == int(lab_today.split(":")[0]):
                        self.lab_end_time = now.replace(
                            hour=hour + self.lab_duration,
                            minute=0,
                            second=0,
                            microsecond=0,
                        )
                        return self.lab_info.get("link", ""), "lab"

        if self.elective_times:
            elective_today = self.elective_times.get(weekday)
            if elective_today:
                if isinstance(elective_today, list):
                    for elective_time in elective_today:
                        if hour == int(elective_time.split(":")[0]):
                            return self.elective_info.get("link", ""), "elective"
                else:
                    if hour == int(elective_today.split(":")[0]):
                        return self.elective_info.get("link", ""), "elective"

        if not self.last_meeting and hour >= self.start_hour and hour < self.end_hour:
            return self.regular_info.get("link", ""), "regular"

        if (
            self.regular_info.get("link", "")
            and self.regular_info.get("time", "") == "regular"
        ):
            return self.regular_info.get("link", ""), "regular"
        return None, None

    def scheduled_meeting_check(self):
        debug("Running scheduled meeting check...")
        url, meeting_type = self.get_current_meeting()
        debug(f"Current meeting check: URL={url}, Type={meeting_type}")
        if url and meeting_type:
            if self.last_meeting != meeting_type:
                self.join_meeting(url, meeting_type)
            else:
                info(f"Already joined {meeting_type} meeting, skipping duplicate join.")
        else:
            current_time = datetime.now().strftime("%H:%M")
            info(f"No meeting scheduled at {current_time}")

    def setup_schedule(self):
        every().minute.do(self.scheduled_meeting_check)
        info("Meeting bot schedule initialized")
        info(
            f"Meetings will occur at: {[f'{hour:02d}:05' for hour in range(self.start_hour, self.end_hour) if hour != self.lunch_hour]}"
        )
        info("Last class will be from 16:05 to 17:00.")

    def run(self):
        info("Setting up meeting schedule...")
        self.setup_schedule()
        info("Meeting bot started. Press Ctrl+C to stop.")

        try:
            while True:
                debug("Refreshing meeting status...")
                run_pending()
                sleep(30)
        except KeyboardInterrupt:
            warning("Meeting bot stopped by user")
        except Exception as e:
            error(f"Unexpected error: {str(e)}")
