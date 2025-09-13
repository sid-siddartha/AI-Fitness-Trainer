import cv2
from pose_estimation.angle_calculation import calculate_angle
from utils.speech import speak_text  # Ensure speak_text is accessible here

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def calculate_angle(self, point1, point2, point3):
        return calculate_angle(point1, point2, point3)  # Calculates angle at point2

    def track_squat(self, landmarks, frame):
        feedback = ""

        def get_point(index):
            return [int(landmarks[index].x * frame.shape[1]), int(landmarks[index].y * frame.shape[0])]

        # Key body points
        shoulder_left = get_point(11)
        hip_left = get_point(23)
        knee_left = get_point(25)
        ankle_left = get_point(27)

        shoulder_right = get_point(12)
        hip_right = get_point(24)
        knee_right = get_point(26)
        ankle_right = get_point(28)

        # Calculate angles
        knee_angle_left = self.calculate_angle(hip_left, knee_left, ankle_left)
        knee_angle_right = self.calculate_angle(hip_right, knee_right, ankle_right)
        back_angle_left = self.calculate_angle(shoulder_left, hip_left, knee_left)
        back_angle_right = self.calculate_angle(shoulder_right, hip_right, knee_right)

        avg_knee_angle = (knee_angle_left + knee_angle_right) / 2
        avg_back_angle = (back_angle_left + back_angle_right) / 2

        # Draw visual aids
        self._draw_connections(frame, hip_left, knee_left, ankle_left, shoulder_left, (178, 102, 255))
        self._draw_connections(frame, hip_right, knee_right, ankle_right, shoulder_right, (51, 153, 255))

        # Display angles
        cv2.putText(frame, f'Knee: {int(avg_knee_angle)}', (knee_left[0] - 50, knee_left[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f'Back: {int(avg_back_angle)}', (hip_left[0] - 50, hip_left[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # ---- FORM CHECKS & FEEDBACK ---- #
        if avg_knee_angle > 140 and self.stage == "Descent":
            feedback = "Go deeper"
        elif avg_knee_angle < 90:
            if avg_back_angle < 70:
                feedback = "Keep your back straight"
            elif hip_left[1] < knee_left[1] - 10:
                feedback = "Don't lean forward"
            elif knee_left[0] < ankle_left[0] - 30 or knee_right[0] > ankle_right[0] + 30:
                feedback = "Knees going over toes"

        # ---- REP COUNTING LOGIC ---- #
        if avg_knee_angle > 160:
            if self.stage == 'Ascent':
                self.counter += 1
                self.stage = 'Starting Position'
            else:
                self.stage = 'Starting Position'
        elif avg_knee_angle < 110:
            if self.stage == 'Starting Position':
                self.stage = 'Descent'
            elif self.stage == 'Descent':
                self.stage = 'Ascent'

        # ---- FEEDBACK DISPLAY ---- #
        if feedback:
            speak_text(feedback)
            cv2.putText(frame, feedback, (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        return self.counter, avg_knee_angle, self.stage

    def _draw_connections(self, frame, hip, knee, ankle, shoulder, color):
        self.draw_line_with_style(frame, hip, knee, color, 2)
        self.draw_line_with_style(frame, knee, ankle, color, 2)
        self.draw_line_with_style(frame, shoulder, hip, color, 2)
        self.draw_circle(frame, hip, color, 6)
        self.draw_circle(frame, knee, color, 6)
        self.draw_circle(frame, ankle, color, 6)
        self.draw_circle(frame, shoulder, color, 6)

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        cv2.circle(frame, center, radius, color, -1)
