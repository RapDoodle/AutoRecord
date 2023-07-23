import re

_DAYS_OF_WEEK = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

def parse_schedule(nl_string):
    nl_string = nl_string.strip().lower()
    schedule_data = {}

    # Check for specific time units
    if "second" in nl_string:
        seconds_match = re.search(r"every (\d+) second(s)?", nl_string)
        if seconds_match:
            schedule_data["seconds"] = int(seconds_match.group(1))
        else:
            schedule_data["seconds"] = 1
    elif "minute" in nl_string:
        minutes_match = re.search(r"every (\d+) minute(s)?", nl_string)
        if minutes_match:
            schedule_data["minutes"] = int(minutes_match.group(1))
        else:
            schedule_data["minutes"] = 1
    elif "hour" in nl_string:
        hours_match = re.search(r"every (\d+) hour(s)?", nl_string)
        if hours_match:
            schedule_data["hours"] = int(hours_match.group(1))
        else:
            schedule_data["hours"] = 1
    elif "day" in nl_string:
        days_match = re.search(r"every (\d+) day(s)?", nl_string)
        if days_match:
            schedule_data["days"] = int(days_match.group(1))
        else:
            schedule_data["days"] = 1
    elif "week" in nl_string:
        weeks_match = re.search(r"every (\d+) week(s)?", nl_string)
        if weeks_match:
            schedule_data["weeks"] = int(weeks_match.group(1))
        else:
            schedule_data["weeks"] = 1

    # Check for specific times
    at_match = re.search(r"at (\d+:\d+(:\d+)?)(, (\w+/)?\w+)?", nl_string)
    if at_match:
        schedule_data["at"] = [at_match.group(1)]
        if at_match.group(4):
            schedule_data["timezone"] = at_match.group(4)

    # Check for days of the week
    
    for day in _DAYS_OF_WEEK:
        if day in nl_string:
            schedule_data["day"] = day
            break

    return schedule_data

def time_string_to_seconds(time_string):
    # Regular expressions to match hours, minutes, and seconds
    hour_pattern = re.compile(r'(\d+)\s*hour')
    minute_pattern = re.compile(r'(\d+)\s*minute')
    second_pattern = re.compile(r'(\d+)\s*second')

    # Extract hours, minutes, and seconds from the string
    hours = hour_pattern.search(time_string)
    minutes = minute_pattern.search(time_string)
    seconds = second_pattern.search(time_string)

    total_seconds = 0

    # Convert hours, minutes, and seconds to seconds and sum them up
    if hours:
        total_seconds += int(hours.group(1)) * 3600
    if minutes:
        total_seconds += int(minutes.group(1)) * 60
    if seconds:
        total_seconds += int(seconds.group(1))

    return total_seconds

def get_default_recorder_config():
    return {
        "sample_rate": 44100,
        "channels": 2,
        "bit_depth": 'int32'
    }