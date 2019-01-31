# coding: utf-8
import cv2
import os
import tensorflow as tf
import numpy as np
from PIL import Image

def resize_to_227_square(image):
    return cv2.resize(image, (227, 227), interpolation = cv2.INTER_LINEAR)

# graph of operations to upload trained model
graph_def = tf.GraphDef()
# list of classes
labels = []
# N.B. Azure Custom vision allows export trained model in the form of 2 files
# model.pb: a tensor flow graph and labels.txt: a list of classes
# import tensor flow graph, r+b mode is open the binary file in read or write mode
with tf.gfile.FastGFile(name='model.pb', mode='rb') as f:
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def=graph_def, name='')
# read labels, add to labels array and create a folder for each class
# it refers to the text mode. There is no difference between r and rt or w and wt since text mode is the default.
with open(file='labels.txt', mode='rt') as labels_file:
    for label in labels_file:
        label = label.strip()
        # append to the labels array (trimmed)
        labels.append(label)
# These names are part of the model and cannot be changed.
output_layer = 'loss:0'
input_node = 'Placeholder:0'
# read test image
image = cv2.imread('1.png')
# get the largest center square
#  The compact models have a network size of 227x227, the model requires this size.
augmented_image = resize_to_227_square(image)
predicted_tag = 'Predicted Tag'
with tf.Session() as sess:
    # difine a directory where the FileWriter serialized its data
    writer = tf.summary.FileWriter('log')
    writer.add_graph(sess.graph)
    prob_tensor = sess.graph.get_tensor_by_name(output_layer)
    predictions = sess.run(prob_tensor, {input_node: [augmented_image]})
    # get the highest probability label
    highest_probability_index = np.argmax(predictions)
    predicted_tag = labels[highest_probability_index]
    print(predicted_tag)
    writer.close()