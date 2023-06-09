import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

def get_hsv_threshold_values(cap):
    cv.namedWindow("HSV")
    cv.resizeWindow("HSV", 400, 240)
    cv.createTrackbar("HUE MIN", "HSV", 0, 179, lambda x: None)
    cv.createTrackbar("HUE MAX", "HSV", 179, 179, lambda x: None)
    cv.createTrackbar("SAT MIN", "HSV", 0, 255, lambda x: None)
    cv.createTrackbar("SAT MAX", "HSV", 255, 255, lambda x: None)
    cv.createTrackbar("VALUE MIN", "HSV", 0, 255, lambda x: None)
    cv.createTrackbar("VALUE MAX", "HSV", 255, 255, lambda x: None)
    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame, (300, 300))
        frame = cv.resize(frame, (480, 240))
        h_min = cv.getTrackbarPos("HUE MIN", "HSV")
        h_max = cv.getTrackbarPos("HUE MAX", "HSV")
        sat_min = cv.getTrackbarPos("SAT MIN", "HSV")
        sat_max = cv.getTrackbarPos("SAT MAX", "HSV")
        val_min = cv.getTrackbarPos("VALUE MIN", "HSV")
        val_max = cv.getTrackbarPos("VALUE MAX", "HSV")

        lower_values = np.array([h_min, sat_min, val_min])
        upper_values = np.array([h_max, sat_max, val_max])
        
        imageHsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        image_mask = cv.inRange(imageHsv, lower_values, upper_values)
        image_thresh = cv.bitwise_and(frame, frame, mask = image_mask)
        
        image_mask = cv.cvtColor(image_mask, cv.COLOR_GRAY2BGR)
        hstack = np.hstack([frame, image_mask, image_thresh])
        cv.imshow("Image", hstack)
        if cv.waitKey(20) & 0xFF == ord("q"):
                break
    cap.release()
    cv.destroyAllWindows()



get_hsv_threshold_values(cap)
