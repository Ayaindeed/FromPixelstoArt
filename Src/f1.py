import cv2


def cartoon_effect(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


cartoon_image = cartoon_effect("C:/Users/hp/Desktop/S/Traitement_dimages/img1.jpg")
cv2.imshow("Cartoon Image", cartoon_image)
cv2.waitKey(0)
cv2.destroyAllWindows()