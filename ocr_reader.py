import pytesseract
from pytesseract import Output
from PIL import Image

class OCRReader:
    def __init__(self):
        # Optionally, one can specify the tesseract command path if not in PATH
        # pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"  # example for Homebrew installation
        pass  # No special initialization needed for Tesseract
    
    def extract_text(self, image):
        """
        Perform OCR on a PIL image. Returns a list of text segments found, 
        each as a dict with 'text', 'bbox', and 'confidence'.
        """
        # Convert image to RGB (Tesseract works on RGB or grayscale)
        img_rgb = image.convert('RGB')
        # Use Tesseract to get detailed OCR results including bounding boxes
        data = pytesseract.image_to_data(img_rgb, output_type=Output.DICT)
        texts = []
        n = len(data['text'])
        for i in range(n):
            text = data['text'][i]
            conf = int(data['conf'][i])
            # Only consider entries with non-empty text and decent confidence
            if text.strip() != "" and conf > 0:
                x = int(data['left'][i]); y = int(data['top'][i])
                w = int(data['width'][i]); h = int(data['height'][i])
                # Compute bounding box (x_min, y_min, x_max, y_max)
                bbox = [x, y, x + w, y + h]
                texts.append({'text': text, 'bbox': bbox, 'confidence': conf})
        return texts

# Example usage:
# ocr = OCRReader()
# text_entries = ocr.extract_text(PIL.Image.open('example.jpg'))
# print(text_entries)
