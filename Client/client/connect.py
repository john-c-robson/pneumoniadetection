#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:        Anthony Donnelly
@contributor:
"""

import socket
import time
import os

def getReply(remote):
	response = remote.recv(1).decode()

	return response

def sendMessage(msg, remote):
	# our packets should be four bytes
	# prevent hanging
	if len(msg) > 4 or len(msg) < 4:
		("Message must be 4 bytes")
	else:
		print("Sending Commands: " + msg)
		remote.sendall(msg.encode())
		response = getReply(remote)
		return response

def sendModel(model, remote):
	response = sendMessage("MODE", remote)

	if response == "0":
		print("Got OK response, sending model")
		model = model[0:4]

		# only send 4 bytes of data
		remote.sendall(model.encode())

		print("Model sent, waiting reply")
		reply = getReply(remote)
		print("Got reply: " + reply)

def sendImage(imageFile, remote):
	bufferSize = 4096

	response = sendMessage("FILE", remote)
	if response == "0":
		print("Got OK response, sending file size and file")

		filesize = os.path.getsize(imageFile)

		# Increase size to meet the buffer
		# since the size is numeric, add digits to fill the buffer
		# strip on server side
		# string start from index 0
		dummysize = str(filesize)
		while (len(dummysize) < 10):
			dummysize += "z"

		print(len(dummysize))
		remote.sendall(dummysize.encode())
		response = getReply(remote)

		while filesize % bufferSize != 0:
			bufferSize -= 1


		count = filesize / bufferSize
		i = 0
		print(response)
		if response == "0":
			with open(imageFile, "rb") as sendFile:
				print(f"Sending {count} chunks")
				while i != filesize:
					chunk = sendFile.read(1)
					if not chunk:
						break
					remote.sendall(chunk)
					i += 1
			sendFile.close()
			print("image file sent")

def disconnect(remote):
	response = sendMessage("BYE!", remote)

	if response == "0":
		message = "Disconnected"
	else:
		message = "No reply from server"

	return message

def receivePred(remote):
	response = sendMessage("PRED", remote)

	if response == "0":
		pred =  getReply(remote)
		print("prediciton is " + pred)

		return pred
