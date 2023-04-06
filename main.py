import openai
import json
from pydub import AudioSegment
from moviepy.editor import *



song = None

def use(song):
    voice_path = input("please input voice path:")
    print("file type:"+voice_path[len(voice_path)-4:])
    if voice_path[len(voice_path)-4:] == '.mp3':
        song = AudioSegment.from_mp3(voice_path)
        format = "mp3"
    elif voice_path[len(voice_path)-4:] == '.flv':
        song = AudioSegment.from_flv(voice_path)
        format = "flv"
    elif voice_path[len(voice_path)-4:] == '.wav':
        song = AudioSegment.from_wav(voice_path)
        format = "wav"
    elif voice_path[len(voice_path)-4:] == '.ogg':
        song = AudioSegment.from_ogg(voice_path)
        format = "ogg"
    elif voice_path[len(voice_path)-4:] == '.raw':
        song = AudioSegment.from_raw(voice_path)
        format = "raw"
    elif voice_path[len(voice_path)-4:] == '.mp4':
        video = VideoFileClip(voice_path)
        video.audio.write_audiofile("voice.mp3")
        song = AudioSegment.from_mp3("voice.mp3")
        format = "mp3"
    else:
        print("error")
    # PyDub handles time in milliseconds
    ten_minutes = 10 * 60 * 1000
    i = 0
    lenght = len(song)/ten_minutes
    print("cycles to do:"+str(lenght))
    file = open("text.txt", "w")
    while i < lenght:
        first_10_minutes = song[:ten_minutes]
        first_10_minutes.export(f"voice_{i}.{format}", format=format)
        openai.api_key = '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'
        Path = f"voice_{i}.{format}"
        audio_file = open(f"{Path}", "rb")
        transcript = str(openai.Audio.transcribe("whisper-1", audio_file))
        data = str(json.loads(transcript))
        a = 0
        text = "\n"
        while len(data)-1 > a:
            if data[a] == "." or data[a] == "?" or data[a] == "!":
                text = text+ data[a] + '\n'
                a = a + 2
            else:
                text = text + data[a]
            a = a + 1
        file.write(text)
        file.close()
        i = i + 1
    print('completed!')

use(song)