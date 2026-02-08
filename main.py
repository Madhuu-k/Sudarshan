import cv2
import mediapipe as mp

from hand_tracker import HandTracker
from gesture import GestureDetector
from anchor import AnchorEngine
from chakra_engine import ChakraEngine

MODEL_PATH = "hand_landmarker.task"
img_path = "assests/chakra.png"  # Path to your chakra image with transparency

cap = cv2.VideoCapture(0)
DEBUG_HAND = True
tracker = HandTracker(MODEL_PATH)
gesture = GestureDetector(required_frames=4)
anchor = AnchorEngine(alpha=0.5)
chakra = ChakraEngine(img_path)
prev_ax = None
prev_ay = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame
    )

    hand_present, landmarks = tracker.process(mp_image)
    active = gesture.update(hand_present, landmarks)

    if active:
        ax, ay = anchor.compute(landmarks)
        x = int(ax * w)
        y = int(ay * h)
        motion = 0.0
        if prev_ax is not None:
            dx = ax - prev_ax
            dy = ay - prev_ay
            motion = (dx*dx + dy*dy) ** 0.5
        prev_ax, prev_ay = ax, ay
        chakra.update(motion)
        chakra.draw(frame, x, y)
    
    if DEBUG_HAND:
        tracker.draw_debug_skeleton(frame)
    
    cv2.imshow("Sudarshan", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
