import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import cv2
import threading
import time
import subprocess

# Import SightAssist modules
from object_detection import ObjectDetector
from ocr_reader import OCRReader
from scene_fusion import SceneFusion
from caption_generator import CaptionGenerator
from speech_synthesizer import SpeechSynthesizer

class SightAssistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SightAssist Accessible Demo")
        self.root.geometry("860x780")
        self.root.configure(bg="#000000")  # pure black background for max contrast
        self.root.option_add("*Font", "Helvetica 16")  # base font

        # Accessibility settings
        self.contrast_mode = "dark"  # dark or light
        self.caption_font_size = 18
        self.audio_enabled = True

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self._configure_styles()

        # Initialize backend modules
        self.detector = ObjectDetector()
        self.ocr = OCRReader()
        self.fusion = SceneFusion()
        self.captioner = CaptionGenerator()
        self.tts = SpeechSynthesizer()

        # Menu for accessibility settings
        self._build_menu()

        # Video frame
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480, bg="#111111", highlightthickness=2, highlightbackground="#FFFFFF")
        self.canvas.pack()

        # Controls frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=5)

        # Start/Stop buttons with keyboard shortcuts
        self.start_button = ttk.Button(self.control_frame, text="Start Camera (S)", command=self.start_camera)
        self.start_button.pack(side="left", padx=5)
        self.stop_button = ttk.Button(self.control_frame, text="Stop Camera (P)", command=self.stop_camera, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        # Settings buttons
        self.bigger_btn = ttk.Button(self.control_frame, text="A+", width=3, command=lambda: self._adjust_caption_font(2))
        self.bigger_btn.pack(side="left", padx=5)
        self.smaller_btn = ttk.Button(self.control_frame, text="A-", width=3, command=lambda: self._adjust_caption_font(-2))
        self.smaller_btn.pack(side="left", padx=5)
        self.theme_btn = ttk.Button(self.control_frame, text="Toggle Contrast", command=self._toggle_contrast)
        self.theme_btn.pack(side="left", padx=5)
        self.audio_btn = ttk.Button(self.control_frame, text="Audio: On", command=self._toggle_audio)
        self.audio_btn.pack(side="left", padx=5)

        # Caption display
        self.caption_var = tk.StringVar(value="Click 'Start Camera' or press 'S' to begin.")
        self.caption_font = tkfont.Font(family="Helvetica", size=self.caption_font_size, weight="bold")
        self.caption_label = ttk.Label(self.root, textvariable=self.caption_var, wraplength=820, justify="center", font=self.caption_font)
        self.caption_label.pack(padx=10, pady=20, ipadx=10, ipady=10)

        # Bind keyboard shortcuts
        self.root.bind('<s>', lambda e: self.start_camera())
        self.root.bind('<S>', lambda e: self.start_camera())
        self.root.bind('<p>', lambda e: self.stop_camera())
        self.root.bind('<P>', lambda e: self.stop_camera())

        # Internal state
        self.cap = None
        self.running = False
        self.last_caption = ""

    def _configure_styles(self):
        fg = "#FFFFFF" if self.contrast_mode == "dark" else "#000000"
        bg = "#000000" if self.contrast_mode == "dark" else "#FFFFFF"
        self.style.configure("TButton", background=bg, foreground=fg, font=("Helvetica", 14, "bold"), padding=8)
        self.style.map("TButton",
                       foreground=[('disabled', '#888888')],
                       background=[('active', '#444444' if self.contrast_mode=='dark' else '#DDDDDD')])
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        acc_menu = tk.Menu(menubar, tearoff=0)
        acc_menu.add_command(label="Increase Text Size", command=lambda: self._adjust_caption_font(2))
        acc_menu.add_command(label="Decrease Text Size", command=lambda: self._adjust_caption_font(-2))
        acc_menu.add_separator()
        acc_menu.add_command(label="Toggle Contrast", command=self._toggle_contrast)
        acc_menu.add_command(label="Toggle Audio", command=self._toggle_audio)
        menubar.add_cascade(label="Accessibility", menu=acc_menu)
        self.root.config(menu=menubar)

    def _adjust_caption_font(self, delta):
        self.caption_font_size = max(12, self.caption_font_size + delta)
        self.caption_font.configure(size=self.caption_font_size)

    def _toggle_contrast(self):
        self.contrast_mode = "light" if self.contrast_mode == "dark" else "dark"
        self.root.configure(bg="#FFFFFF" if self.contrast_mode=="light" else "#000000")
        self._configure_styles()

    def _toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        text = "Audio: On" if self.audio_enabled else "Audio: Off"
        self.audio_btn.config(text=text)

    def start_camera(self):
        # macOS AVFoundation backend and permission check
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        except Exception:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to open camera. Check permissions.")
            return
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="enabled")
        threading.Thread(target=self.video_loop, daemon=True).start()
        threading.Thread(target=self.process_loop, daemon=True).start()

    def stop_camera(self):
        self.running = False
        self.start_button.config(state="enabled")
        self.stop_button.config(state="disabled")
        if self.cap:
            self.cap.release()
        self.canvas.delete("all")
        self.caption_var.set("Camera stopped.")

    def video_loop(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            pil.thumbnail((640, 480))
            tk_img = ImageTk.PhotoImage(pil)
            self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
            self.canvas.image = tk_img
            time.sleep(1/30)

    def process_loop(self):
        while self.running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.5)
                    continue
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil = Image.fromarray(rgb)
                w, h = pil.size
                roi = pil.crop((w//4, h//4, w*3//4, h*3//4))

                objs = self.detector.detect_objects(roi)
                texts = self.ocr.extract_text(roi)
                scene = self.fusion.fuse(objs, texts)
                caption = self.captioner.generate_caption(roi, scene)

                if caption != self.last_caption:
                    self.last_caption = caption
                    self.caption_var.set(caption)
                    self.caption_label.update_idletasks()
                    if self.audio_enabled:
                        audio_file = self.tts.text_to_speech(caption, output_path="output.wav")
                        if audio_file:
                            subprocess.call(["afplay", audio_file])
            time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SightAssistApp(root)
    root.mainloop()
