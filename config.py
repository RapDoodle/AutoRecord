from hooks.browser import open_chrome, close_chrome

# Record Never Gonna Give You Up for 30 seconds
SCHEDULED_EVENTS = [
    {
        "schedule": "every day at 19:20",
        "event": {
            "filename": "Never Gonna Give You Up %Y%m%d%H%M%S",
            "format": "mp3",
            "recorder_config": {

            },
            "duration": "30 seconds",
            "before_recording": {
                "func": open_chrome,
                "args": {
                    "url": "https://shattereddisk.github.io/rickroll/rickroll.mp4"
                }
            },
            "after_recording": {
                "func": close_chrome,
                "args": {}
            }
        }
    },
]