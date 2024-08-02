#from pyngrok import ngrok
from flask import Flask, request, jsonify
from PIL import Image
import io
import time
# import cv2

# import supervision as sv
from ultralytics import YOLOv10

# port_no = 5000
modelm = YOLOv10('yolov10b.pt')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask! nooooooooo'



# model = YOLOv10('yolov10b.pt')
model = modelm

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is active"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    # model_results = []

    # Record the start time
    start_time = time.time()

    # Run the model on the image
    results = model(source=image, conf=0.25)

    # Record the end time
    end_time = time.time()

    # Calculate the inference speed
    inference_time = end_time - start_time

    # Extract the first result
    result = results[0]

    # Get bounding box information
    boxes = result.boxes  # This is an ultralytics.engine.results.Boxes object
    names = result.names  # This dictionary maps class indices to class names
    num_boxes = len(boxes)  # Count the number of bounding boxes

    # # Store the results
    # model_results.append({
    #     'model_name': 'yolov10b',
    #     'inference_time': inference_time,
    #     'boxes': boxes,
    #     'names': names,
    #     'num_boxes': num_boxes
    # })

        # Get bounding box information
    # Get bounding box information
    boxes = result.boxes  # This is an ultralytics.engine.results.Boxes object
    names = result.names  # This dictionary maps class indices to class names

    # Prepare the JSON-serializable results
    json_results = {
        'model_name': 'yolov10b',
        'inference_time': inference_time,
        'num_boxes': len(boxes),
        'detections': []
    }

    # Access box coordinates using the xyxy property
    for box in boxes:
        coords = box.xyxy[0].cpu().numpy()  # Get the [x1, y1, x2, y2] coordinates
        json_results['detections'].append({
            'xmin': float(coords[0]),
            'ymin': float(coords[1]),
            'xmax': float(coords[2]),
            'ymax': float(coords[3]),
            'confidence': float(box.conf.item()),
            'class': int(box.cls.item()),
            'name': names[int(box.cls.item())] if names else None
        })
    return jsonify(json_results), 200

    json_results = model_results
    # Perform inference
    # results = model(image)
    # Convert results to a dictionary format for JSON response
    # json_results = results.pandas().xyxy[0].to_dict(orient="records")

    # return jsonify(json_results), 200
    return json_results

# app = Flask(__name__)
# ngrok.set_auth_token("your_token")
# public_url =  ngrok.connect(port_no).public_url

# # @app.route("/")
# # def home():
# #     return f"Running Flask on Google Colab!"

# print(f"To acces the Gloable link please click {public_url}")

# app.run(port=port_no)
