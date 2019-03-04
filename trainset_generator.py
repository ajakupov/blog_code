# coding utf-8
import cv2
import os
import tensorflow as tf
import numpy as np
from numba import jit

# BGR colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
# Output text parameters
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
LINE_TYPE = 1

WINDOW_NAME = 'iteration1.2'


def resize_to_224_square(image):
    return cv2.resize(image, (224, 224), interpolation=cv2.INTER_LINEAR)


def get_best_rectangle(faces):
    """
    get the largest square from the faces array to avoid noise
    :param faces:
    :return: the coordinates of the largest square
    """
    # coordinates of the largest square
    maxX = 0
    maxY = 0
    maxW = 0
    maxH = 0
    maxArea = 0
    # iterate over each face detected
    for (x, y, w, h) in faces:
        # check if the square is larger than the current max
        if w*h > maxArea:
            # update the current max
            maxArea = w*h
            # and the coordinates
            maxX = x
            maxY = y
            maxH = h
            maxW = w
    # return the real face coordinates
    return (maxX, maxY, maxW, maxH)

# global parameters to compare the position of an object in the frame
counter = 0
previousX = 0
previousY = 0

# graph of operations to upload trained model
graph_def = tf.GraphDef()
# list of classes
labels = []
# N.B. Azure Custom vision allows export trained model in the form of 2 files
# model.pb: a tensor flow graph and labels.txt: a list of classes
# import tensor flow graph, r+b mode is open the binary file in read or write mode
with tf.gfile.FastGFile(name='it1_model.pb', mode='rb') as f:
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def=graph_def, name='')
# read labels, add to labels array and create a folder for each class
# t refers to the text mode. There is no difference between r and rt or w and wt since text mode is the default.
with open(file='it1_labels.txt', mode='rt') as labels_file:
    for label in labels_file:
        label = label.strip()
        # append to the labels array (trimmed)
        labels.append(label)
        # check if the folder already exists
        if not os.path.exists(label):
            os.makedirs(label)
# initialize video capture object to read video from external webcam
video_capture = cv2.VideoCapture(1)
# if there is no external camera then take the built-in camera
if not video_capture.read()[0]:
    video_capture = cv2.VideoCapture(0)

# Full screen mode
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while(video_capture.isOpened()):
    # read video frame by frame
    ret, frame = video_capture.read()

    try:
        # frame width and height
        w, h = 200, 200
        # set upper and lower boundaries
        upX = 250
        upY = 150
        lowX = upX + w
        lowY = upY + h
        image = frame[upY:lowY, upX:lowX]
        # These names are part of the model and cannot be changed.
        output_layer = 'loss:0'
        input_node = 'Placeholder:0'
        # get the largest center square
        # The compact models have a network size of 227x227, the model requires this size.
        augmented_image = resize_to_227_square(image)
        predicted_tag = 'Predicted Tag'
        with tf.Session() as sess:
            prob_tensor = sess.graph.get_tensor_by_name(output_layer)
            predictions = sess.run(prob_tensor, {input_node: [augmented_image]})
            # get the highest probability label
            highest_probability_index = np.argmax(predictions)
            predicted_tag = labels[highest_probability_index]
            output_text = predicted_tag
            if predicted_tag == 'ok':
                frameColor = GREEN
            elif predicted_tag == 'ko':
                frameColor = RED
            else:
                frameColor = BLUE
            # to not erase previously saved photos counter (image name) = number of photos in a folder + 1
            image_counter = len([name for name in os.listdir(predicted_tag)
                                 if os.path.isfile(os.path.join(predicted_tag, name))])
            # save image to the dedicated folder (folder name = label)
            cv2.imwrite(predicted_tag + '/' + str(image_counter) + '.png', image)
            # increment image counter
            image_counter += 1
            cv2.rectangle(frame, (upX, upY), (lowX, lowY), frameColor, 1)
    except:
        continue
    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release video capture object
video_capture.release()
cv2.destroyAllWindows()
