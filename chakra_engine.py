import cv2
import numpy as np

class ChakraEngine:
    def __init__(self, img_path):
        # Load RGBA image
        self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if self.img is None:
            raise ValueError("Chakra image not found")

        # Fixed render size
        self.size = 220
        self.img = cv2.resize(self.img, (self.size, self.size))

    def update(self, motion=0):
        pass

    def draw(self, frame, x, y):
        if self.img is None:
            return

        h, w = frame.shape[:2]
        cx = cy = self.size // 2

        # Overlay position
        x1 = int(x - cx)
        y1 = int(y - cy)
        x2 = x1 + self.size
        y2 = y1 + self.size

        # Clip to frame bounds
        if x2 <= 0 or y2 <= 0 or x1 >= w or y1 >= h:
            return

        rx1 = max(0, -x1)
        ry1 = max(0, -y1)
        rx2 = self.size - max(0, x2 - w)
        ry2 = self.size - max(0, y2 - h)

        fx1 = max(0, x1)
        fy1 = max(0, y1)
        fx2 = min(w, x2)
        fy2 = min(h, y2)

        # Split RGBA
        chakra_rgb = self.img[ry1:ry2, rx1:rx2, :3]
        alpha = self.img[ry1:ry2, rx1:rx2, 3:] / 255.0

        # Alpha blend
        frame[fy1:fy2, fx1:fx2] = (
            chakra_rgb * alpha +
            frame[fy1:fy2, fx1:fx2] * (1 - alpha)
        ).astype(np.uint8)