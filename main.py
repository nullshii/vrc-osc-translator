import json

import pyaudio
import pythonosc.udp_client
from vosk import Model, KaldiRecognizer
import argostranslate.package
import argostranslate.translate


def main():
    from_code = "ru"
    to_code = "en"
    model = Model(r"models/ru-s")
    recognizer = KaldiRecognizer(model, 16000)

    udp_client = pythonosc.udp_client.SimpleUDPClient("127.0.0.1", 9000)

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    ))
    argostranslate.package.install_from_path(package_to_install.download())

    audio_device = pyaudio.PyAudio()
    stream = audio_device.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = json.loads(str(recognizer.Result()))["text"]

            if not text:
                continue

            text = f"{text} / {argostranslate.translate.translate(text, from_code, to_code)}"
            print(text)
            udp_client.send_message("/chatbox/input", [text, True])


if __name__ == '__main__':
    main()
