from flask import Flask, render_template, Response
import cv2 as cv
import numpy as np
import mediapipe as mp

app = Flask(__name__)

# Initialize Mediapipe Hands
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video = cv.VideoCapture(-1)
canvas = None
color = (0, 255, 0)  # Default: Green(BGR)
thickness = 5
color_code = False
eraser_mode = False
prev_x, prev_y = None, None

button_x1, button_y1, button_x2, button_y2 = 50, 50, 150, 100  # Eraser button
button_a1, button_b1, button_a2, button_b2 = 450, 50, 550, 100  # Color button

def generate_frames():
    global canvas, prev_x, prev_y, color_code, eraser_mode, color

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while True:
            ret, image = video.read()
            if not ret:
                break

            image = cv.flip(image, 1)
            h, w, _ = image.shape

            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = hands.process(image_rgb)
            image_rgb.flags.writeable = True
            image = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)

            if canvas is None:
                canvas = np.zeros_like(image)

            # Draw buttons
            if color_code:
                cv.rectangle(image, (button_a1, button_b1), (button_a2, button_b2), (255, 0, 0), -1)
            else:
                cv.rectangle(image, (button_a1, button_b1), (button_a2, button_b2), (0, 0, 255), 2)
            cv.putText(image, "RED", (button_a1, button_b1 + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)

            if eraser_mode:
                cv.rectangle(image, (button_x1, button_y1), (button_x2, button_y2), (0, 0, 255), -1)
            else:
                cv.rectangle(image, (button_x1, button_y1), (button_x2, button_y2), (0, 0, 255), 2)
            cv.putText(image, "Eraser", (button_x1, button_y1 + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)

            if results.multi_hand_landmarks:
                for hand_landmark in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

                    x = int(hand_landmark.landmark[8].x * w)
                    y = int(hand_landmark.landmark[8].y * h)

                    y_mcp = int(hand_landmark.landmark[5].y * h)
                    y_pip = int(hand_landmark.landmark[6].y * h)

                    if button_a1 < x < button_a2 and button_b1 < y < button_b2:
                        color_code = not color_code
                        eraser_mode = False
                        color = (0, 0, 255) if color_code else (0, 255, 0)
                        cv.waitKey(500)
                    
                    elif button_x1 < x < button_x2 and button_y1 < y < button_y2:
                        eraser_mode = not eraser_mode
                        color_code = False
                        cv.waitKey(500)
                    
                    elif y < y_pip and y_pip < y_mcp:
                        if prev_x is not None and prev_y is not None:
                            draw_color = (0, 0, 0) if eraser_mode else (0, 0, 255) if color_code else color
                            thickness = 60 if eraser_mode else 5
                            cv.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                        prev_x, prev_y = x, y
                    else:
                        prev_x, prev_y = None, None

            image = cv.addWeighted(image, 0.6, canvas, 1, 0)

            _, buffer = cv.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
