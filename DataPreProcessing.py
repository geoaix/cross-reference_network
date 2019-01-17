# -*- coding:utf-8 -*-
"""
@author:Xu Jingyi
@file:DataPreProcessing.py
@time:2018/11/2722:29
"""
import tensorflow as tf
import random
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from copy import deepcopy


class LoadData(object):

    def __init__(self, seed, noise_level, augmentation):
        self.seed = seed
        self.noise_level = noise_level
        self.augmentation = augmentation

    def load_data(self):
        raise NotImplementedError("Do not implement this method")

    def data_augmentation(self, x_train, y_train):
        img_generator = ImageDataGenerator(rotation_range=15, width_shift_range=0.2, height_shift_range=0.2,
                                           zoom_range=0.2)
        data_num = x_train.shape[0]
        data_augmentation = img_generator.flow(x_train, y_train, batch_size=data_num)
        x_train = np.concatenate((x_train, data_augmentation[0][0]), axis=0)
        y_train = np.concatenate((y_train, data_augmentation[0][1]), axis=0)
        return x_train, y_train

    def generate_noise_labels(self, y_train):
        num_noise = int(self.noise_level * y_train.shape[0])
        noise_index = np.random.choice(y_train.shape[0], num_noise, replace=False)
        label_slice = np.argmax(y_train[noise_index], axis=1)
        new_label = np.random.randint(low=0, high=self.num_classes, size=num_noise)
        while sum(label_slice == new_label) > 0:
            n = sum(label_slice == new_label)
            new_label[label_slice == new_label] = np.random.randint(low=0, high=self.num_classes, size=n)
        y_train[noise_index] = tf.contrib.keras.utils.to_categorical(new_label, self.num_classes)
        return y_train

    def data_preprocess(self):
        x_train, y_train_orig, x_test, y_test = self.load_data()
        if self.noise_level > 0:
            y_train = self.generate_noise_labels(y_train_orig)
        else:
            y_train = deepcopy(y_train_orig)
        if self.augmentation:
            x_train, y_train = self.data_augmentation(x_train, y_train)
        return x_train, y_train, y_train_orig, x_test, y_test


class MNIST(LoadData):

    def __init__(self, seed, noise_level, augmentation):
        LoadData.__init__(self, seed, noise_level, augmentation)
        self.num_classes = 10
        self.img_rows, self.img_cols = 28, 28
        self.input_size = (28, 28, 1)
        self.x_train, self.y_train, self.y_train_orig, self.x_test, self.y_test = self.data_preprocess()

    def load_data(self):
        # load data
        mnist = tf.contrib.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0
        x_train = x_train.reshape(x_train.shape[0], self.img_rows, self.img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], self.img_rows, self.img_cols, 1)

        # transform labels to one-hot vectors
        y_train = tf.contrib.keras.utils.to_categorical(y_train, self.num_classes)
        y_test = tf.contrib.keras.utils.to_categorical(y_test, self.num_classes)
        return x_train, y_train, x_test, y_test


class CIFAR10(LoadData):

    def __init__(self, seed, noise_level, augmentation):
        LoadData.__init__(self, seed, noise_level, augmentation)
        self.num_classes = 10
        self.img_rows, self.img_cols = 32, 32
        self.input_size = (32, 32, 3)
        self.x_train, self.y_train, self.y_train_orig, self.x_test, self.y_test = self.data_preprocess()

    def load_data(self):
        # load data
        cifar10 = tf.keras.datasets.cifar10
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0
        x_train = x_train.reshape(x_train.shape[0], self.img_rows, self.img_cols, 3)
        x_test = x_test.reshape(x_test.shape[0], self.img_rows, self.img_cols, 3)

        # transform labels to one-hot vectors
        y_train = tf.contrib.keras.utils.to_categorical(y_train, self.num_classes)
        y_test = tf.contrib.keras.utils.to_categorical(y_test, self.num_classes)
        return x_train, y_train, x_test, y_test


class NORB(LoadData):

    def __init__(self, seed, noise_level, augmentation):
        LoadData.__init__(self, seed, noise_level, augmentation)

    def load_data(self):
        pass


class NewsGroup(LoadData):

    def __init__(self, seed, noise_level, augmentation):
        LoadData.__init__(self, seed, noise_level, augmentation)

    def load_data(self):
        pass
