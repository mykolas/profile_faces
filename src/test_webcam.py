import cv2

size = 4
webcam = cv2.VideoCapture(0)
classifier = cv2.CascadeClassifier('..\\cascades\\cascade.xml')
while True:
    (rval, im) = webcam.read()
    im=cv2.flip(im,1,0)
    mini = cv2.resize(im, (im.shape[1] / size, im.shape[0] / size))
    faces = classifier.detectMultiScale(mini)
    for f in faces:
        (x, y, w, h) = [v * size for v in f]
        cv2.rectangle(im, (x, y), (x + w, y + h),(0,255,0),thickness=4)
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break
