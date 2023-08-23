#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 07:05:06 2021

@author: 	Anthony Donnelly
@contributor:
"""
from PySide2.QtWidgets import QApplication, QFileDialog
import glob, os

def browseFiles():
    openFile = QFileDialog.getExistingDirectory(None, 'Select a folder:',
                                '/home/', QFileDialog.ShowDirsOnly)

    return openFile
        #fileInput.setText(openFile)


def addAllPngFiles(folderName):
    fileList = list()
    for file in os.listdir(folderName):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            fileList.append(file)

    return fileList

def saveFile():
    saveFile , check = QFileDialog.getSaveFileName(None, "Save file as...",
                                               "", "All Files (*)")

    if check:
        return saveFile
