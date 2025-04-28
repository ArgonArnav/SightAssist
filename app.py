import io, base64
from flask import Flask, request, jsonify, render_template
from PIL import Image
from object_detection import ObjectDetector
from ocr_reader     import OCRReader
from scene_fusion   import SceneFusion
from caption_generator import CaptionGenerator
from speech_synthesizer import SpeechSynthesizer

app = Flask(__name__, static_folder="static", template_folder="templates")

# initialize once
detector   = ObjectDetector()
ocr        = OCRReader()
fusion     = SceneFusion()
captioner  = CaptionGenerator()
tts        = SpeechSynthesizer()

@app.route('/')
def index():
    return render_template('index.html')  # will be your upload form

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Receives a JSON payload: {'image': 'data:image/jpeg;base64,...'}
    Crops the center ROI, runs your pipeline, and returns JSON.
    """
    data = request.get_json()
    img_b64 = data.get('image', '').split(',', 1)[-1]
    if not img_b64:
        return jsonify(error="No image"), 400

    # decode & open
    img_bytes = base64.b64decode(img_b64)
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # OPTIONAL: crop ROI to center half of frame
    w, h = image.size
    roi = image.crop((w//4, h//4, w*3//4, h*3//4))

    # run pipeline
    objs   = detector.detect_objects(roi)
    texts  = ocr.extract_text(roi)
    scene  = fusion.fuse(objs, texts)
    caption = captioner.generate_caption(roi, scene)

    return jsonify({
        "objects": objs,
        "texts": texts,
        "caption": caption
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
