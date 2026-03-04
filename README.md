# Simulador de Entrevista com IA

Sistema de simulação de entrevista/prova oral usando:

* Gravação de voz
* Transcrição com Whisper
* Geração de pergunta com IA local
* Avaliação automática da resposta
* Feedback em áudio
---

# Como Funciona

1. A IA gera uma pergunta sobre IA / ML / Redes Neurais
2. Você responde por voz
3. O Whisper transcreve
4. Um modelo local avalia sua resposta
5. O sistema gera nota + explicação
6. O feedback é falado em áudio

---

# Tecnologias Usadas

* Python
* Whisper (transcrição de voz)
* Ollama (execução de LLM local)
* Mistral 7B (modelo de linguagem)
* sounddevice (gravação)
* gTTS (texto para voz)