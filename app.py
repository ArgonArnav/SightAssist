import io, base64
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask import flash, redirect, url_for
from PIL import Image
import os
import time
from object_detection import ObjectDetector
from ocr_reader import OCRReader
from scene_fusion import SceneFusion
from caption_generator import CaptionGenerator
from speech_synthesizer import SpeechSynthesizer

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.urandom(24)

# Ensure output directory exists
os.makedirs(os.path.join(app.static_folder, 'audio'), exist_ok=True)

# Initialize backend modules once
detector = ObjectDetector()
ocr      = OCRReader()
fusion   = SceneFusion()
captioner = CaptionGenerator()
tts      = SpeechSynthesizer()

@app.route('/')
def index():
    # Render accessible front-end
    return render_template('index.html')

@app.route('/audio/<filename>')
def serve_audio(filename):
    # Serve generated audio files
    return send_from_directory(os.path.join(app.static_folder, 'audio'), filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    img_b64 = data.get('image', '').split(',', 1)[-1]
    if not img_b64:
        return jsonify(error="No image data"), 400

    # Decode image
    try:
        img_bytes = base64.b64decode(img_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return jsonify(error="Invalid image format"), 400

    # Crop center ROI
    w, h = image.size
    roi = image.crop((w//4, h//4, w*3//4, h*3//4))

    # Run pipeline
    tobjs = detector.detect_objects(roi)
    ttexts = ocr.extract_text(roi)
    scene = fusion.fuse(tobjs, ttexts)
    caption = captioner.generate_caption(roi, scene)

    # Generate audio if enabled
    audio_url = None
    if data.get('audio', True):
        filename = f"desc_{int(time.time())}.wav"
        path = os.path.join(app.static_folder, 'audio', filename)
        tts.text_to_speech(caption, output_path=path)
        audio_url = url_for('serve_audio', filename=filename)

    return jsonify(
        objects=tobjs,
        texts=ttexts,
        caption=caption,
        audio=audio_url
    )

if __name__ == '__main__':
    # Toggle debug off for production
    app.run(host='0.0.0.0', port=5000)