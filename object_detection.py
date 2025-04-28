import torch
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, use_cuda=False):
        """
        Initialize a YOLO11n model for object detection via the Ultralytics package.
        """
        # Load YOLO11n weights (downloads if needed)
        self.model = YOLO("yolo11n.pt")                        

        # Move model to GPU if requested
        device = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
        self.model.to(device)
        # self.model.val()

    def detect_objects(self, image):
        """
        Run object detection on an image. Returns a list of dicts:
        {'label': str, 'bbox': [xmin,ymin,xmax,ymax], 'confidence': float}
        """
        results    = self.model(image)               # infer
        detections = []

        # Loop over each image result (usually batch size = 1)
        for res in results:
            # Iterate each detected box
            for obj in res.boxes:
                # Unpack the single-row tensor into four floats
                xmin, ymin, xmax, ymax = obj.xyxy[0].tolist()
                # Extract confidence and class, converting tensors to Python scalars
                conf = obj.conf.item()
                cls  = int(obj.cls.item())

                label = self.model.names[cls]        # human-readable class name
                detections.append({
                    "label":      label,
                    "bbox":       [xmin, ymin, xmax, ymax],
                    "confidence": conf
                })
        return detections