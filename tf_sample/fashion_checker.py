import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf

class FashionChecker(object):
    def __init__(self):
        self.class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                            'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    def create_model(self):
        # Data Preprocessing
        fashion_mnist = keras.datasets.fashion_mnist
        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
        '''
        plt.figure()
        plt.imshow(train_images[10])
        plt.colorbar()
        plt.grid(False)
        plt.show()'''

        # Modeling
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28,28)),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # Learning
        model.fit(train_images, train_labels, epochs=5)

        # Test
        test_loss, test_acc = model.evaluate(test_images, test_labels)
        print(f'Test Accuracy: {test_acc}')



if __name__ == '__main__':
    f = FashionChecker()
    f.create_model()