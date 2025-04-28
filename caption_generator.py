from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class CaptionGenerator:
    def __init__(self):
        # Load BLIP image captioning model (base size) and its processor
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        # Move to CPU or GPU depending on availability (here assume CPU for MacBook, or MPS for Apple Silicon if supported)
        self.model.eval()
    
    def generate_caption(self, image, scene):
        """
        Generate a caption for the given image and scene data.
        `image`: PIL image
        `scene`: dict with 'objects' and 'texts' from SceneFusion
        """
        # First, use BLIP to generate a base caption from the image alone.
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs, max_length=50)
        base_caption = self.processor.decode(out[0], skip_special_tokens=True)
        
        # Prepare to augment caption with any OCR text if relevant
        final_caption = base_caption
        # If text is present in scene, and not already mentioned in base_caption, append it.
        texts = [t['text'] for t in scene.get('texts', []) if t['text'].strip() != ""]
        if texts:
            # Combine all texts into one string (comma-separated if multiple)
            unique_texts = list({txt.strip() for txt in texts})
            text_str = ", ".join([f"\"{t}\"" for t in unique_texts])
            if len(unique_texts) == 1:
                # Single text string
                if unique_texts[0].lower() not in base_caption.lower():
                    final_caption = f"{base_caption} The scene contains text: {text_str}."
            else:
                # Multiple pieces of text
                final_caption = f"{base_caption} The scene contains text such as: {text_str}."
        return final_caption

# Example usage:
# cg = CaptionGenerator()
# caption = cg.generate_caption(image, scene_data)
# print("Caption:", caption)
