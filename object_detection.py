import torch

class ObjectDetector:
    def __init__(self, model_weights='yolov5s', use_cuda=False):
        """
        Initialize the YOLOv5 model for object detection.
        model_weights: can be a string for a pre-trained model (e.g. 'yolov5s')
                       or a path to custom weights (e.g. after fine-tuning).
        use_cuda: set to True to use GPU (if available) for faster inference.
        """
        # Load YOLOv5 model from PyTorch Hub (downloads weights if not present).
        # 'yolov5s' is the small COCO-pretrained model. For a custom fine-tuned model, provide path.
        self.model = torch.hub.load('ultralytics/yolov5', model_weights, pretrained=True)
        # Use CUDA/GPU if requested and available
        if use_cuda and torch.cuda.is_available():
            self.model.to('cuda')
        else:
            self.model.to('cpu')
        self.model.eval()  # Set model to evaluation mode (not training)

    def detect_objects(self, image):
        """
        Run object detection on a PIL image. Returns a list of detections, 
        each a dict with keys: 'label', 'bbox', 'confidence'.
        """
        # YOLOv5 can accept a PIL Image directly or a NumPy array or file path.
        results = self.model(image)  # perform inference
        # Parse results. We use the pandas DataFrame output for convenience.
        detections = []
        for _, row in results.pandas().xyxy[0].iterrows():
            label = str(row['name'])        # class name
            conf  = float(row['confidence'])  # confidence score
            # Bounding box coordinates (xmin, ymin, xmax, ymax)
            xmin, ymin, xmax, ymax = float(row['xmin']), float(row['ymin']), float(row['xmax']), float(row['ymax'])
            bbox = [xmin, ymin, xmax, ymax]
            detections.append({'label': label, 'bbox': bbox, 'confidence': conf})
        return detections

# Example usage:
# detector = ObjectDetector()
# detections = detector.detect_objects(PIL.Image.open('example.jpg'))
# print(detections)
