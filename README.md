# Pneumonia project for MSC Project

## Table of contents

- [Project information](#project-information)
- [Technologies](#technologies)
- [Repository](#repository)
- [Documentation](#documentation)
- [Solution Development Report](#solution-development-report)
- [Server](#server)
- [Client](#client)

## Project information

This project aims to create a model that uses static images of chest x-rays to detect pneumonia at an early stage.

This project is experimentation to create a model that uses static images of chest x-rays to detect pneumonia on an early stage.

This repository was submitted on 10 May 2021 for an MSC project.

J. Robson w19036980 john3.robson@northumbria.ac.uk, A. Donnelly w19008099 anthony.donnelly@northumbria.ac.uk, are from the
Department of Computer Information Sciences, Faculty of Engineering and Environment, Northumbria University.

## Technologies

Project is divided into parts such as:

Google collaboration file for pneumonia detection:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11cqn_Fo19JjHyRk6qKt2DUYJp47LsYaG?usp=sharing)

Baseline model
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Wh5pCY6eLOir8lFQollzUkcX8iNJnzDp?usp=sharing)

## Repository

The repository of the project contains cnnModels.ipynb, pneumoniaDetect.py, README.md, GUI files, as well as files with our missions.

The first cnnModels.ipnyb file is the most important file of our project. In this notebook, the project can be either trained or loaded with five additional models on top of our model that we have created.

pneumoniaDetect.py file is used for the Graphical Interface.

README.md file provides all necessary information about the project and files.

## Solution Development report

### Pipeline Evaluations

Without any pre-processing of the dataset, overfitting became problematic, making prediction accuracy very low with the test set. Also, as a measure to ensure the models can handle a broad range of variables that could occur in images as they are fed to the pipeline, training and test images went under data augmentation to produce images with possible expected variations. This consisted of rescaling, rotation, zoom, brightness changes, and even horizontal and vertical flips. Doing this allows the models to be trained against these variations and better understand how to handle them. With this augmentation method, overfitting no longer occurred. As the pipeline is designed for use with even lightweight systems like mobile phones, understanding how new data may be presented to the system has been addressed.

### Model Evaluations

As a baseline model, C-NN was used initially for the system, which performed at 88% accuracy. To ensure better accuracy for predictions, alternative models were introduced to the data providing a range of models to test against. By doing this, ensembling became possible to connect the performances of all the models to offer a high accuracy of 93% against the test set and 95% with the optional validation set.

### Parameter Justifications

Initially, the final activation parameter for the baseline model was sigmoid. We have a binary classification issue, which was the most suitable activation function. As we moved onto the iterative development, The group decided to switch
to softmax and categorical cross-entropy so that anyone can retrain the model on more classes to detect a broader range of
lung diseases.

The optimiser adam was used, along with RMSprop, as they both provided the highest accuracy yield. In the iterative model
we switched from Adam to RMSprop as RMSprop was slightly better.

Ten epochs seemed to produce the best output, as anything after this point; the model didn't improve much more. Using ten epochs kept training time
to an optimal level without being too time-consuming.

### Reproducible Code

For reproducing all experiments, the trained models are saved onto google drive and can be fetched within
the google collaboration file using shell script. The training history pickle file is also fetched so that
the training accuracy and training loss can be visualised and the validation loss.

## Server

This is a simple server written in python that accepts numerous commands to receive an image and make a prediction of the image and return the result.

This server can perform the prediction on a server with suitable hardware and allow people to run a client and still use the model regardless of their hardware.

Any one can use an interface for the following devices:

1. Mobile Devices
2. Laptops
3. Desktops

An example client is available in the client folder also written in python.

## Client

Minimalistic gui and [connect.py](https://github.com/john-c-robson/pneumoniadetection/blob/main/Client/client/connect.py) file to add some basic functions to allow sending and receiving replies from the server.

[connect.py](https://github.com/john-c-robson/pneumoniadetection/blob/main/Client/client/connect.py) can be included into any python script and allow sending files to to the server.

An example gui making use of [connect.py](https://github.com/john-c-robson/pneumoniadetection/blob/main/Client/client/connect.py) can also be found [here](https://github.com/john-c-robson/pneumoniadetection/blob/main/Client/pneumoniaDetect.py).
