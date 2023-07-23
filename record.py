import time
import argparse
import schedule
import datetime
import importlib
import sounddevice as sd
import wavio
from pydub import AudioSegment

from utils import parse_schedule, time_string_to_seconds, get_default_recorder_config

def record_event(event):
    def exec_hook(phase):
        if phase in event:
            hook = event[phase]
            func = hook.get('func', None)
            if func is None:
                return
            func_args = hook.get('args', {})
            func(context, **func_args)

    recorder_config = get_default_recorder_config()
    recorder_config.update(event.get("recorder_config", {}))

    context = {}
    context['recorder_config'] = recorder_config
    context['event'] = event
    context['created_at'] = datetime.datetime.now()

    # Before recording hook
    exec_hook('before_recording')

    # Record audio
    duration = time_string_to_seconds(event['duration'])
    audio_data = sd.rec(
        frames = int(duration * recorder_config['sample_rate']),
        samplerate=recorder_config['sample_rate'], 
        channels=recorder_config['channels'],
        dtype=recorder_config['bit_depth']
    )
    # Wait until recording is done
    sd.wait()

    # After recording hook
    exec_hook('after_recording')

    # Save to file
    filename = context['created_at'].strftime(event['filename'])
    format = event.get('format', 'wav')
    if format == 'mp3':
        # Convert the audio data to an AudioSegment
        audio_segment = AudioSegment(
            audio_data.tobytes(), 
            frame_rate=recorder_config['sample_rate'],
            sample_width=audio_data.dtype.itemsize, 
            channels=recorder_config['channels']
        )
        
        # Export the AudioSegment as an MP3 file
        audio_segment.export(f"{filename}.mp3", format="mp3")
    elif format == 'wav':
        wavio.write(
            file=f"{filename}.wav", 
            data=audio_data, 
            rate=recorder_config['sample_rate'],
        )
    
    exec_hook('on_complete')


def schedule_event(schedule_string, event):
    schedule_data = parse_schedule(schedule_string)
    job = None

    if 'seconds' in schedule_data:
        job = schedule.every(schedule_data['seconds']).seconds
    elif 'minutes' in schedule_data:
        job = schedule.every(schedule_data['minutes']).minutes
    elif 'hours' in schedule_data:
        job = schedule.every(schedule_data['hours']).hours
    elif 'days' in schedule_data:
        job = schedule.every(schedule_data['days']).days
    elif 'weeks' in schedule_data:
        job = schedule.every(schedule_data['weeks']).weeks

    if 'at' in schedule_data:
        for timing in schedule_data['at']:
            job.at(timing).do(record_event, event)
        return  # Return early since we've already scheduled the job

    if 'day' in schedule_data:
        days_of_week = {
            'monday': job.monday,
            'tuesday': job.tuesday,
            'wednesday': job.wednesday,
            'thursday': job.thursday,
            'friday': job.friday,
            'saturday': job.saturday,
            'sunday': job.sunday
        }
        job = days_of_week[schedule_data['day'].lower()]

    job.do(record_event, event)

def main():
    parser = argparse.ArgumentParser(description="Schedule recording events.")
    parser.add_argument(
        '-c',
        '--config', 
        default='config', 
        help='Name of the configuration module (without .py)'
    )
    args = parser.parse_args()

    try:
        config_module = importlib.import_module(args.config)
    except:
        print(f"Unable to find the configuration {args.config}.py")
        exit(1)
    for event in config_module.SCHEDULED_EVENTS:
        schedule_event(event['schedule'], event['event'])

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
