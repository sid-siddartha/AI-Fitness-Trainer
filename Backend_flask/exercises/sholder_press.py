import cv2
from pose_estimation.angle_calculation import calculate_angle


class ShoulderPress:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def calculate_angle(self, point1, point2, point3):
        return calculate_angle(point1, point2, point3)  # Calculates angle at point2

    def track_shoulder_press(self, landmarks, frame):
        # Extract coordinates for the left side
        shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_left = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        wrist_left = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        # Extract coordinates for the right side
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_right = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        wrist_right = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        # Calculate elbow angles
        angle_left = self.calculate_angle(shoulder_left, elbow_left, wrist_left)
        angle_right = self.calculate_angle(shoulder_right, elbow_right, wrist_right)

        # Draw lines and circles for visualization
        self.draw_line_with_style(frame, shoulder_left, elbow_left, (178, 102, 255), 2)
        self.draw_line_with_style(frame, elbow_left, wrist_left, (178, 102, 255), 2)
        self.draw_circle(frame, shoulder_left, (178, 102, 255), 8)
        self.draw_circle(frame, elbow_left, (178, 102, 255), 8)
        self.draw_circle(frame, wrist_left, (178, 102, 255), 8)

        self.draw_line_with_style(frame, shoulder_right, elbow_right, (51, 153, 255), 2)
        self.draw_line_with_style(frame, elbow_right, wrist_right, (51, 153, 255), 2)
        self.draw_circle(frame, shoulder_right, (51, 153, 255), 8)
        self.draw_circle(frame, elbow_right, (51, 153, 255), 8)
        self.draw_circle(frame, wrist_right, (51, 153, 255), 8)

        # Display angles
        cv2.putText(frame, f'Left: {int(angle_left)}', (elbow_left[0] + 10, elbow_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f'Right: {int(angle_right)}', (elbow_right[0] + 10, elbow_right[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Use average of both elbow angles
        avg_elbow_angle = (angle_left + angle_right) / 2

        # Rep counting logic
        if avg_elbow_angle > 160:
            if self.stage == 'Descent':
                self.counter += 1
                self.stage = 'Start'
            else:
                self.stage = 'Start'
        elif avg_elbow_angle < 70:
            if self.stage == 'Start':
                self.stage = 'Ascent'
            elif self.stage == 'Ascent':
                self.stage = 'Descent'

        # Optional debug log
        print(f"Avg Angle: {avg_elbow_angle}, Stage: {self.stage}, Count: {self.counter}")

        return self.counter, avg_elbow_angle, self.stage

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        cv2.circle(frame, center, radius, color, -1)  # Filled circle
