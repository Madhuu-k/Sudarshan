import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path, alpha=0.25):
        self.alpha = alpha
        self.smoothed_landmarks = None
        self.last_seen_time = 0

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def process(self, mp_image):
        timestamp = int(time.time() * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]

            if self.smoothed_landmarks is None:
                self.smoothed_landmarks = []
                for lm in hand:
                    new_lm = type(lm)()
                    new_lm.x, new_lm.y, new_lm.z = lm.x, lm.y, lm.z
                    self.smoothed_landmarks.append(new_lm)
            else:
                for i in range(21):
                    self.smoothed_landmarks[i].x = self.alpha * hand[i].x + (1 - self.alpha) * self.smoothed_landmarks[i].x
                    self.smoothed_landmarks[i].y = self.alpha * hand[i].y + (1 - self.alpha) * self.smoothed_landmarks[i].y
                    self.smoothed_landmarks[i].z = self.alpha * hand[i].z + (1 - self.alpha) * self.smoothed_landmarks[i].z

            self.last_seen_time = time.time()
        
        return result.hand_landmarks, self.smoothed_landmarks
    
    def draw_debug_skeleton(self, frame):
        if self.smoothed_landmarks is None:
            return

        h, w, _ = frame.shape

        points = []
        for lm in self.smoothed_landmarks:
            x = int(lm.x * w)
            y = int(lm.y * h)
            points.append((x, y))
            cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

        HAND_CONNECTIONS = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (5,9),(9,10),(10,11),(11,12),
        (9,13),(13,14),(14,15),(15,16),
        (13,17),(17,18),(18,19),(19,20),
        (0,17)
    ]

        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, points[start], points[end], (0,255,0), 2)
