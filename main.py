
__author__  = "RinkLinky"
__version__ = "Alpha 0.3.1"

from required import *
from gui import gui
from gameplay_events import gameplay_events
from gui_navigation import gui_navigation
from statistics import statistics

class App(gui, gui_navigation, required_methods, gameplay_events, statistics):
    """Initialization the game"""
    def __init__(self):
        super().__init__()
        self.get_gui()
        self.apply_pallete(app)
        self.create_eventTimers()

        self.show()        
        self.open_mainMenuScreen()
        self.close_pauseScreen()
        self.close_gameplayScreen()

        self.saves_reading()
        self.saves_filling()

        # Creating the signals
        self.newGame_btn.clicked.connect(self.show_newGameMenu)
        self.continueGame_btn.clicked.connect(self.show_continueGameMenu)
        self.settings_btn.clicked.connect(self.show_settingsMenu)
        self.exit_btn.clicked.connect(sys.exit)
        self.return_btn.clicked.connect(self.show_mainMenu)

        self.newSave_btn.clicked.connect(self.newGame)
        self.gameModeChange_btn.clicked.connect(self.gameMode_selection)
        self.difficultyChange_btn.clicked.connect(self.difficulty_selection)

        self.savesList_edit.itemDoubleClicked.connect(self.continueSave)
        self.continueSave_btn.clicked.connect(self.continueSave)
        self.changeSave_btn.clicked.connect(self.changeSave)
        self.deleteSave_btn.clicked.connect(self.deleteSave)

        self.saveUpdatedSave_btn.clicked.connect(self.saveUpdatedSave)
        self.cancel_btn.clicked.connect(self.hide_renameSaveMenu)

        self.returnToGameplay_btn.clicked.connect(self.returnToGameplay)
        self.exitToMainMenu_btn.clicked.connect(self.finishGame)


    """Creating the new save"""
    def newGame(self):
        saveName = self.saveName_edit.text().strip() # Clearning the spaces on sides
        if saveName == "":
            saveName = "new save"

        newSave = { # Creating new save
            "name": saveName,
            "gamemode": self.gameMode,
            "difficulty": self.difficulty,
            "score": 0,
            
            "statistics": {
                "time": 0,
                "background_clicks": 0,
                "enemies1_clicks": 0,
                "enemies2_clicks": 0,
                "enemies3_clicks": 0,
            }
        }

        self.saves.insert(0, newSave) # Inserting the save to 0 index in list of saves

        with open("saves.sav", "wb") as file: # Saving the new list with saves
            pickle.dump(self.saves, file)

        self.saves_filling() # Filling the QListWidget with saves

        self.saveName = saveName
        self.score = 0

        self.time = 0
        self.background_clicks = 0
        self.enemies1_clicks = 0
        self.enemies2_clicks = 0
        self.enemies3_clicks = 0
        
        self.apply_difficulty(self.difficulty)
        self.startGame()

    """Continuation the save"""
    def continueSave(self):
        currentSaveId = self.savesList_edit.currentRow() # Getting the selected save
        if currentSaveId != -1:
            save = self.saves[self.savesList_edit.currentRow()]

            del self.saves[currentSaveId]
            self.saves.insert(0, save)

            with open("saves.sav", "wb") as file:
                pickle.dump(self.saves, file)

            # Values assignment of save
            self.saveName = save["name"]
            self.gameMode = save["gamemode"]
            self.difficulty = save["difficulty"]
            self.score = save["score"]
            
            self.time = save["statistics"]["time"]
            self.background_clicks = save["statistics"]["background_clicks"]
            self.enemies1_clicks = save["statistics"]["enemies1_clicks"]
            self.enemies2_clicks = save["statistics"]["enemies2_clicks"]
            self.enemies3_clicks = save["statistics"]["enemies3_clicks"]

            self.apply_difficulty(self.difficulty)
            self.startGame()

    """Starting the gameplay"""
    def startGame(self):
        self.close_mainMenuScreen()

        self.score_lbl.setText(str("Счёт: " + str(self.score)))
        self.open_gameplayScreen()
    
    """Finishing the gameplay"""
    def finishGame(self):
        self.close_pauseScreen()

        # Updating time for time-out the enemies to 0
        self.enemyTime_1 = 0
        self.enemyTime_2 = 0
        self.enemyTime_3 = 0
        self.backgroundTime = 0

        # Movement of enemies
        self.enemy_1.move(random.randint(20, 1200), random.randint(20, 550))
        self.enemy_2.move(random.randint(20, 1200), random.randint(20, 550))
        self.enemy_3.move(random.randint(20, 1200), random.randint(20, 550))

        updatedSave = { # Updating the save
            "name": self.saveName,
            "gamemode": self.gameMode,
            "difficulty": self.difficulty,
            "score": self.score,

            "statistics": {
                "time": self.time,
                "background_clicks": self.background_clicks,
                "enemies1_clicks": self.enemies1_clicks,
                "enemies2_clicks": self.enemies2_clicks,
                "enemies3_clicks": self.enemies3_clicks,
            }
        }

        self.saves[0] = updatedSave

        with open("saves.sav", "wb") as file:
            pickle.dump(self.saves, file)
        
        self.saves_filling()
        self.open_mainMenuScreen()

    """Changing the 
    selected save by player"""
    def changeSave(self):
        self.selectedSave_id = self.savesList_edit.currentRow()
        if self.selectedSave_id != -1: # Index (-1) means that save not selected by player
            self.saveName_edit.setText(self.saves[self.selectedSave_id]["name"])
            self.show_renameSaveMenu()

    """Saving of changes
    for selected save by player"""
    def saveUpdatedSave(self):
        if self.saveName_edit.text().strip() == "": # If new name not empty after clearning the spaces on sides - save will be updated.
            self.saveName_edit.clear()
        else:
            self.hide_renameSaveMenu()

            if self.saveName_edit.text().strip() != self.saves[self.selectedSave_id]["name"]: # Updating the save in list
                self.saves[self.selectedSave_id]["name"] = self.saveName_edit.text().strip()
                with open("saves.sav", "wb") as file:
                    pickle.dump(self.saves, file)
            
                self.saves_filling()

    """Deleting the 
    selected save by player"""
    def deleteSave(self):
        selectedSave_id = self.savesList_edit.currentRow()
        if selectedSave_id != -1:
            del self.saves[selectedSave_id]
            with open("saves.sav", "wb") as file:
                pickle.dump(self.saves, file)

            self.saves_filling()


    """Open/Close pause screen"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: # If pressed button is ESC - opens the pause screen,
            if self.mainMenu_status == False: # And player not in main-menu,
                if self.pause_status == False: # And pause screen already not opened. If pause opened - pause will be closed.
                    self.close_gameplayScreen()
                    self.open_pauseScreen()
                else:
                    self.close_pauseScreen()
                    self.open_gameplayScreen()

    """Return to gameplay"""
    def returnToGameplay(self): # Return to gameplay from pause menu
        self.close_pauseScreen()
        self.open_gameplayScreen()

    """Selection of gamemode for save"""
    def gameMode_selection(self):
        pass

    """Selection of difficulty for save"""
    def difficulty_selection(self): # Changing difficulty text on button
        if self.difficulty == 1:
            self.difficulty = 2
            self.difficultyChange_btn.setText("Нормально")

        elif self.difficulty == 2:
            self.difficulty = 3
            self.difficultyChange_btn.setText("Сложно")
            
        elif self.difficulty == 3:
            self.difficulty = 1
            self.difficultyChange_btn.setText("Легко")

    
    """Filling the QListWidget with saves"""
    def saves_filling(self):
        self.savesList_edit.clear()

        for save in self.saves: # Text formating for displying information of save in QListWidget
            if save["gamemode"] == 1:
                gamemode = "Бесконечный режим"
            
            if save["difficulty"] == 1:
                difficulty = "Легко"
            elif save["difficulty"] == 2:
                difficulty = "Нормально"
            elif save["difficulty"] == 3:
                difficulty = "Сложно"

            newItem = save["name"] + "\n" + difficulty + " / " + "Счёт: " + str(save["score"])

            self.savesList_edit.addItem(newItem)

        if self.savesList_edit.count() == 0:
            self.continueGame_btn.setEnabled(False)
        else:
            self.continueGame_btn.setEnabled(True)

    """Applying gameplay changes
    for current difficulty"""
    def apply_difficulty(self, difficulty):
        if difficulty == 1:
            self.enemyTimeout_1 = 7
            self.enemyTimeout_2 = 4
            self.enemyTimeout_3 = 2

            self.enemyScore_1 = 2
            self.enemyScore_2 = 5
            self.enemyScore_3 = 7

        elif difficulty == 2:
            self.enemyTimeout_1 = 4
            self.enemyTimeout_2 = 2.5
            self.enemyTimeout_3 = 1

            self.enemyScore_1 = 5
            self.enemyScore_2 = 10
            self.enemyScore_3 = 15
            
        elif difficulty == 3:
            self.enemyTimeout_1 = 2
            self.enemyTimeout_2 = 1
            self.enemyTimeout_3 = 0.7

            self.enemyScore_1 = 8
            self.enemyScore_2 = 18
            self.enemyScore_3 = 25

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=App()
    app.installEventFilter(ex)
    sys.exit(app.exec_())
