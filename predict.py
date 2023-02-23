from tensorflow import io, image, keras, data, constant, float32
import numpy as np

IMG_SIZE = 224

def preprocess(img_path):
    img = io.read_file(img_path)
    img = image.decode_jpeg(img, channels=3)
    img = image.convert_image_dtype(img, float32)
    img = image.resize(img, size=[IMG_SIZE, IMG_SIZE])
    return img

def get_prediction(img_path):
    model = keras.models.load_model('my_model')

    BATCH_SIZE = 32

    with open('unique_breeds.txt', 'r') as file:
        lines = file.readlines()
    unique_breeds = lines[0].split(' ')

    img = preprocess(img_path)

    def plc(x):
        return img

    data_ = data.Dataset.from_tensor_slices((constant(img)))
    data_batch = data_.map(plc).batch(BATCH_SIZE)

    pred = model.predict(data_batch, verbose = 1)

    pred_prob = round(np.max(pred[0]) * 100, 2)

    if pred_prob < 40:
        prediction_dict = {
            'breed': 'no_dog_detected',
            'perc': 'low'
        }
    else:
        prediction_dict = {
            'breed': unique_breeds[pred[0].argmax()],
            'perc': f'{pred_prob}%'
        }

    return prediction_dict
