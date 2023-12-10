import cv2
# from matplotlib import pyplot as plt


img = cv2.imread('cars.jpg')
img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


xml_data = cv2.CascadeClassifier("cars.xml")
detecting = xml_data.detectMultiScale(img_color, minSize=(70, 70), scaleFactor=1.03333)
detect = len(detecting)

if detect != 0:
    for (a, b, width, height) in detecting:
        cv2.rectangle(img_color, (a, b), (a+height, b+width), (0, 255, 0), 5)

# plt.subplot(1, 1, 1)
# plt.imshow(img_color)
# plt.show()
cv2.imshow('avto', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
