# Hand Gesture Drawing Web App

This project is a Flask-based web application that allows users to draw on a virtual canvas using hand gestures. It leverages OpenCV and MediaPipe for hand tracking.

## Features

- **Hand Gesture-Based Drawing**: Draw using your index finger.
- **Eraser Mode**: Toggle eraser mode to clear parts of the drawing.
- **Color Change**: Toggle between red and green colors for drawing.
- **Live Video Feed**: Stream the video feed with real-time gesture tracking.

## Technologies Used

- OpenCV (for video processing)
- MediaPipe (for hand tracking)
- NumPy (for image processing)

## Installation

### Prerequisites

Ensure you have Python installed on your system.

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/hand-gesture-drawing.git
   cd hand-gesture-drawing
   ```
2. Install required dependencies:
   ```sh
   pip install flask opencv-python mediapipe numpy
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. Open a web browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

- Raise your index finger to draw.
- Tap on the "Eraser" button to enable/disable erasing mode.
- Tap on the "RED" button to switch between red and green colors.
- The canvas overlays the video feed and updates in real time.

## File Structure

```
├── app.py          # Main application script
├── templates
│   ├── index.html  # Frontend HTML template
├── static
│   ├── styles.css  # (Optional) CSS for styling
├── README.md       # Project documentation
```

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

This project is licensed under the MIT License.

