import cv2 as cv
import numpy as np


def value_changed():
    pass

def draw_points(img, points):
    for x in range(4):
        cv.circle(img, (int(points[x][0]), int(points[x][1])), 10, (255, 0, 0), cv.FILLED)
    return img

def thresholding(image, lower_values, upper_values):
    imageHsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image_mask = cv.inRange(imageHsv, lower_values, upper_values)
    image_thresh = cv.bitwise_and(image, image, mask = image_mask)
    return image_mask

def rgb_thresh(image, r_min, g_min, b_min, r_max, g_max, b_max):
    lower_values = np.array([r_min, g_min, b_min])
    upper_values = np.array([r_max, g_max, b_max])
        
    image_mask = cv.inRange(image, lower_values, upper_values)
    image_thresh = cv.bitwise_and(image, image, mask = image_mask)
    return image_mask
    
def getHistogram(img,minPer=0.1, region=0.45):
 
    
    histValues = np.sum(img[int(img.shape[0]*region):,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    return basePoint

def get_histogram(img, min_perc = 0.5, region = 0.3):
    hist_values = np.sum(img[int(img.shape[0]*region):,:], axis = 0)
    max_value = np.max(hist_values)
    min_thresh_value = min_perc*max_value
    index_array = np.where(hist_values >= min_thresh_value)
    base_point = np.average(index_array)
    #cv.circle(img,(base_point,img.shape[0]),20,(0,255,0),cv.FILLED)
    return int(base_point)

def should_we_stop(image, min_per, min_number_line):
    hist_values = np.sum(image, axis = 1)
    max_value = np.max(hist_values)
    print(max_value)
    min_value_to_consider_as_zero = min_per*max_value
    index_array = np.where(hist_values <= min_value_to_consider_as_zero)
    print(index_array[0].shape)
    number_of_zero_line = index_array[0].shape[0]
    if number_of_zero_line >= min_number_line:
        return True
    return False

def warp_image(image, points, w, h):
    pt1 = np.float32(points)
    pt2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    mat = cv.getPerspectiveTransform(pt1, pt2)
    img_warp = cv.warpPerspective(image, mat, (w, h))
    return img_warp

def get_rgb_thresold_values(cap):
    cv.namedWindow("RGB")
    cv.resizeWindow("RGB", 400, 240)
    cv.createTrackbar("RED MIN", "RGB", 0, 255, value_changed)
    cv.createTrackbar("RED MAX", "RGB", 255, 255, value_changed)
    cv.createTrackbar("GREEN MIN", "RGB", 0, 255, value_changed)
    cv.createTrackbar("GREEN MAX", "RGB", 255, 255, value_changed)
    cv.createTrackbar("BLUE MIN", "RGB", 0, 255, value_changed)
    cv.createTrackbar("BLUE MAX", "RGB", 255, 255, value_changed)
    frame_counter = 0
    while True:
        frame_counter += 1
        if int(cap.get(cv.CAP_PROP_FRAME_COUNT)-2) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0
        ret, frame = cap.read()
        frame = cv.resize(frame, (300, 300))
        
        r_min = cv.getTrackbarPos("RED MIN", "RGB")
        r_max = cv.getTrackbarPos("RED MAX", "RGB")
        g_min = cv.getTrackbarPos("GREEN MIN", "RGB")
        g_max = cv.getTrackbarPos("GREEN MAX", "RGB")
        b_min = cv.getTrackbarPos("BLUE MIN", "RGB")
        b_max = cv.getTrackbarPos("BLUE MAX", "RGB")

        lower_values = np.array([r_min, g_min, b_min])
        upper_values = np.array([r_max, g_max, b_max])
        
        image_mask = cv.inRange(frame, lower_values, upper_values)
        image_thresh = cv.bitwise_and(frame, frame, mask = image_mask)
        
        image_mask = cv.cvtColor(image_mask, cv.COLOR_GRAY2BGR)
        hstack = np.hstack([frame, image_mask, image_thresh])
        cv.imshow("Image", hstack)
        if cv.waitKey(20) & 0xFF == ord("q"):
                break
    cap.release()
    cv.destroyAllWindows()
    
def get_warp_values(cap):
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    width = int(width)
    height = int(height)
    print(width)
    cv.namedWindow("WARP")
    cv.resizeWindow("WARP", 400, 240)
    cv.createTrackbar("width top", "WARP", 100, int(width//2), value_changed)
    cv.createTrackbar("height top", "WARP", 100, int(height), value_changed)
    cv.createTrackbar("width bottom", "WARP", 100, int(width//2), value_changed)
    cv.createTrackbar("height bottom", "WARP", 100, int(height), value_changed)
    frame_counter = 0
    while True:
        frame_counter += 1
        if int(cap.get(cv.CAP_PROP_FRAME_COUNT)-2) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0
        ret, frame = cap.read()
        
        w_top = cv.getTrackbarPos("width top", "WARP")
        h_top = cv.getTrackbarPos("height top", "WARP")
        w_bottom = cv.getTrackbarPos("width bottom", "WARP")
        h_bottom = cv.getTrackbarPos("height bottom", "WARP")

        points = np.float32([[w_top, h_top], [int(width-w_top), h_top], [w_bottom, h_bottom], [int(width-w_bottom), h_bottom]])
        img_warp = warp_image(frame, points, width, height)
        img_points = draw_points(frame, points)
        cv.imshow("Image warped", img_warp)
        cv.imshow("Image with points", img_points)
        if cv.waitKey(20) & 0xFF == ord("q"):
                break
    cap.release()
    cv.destroyAllWindows()
    


def get_hsv_threshold_values(cap):
    cv.namedWindow("HSV")
    cv.resizeWindow("HSV", 400, 240)
    cv.createTrackbar("HUE MIN", "HSV", 0, 179, value_changed)
    cv.createTrackbar("HUE MAX", "HSV", 179, 179, value_changed)
    cv.createTrackbar("SAT MIN", "HSV", 0, 255, value_changed)
    cv.createTrackbar("SAT MAX", "HSV", 255, 255, value_changed)
    cv.createTrackbar("VALUE MIN", "HSV", 0, 255, value_changed)
    cv.createTrackbar("VALUE MAX", "HSV", 255, 255, value_changed)
    frame_counter = 0
    while True:
        frame_counter += 1
        if int(cap.get(cv.CAP_PROP_FRAME_COUNT)-2) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0
        ret, frame = cap.read()
        frame = cv.resize(frame, (300, 300))
        
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




    
