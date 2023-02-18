import tensorflow as tf
import numpy as np

IMG_SIZE = 224

def preprocess(img_path):
    image = tf.io.read_file(img_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])
    return image

def get_prediction(img_path):
    model = tf.keras.models.load_model('my_model')

    BATCH_SIZE = 32

    with open('unique_breeds.txt', 'r') as file:
        lines = file.readlines()
    unique_breeds = lines[0].split(' ')

    image = preprocess(img_path)

    def plc(x):
        return image

    data = tf.data.Dataset.from_tensor_slices((tf.constant(image)))
    data_batch = data.map(plc).batch(BATCH_SIZE)

    pred = model.predict(data_batch, verbose = 1)

    pred_prob = round(np.max(pred[0]) * 100, 2)

    if pred_prob < 30:
        prediction_dict = {
            'breed': 'No dog detected',
            'perc': 'low'
        }
    else:
        prediction_dict = {
            'breed': unique_breeds[pred[0].argmax()],
            'perc': f'{pred_prob}%'
        }

    return prediction_dict
