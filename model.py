"""Helper class for building Siamese model for One-shot learning.

   @description
     For visualizing, pre-processing and loading the Omniglot dataset.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola/

   @project
     File: model.py
     Created on 13 July, 2018 @ 9:10 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
import tensorflow as tf

from tensorflow import keras
import numpy as np


class SiameseNetwork(keras.Model):

    def __init__(self, num_classes: int=1, **kwargs):
        super(SiameseNetwork, self).__init__(name='SiameseNetwork')

        # Positional Arguments.
        self.num_classes = num_classes

        # Keyword Arguments.
        self.batch_size = kwargs.get('batch_size', 16)
        self.in_shape = kwargs.get('input_shape', (105, 105, 1))

        # Input layer.
        self.input_layer = keras.layers.InputLayer(input_shape=self.in_shape,
                                                   batch_size=self.batch_size,
                                                   dtype=tf.float32, name='Images')

        # 1st layer (64@10x10)
        self.conv1 = keras.layers.Conv2D(filters=64, kernel_size=(10, 10),
                                         kernel_regularizer=keras.regularizers.l2,
                                         activation=keras.activations.relu)
        self.pool1 = keras.layers.MaxPool2D(pool_size=(2, 2))

        # 2nd layer (128@7x7)
        self.conv2 = keras.layers.Conv2D(filters=128, kernel_size=(7, 7),
                                         kernel_regularizer=keras.regularizers.l2,
                                         activation=tf.keras.activations.relu)
        self.pool2 = keras.layers.MaxPool2D(pool_size=(2, 2))

        # 3rd layer (128@4x4)
        self.conv3 = keras.layers.Conv2D(filters=128, kernel_size=(4, 4),
                                         kernel_regularizer=keras.regularizers.l2,
                                         activation=keras.activations.relu)
        self.pool3 = keras.layers.MaxPool2D(pool_size=(2, 2))

        # 4th layer (265@4x4)
        self.conv4 = keras.layers.Conv2D(filters=256, kernel_size=(4, 4),
                                         kernel_regularizer=keras.regularizers.l2,
                                         activation=keras.activations.relu)
        self.pool4 = keras.layers.MaxPool2D(pool_size=(2, 2))

        # 5th layer  (9216x4096)
        self.flatten = keras.layers.Flatten()
        self.dense = keras.layers.Dense(units=4096,
                                        activation=keras.activations.sigmoid)

        # 6th - L1 layer -distance layer.
        self.l1 = keras.layers.Lambda(lambda x: tf.abs(x[0] - x[1]))

        # Output layer (4096x1)
        self.prediction = keras.layers.Dense(units=self.num_classes,
                                             activation=keras.activations.sigmoid)

    def __repr__(self):
        return f'models.SiameseNetwork(num_classes={self.num_classes})'

    def call(self, inputs, **kwargs):
        """Calls the model on new inputs.

        In this case `call` just reapplies all ops in the graph to the new inputs
        (e.g. build a new computational graph from the provided inputs).

        Arguments:
            inputs: A tensor or list of tensors.
            training: Boolean or boolean scalar tensor, indicating whether to run
            the `Network` in training mode or inference mode.
            mask: A mask or list of masks. A mask can be
                either a tensor or None (no mask).

        Returns:
            A tensor if there is a single output, or
            a list of tensors if there are more than one outputs.
        """

        def encoder(x):
            # Input layer.
            x = self.input_layer(inputs)

            # Convolutional blocks.
            x = self.pool1(self.conv1(x))
            x = self.pool2(self.conv2(x))
            x = self.pool3(self.conv3(x))
            x = self.pool4(self.conv4(x))

            # Flatten & fully connected layers
            x = self.flatten(x)
            x = self.dense(x)

            return x

        # Sister networks.
        first = encoder(inputs[0])
        second = encoder(inputs[1])

        # L1 distance.
        distance = self.l1((first, second))

        # Prediction.
        x = self.prediction(x)

        return x

    def compute_output_shape(self, input_shape):
        shape = tf.TensorShape(input_shape).as_list()
        shape[-1] = self.num_classes
        return tf.TensorShape(shape)


if __name__ == '__main__':
    net = SiameseNetwork(num_classes=1)

    net.compile(optimizer=keras.optimizers.Adam(lr=1e-3),
                loss=keras.losses.binary_crossentropy,
                metrics=[keras.metrics.binary_accuracy])

    print(net)
