#!/usr/bin/env python3

from lib.configparser import parseConfig
from lib.log import log

import select, socket, sys, random
from threading import Thread
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf
import numpy as np
import cv2

host, port = parseConfig('ini/config.ini')

imageName = "pneumonia%s.jpg"
incomingFolder = "./incomming/"
modelFolder = "./models/"

# GPU setup
physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

def sendMessage(connected, msg):
	log(f"[INFO] Replying to {clientAddress}:  {msg}", "info")
	connected.sendall(msg.encode())

def requestModel(connected):
	log(f"[INFO] Waiting for model from {clientAddress}", "info")

	model = connected.recv(4).decode()

	log("[INFO] Got model: " + model.lower(), "info")
	model = model.lower()
	if model == "ince":
		model = "Inception"
	elif model == "dens":
		model = "densenet"
	elif model == "mycn":
		model = "myCNN"
	elif model == "vgg!":
		model = "VGG"
	elif model == "xcep":
		model = "Xception"
	elif model == "resn":
		model = "Resnet"
	else:
		model = "fail"

	if model == "fail":
		log(f"[EE] Replying to {clientAddress}: 3", "warning")
		connected.sendall("3".encode())
	else:
		log(f"[INFO] Replying to {clientAddress}: Success", "info")
		connected.sendall("0".encode())
		return model

def prepareImage(imageFile):
	image = cv2.imread(imageFile)
	image = cv2.resize(image,(224,224))
	image = np.asarray(image)
	image = np.expand_dims(image, axis=0)

	return image

def makePrediction(connected, imageFile, model):
	trainedModel = tf.keras.models.load_model(modelFolder + model)

	processedImage = prepareImage(imageFile)

	pred = np.argmax(trainedModel.predict(processedImage), axis=-1)

	if pred == 0:
		results = "N"
	else:
		results = "P"

	log(f"[INFO] Sending Prediction to {clientAddress}: {results}", "info")
	connected.sendall(results.encode())

def parseImage(data, saveLocation):
	# Save each image into temp with random num
	randNum =random.randint(0,100)

	imageFile = open(imageName % randNum, 'wb')
	imageFile.write(data)
	imageFile.close()

	return (imageName % randNum)

def receiveImage(connected):
	bufferSize = 4096

	log(f"[INFO] Waiting for image from {clientAddress}", "info")
	results = connected.recv(10).decode()
	log(f"[INFO] Sending okay to  {clientAddress}", "info")
	sendMessage(connected, ("0"))
	log("Got size: " + results, "info")

	fileSize = ""
	for digit in results:
		if digit.isdigit():
			fileSize += digit

	while ((int(fileSize) % bufferSize) != 0):
		bufferSize -= 1


	# Receive files in chunks, handle remainder if file isn't divisble by chunk size
	incommingTotal = b''
	i = 0

	count = int(fileSize) / bufferSize
	while i != int(fileSize):
		incommingPart = connected.recv(1)

		if not incommingPart:
			break
		incommingTotal += incommingPart
		i += 1


	log(f"[INFO] Image received from {clientAddress}", "info")
	savedName = parseImage(incommingTotal, incomingFolder)

	return savedName

def removeClient(connected, msg):
	log(f"remove client {clientAddress}: {msg}", "info")
	try:
		clientSockets.remove(connected)
	except KeyError:
		log(f"[WARN] client {clientAddress} already removed", "warning")

	return False

def parseCommand(connected):
		stillThere = True
		timeout = 0
		# Execute the function depending on the request
		while stillThere:
			message = ''
			log(f"[INFO] Waiting for next command: {clientAddress}", "info")

			while message == '':
				if timeout >= 60:
					removeClient(connected, "timeout")
					stillThere = False
					break

				time.sleep(1)
				try:
					message = connected.recv(4).decode()
				except Exception as e:
					log(f"[ERR] {clientAddress} : {e}", "error")
					stillThere = removeClient(connected, "Error occured")
					break
				timeout += 1

			if stillThere:
				log(f"[INFO] Command Recv from {clientAddress}: {message}", "info")
				if message == "FILE":
					sendMessage(connected, "0")
					imageFile = receiveImage(connected)
					breakCon = True
				elif message == "MODE":
					sendMessage(connected, "0")
					selectedModel = requestModel(connected)
				elif message == "PRED":
					try:
						selectedModel, imageFile
					except NameError:
						sendMessage(connected, "1")
					else:
						sendMessage(connected, "0")
						makePrediction(connected, imageFile, selectedModel)
				elif message == "BYE!":
					sendMessage(connected, "0")
					stillThere = removeClient(connected, "bye")
					break
				else:
					log(f"[WARN] Invalid request from {clientAddress}: {message}", "warning")
					stillThere = removeClient(connected, "Invalid command")

def waitForClient(socket):
	try:
		msg = socket.send("?".encode())
	except Exception as e:
		# client no longer connected
		# remove it from the set
		log(f"[ERR] {clientAddress} : {e}", "Error")
		try:
			clientSockets.remove(socket)
		except Exception as e:
			log(f"[ERR] {clientAddress} : {e}", "error")
	else:
		parseCommand(socket)

# initialize list/set of all connected client's sockets
clientSockets = set()

# create a TCP socket
serverSocket = socket.socket()

# make the port as reusable port
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

# bind the socket to the address we specified
serverSocket.bind((host, int(port)))

# listen for upcoming connections
serverSocket.listen(5)

log(f"[INFO] Starting up server as {host}:{port}", "info")

while True:
	# we keep listening for new connections all the time
	clientSocket, clientAddress = serverSocket.accept()
	log(f"[INFO] {clientAddress} connected.", "info")

	 # add the new connected client to connected sockets
	clientSockets.add(clientSocket)

	# start a new thread that listens for each client's messages
	threadT = Thread(target=waitForClient, args=(clientSocket,))

	# make the thread daemon so it ends whenever the main thread ends
	threadT.daemon = True
	# start the thread
	threadT.start()


for cs in clientSockets:
	cs.close()
