import tensorflow as tf
import numpy as np
import glob, os
from tensorflow.keras.models import model_from_json
from PIL import Image

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# load model from json file and create
os.chdir(os.path.abspath(os.getcwd()) + '/models')

json_file = open('mnist.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)

# load weights into model from h5 file
loaded_model.load_weights("mnist.h5")
print("Loaded model from disk")

#compile the loaded JSON model
loaded_model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

def pre_process(image_file):
    image = Image.open(image_file)
    im_as_array = np.asarray(image)
    return im_as_array

def predict_image(my_image):
    #make predictions on the model
    processed_image = pre_process(my_image)
    processed_image = np.asarray(processed_image) / 255.0
    predictions = str(np.argmax(loaded_model.predict(processed_image.reshape((1, 28, 28, 1)))[0]))
    # predictions = loaded_model.predict_classes(processed_image.reshape((1,28,28,1)))

    return predictions




