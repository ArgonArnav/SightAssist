class SceneFusion:
    def __init__(self):
        pass

    def fuse(self, objects, texts):
        """
        Fuse object and text detections. Returns a scene dictionary containing:
        - 'objects': list of objects (each with label, bbox, confidence, and optional 'text' if associated)
        - 'texts': list of text entries (each with text, bbox, confidence).
        """
        scene = {'objects': [], 'texts': []}
        # Make a copy of objects to potentially add text association
        obj_list = []
        for obj in objects:
            obj_copy = obj.copy()
            obj_copy.pop('text', None)  # ensure no residual 'text' field
            obj_list.append(obj_copy)
        # Associate texts with objects if overlap is significant
        associated_texts = set()
        for text in texts:
            tx_min, ty_min, tx_max, ty_max = text['bbox']
            for obj in obj_list:
                ox_min, oy_min, ox_max, oy_max = obj['bbox']
                # Check if text bbox lies within object bbox (rough overlap check)
                if (tx_min >= ox_min and ty_min >= oy_min and tx_max <= ox_max and ty_max <= oy_max):
                    # Associate this text with the object
                    obj['text'] = text['text']
                    associated_texts.add(text['text'])
        # Prepare final lists
        scene['objects'] = obj_list
        # Include all texts; they might be standalone or also associated (to keep record of all text)
        scene['texts'] = texts  
        return scene

# Example usage:
# fusion = SceneFusion()
# scene_data = fusion.fuse(detections, text_entries)
# print(scene_data)
