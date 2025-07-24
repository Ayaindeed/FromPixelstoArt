import cv2
import numpy as np


def apply_glitch_filter(image_path):
    image = cv2.imread(image_path)
    blue, green, red = cv2.split(image)
    glitch_blue = np.roll(blue, shift=50, axis=1)
    glitch_green = np.roll(green, shift=-30, axis=0)
    glitch_red = np.roll(red, shift=20, axis=1)
    glitched_image = cv2.merge((glitch_blue, glitch_green, glitch_red))
    return glitched_image


# Example usage
glitched_image = apply_glitch_filter("C:/Users/hp/Desktop/S/Traitement_dimages/img1.jpg")

# Display the glitched image
cv2.imshow("Glitched Image", glitched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
