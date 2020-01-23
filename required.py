from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import pickle
import os
import sys
import random

"""Class with required methods for game."""
class required_methods(object):
    
    """Reading the game-resources from file
    and converting to PyQt-friendly format."""
    def resources_reading(self):
        try:
            if os.path.isfile("data.bin") == False: # If file not exists.
                with open("error_log.txt", "w") as log_file:
                    log_file.write("File 'data.bin' with resources not found :(")
                sys.exit()

            with open("data.bin", "rb") as file: # Reading the file.
                self.resources = pickle.loads(file.read())
            
            # Converting the resources
            self.mainMenu_gif_bytesArray = QByteArray(self.resources["mainMenu"])
            self.mainMenu_gif = QBuffer(self.mainMenu_gif_bytesArray)
            self.mainMenu_gif.open(QIODevice.ReadOnly)

            self.logo_pixmap = QPixmap()
            self.logo_pixmap.loadFromData(self.resources["logo"])

            self.blackScreen_pixmap = QPixmap()
            self.blackScreen_pixmap.loadFromData(self.resources["blackScreen"])

            self.ememy_1_pixmap = QPixmap()
            self.ememy_1_pixmap.loadFromData(self.resources["enemies"][0])

            self.ememy_2_pixmap = QPixmap()
            self.ememy_2_pixmap.loadFromData(self.resources["enemies"][1])

            self.ememy_3_pixmap = QPixmap()
            self.ememy_3_pixmap.loadFromData(self.resources["enemies"][2])

            self.pause_background_pixmap = QPixmap()
            self.pause_background_pixmap.loadFromData(self.resources["pause_background"])

            self.random_gameplayBackground_pixmap = QPixmap()
            self.random_gameplayBackground_pixmap.loadFromData(self.resources["backgrounds"][random.randint(0,16)])        

            self.pause_title_pixmap = QPixmap()
            self.pause_title_pixmap.loadFromData(self.resources["pause_title"])

            fontDB = QFontDatabase() # Font-database for displying the font in game.
            fontDB.addApplicationFontFromData(self.resources["font"])
            self.font = fontDB.applicationFontFamilies(0)[0]
        except Exception as error:
            with open("error_log.txt", "w") as log_file: # If an error occurred then game will be closed.
                log_file.write("File 'data.bin' is damaged :(" + "\n\n" + "Details:" + "\n" + str(error))
            sys.exit()

    """Reading the file with saves."""
    def saves_reading(self):
        if not os.path.isfile("saves.sav"):
            with open("saves.sav", "wb") as file:
                pickle.dump([], file)
        
        try:
            with open("saves.sav", "rb") as file: # If file not exists.
                self.saves = pickle.loads(file.read())
        except:
            with open("error_log.txt", "w") as log_file:
                log_file.write("File with saves is damaged :(")
            sys.exit()

    """Applying the PyQt-pallete for
    correct displaying the graphics."""
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
