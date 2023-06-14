import pyaudio
from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio

model = Model("E:\\Programming\\Project\\Master\\classes\\model")
sr = KaldiRecognizer(model,16000)

mic = PyAudio()
stream = mic.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=8192)

def Listen():
    print("Listening")
    while True:
        data = stream.read(4096)
        if sr.AcceptWaveform(data):
            text = sr.Result()
            text = text[14:-3]

            print(text)


while True:
    Listen()
