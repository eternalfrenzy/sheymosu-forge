
from required import *

"""Class for gui-navigation from main-class"""
class gui_navigation():

    # Main-menu Screen methods:

    """Open Main-menu Screen"""
    def open_mainMenuScreen(self):
        self.show_mainMenu()

        self.mainMenu_background.show()
        self.mainMenuScreen.show()
        self.mainMenu_logo.show()
        self.gameVersion_lbl.show()

        self.mainMenu_status = True

    """Close Main-menu Screen"""
    def close_mainMenuScreen(self):
        self.mainMenu_background.hide()
        self.mainMenuScreen.hide()
        self.mainMenu_logo.hide()
        self.gameVersion_lbl.hide()

        self.hide_newGameMenu()
        self.hide_continueGameMenu()

        self.mainMenu_status = False

    """Show main menu"""
    def show_mainMenu(self):
        self.hide_newGameMenu()
        self.hide_continueGameMenu()
        self.hide_settingsMenu()
        
        self.newGame_btn.show()
        self.continueGame_btn.show()
        self.settings_btn.show()
        self.exit_btn.show()
    
    """Hide main menu"""
    def hide_mainMenu(self):
        self.newGame_btn.hide()
        self.continueGame_btn.hide()
        self.settings_btn.hide()
        self.exit_btn.hide()
    
    """Show menu for creating the new save"""
    def show_newGameMenu(self):
        self.hide_mainMenu()

        self.saveName_lbl.show()
        self.saveName_edit.show()
        self.gameModeChange_btn.show()
        self.difficulty_lbl.show()
        self.difficultyChange_btn.show()
        self.newSave_btn.show()
        
        self.return_btn.show()

        self.saveName_edit.setText("new save")
        self.difficultyChange_btn.setText("Нормально")
        
        self.gameMode = 1
        self.difficulty = 2

    """Hide menu for creating the new save"""
    def hide_newGameMenu(self):
        self.saveName_lbl.hide()
        self.saveName_edit.hide()
        self.gameModeChange_btn.hide()
        self.difficulty_lbl.hide()
        self.difficultyChange_btn.hide()
        self.newSave_btn.hide()
        
        self.return_btn.hide()

    """Show menu for continue saves"""
    def show_continueGameMenu(self):
        self.hide_mainMenu()

        self.savesList_edit.show()
        self.continueSave_btn.show()
        self.changeSave_btn.show()
        self.deleteSave_btn.show()
        
        self.return_btn.show()

    """Hide menu for continue saves"""
    def hide_continueGameMenu(self):
        self.savesList_edit.hide()
        self.continueSave_btn.hide()
        self.changeSave_btn.hide()
        self.deleteSave_btn.hide()
        
        self.return_btn.hide()

    """Show menu for changing the save"""
    def show_renameSaveMenu(self):
        self.savesList_edit.hide()
        self.continueSave_btn.hide()
        self.changeSave_btn.hide()
        self.deleteSave_btn.hide()
        self.return_btn.hide()

        self.saveName_lbl.show()
        self.saveName_edit.show()
        self.saveUpdatedSave_btn.show()
        self.cancel_btn.show()

    """Hide menu for changing the save"""
    def hide_renameSaveMenu(self):
        self.saveName_lbl.hide()
        self.saveName_edit.hide()
        self.saveUpdatedSave_btn.hide()
        self.cancel_btn.hide()

        self.savesList_edit.show()
        self.continueSave_btn.show()
        self.changeSave_btn.show()
        self.deleteSave_btn.show()
        self.return_btn.show()

    """Show settings-menu"""
    def show_settingsMenu(self):
        self.hide_mainMenu()

        self.settings_lbl.show()
        
        self.return_btn.show()

    """Hide settings-menu"""
    def hide_settingsMenu(self):
        self.settings_lbl.hide()
        
        self.return_btn.hide()

    # Gameplay Screen methods:

    """Open Gameplay screen"""
    def open_gameplayScreen(self):
        self.show_gameplayScreen()

        self.enemy_1.show()
        self.enemy_2.show()
        self.enemy_3.show()

        self.enemyTimer_1.start()
        self.enemyTimer_2.start()
        self.enemyTimer_3.start()
        self.backgroundTimer.start()
        self.gameplayTimeCounter.start()

    """Close Gameplay screen"""
    def close_gameplayScreen(self):
        self.hide_gameplayScreen()

        self.enemy_1.hide()
        self.enemy_2.hide()
        self.enemy_3.hide()

        self.enemyTimer_1.stop()
        self.enemyTimer_2.stop()
        self.enemyTimer_3.stop()
        self.backgroundTimer.stop()
        self.gameplayTimeCounter.stop()

    """Show Gameplay GUI only"""
    def show_gameplayScreen(self):
        self.gameplay_background.show()
        self.gameplayInfo_background.show()
        self.score_lbl.show()

    """Hide Gameplay GUI only"""
    def hide_gameplayScreen(self):
        self.gameplay_background.hide()
        self.gameplayInfo_background.hide()
        self.score_lbl.hide()

    # Pause Screen methods:

    """Open Pause Screen"""
    def open_pauseScreen(self):
        self.pause_background.show()
        self.pauseMenu_background.show()

        self.show_pauseMenu()
        
        self.pause_status = True

    """Close Pause Screen"""
    def close_pauseScreen(self):
        self.pause_background.hide()
        self.pauseMenu_background.hide()

        self.hide_pauseMenu()

        self.pause_status = False

    """Show Pause-menu"""
    def show_pauseMenu(self):
        self.pauseMenu_title.show()
        
        self.returnToGameplay_btn.show()
        self.statistics_btn.show()
        self.exitToMainMenu_btn.show()

    """Close Pause-menu"""
    def hide_pauseMenu(self):
        self.pauseMenu_title.hide()
        
        self.returnToGameplay_btn.hide()
        self.statistics_btn.hide()
        self.exitToMainMenu_btn.hide()
