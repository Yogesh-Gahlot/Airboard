from flask import Flask, render_template, request, jsonify, send_file
import cv2 as cv
import numpy as np
import mediapipe as mp
import base64
import io

app = Flask(__name__)

# Initialize Mediapipe Hands
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

canvas = None
color = (0, 255, 0)  # Default: Green (BGR)
thickness = 5
color_code = False
eraser_mode = False
prev_x, prev_y = None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global canvas, prev_x, prev_y, color_code, eraser_mode, color

    # Decode base64 image from frontend
    data = request.json['image'].split(',')[1]
    image_bytes = base64.b64decode(data)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv.imdecode(image_np, cv.IMREAD_COLOR)

    # Flip image
    image = cv.flip(image, 1)
    h, w, _ = image.shape

    if canvas is None:
        canvas = np.zeros_like(image)

    # Convert image to RGB for Mediapipe
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmark.landmark[8].x * w)
            y = int(hand_landmark.landmark[8].y * h)

            if prev_x is not None and prev_y is not None:
                draw_color = (0, 0, 255) if color_code else color
                thickness = 60 if eraser_mode else 5
                cv.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)

            prev_x, prev_y = x, y
    else:
        prev_x, prev_y = None, None

    # Merge image and canvas
    image = cv.addWeighted(image, 0.6, canvas, 1, 0)

    # Convert to JPEG and send back
    _, buffer = cv.imencode('.jpg', image)
    return send_file(io.BytesIO(buffer), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
