import json

import pyaudio
import pythonosc.udp_client
from vosk import Model, KaldiRecognizer

import translate


def main():
    from_code = "en"
    to_code = "ja"
    model = Model(r"models/en-s")
    recognizer = KaldiRecognizer(model, 16000)

    udp_client = pythonosc.udp_client.SimpleUDPClient("127.0.0.1", 9000)

    translate.init(from_code, to_code)

    audio_device = pyaudio.PyAudio()
    stream = audio_device.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = json.loads(str(recognizer.Result()))["text"]

            if not text:
                continue

            text = f"{text} / {translate.translate(text, from_code, to_code)}"
            print(text)
            udp_client.send_message("/chatbox/input", [text, True])


if __name__ == '__main__':
    main()
