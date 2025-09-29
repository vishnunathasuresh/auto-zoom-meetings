## Using Environment Variables (.env)

You can store sensitive or environment-specific values (like Zoom links) in a `.env` file and load them automatically.

1. **Create a `.env` file in your project directory:**
   ```env
   LABS=https://zoom.us/j/your_lab_meeting_id
   ELECTIVES=https://zoom.us/j/your_elective_meeting_id
   REGULAR=https://zoom.us/j/your_regular_meeting_id
   ```



This keeps sensitive data out of your codebase and makes it easy to change links or credentials without editing code.
# Auto Zoom Meeting Bot

An automated Python bot that joins scheduled Zoom meetings. The bot runs continuously, opening meetings in your default browser at the right time, and automatically refreshes its schedule every day.

## Features

- **Automatic Scheduling:** Joins meetings at 5 minutes past each hour, skipping lunch (1-2 PM)
- **Configurable:** Supports regular, lab, and elective meetings with custom times and durations
- **Priority Logic:** Lab > Elective > Regular (never joins more than one at a time)
- **IST Timezone:** Designed for Indian Standard Time
- **Weekend Support:** Optional meetings on weekends
- **Daily Refresh:** Regenerates schedule at midnight, no need to restart
- **Logging:** Logs all actions to `meeting_bot.log` and the console

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install pyyaml schedule
   # or
   uv add pyyaml schedule python-dotenv
   ```
2. **Edit `config.yaml`:**
   - Set your Zoom links and schedule (see below)
3. **Run the bot:**
   ```bash
   python main.py
   ```
## How It Works

1. Loads your config and builds a daily schedule of meetings.
2. Schedules each meeting using the `schedule` library.
3. At the scheduled time, opens the Zoom link in your browser.
4. At midnight, automatically refreshes the schedule for the new day.
5. Skips meetings during lunch and on weekends (unless enabled).
6. Logs all actions and errors.

## Schedule Logic

- **Meeting Times:** 09:05, 10:05, 11:05, 12:05, 14:05, 15:05, 16:05 (IST)
- **Lunch Break:** 13:00-14:00 (1-2 PM)
- **Last Class:** Starts at 16:05, ends at 17:00
- **Priority:** Lab > Elective > Regular
- **No Retroactive Joins:** Missed meetings are not joined later

## Troubleshooting

- Check your system clock and timezone (should be IST)
- Make sure `config.yaml` is valid YAML and matches the example
- Check `meeting_bot.log` for errors
- If the bot misses meetings, ensure your computer is on and not asleep

## Running on Startup (Windows)
2. Place the batch file in the Startup folder (`Win+R`, type `shell:startup`)

## File Structure

```
auto-zoom-meetings/
├── main.py           # Main entry point
├── bot.py            # Bot logic
├── config.yaml       # Meeting configuration
├── README.md         # Documentation
├── pyproject.toml    # Project metadata
└── meeting_bot.log   # Log file
```

## License

MIT License