# SightAssist: Real-Time Vision-Language Assistant for the Visually Impaired

**SightAssist** is an open-source, modular Python application that combines computer vision and natural language processing to provide real-time spoken scene descriptions. It supports both a **desktop GUI** and a **web interface**, and runs entirely locally (no cloud services required) for maximum privacy and accessibility.

---

## Table of Contents
1. [Features](#features)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Setup](#setup)
6. [Usage](#usage)
   - [Desktop GUI](#desktop-gui)
   - [Web App](#web-app)
7. [Project Structure](#project-structure)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features
- **Real-time Object Detection** using the latest YOLO11n (via Ultralytics PyTorch Hub)
- **Scene Text Recognition (OCR)** via Tesseract (or easily swappable CRNN)
- **Multimodal Fusion**: associates text with detected objects
- **Natural-Language Captioning** with BLIP (Vision-Language Transformer)
- **Text-to-Speech** using Coqui TTS for offline, high-quality audio
- **Accessible Interfaces**:
  - Dark/light modes, high-contrast controls
  - Large, resizable fonts and audio toggles for visual/hearing impairments
  - Keyboard shortcuts (S/P to start/stop)
- **Dual Modes**:
  - **Desktop GUI** (Tkinter)
  - **Web App** (Flask + HTML5 canvas)

---

## Architecture

```
[Camera] → [ObjectDetector] → [OCRReader]
         ↘ [SceneFusion] ↘ [CaptionGenerator] → [SpeechSynthesizer]
```

1. **ObjectDetector** (`object_detection.py`) loads the latest YOLO11n model to detect objects and bounding boxes.
2. **OCRReader** (`ocr_reader.py`) runs Tesseract OCR to extract text segments from the scene.
3. **SceneFusion** (`scene_fusion.py`) merges object & text outputs, associating text inside object bounds.
4. **CaptionGenerator** (`caption_generator.py`) uses BLIP to generate an image caption, then appends any extracted text.
5. **SpeechSynthesizer** (`speech_synthesizer.py`) uses Coqui TTS to convert the caption into a WAV file.
6. **User Interfaces**:
   - **Desktop GUI** (`desktop_app.py`) for local, standalone use.
   - **Web App** (`app.py` + `templates/index.html`) served via Flask.

---

## Prerequisites
- **Operating System**: macOS (tested on Intel & Apple Silicon)
- **Python**: 3.8+
- **Homebrew** (for macOS system packages)
- **Tesseract OCR** (v4+)
- **Git** (to clone the repo)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/SightAssist.git
   cd SightAssist
   ```

2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   ```bash
   brew install tesseract
   ```

> Coqui TTS, PyTorch, Hugging Face Transformers, Flask, and other packages will be installed via `requirements.txt`.

---

## Setup

- **Tesseract CLI** must be in your `PATH`. If installed via Homebrew, it will be at `/usr/local/bin/tesseract` (Intel) or `/opt/homebrew/bin/tesseract` (Apple Silicon).
- **First-run model downloads**:
  - YOLOv5 (Ultralytics) downloads ~50 MB of weights.
  - BLIP (Salesforce) downloads ~400 MB for image captioning.
  - Coqui TTS models download ~300 MB on first TTS call.

Make sure you have an internet connection on first execution; afterward, models are cached locally.

---

## Usage

### Desktop GUI

1. **Run the GUI app**
   ```bash
   python desktop_app.py
   ```
2. **Use controls or keyboard**:
   - Click **Start (S)** or press **S** to open your webcam.
   - Click **Stop (P)** or press **P** to halt capture.
   - **A+ / A−** buttons or menu to adjust caption font size.
   - **Toggle Contrast** and **Audio On/Off** via menu or buttons.
3. **Speak back**: Captions are spoken automatically (Coqui TTS) and displayed in large text.

### Web App

1. **Run the Flask server**
   ```bash
   python app.py
   ```
2. **Open** your browser at `http://localhost:5000`
3. **Use the on-screen controls**:
   - **Start (S)**, **Stop (P)**, **Audio On/Off**, **A+ / A−**
   - Live video + animated bounding boxes + captions + audio playback

> **Note**: The web front-end is static and can be hosted on GitHub Pages; only the Flask backend must run on a Python host.

---

## Project Structure

```
SightAssist/
├── object_detection.py      # YOLOv5 inference
├── ocr_reader.py            # Tesseract OCR wrapper
├── scene_fusion.py          # Merge detections & text
├── caption_generator.py     # BLIP-based captions
├── speech_synthesizer.py    # Coqui TTS wrapper
├── desktop_app_accessible.py# Tkinter GUI
├── web_app_accessible.py    # Flask backend
├── templates/
│   └── index.html           # Accessible front-end
├── static/
│   └── audio/               # Generated .wav files
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Troubleshooting

- **Camera Errors**:
  - macOS: Grant camera access in **System Preferences → Security & Privacy → Camera** for your Python interpreter.
  - If `VideoCapture` fails, try forcing AVFoundation backend: `cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)`.

- **Model Download Failures**:
  - Ensure you have >1 GB free disk space and a stable internet connection on first run.
  - Check cache at `~/.cache/torch/hub` and `~/.cache/huggingface`.

- **TTS Issues**:
  - If Coqui TTS fails to download, check network and rerun the script.
  - As a fallback, disable audio or install `pyttsx3` and swap in the simpler TTS engine.


---

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature/my-feature`).
5. Open a Pull Request.


---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
