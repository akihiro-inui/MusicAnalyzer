#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 17 May 2019
@author: Akihiro Inui
"""

import os
import torch
import numpy as np
from torch import nn, optim
import torch.nn.functional as F
import matplotlib.pyplot as plt


class LogisticRegression:
    """
    Logistic Regression
    """
    def __init__(self, validation_rate, num_classes):
        """
        Init
        :param  validation_rate: validation rate
        :param  num_classes: number of classes
        """
        self.validation_rate = validation_rate
        self.num_classes = num_classes

    def training(self, train_data, train_label, visualize=None):
        """
        Training for Gated Recurrent Unit
        :param  train_data: training data
        :param  train_label: train label
        :param  visualize: True/False to visualize training history
        :return model: trained model
        """
        # Convert training data
        train_data = torch.tensor(np.array(train_data), dtype=torch.float32)

        # One hot encode
        onehot_train_label = torch.tensor(np.array(train_label), dtype=torch.long)

        # Define the model
        model = nn.Linear(train_data.shape[1], self.num_classes)

        # Softmax Cross Entropy
        loss_fn = nn.CrossEntropyLoss()

        # SGD
        optimizer = optim.SGD(model.parameters(), lr=0.01)

        # To log losses
        losses = []
        for epoch in range(30000):
            # Delete gradient value calculated in previous epoch
            optimizer.zero_grad()

            # Make prediction
            predicted_label = model(train_data)

            # Calculate MSE loss
            loss = loss_fn(predicted_label, onehot_train_label)
            loss.backward()

            # Update gradient
            optimizer.step()

            # Log loss
            losses.append(loss.item())

        # Visualize losses
        if visualize is True:
            plt.plot(losses)
            plt.show()

        return model

    def load_model(self, model_file_name: str):
        """
        Load trained model
        :param  model_file_name: name of model file to load
        :return model: trained model
        """
        # Load model if it exists
        assert os.path.exists(model_file_name), "Given model file does not exist"
        return torch.load(model_file_name, map_location="cpu")

    def save_model(self, model, output_directory: str):
        """
        Save model
        :param  model: trained model
        :param  output_directory: output directory path
        """
        a = model.state_dict()
        torch.save(model.state_dict(), os.path.join(output_directory, "logistic_regression.prm"), pickle_protocol=4)

    def test(self, model, test_data, test_label):
        """
        Make a test for the given dataset
        :param  model: trained model
        :param  test_data: test data
        :param  test_label: test label
        :return result of test
        """
        # One hot encode
        onehot_test_label = torch.tensor(np.array(test_label), dtype=torch.long)
        # Make predictions and output result
        predicted = torch.max(model(torch.tensor(np.array(test_data), dtype=torch.float32)), 1)[1]
        return (predicted == onehot_test_label).sum().item()/len(test_label)

    def predict(self, model, target_data):
        """
        Make prediction to a given target data and return the prediction result with accuracy for each sample
        :param  model: trained model
        :param  target_data: target data without label
        :return prediction array with probability
        """
        # Make prediction to the target data
        return model(torch.tensor(np.array(target_data), dtype=torch.float32))
