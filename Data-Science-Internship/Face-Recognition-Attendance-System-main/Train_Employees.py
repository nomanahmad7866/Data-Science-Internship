from architecture import *
import os
import cv2
import mtcnn

import pickle
import numpy as np
from sklearn.preprocessing import Normalizer

######paths and vairables#########
face_data = 'Faces/'
required_shape = (160,160)
face_encoder = InceptionResNetV2()
path = "facenet_keras_weights.h5"
face_encoder.load_weights(path)
face_detector = mtcnn.MTCNN()
encodes = []
encoding_dict = dict()
l2_normalizer = Normalizer('l2')

###############################
"""Training model on all employees database"""
###############################



def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std

#=====================================Implementation of the triplet loss============================#

"""triplet loss tries to "push" the encodings of two images of the same person (Anchor and Positive)
closer together,while "pulling" the encodings of two images of different persons (Anchor, Negative)
further apart"""

def triplet_loss(y_true, y_pred, alpha=0.3):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # Computing the (encoding) distance between the anchor and the positive
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    # Computing the (encoding) distance between the anchor and the negative
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    # subtracting the two previous distances and adding alpha.
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    # Taking the maximum of basic_loss and 0.0. Sum over the training examples.
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))

    return loss


for face_names in os.listdir(face_data):
    person_dir = os.path.join(face_data,face_names)

    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir,image_name)

        img_BGR = cv2.imread(image_path)
        img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)

        x = face_detector.detect_faces(img_RGB)
        x1, y1, width, height = x[0]['box']
        x1, y1 = abs(x1) , abs(y1)
        x2, y2 = x1+width , y1+height
        face = img_RGB[y1:y2 , x1:x2]

        face = normalize(face)
        face = cv2.resize(face, required_shape)
        face_d = np.expand_dims(face, axis=0)
        encode = face_encoder.predict(face_d)[0]
        encodes.append(encode)

    if encodes:
        encode = np.sum(encodes, axis=0 )
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
        encoding_dict[face_names] = encode

path = 'encodings/encodings.pkl'
with open(path, 'wb') as file:
    pickle.dump(encoding_dict, file)








