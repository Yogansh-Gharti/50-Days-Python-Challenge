import cv2

cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

image = cv2.imread("input.jpg")

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

faces = cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(40, 40)
)

for (x, y, w, h) in faces:

    roi = image[y:y+h, x:x+w]

    blur = cv2.GaussianBlur(
        roi,
        (99, 99),
        30
    )

    image[y:y+h, x:x+w] = blur

cv2.imwrite(
    "output.jpg",
    image
)

print("✅ Face Blur Completed Successfully!")

cv2.imshow("Output", image)

cv2.waitKey(0)

cv2.destroyAllWindows()
