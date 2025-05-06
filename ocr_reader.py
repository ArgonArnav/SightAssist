# ocr_reader.py
import numpy as np
import easyocr
from PIL import Image

class OCRReader:
    def __init__(self, languages=['en']):
        """
        Initialize an EasyOCR reader (which uses a CRNN + CTC model under the hood).
        `languages` is a list like ['en','es']—by default we load English only.
        """
        # disable GPU if you don't have CUDA; set gpu=True if you do.
        self.reader = easyocr.Reader(languages, gpu=False)

    def extract_text(self, image: Image.Image):
        """
        Perform OCR on a PIL image using EasyOCR.
        Returns a list of dicts: { 'text': str,
                                  'bbox': [x_min,y_min,x_max,y_max],
                                  'confidence': float }
        """
        # Convert PIL→NumPy (H×W×C)
        img_array = np.array(image)
        # easyocr returns list of (bbox, text, confidence)
        raw_results = self.reader.readtext(img_array)
        results = []
        for bbox_pts, txt, conf in raw_results:
            # bbox_pts is [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
            xs = [pt[0] for pt in bbox_pts]
            ys = [pt[1] for pt in bbox_pts]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            results.append({
                'text': txt,
                'bbox': [x_min, y_min, x_max, y_max],
                'confidence': float(conf)
            })
        return results
