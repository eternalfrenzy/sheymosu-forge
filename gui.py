
from required import *

"""Class for creating the GUI"""
class gui(QWidget):
    
    """Initialization the GUI"""
    def get_gui(self):
        self.setMinimumSize(QSize(1280,720))
        self.setMaximumSize(QSize(1280,720))

        self.setWindowTitle("SheymOsu Alpha")
        self.setWindowIcon(QIcon("icon.ico"))

        self.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid yellow}")

        self.resources_reading()

        
        # Main-menu screen
        
        self.mainMenuScreen = QLabel(self)
        self.mainMenuScreen_gif = QMovie(self.mainMenu_gif, b'GIF')
        self.mainMenuScreen.setMovie(self.mainMenuScreen_gif)
        self.mainMenuScreen_gif.start()

        self.mainMenu_background = QLabel(self)
        self.mainMenu_background.setPixmap(self.blackScreen_pixmap)
        self.mainMenu_background.resize(250, 720)

        self.mainMenu_logo = QLabel(self)
        self.mainMenu_logo.setPixmap(self.logo_pixmap)
        self.mainMenu_logo.move(0, 125)

        self.gameVersion_lbl = QLabel("Alpha 0.3.1", self)
        self.gameVersion_lbl.move(14, 685)
        self.gameVersion_lbl.setFont(QFont(self.font, 20))

        self.newGame_btn = QPushButton("Новая игра",self)
        self.newGame_btn.resize(220, 40)
        self.newGame_btn.move(14, 400)
        self.newGame_btn.setFont(QFont(self.font, 25))
        self.newGame_btn.setFocusPolicy(Qt.NoFocus)

        self.continueGame_btn = QPushButton("Продолжить",self)
        self.continueGame_btn.resize(220, 40)
        self.continueGame_btn.move(14, 350)
        self.continueGame_btn.setFont(QFont(self.font, 25))
        self.continueGame_btn.setFocusPolicy(Qt.NoFocus)

        self.settings_btn = QPushButton("Настройки",self)
        self.settings_btn.resize(220, 40)
        self.settings_btn.move(14, 450)
        self.settings_btn.setFont(QFont(self.font, 25))
        self.settings_btn.setFocusPolicy(Qt.NoFocus)

        self.exit_btn = QPushButton("Выйти",self)
        self.exit_btn.resize(220, 40)
        self.exit_btn.move(14, 500)
        self.exit_btn.setFont(QFont(self.font, 25))
        self.exit_btn.setFocusPolicy(Qt.NoFocus)

        # Menu for creating new save
        
        self.saveName_lbl = QLabel("Название сохранения",self)
        self.saveName_lbl.setFont(QFont(self.font, 15))
        self.saveName_lbl.move(41, 350)

        self.saveName_edit = QLineEdit(self)
        self.saveName_edit.resize(190, 25)
        self.saveName_edit.move(30, 370)
        self.saveName_edit.setFont(QFont(self.font, 14))
        self.saveName_edit.setMaxLength(20)
        self.saveName_edit.setStyleSheet("border: 1px solid black")
        self.saveName_edit.setContextMenuPolicy(Qt.NoContextMenu)

        self.gameModeChange_btn = QPushButton("Бесконечный режим",self)
        self.gameModeChange_btn.resize(170, 25)
        self.gameModeChange_btn.move(40, 400)
        self.gameModeChange_btn.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid red}")
        self.gameModeChange_btn.setFont(QFont(self.font, 15))
        self.gameModeChange_btn.setFocusPolicy(Qt.NoFocus)

        self.difficulty_lbl = QLabel("Сложность игры",self)
        self.difficulty_lbl.setFont(QFont(self.font, 15))
        self.difficulty_lbl.move(60, 438)

        self.difficultyChange_btn = QPushButton("Сложность",self)
        self.difficultyChange_btn.resize(135, 25)
        self.difficultyChange_btn.move(56, 460)
        self.difficultyChange_btn.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid red}")
        self.difficultyChange_btn.setFont(QFont(self.font, 15))
        self.difficultyChange_btn.setFocusPolicy(Qt.NoFocus)

        self.newSave_btn = QPushButton("Создать",self)
        self.newSave_btn.resize(220, 40)
        self.newSave_btn.move(14, 500)
        self.newSave_btn.setFont(QFont(self.font, 25))
        self.newSave_btn.setFocusPolicy(Qt.NoFocus)

        # Continue-game-menu
        
        self.savesList_edit = QListWidget(self)
        self.savesList_edit.resize(220, 130)
        self.savesList_edit.move(14, 350)
        self.savesList_edit.setFont(QFont(self.font, 15))

        self.continueSave_btn = QPushButton("Запустить",self)
        self.continueSave_btn.resize(220, 25)
        self.continueSave_btn.move(14, 485)
        self.continueSave_btn.setFont(QFont(self.font, 13))
        self.continueSave_btn.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid red}")
        self.continueSave_btn.setFocusPolicy(Qt.NoFocus)

        self.changeSave_btn = QPushButton("Изменить",self)
        self.changeSave_btn.resize(109, 25)
        self.changeSave_btn.move(14, 512)
        self.changeSave_btn.setFont(QFont(self.font, 13))
        self.changeSave_btn.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid red}")
        self.changeSave_btn.setFocusPolicy(Qt.NoFocus)

        self.deleteSave_btn = QPushButton("Удалить",self)
        self.deleteSave_btn.resize(109, 25)
        self.deleteSave_btn.move(126, 512)
        self.deleteSave_btn.setFont(QFont(self.font, 13))
        self.deleteSave_btn.setStyleSheet("QPushButton:hover:!pressed{border: 1px solid red}")
        self.deleteSave_btn.setFocusPolicy(Qt.NoFocus)

        # Menu for changing the save
        
        self.saveUpdatedSave_btn = QPushButton("Изменить", self)
        self.saveUpdatedSave_btn.resize(220, 40)
        self.saveUpdatedSave_btn.move(14, 450)
        self.saveUpdatedSave_btn.setFont(QFont(self.font, 25))
        self.saveUpdatedSave_btn.setFocusPolicy(Qt.NoFocus)
        self.saveUpdatedSave_btn.hide()

        self.cancel_btn = QPushButton("Отмена", self)
        self.cancel_btn.resize(220, 40)
        self.cancel_btn.move(14, 500)
        self.cancel_btn.setFont(QFont(self.font, 25))
        self.cancel_btn.setFocusPolicy(Qt.NoFocus)
        self.cancel_btn.hide()

        # Settings-menu
        
        self.settings_lbl = QLabel("Здесь пока что\nничего нет :(", self)
        self.settings_lbl.setFont(QFont(self.font, 25))
        self.settings_lbl.move(30, 400)

        # Button for return the previous menu
        self.return_btn = QPushButton("Назад",self)
        self.return_btn.resize(220, 40)
        self.return_btn.move(14, 550)
        self.return_btn.setFont(QFont(self.font, 25))
        self.return_btn.setFocusPolicy(Qt.NoFocus)

        
        # Gameplay screen
        
        self.gameplay_background = QLabel(self)
        self.gameplay_background.setPixmap(self.random_gameplayBackground_pixmap)
        self.gameplay_background.move(0, -50)

        self.gameplayInfo_background = QLabel(self)
        self.gameplayInfo_background.setPixmap(self.blackScreen_pixmap)
        self.gameplayInfo_background.resize(1280, 50)
        self.gameplayInfo_background.move(0, 670)

        self.score_lbl = QLabel(self)
        self.score_lbl.resize(1255, 30)
        self.score_lbl.move(14, 682)
        self.score_lbl.setFont(QFont(self.font, 33))

        # Gameplay enemies
        
        self.enemy_1 = QPushButton(self)
        self.enemy_1.resize(50, 50)
        self.enemy_1.setIcon(QIcon(self.ememy_1_pixmap))
        self.enemy_1.setIconSize(QSize(50, 50))
        self.enemy_1.setStyleSheet("border: 0px")
        self.enemy_1.move(random.randint(20, 1200), random.randint(20, 620))

        self.enemy_2 = QPushButton(self)
        self.enemy_2.resize(50, 50)
        self.enemy_2.setIcon(QIcon(self.ememy_2_pixmap))
        self.enemy_2.setIconSize(QSize(50, 50))
        self.enemy_2.setStyleSheet("border: 0px")
        self.enemy_2.move(random.randint(20, 1200), random.randint(20, 620))

        self.enemy_3 = QPushButton(self)
        self.enemy_3.resize(32, 90)
        self.enemy_3.setIcon(QIcon(self.ememy_3_pixmap))
        self.enemy_3.setIconSize(QSize(32, 90))
        self.enemy_3.setStyleSheet("border: 0px")
        self.enemy_3.move(random.randint(20, 1200), random.randint(20, 550))
        
        # Pause-menu screen
        
        self.pause_background = QLabel(self)
        self.pause_background.setPixmap(self.pause_background_pixmap)
        self.pause_background.resize(1280, 720)

        self.pauseMenu_background = QLabel(self)
        self.pauseMenu_background.setPixmap(self.blackScreen_pixmap)
        self.pauseMenu_background.resize(250, 720)
        self.pauseMenu_background.move(1030, 0)

        self.pauseMenu_title = QLabel(self)
        self.pauseMenu_title.setPixmap(self.pause_title_pixmap)
        self.pauseMenu_title.move(1030, 150)

        self.returnToGameplay_btn = QPushButton("Продолжить", self)
        self.returnToGameplay_btn.resize(220, 40)
        self.returnToGameplay_btn.move(1046, 350)
        self.returnToGameplay_btn.setFont(QFont(self.font, 25))
        self.returnToGameplay_btn.setFocusPolicy(Qt.NoFocus)

        self.statistics_btn = QPushButton("Статистика", self)
        self.statistics_btn.resize(220, 40)
        self.statistics_btn.move(1046, 400)
        self.statistics_btn.setFont(QFont(self.font, 25))
        self.statistics_btn.setFocusPolicy(Qt.NoFocus)
        self.statistics_btn.setEnabled(False)

        self.exitToMainMenu_btn = QPushButton("Выйти", self)
        self.exitToMainMenu_btn.resize(220, 40)
        self.exitToMainMenu_btn.move(1046, 450)
        self.exitToMainMenu_btn.setFont(QFont(self.font, 25))
        self.exitToMainMenu_btn.setFocusPolicy(Qt.NoFocus)
