# Anchor the chakra to the tip of the index finger, with a small offset in the direction of the finger.
import numpy as np
class AnchorEngine:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.x = None
        self.y = None

    def compute(self, landmarks):
        base = landmarks[5] # Base of the index finger (MCP joint)
        tip = landmarks[8] # Tip of the index finger

        dx = tip.x - base.x # Calculate the horizontal difference between the tip and base of the index finger
        dy = tip.y - base.y # Calculate the vertical difference between the tip and base of the index finger

        length = np.sqrt(dx*dx + dy*dy) # Calculate the length of the vector from the base to the tip of the index finger
        if length > 0:
            dx /= length
            dy /= length

        depth = np.clip(-tip.z, 0.02, 0.1) # Use the z-coordinate of the tip 
        distance = 0.03 + depth # Base distance plus depth-based offset

        ax = tip.x + dx * distance # Calculate the anchored x position by adding the offset in the direction of the finger
        ay = tip.y + dy * distance # Calculate the anchored y position by adding the offset in the direction of the finger

        if self.x is None:
            self.x, self.y = ax, ay # Initialize the anchor position on the first frame
        else:
            self.x = self.alpha * ax + (1 - self.alpha) * self.x # Smoothly update the anchor's x position using exponential moving average
            self.y = self.alpha * ay + (1 - self.alpha) * self.y # Smoothly update the anchor's y position using exponential moving average

        return self.x, self.y
