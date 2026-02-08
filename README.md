
# Jarvis - Local Voice Assistant Using Picovoice

Jarvis is a local voice assistant written in Python using the Picovoice SDK stack.
It performs wake-word detection, speech-to-text, local LLM inference, and text-to-speech entirely on-device.

This project is intended for experimentation, learning, and prototyping real-time audio pipelines and local AI assistants.

## Features

- Wake-word detection with Picovoice Porcupine
  - Supported wake words: `jarvis`, `bumblebee`
- Speech-to-text using Picovoice Cheetah
- Local LLM inference using Picovoice picoLLM
- Text-to-speech using Picovoice Orca
- No cloud-based audio or text processing

## System Overview

```text
Microphone Input
  -> Porcupine (wake word detection)
  -> Cheetah (speech to text)
  -> picoLLM (LLM inference)
  -> Orca (text to speech)
  -> System audio output
