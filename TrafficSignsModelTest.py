
# relevent libraries :
import cv2
from PIL import Image
import tensorflow
import numpy as np
from tensorflow.keras.models import load_model



# Label Overview
classes = {
            14:'Stop',
            19:'Turn left',
            20:'Turn right',
            21:'curve',
            26:'Traffic signals',
            33:'Turn right',
            34:'Turn left',
            38:'Turn right',
            39:'Turn left' }

# Resizing the images to 30x30x3
IMG_HEIGHT = 30
IMG_WIDTH = 30
channels = 3


# loading the trained model :
model = load_model("/home/raspberry/project/traficsigns1.h5")



# tesing livestream :


def preprocess_image(image):
    image_fromarray = Image.fromarray(image, 'RGB')
    resize_image = image_fromarray.resize((IMG_HEIGHT, IMG_WIDTH))
    image_data = np.array(resize_image)
    image_data = image_data / 255.0
    image_data = np.expand_dims(image_data, axis=0)
    return image_data


# Open the video stream
cap = cv2.VideoCapture(0)

while True:
    # Capture each frame
    ret, frame = cap.read()

    # Preprocess the frame and make predictions
    preprocessed_frame = preprocess_image(frame)
    probabilities = model.predict(preprocessed_frame)
    predicted_class = np.argmax(probabilities)
    print(predicted_class)
    if predicted_class in classes :
        print(classes[predicted_class])
        # Display the frame with the predicted class name
        cv2.putText(frame, classes[predicted_class], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else : pass
    cv2.imshow('Real-time Traffic Sign Recognition', frame)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
