import os
import subprocess

from intents import determine_intent
from speech_to_text import speech_to_text

DEFAULT_TEXT_TO_SAY = "Sorry, I could not understand"


def speak(output: str):
    subprocess.run(['python3', 'text-to-speech/tts.py', output])


def execute_weather_action(weather_intent):
    process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'weather_api_key'],
                             stdout=subprocess.PIPE)
    weather_api_key = process.stdout.decode('utf-8').rstrip()
    if weather_api_key == '':
        try:
            with open('actions/weather/api_key') as f:
                weather_api_key = f.read()
        except FileNotFoundError:
            speak("You do not have a weather API key")
            return

    city = weather_intent.get('Location')
    if city is None:
        process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'city'],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        if output != '':
            city = output
        else:
            speak("No location is specified")
            return

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'weather', weather_api_key, city],
                             stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)


def execute_joke_action():
    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'joke'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)


def execute_what_is_action(what_is_intent):
    subject = what_is_intent.get('Subject')
    if subject is None:
        speak("Please specify a subject")
        return

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'what_is', subject], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)


def execute_time_action():
    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'time'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)


def execute_news_action(news_intent):
    process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'news_api_key'],
                             stdout=subprocess.PIPE)
    news_api_key = process.stdout.decode('utf-8').rstrip()
    if news_api_key == '':
        try:
            with open('actions/news/api_key') as f:
                news_api_key = f.read()
        except FileNotFoundError:
            speak("You do not have a news API key")
            return

    topic = news_intent.get('Topic')
    if topic is not None:

        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'news', news_api_key, topic],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()

        speak(output)
    else:
        speak('Please provide a topic')


def execute_todo_action(todo_intent) -> bool:
    action = todo_intent.get('TodoCommand')
    list_type = todo_intent.get('ListType')

    storage_path = os.getcwd() + "/actions/todo/lists.json"
    if action == 'add' or action == 'remove':
        item = todo_intent.get('Item')

        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', action, list_type, item, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    elif action == 'get' or action == 'tell me':
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', 'get', list_type, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    elif action == 'clear':
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', action, list_type, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    else:
        speak("Unknown action")


if __name__ == "__main__":
    text = speech_to_text.recognize(speech_to_text.get_audio(save=False))
    print(text)
    if text is None:
        speak(DEFAULT_TEXT_TO_SAY)
        exit(0)

    # The daemon has to be started in order to execute a command
    intent = determine_intent(text)
    if intent is None:
        speak(DEFAULT_TEXT_TO_SAY)
    elif intent.get('intent_type') == 'WeatherIntent':
        execute_weather_action(intent)
    elif intent.get('intent_type') == 'JokeIntent':
        execute_joke_action()
    elif intent.get('intent_type') == 'WhatIsIntent':
        execute_what_is_action(intent)
    elif intent.get('intent_type') == 'TimeIntent':
        execute_time_action()
    elif intent.get('intent_type') == 'NewsIntent':
        execute_news_action(intent)
    elif intent.get('intent_type') == 'TodoIntent':
        execute_todo_action(intent)