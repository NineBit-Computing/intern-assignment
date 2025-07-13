import whisper
import sounddevice as sd
import numpy as np
import queue

model = whisper.load_model("base")
q = queue.Queue()
samplerate = 16000
blocksize = 4000

def audio_callback(indata, frames, time, status):
    q.put(indata.copy())

def transcribe_meeting():
    result_texts = []
    with sd.InputStream(samplerate=samplerate, blocksize=blocksize, channels=1, callback=audio_callback):
        try:
            while True:
                audio = q.get()
                audio_fp32 = np.float32(audio[:, 0])
                result = model.transcribe(audio_fp32, fp16=False)
                text = result.get("text", "").strip()
                if text:
                    print("📝", text)
                    result_texts.append(text)
        except KeyboardInterrupt:
            print("\nTranscription ended.")
    return " ".join(result_texts)
