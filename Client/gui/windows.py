from PySide2.QtWidgets import  QMainWindow
from PySide2.QtCore import QProcess
from PySide2.QtGui import QImage, QPixmap

#Import our generated class to create a child class
from gui.ui.ui_mainwindow import Ui_MainWindow

from lib import file
from lib import errors
from client import connect as server
from threading import Thread
import socket, sys

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.connectSignalsSlots()
		self.model = ''
		self.imageFile = ''
		self.remote = ''
		self.folderName = ''
		self.Failed = False

	def connectSignalsSlots(self):
		self.ui.browseFilesButton.clicked.connect(self.bbrowseFiles)
		self.ui.predictButton.clicked.connect(self.getPrediction)
		self.ui.fileList.itemSelectionChanged.connect(self.showImage)
		self.ui.actionExit.triggered.connect(self.quit)

	def quit(self):
		sys.exit(0)

	def connect(self):
		self.remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.remote.connect(('127.0.1.1',50022))
		except ConnectionRefusedError:
			self.ui.txtOutput.append("Connection refused")
			self.failed = True

		response = server.getReply(self.remote)

		if response == "?":
			self.ui.txtOutput.append("Connected to server")
			return True
		else:
			return False

	def showImage(self):
		selectedImage = [item.text() for item in self.ui.fileList.selectedItems()]
		self.imageFile = self.folderName + "/" + selectedImage[0]
		pixmap = QPixmap(self.imageFile)
		self.ui.picView.setPixmap(pixmap.scaled(self.ui.picView.width(),self.ui.picView.height()))

	def bbrowseFiles(self):
		self.folderName = file.browseFiles()
		self.ui.lblFilename.setText(self.folderName)

		images = file.addAllPngFiles(self.folderName)

		for item in images:
			self.ui.fileList.addItem(item)

	def sendModels(self):
		self.ui.txtOutput.append(f"Sending model: {self.model}")
		self.model = str(self.ui.modelList.currentText())
		reply = server.sendModel(self.model, self.remote)

	def getPrediction(self):
		connected = self.connect()

		if connected:
			self.ui.txtOutput.append(f"Sending image file: {self.imageFile}")
			server.sendImage(self.imageFile, self.remote)

			self.sendModels()

			self.ui.txtOutput.append("Waiting for prediction")
			pred = server.receivePred(self.remote)

			self.ui.txtOutput.append(f"got prediction {pred}")
			if pred == "P":
				pred = "Pneumonia"
			else:
				pred = "Normal"

			self.ui.lblPredict.setText(pred)
