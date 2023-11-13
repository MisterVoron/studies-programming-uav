import cv2


img = cv2.imread('many-cats-various-breeds-colors-looking-expectantly-camera-created-with-generative-ai_124507-172417.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
blur_gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
contrast_img = cv2.threshold(blur_gray_img, 60, 255, cv2.THRESH_BINARY)[1]
contur, _ = cv2.findContours(contrast_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contur, -1, (0, 0, 255), 2)
cv2.imshow('cats', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

