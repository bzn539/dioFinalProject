import os
import platform
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import numpy as np
import requests
from gtts import gTTS

SAMPLE_RATE = 44100
ARQUIVO_AUDIO = "resposta.wav"
IDIOMA = "pt"

# GERAR PERGUNTA

def gerar_pergunta():
    print("\n🤖 Gerando pergunta...")

    prompt = """
Gere uma pergunta oral sobre Inteligência Artificial,
Machine Learning ou Redes Neurais.

A pergunta deve exigir explicação.
Responda apenas com a pergunta.
Em português.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    pergunta = response.json()["response"].strip()

    print("\n📢 PERGUNTA:")
    print(pergunta)

    return pergunta

# GRAVAÇÃO

def gravar_audio():
    print("\n🎤 Fale sua resposta.")
    print("⏹ Pressione ENTER para parar.\n")

    audio_data = []

    def callback(indata, frames, time, status):
        audio_data.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        callback=callback
    ):
        input()

    audio = np.concatenate(audio_data, axis=0)
    wav.write(ARQUIVO_AUDIO, SAMPLE_RATE, audio)

    print("✅ Áudio gravado!")

# WHISPER

print("📦 Carregando modelo Whisper...")
modelo = whisper.load_model("small")

def transcrever_audio():
    print("🧠 Transcrevendo...")

    resultado = modelo.transcribe(
        ARQUIVO_AUDIO,
        language="pt",
        task="transcribe"
    )

    texto = resultado["text"]

    print("\n📝 Você disse:")
    print(texto)

    return texto


# IA AVALIA

def avaliar_resposta(pergunta, resposta):
    print("\n🤖 IA avaliando resposta...")

    prompt = f"""
Você é um professor avaliando um aluno oralmente.

Pergunta:
{pergunta}

Resposta do aluno:
{resposta}

Faça:
1) Dê uma nota de 0 a 10
2) Explique o motivo da nota
3) Explique a resposta correta resumidamente

Responda em português.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    resultado = response.json()["response"]

    print("\n📊 Resultado da IA:")
    print(resultado)

    return resultado


# TEXTO PARA VOZ

def falar_resposta(texto):
    print("\n🔊 Gerando áudio do feedback...")
    arquivo_mp3 = "feedback.mp3"

    tts = gTTS(text=texto, lang=IDIOMA)
    tts.save(arquivo_mp3)

    if platform.system() == "Windows":
        os.system(f"start {arquivo_mp3}")
    elif platform.system() == "Darwin":
        os.system(f"afplay {arquivo_mp3}")
    else:
        os.system(f"xdg-open {arquivo_mp3}")


# MAIN

if __name__ == "__main__":
    pergunta = gerar_pergunta()
    gravar_audio()
    texto = transcrever_audio()
    feedback = avaliar_resposta(pergunta, texto)
    falar_resposta(feedback)