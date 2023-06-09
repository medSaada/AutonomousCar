import cv2 as cv
from functions_and_classes import *
import motor
import RPi.GPIO as pins
from time import sleep

#cv.namedWindow("Trackbars")
cv.namedWindow("Thresh")

curveList = []

#cv.createTrackbar("gauche doite", "Trackbars", 0, 70, lambda x: None)
#cv.createTrackbar("devant", "Trackbars", 0, 70, lambda x: None)
moteur = motor.Motor(33, 31, 29, 40, 38, 36)
def get_lane_curve(image, width=480, height=240):
    lower_values = np.array([0, 23, 128])
    upper_values = np.array([19, 255, 255])
    w_top = 0
    h_top = 140
    font = cv.FONT_HERSHEY_SIMPLEX
    w_bottom = 0
    h_bottom = 240
    points = np.float32([[w_top, h_top], [int(width-w_top), h_top], [w_bottom, h_bottom], [int(width-w_bottom), h_bottom]])
    image_thresh = thresholding(image, lower_values, upper_values)
    image_warped = warp_image(image_thresh, points, int(width), int(height))

    base_point = get_histogram(image_warped, 0.45, region=0)
    color = (0, 0, 255)
    mid_point= get_histogram(image_warped, 0.9, region=0.75)
    #s,m=getHistogram(image_warped, 0.45, region=0)
    #print(m)
    start_point = (mid_point, 0)
    end_point = (mid_point, int(height))
    color = (0, 0, 255)
    thickness = 2
    cv.line(image, start_point, end_point, color, thickness)
    cv.circle(image, (base_point, int(height)), 10, (255, 0, 0), cv.FILLED)
    curve = base_point-mid_point
    
    #if mid_point < int(width/2)-70: curve = -15
    #elif mid_point > int(width/2)+70: curve = 15
    norm_curve=curve/100
       

    if norm_curve > 0:
        cv.putText(image, f"{norm_curve} droite", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
    elif base_point-mid_point < 0:
        cv.putText(image, f"{norm_curve} gauche", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
    elif norm_curve==0:
        cv.putText(image, f"{norm_curve} tout droit", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
    return image, image_warped, norm_curve, image_thresh
        
    

if __name__ == "__main__":
    video_path = "opencv_video_record2.mp4"
    cap = cv.VideoCapture(0)
    while True:
        #dg = cv.getTrackbarPos("gauche doite", "Trackbars")
        #devant = cv.getTrackbarPos("devant", "Trackbars")
        
        ret, image = cap.read()
        image = cv.resize(image, (480, 240))
        image_out, img_warped, norm_curve,image_thresh = get_lane_curve(image)
        cv.imshow("ImageW", img_warped)
        cv.imshow("image_thresh",image_thresh)
        cv.imshow("Image_", image_out)
        #cv.imshow("Image2_", image_thresh)
        key = cv.waitKey(1)
        print(norm_curve)
        if (norm_curve==0):
            moteur.move(0.2, norm_curve, 0.06)
        elif (norm_curve < 0.5)and(norm_curve > 0):
            moteur.move(0.2, norm_curve, 0.06)
        elif norm_curve > 0.6:
            moteur.right(0.54)
            sleep(1)
        else:
            moteur.move(0.2, norm_curve,0.06)

        if key == ord("q"):
            break
    pins.cleanup()
            
            
        
        
        
        
    







        

