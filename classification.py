from keras.models import load_model
from PIL import Image
import numpy as np
model = load_model('imageclassification_model.h5')

label = ['비행기', '자동차', '새', '고양이', '사슴', '개', '개구리', '말', '배', '트럭']


def predict_image(src):
    img = Image.open(src).convert('RGB')
    size = (32, 32)
    img = img.resize(size)
    arr = np.array(img).reshape(1, 32, 32, 3)
    pred = model.predict(arr)
    return label[np.argmax(pred)]
