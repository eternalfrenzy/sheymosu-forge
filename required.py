from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import pickle
import os
import sys
import random

"""Class with required methods for game"""
class required_methods():

    """Reading the game-resources from file"""
    def extract_resources(self):
        try:
            if os.path.isfile("data.bin") == False: # If file not exists
                with open("LAST_CRASH.txt", "w") as log_file:
                    log_file.write("File 'data.bin' with resources of game not found :(")
                sys.exit()

            with open("data.bin", "rb") as file: # Reading the file
                self.resources = pickle.loads(file.read())

            # Converting the gif data to PyQt-friendly format
            self.mainMenuScreen_background_gif_bytesArray = QByteArray(self.resources["mainMenu"])
            self.mainMenuScreen_background_gif_data = QBuffer(self.mainMenuScreen_background_gif_bytesArray)
            self.mainMenuScreen_background_gif_data.open(QIODevice.ReadOnly)

            fontDB = QFontDatabase() # Font-database for displying the font in game
            fontDB.addApplicationFontFromData(self.resources["font"])
            self.font = fontDB.applicationFontFamilies(0)[0]
        
        except Exception as error: # If an error occurred then game will be closed
            with open("LAST_CRASH.txt", "w") as log_file:
                log_file.write("File 'data.bin' is damaged :(" + "\n\n" + "Exception details:" + "\n" + str(error))
            sys.exit()

    def load_img(self, data, other_data = None):
        img = QPixmap()

        try:
            if other_data == None:
                img.loadFromData(self.resources[data])
            else:
                img.loadFromData(self.resources[data][other_data])
        
        except Exception as error:
            with open("LAST_CRASH.txt", "w") as log_file:
                log_file.write("File 'data.bin' is damaged :(" + "\n\n" + "Exception details:" + "\n" + str(error))
            sys.exit()
        
        return img

    """Reading the file with saves"""
    def read_saves(self):
        if not os.path.isfile("saves.sav"):
            with open("saves.sav", "wb") as file:
                pickle.dump([], file)
        
        try:
            with open("saves.sav", "rb") as file: # If file not exists
                self.saves = pickle.loads(file.read())
                
        except Exception as error:
            with open("LAST_CRASH.txt", "w") as log_file:
                log_file.write("File 'saves.sav' is damaged :(" + "\n\n" + "Exception details:" + "\n" + str(error))
            sys.exit()

    """PyQt-pallete applying for
    correct displaying the graphics"""
    def apply_pallete(self, app):
        app.setStyle("Fusion")
        palette=QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(19, 19, 19))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, Qt.black)
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, Qt.red)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)
