import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
# Import SightAssist modules
from object_detection import ObjectDetector
from ocr_reader import OCRReader
from scene_fusion import SceneFusion
from caption_generator import CaptionGenerator
from speech_synthesizer import SpeechSynthesizer

# Initialize backend modules once
detector = ObjectDetector()
ocr = OCRReader()
fusion = SceneFusion()
captioner = CaptionGenerator()
tts = SpeechSynthesizer()

# Create Tkinter window
root = tk.Tk()
root.title("SightAssist Demo")

# GUI Elements: a label to show image (optional) and a label to show caption, and a button
img_label = tk.Label(root)
img_label.pack(padx=10, pady=10)
caption_label = tk.Label(root, text="No image selected.", wraplength=400, justify="center")
caption_label.pack(padx=10, pady=10)

def open_image():
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(title="Choose an image",
                                           filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if not file_path:
        return  # user cancelled
    # Load image
    try:
        image = Image.open(file_path).convert('RGB')
    except Exception as e:
        caption_label.config(text=f"Error opening image: {e}")
        return
    # Display the image in GUI (resize to fit if necessary)
    max_size = 400
    img_copy = image.copy()
    img_copy.thumbnail((max_size, max_size))
    tk_img = ImageTk.PhotoImage(img_copy)
    img_label.configure(image=tk_img)
    img_label.image = tk_img  # keep a reference
    
    # Process the image through SightAssist pipeline
    caption_label.config(text="Processing... please wait.")
    root.update()  # refresh GUI
    objects = detector.detect_objects(image)
    texts = ocr.extract_text(image)
    scene_data = fusion.fuse(objects, texts)
    caption_text = captioner.generate_caption(image, scene_data)
    caption_label.config(text=f"Caption: {caption_text}")
    # Synthesize speech and play audio
    audio_file = tts.text_to_speech(caption_text, output_path="output.wav")
    if audio_file:
        # Use afplay on macOS to play the wav file (afplay is a default CLI audio player on macOS)
        try:
            subprocess.call(["afplay", audio_file])
        except FileNotFoundError:
            print(f"Could not play audio (afplay not found). Caption text: {caption_text}")

# Button to open image
open_button = tk.Button(root, text="Open Image...", command=open_image)
open_button.pack(pady=5)

# Start the GUI event loop
root.mainloop()
