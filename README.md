# Auto Zoom Meeting Bot

An automated Zoom meeting bot that joins scheduled meetings based on a configurable YAML file. The bot runs continuously and automatically opens Zoom meetings in your default browser at scheduled times.

## Features

- 🕐 **Automatic Scheduling**: Joins meetings at 5 minutes past each hour
- 📅 **Configurable Schedule**: Define different meeting types (regular, lab, elective)
- 🎯 **Smart Scheduling**: Prioritizes lab sessions > electives > regular classes
- 🍽️ **Lunch Break**: No meetings during 1-2 PM
- 📱 **Weekend Support**: Optional weekend meetings
- 🇮🇳 **IST Timezone**: Uses Indian Standard Time
- 📊 **Logging**: Comprehensive logging to file and console
- 🔄 **One Meeting at a Time**: Prevents duplicate meeting joins

## Prerequisites

- Python 3.8 or higher
- Internet connection
- Default web browser configured

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd auto-zoom-meetings
   ```

2. Install dependencies:
   ```bash
   pip install pyyaml schedule
   # OR using uv
   uv add pyyaml schedule
   ```

## Configuration

### Config File Structure

Create or modify `config.yaml`:

```yaml
start_time: "09:00"  # Start of class hours
end_time: "17:00"    # End of class hours (last class starts at 16:05)
repeat: true         # Enable recurring meetings
occurrences: 1       # Number of occurrences
weekend: false       # Enable weekend meetings

type:
  regular:
    link: https://zoom.us/j/your-regular-meeting-id
    time: "regular"    # Regular schedule
    duration: "1 hour"
    
  lab:
    link: https://zoom.us/j/your-lab-meeting-id
    time: 
      mon: "11:00"
      tue: "15:00"
      wed: 
        - "10:00"
        - "15:00"
    duration: "2 hours"
  
  elective:
    link: https://zoom.us/j/your-elective-meeting-id
    time:
      thu: "12:00"
      fri: "09:00"
    duration: "1 hour"
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|--------|
| `start_time` | Start of class hours (24-hour format) | "09:00" |
| `end_time` | End of class hours | "17:00" |
| `repeat` | Enable recurring meetings | true |
| `occurrences` | Number of meeting occurrences | 1 |
| `weekend` | Allow meetings on weekends | false |

### Meeting Types

#### Regular Meetings
- Scheduled at regular intervals during class hours
- Joins at 5 minutes past each hour (except lunch hour)

#### Lab Sessions
- Higher priority than regular meetings
- 2-hour duration
- Can be scheduled for specific days and times
- Supports multiple sessions per day

#### Elective Classes
- Medium priority (between lab and regular)
- Typically on specific days (Thu/Fri)
- 1-hour duration

## Usage

1. **Configure your meetings**: Edit `config.yaml` with your Zoom links and schedule

2. **Run the bot**:
   ```bash
   python main.py
   ```

3. **Stop the bot**: Press `Ctrl+C`

## How It Works

1. **Initialization**: Loads configuration from `config.yaml`
2. **Scheduling**: Sets up minute-by-minute checks
3. **Meeting Detection**: At each check, determines if a meeting should start
4. **Priority Logic**: Lab > Elective > Regular meetings
5. **Browser Launch**: Opens the appropriate Zoom link in your default browser
6. **Logging**: Records all actions to `meeting_bot.log`

## Schedule Logic

- **Meeting Times**: 09:05, 10:05, 11:05, 12:05, 14:05, 15:05, 16:05 (IST)
- **Lunch Break**: 13:00-14:00 (1-2 PM) - No meetings
- **Last Class**: Starts at 16:05, ends at 17:00
- **Weekends**: Meetings only if `weekend: true` in config
- **Priority**: Lab sessions override regular/elective meetings

## Logging

The bot creates detailed logs in:
- **Console**: Real-time output
- **File**: `meeting_bot.log` with timestamps

Log levels:
- `INFO`: Meeting joins, schedule info
- `DEBUG`: Schedule checks (when no meetings)
- `ERROR`: Failed meeting joins, configuration errors

## File Structure

```
auto-zoom-meetings/
├── main.py           # Main application
├── config.yaml       # Meeting configuration
├── meetings.yaml     # Alternative config format
├── README.md         # This documentation
├── pyproject.toml    # Project metadata
└── meeting_bot.log   # Generated log file
```

## Troubleshooting

### Common Issues

1. **No meetings joining**:
   - Check system time is correct (IST)
   - Verify `config.yaml` format
   - Ensure `weekend: true` if testing on weekends

2. **Wrong meeting opened**:
   - Check priority logic (Lab > Elective > Regular)
   - Verify meeting times in config

3. **Browser not opening**:
   - Ensure default browser is set
   - Check Zoom links are valid
   - Verify internet connection

### Debug Mode

To see all schedule checks, modify logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Development

### Constants

Key constants defined in `main.py`:
- `LUNCH_HOUR = 13` (1 PM)
- `LAST_CLASS_START_HOUR = 16` (4 PM)
- `CHECK_MINUTE = 5` (Check at X:05)
- `IST_TIMEZONE = 'Asia/Kolkata'`

### Adding Features

1. **New Meeting Types**: Add to `config.yaml` and update priority logic
2. **Different Time Zones**: Modify `IST_TIMEZONE` constant
3. **Custom Schedule**: Update time checking logic in `get_current_meeting()`

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files
3. Create an issue with:
   - Your `config.yaml` (remove sensitive links)
   - Relevant log entries
   - System information