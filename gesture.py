# Detects a specific hand gesture (index finger up, others down) over a series of frames to confirm the gesture is intentional.

class GestureDetector:
    def __init__(self, required_frames=4):
        self.required_frames = required_frames
        self.gesture_frames = 0

    def update(self, has_hand, landmarks    ):
        if not has_hand or landmarks is None:
            self.gesture_frames = 0
            return False

        tip = landmarks[8]      # index tip
        pip = landmarks[6]      # index PIP
        wrist = landmarks[0]

    # STRICT distance-based logic
        index_up = landmarks[8].y < landmarks[6].y < landmarks[5].y

        middle_down = landmarks[12].y > landmarks[10].y
        ring_down   = landmarks[16].y > landmarks[14].y
        pinky_down  = landmarks[20].y > landmarks[18].y

        if index_up and middle_down and ring_down and pinky_down:
            self.gesture_frames += 1
        else:
            self.gesture_frames = 0

        return self.gesture_frames >= self.required_frames

