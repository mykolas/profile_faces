import cv2

size = 4
webcam = cv2.VideoCapture(0)
classifier_hog = cv2.CascadeClassifier('..\\cascades\\cascade_hog.xml')
classifier_haar = cv2.CascadeClassifier('..\\cascades\\cascade_haar.xml')
classifier_lbp = cv2.CascadeClassifier('..\\cascades\\cascade_lbp.xml')
while True:
    (rval, im) = webcam.read()
    im=cv2.flip(im,1,0)
    mini = cv2.resize(im, (im.shape[1] / size, im.shape[0] / size))
    faces_haar = classifier_haar.detectMultiScale(mini)
    faces_hog = classifier_hog.detectMultiScale(mini)
    faces_lbp = classifier_lbp.detectMultiScale(mini)
    for f in faces_haar:
        (x, y, w, h) = [v * size for v in f]
        cv2.rectangle(im, (x, y), (x + w, y + h),(0, 255, 0),thickness=4)
    for f in faces_hog:
        (x, y, w, h) = [v * size for v in f]
        cv2.rectangle(im, (x, y), (x + w, y + h),(255, 0, 0),thickness=4)
    for f in faces_lbp:
        (x, y, w, h) = [v * size for v in f]
        cv2.rectangle(im, (x, y), (x + w, y + h),(0, 0, 255),thickness=4)
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break
