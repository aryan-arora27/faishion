from ultralytics import YOLO
from PIL import Image
import os

model = YOLO("../runs/detect/train/weights/best.pt")

def detect(image_path):
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    results = model(image_path)[0]

    image = Image.open(image_path).convert("RGB")

    if len(results.boxes) == 0:
        print("[APPAREL DETECTOR] No apparel detected.")
        return "unknown", image

    box = results.boxes[0]
    class_id = int(box.cls.item())
    class_name = model.names[class_id]
    
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cropped = image.crop((x1, y1, x2, y2))

    print(f"[APPAREL DETECTOR] Detected: {class_name}")
    return class_name, cropped
