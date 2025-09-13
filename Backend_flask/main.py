from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import pyttsx3
import time
import threading

from pose_estimation.estimation import PoseEstimator
from exercises.squat import Squat
from exercises.hammer_curl import HammerCurl
from exercises.push_up import PushUp
from feedback.layout import layout_indicators
from feedback.information import get_exercise_info
from utils.draw_text_with_background import draw_text_with_background

app = Flask(__name__)
CORS(app)

cap = cv2.VideoCapture(0)
pose_estimator = PoseEstimator()
exercise_type = "push_up"

# 🟡 Utility to speak text in a non-blocking thread
def speak_text(text):
    def _speak():
        tts = pyttsx3.init()
        tts.say(text)
        tts.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

# 🟡 Function to speak exercise instructions
def play_instructions(ex_type):
    instructions_map = {
        "push_up": [
            "Welcome to Push Up Tracker.",
            "Get into a high plank position.",
            "Make sure your hands are under your shoulders.",
            "Keep your body in a straight line from head to heels.",
            "Lower yourself until your elbows are at 90 degrees.",
            "Push back up to the starting position.",
            "Let's get ready!"
        ],
        "squat": [
            "Welcome to Squat Tracker.",
            "Stand with your feet shoulder-width apart.",
            "Keep your chest up and back straight.",
            "Lower your body by bending your knees.",
            "Go as low as comfortable, then stand back up.",
            "Let's get ready!"
        ],
        "hammer_curl": [
            "Welcome to Hammer Curl Tracker.",
            "Hold dumbbells with a neutral grip.",
            "Keep your elbows close to your body.",
            "Curl the weights up while keeping your wrists straight.",
            "Lower back slowly.",
            "Let's get ready!"
        ]
    }

    instructions = instructions_map.get(ex_type, instructions_map["push_up"])

    for line in instructions:
        speak_text(line)
        time.sleep(1)

    speak_text("Starting in")
    for i in range(3, 0, -1):
        speak_text(str(i))
        time.sleep(1)

@app.route('/set-exercise', methods=['POST'])
def set_exercise():
    global exercise_type
    data = request.get_json(force=True)
    exercise_type = data.get("exercise_type", "push_up")
    return jsonify({"status": "exercise set", "exercise": exercise_type})

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    global exercise_type

    prev_counter_push_squat = -1
    prev_counter_left = -1
    prev_counter_right = -1

    play_instructions(exercise_type)

    if not cap.isOpened():
        print("Camera not opened!")
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n'
        return

    if exercise_type == "hammer_curl":
        exercise = HammerCurl()
    elif exercise_type == "squat":
        exercise = Squat()
    else:
        exercise = PushUp()

    exercise_info = get_exercise_info(exercise_type)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break

        results = pose_estimator.estimate_pose(frame, exercise_type)

        if results.pose_landmarks:
            if exercise_type == "squat":
                counter, angle, stage = exercise.track_squat(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage))

                if counter != prev_counter_push_squat:
                    prev_counter_push_squat = counter
                    speak_text(f"{counter}")

            elif exercise_type == "hammer_curl":
                (counter_right, angle_right, counter_left, angle_left,
                 warning_message_right, warning_message_left, progress_right, progress_left,
                 stage_right, stage_left) = exercise.track_hammer_curl(
                    results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (
                    counter_right, angle_right, counter_left, angle_left,
                    warning_message_right, warning_message_left,
                    progress_right, progress_left, stage_right, stage_left))

                if counter_right != prev_counter_right:
                    prev_counter_right = counter_right
                    speak_text(f"{counter_right}")

                if counter_left != prev_counter_left:
                    prev_counter_left = counter_left
                    speak_text(f"{counter_left}")

            elif exercise_type == "push_up":
                counter, angle, stage = exercise.track_push_up(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage))

                if counter != prev_counter_push_squat:
                    prev_counter_push_squat = counter
                    speak_text(f"{counter}")

        draw_text_with_background(frame, f"Exercise: {exercise_info.get('name', 'N/A')}", (20, 50),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), (118, 29, 14, 200), 1)
        draw_text_with_background(frame, f"Reps: {exercise_info.get('reps', 0)}", (20, 80),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), (118, 29, 14, 200), 1)
        draw_text_with_background(frame, f"Sets: {exercise_info.get('sets', 0)}", (20, 110),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), (118, 29, 14, 200), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
