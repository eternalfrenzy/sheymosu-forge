import random

from PyQt5 import QtWidgets, QtGui, QtCore

def load_pixmap(data):
    """Convert image data to PyQt-friendly format"""
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(data)

    return pixmap

class Gui(QtWidgets.QWidget):
    """Class for game GUI and PyQt events"""

    def __init__(self, resources):
        super().__init__()

        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))

        self.setWindowTitle('SheymOsu')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        # the buttons will have CSS-styled yellow borders when hovered over
        self.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid yellow}')

        FONTS_DB = QtGui.QFontDatabase() # font-database for fonts from game-resources
        FONTS_DB.addApplicationFontFromData(resources['FONTS']['DETERMINATION_2'])
        FONT1 = FONTS_DB.applicationFontFamilies(0)[0] # "determination 2" font

        if random.randint(0, 9999) == 666: # easter egg :D
            GIF1_DATA = resources['BACKGROUNDS']['CLOSE_EVENT']
        else:
            GIF1_DATA = resources['BACKGROUNDS']['START_SCREEN']

        # converting the gif data to PyQt-friendly format
        self.GIF1_DATA_BYTEARRAY = QtCore.QByteArray(GIF1_DATA)
        self.GIF1_DATA_BUFFER = QtCore.QBuffer(self.GIF1_DATA_BYTEARRAY)
        self.GIF1_DATA_BUFFER.open(QtCore.QIODevice.ReadOnly)

        # START-SCREEN #

        self.startScreen_background = QtWidgets.QLabel(self)
        self.startScreen_background_gif = QtGui.QMovie(self.GIF1_DATA_BUFFER, b'GIF')
        self.startScreen_background.setMovie(self.startScreen_background_gif)
        self.startScreen_background_gif.start()

        self.startScreen_menu_background = QtWidgets.QLabel(self)
        self.startScreen_menu_background.setStyleSheet('background-color: black')
        self.startScreen_menu_background.resize(250, 720)

        self.startScreen_menu_logo = QtWidgets.QLabel(self)
        self.startScreen_menu_logo.setPixmap(load_pixmap(resources['LOGO']))
        self.startScreen_menu_logo.move(0, 125)

        self.gameVersion_lbl = QtWidgets.QLabel(self)
        self.gameVersion_lbl.resize(225, 20)
        self.gameVersion_lbl.move(14, 685)
        self.gameVersion_lbl.setFont(QtGui.QFont(FONT1, 20))

        self.newGame_btn = QtWidgets.QPushButton(self)
        self.newGame_btn.resize(220, 40)
        self.newGame_btn.move(14, 400)
        self.newGame_btn.setFont(QtGui.QFont(FONT1, 25))
        self.newGame_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.continueGame_btn = QtWidgets.QPushButton(self)
        self.continueGame_btn.resize(220, 40)
        self.continueGame_btn.move(14, 350)
        self.continueGame_btn.setFont(QtGui.QFont(FONT1, 25))
        self.continueGame_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.settings_btn = QtWidgets.QPushButton(self)
        self.settings_btn.resize(220, 40)
        self.settings_btn.move(14, 450)
        self.settings_btn.setFont(QtGui.QFont(FONT1, 25))
        self.settings_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.quitGame_btn = QtWidgets.QPushButton(self)
        self.quitGame_btn.resize(220, 40)
        self.quitGame_btn.move(14, 500)
        self.quitGame_btn.setFont(QtGui.QFont(FONT1, 25))
        self.quitGame_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.aboutGame_btn = QtWidgets.QPushButton(self)
        self.aboutGame_btn.resize(220, 100)
        self.aboutGame_btn.move(14, 145)
        self.aboutGame_btn.setFont(QtGui.QFont(FONT1, 25))
        self.aboutGame_btn.setStyleSheet('border: 0px')
        self.aboutGame_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # BUTTON FOR BACK START-SCREEN MENU #
        self.back_startScreen_menu_btn = QtWidgets.QPushButton(self)
        self.back_startScreen_menu_btn.resize(220, 40)
        self.back_startScreen_menu_btn.move(14, 550)
        self.back_startScreen_menu_btn.setFont(QtGui.QFont(FONT1, 25))
        self.back_startScreen_menu_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # NEW-GAME MENU #

        self.saveName_lbl = QtWidgets.QLabel(self)
        self.saveName_lbl.resize(190, 15)
        self.saveName_lbl.move(30, 350)
        self.saveName_lbl.setFont(QtGui.QFont(FONT1, 15))
        self.saveName_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.saveName_edit = QtWidgets.QLineEdit(self)
        self.saveName_edit.resize(190, 25)
        self.saveName_edit.move(30, 370)
        self.saveName_edit.setMaxLength(32)
        self.saveName_edit.setFont(QtGui.QFont(FONT1, 14))
        self.saveName_edit.setStyleSheet('border: 1px solid black')
        self.saveName_edit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.change_gamemode_btn = QtWidgets.QPushButton(self)
        self.change_gamemode_btn.resize(170, 25)
        self.change_gamemode_btn.move(40, 400)
        self.change_gamemode_btn.setFont(QtGui.QFont(FONT1, 15))
        self.change_gamemode_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid red}')
        self.change_gamemode_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.difficulty_lbl = QtWidgets.QLabel(self)
        self.difficulty_lbl.resize(190, 18)
        self.difficulty_lbl.move(30, 438)
        self.difficulty_lbl.setFont(QtGui.QFont(FONT1, 15))
        self.difficulty_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.change_difficulty_btn = QtWidgets.QPushButton(self)
        self.change_difficulty_btn.resize(135, 25)
        self.change_difficulty_btn.move(56, 460)
        self.change_difficulty_btn.setFont(QtGui.QFont(FONT1, 15))
        self.change_difficulty_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid red}')
        self.change_difficulty_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.create_save_btn = QtWidgets.QPushButton(self)
        self.create_save_btn.resize(220, 40)
        self.create_save_btn.move(14, 500)
        self.create_save_btn.setFont(QtGui.QFont(FONT1, 25))
        self.create_save_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # CONTINUE-GAME MENU #

        self.savesList_edit = QtWidgets.QListWidget(self)
        self.savesList_edit.resize(220, 130)
        self.savesList_edit.move(14, 350)
        self.savesList_edit.setFont(QtGui.QFont(FONT1, 15))
        self.savesList_edit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.continue_save_btn = QtWidgets.QPushButton(self)
        self.continue_save_btn.resize(220, 25)
        self.continue_save_btn.move(14, 485)
        self.continue_save_btn.setFont(QtGui.QFont(FONT1, 13))
        self.continue_save_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid red}')
        self.continue_save_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.change_save_btn = QtWidgets.QPushButton(self)
        self.change_save_btn.resize(109, 25)
        self.change_save_btn.move(14, 512)
        self.change_save_btn.setFont(QtGui.QFont(FONT1, 13))
        self.change_save_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid red}')
        self.change_save_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.delete_save_btn = QtWidgets.QPushButton(self)
        self.delete_save_btn.resize(109, 25)
        self.delete_save_btn.move(126, 512)
        self.delete_save_btn.setFont(QtGui.QFont(FONT1, 13))
        self.delete_save_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid red}')
        self.delete_save_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # CHANGE-SAVE MENU #

        self.save_changedSave_btn = QtWidgets.QPushButton(self)
        self.save_changedSave_btn.resize(220, 40)
        self.save_changedSave_btn.move(14, 450)
        self.save_changedSave_btn.setFont(QtGui.QFont(FONT1, 25))
        self.save_changedSave_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.save_changedSave_btn.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.cancel_btn = QtWidgets.QPushButton(self)
        self.cancel_btn.resize(220, 40)
        self.cancel_btn.move(14, 500)
        self.cancel_btn.setFont(QtGui.QFont(FONT1, 25))
        self.cancel_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # DELETE-SAVE MENU #

        self.deleteSave_warning_lbl = QtWidgets.QLabel(self)
        self.deleteSave_warning_lbl.resize(220, 80)
        self.deleteSave_warning_lbl.move(14, 350)
        self.deleteSave_warning_lbl.setFont(QtGui.QFont(FONT1, 15))
        self.deleteSave_warning_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.confirm_deleteSave_btn = QtWidgets.QPushButton(self)
        self.confirm_deleteSave_btn.resize(220, 40)
        self.confirm_deleteSave_btn.move(14, 450)
        self.confirm_deleteSave_btn.setFont(QtGui.QFont(FONT1, 25))
        self.confirm_deleteSave_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # SETTINGS MENU #

        self.settings_lbl = QtWidgets.QLabel(self)
        self.settings_lbl.resize(190, 30)
        self.settings_lbl.move(30, 325)
        self.settings_lbl.setFont(QtGui.QFont(FONT1, 25))
        self.settings_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.language_lbl = QtWidgets.QLabel(self)
        self.language_lbl.resize(190, 20)
        self.language_lbl.move(14, 365)
        self.language_lbl.setFont(QtGui.QFont(FONT1, 15))

        self.language_combobox = QtWidgets.QComboBox(self)
        self.language_combobox.resize(110, 25)
        self.language_combobox.move(124, 363)
        self.language_combobox.setFont(QtGui.QFont(FONT1, 15))
        self.language_combobox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.background_changeDelay_lbl = QtWidgets.QLabel(self)
        self.background_changeDelay_lbl.resize(160, 40)
        self.background_changeDelay_lbl.move(14, 395)
        self.background_changeDelay_lbl.setFont(QtGui.QFont(FONT1, 15))

        self.background_changeDelay_spinbox = QtWidgets.QSpinBox(self)
        self.background_changeDelay_spinbox.resize(60, 25)
        self.background_changeDelay_spinbox.move(174, 400)
        self.background_changeDelay_spinbox.setFont(QtGui.QFont(FONT1, 15))
        self.background_changeDelay_spinbox.setMaximum(999)
        self.background_changeDelay_spinbox.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.autosaving_checkbox = QtWidgets.QCheckBox(self)
        self.autosaving_checkbox.resize(220, 20)
        self.autosaving_checkbox.move(14, 440)
        self.autosaving_checkbox.setFont(QtGui.QFont(FONT1, 15))
        self.autosaving_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.discord_rpc_checkbox = QtWidgets.QCheckBox('Discord RPC', self)
        self.discord_rpc_checkbox.resize(220, 20)
        self.discord_rpc_checkbox.move(14, 465)
        self.discord_rpc_checkbox.setFont(QtGui.QFont(FONT1, 15))
        self.discord_rpc_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.audio_settings_btn = QtWidgets.QPushButton(self)
        self.audio_settings_btn.resize(220, 40)
        self.audio_settings_btn.move(14, 500)
        self.audio_settings_btn.setFont(QtGui.QFont(FONT1, 25))
        self.audio_settings_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # AUDIO SETTINGS #

        self.audio_settings_lbl = QtWidgets.QLabel(self)
        self.audio_settings_lbl.resize(190, 30)
        self.audio_settings_lbl.move(30, 350)
        self.audio_settings_lbl.setFont(QtGui.QFont(FONT1, 25))
        self.audio_settings_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.music_volume_lbl = QtWidgets.QLabel(self)
        self.music_volume_lbl.resize(190, 30)
        self.music_volume_lbl.move(20, 385)
        self.music_volume_lbl.setFont(QtGui.QFont(FONT1, 13))

        self.music_volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.music_volume_slider.resize(220, 15)
        self.music_volume_slider.move(14, 410)
        self.music_volume_slider.setRange(0, 100)
        self.music_volume_slider.setStyleSheet('color: white')
        self.music_volume_slider.setFocusPolicy(QtCore.Qt.NoFocus)

        self.sfx_volume_lbl = QtWidgets.QLabel(self)
        self.sfx_volume_lbl.resize(190, 30)
        self.sfx_volume_lbl.move(20, 425)
        self.sfx_volume_lbl.setFont(QtGui.QFont(FONT1, 13))

        self.sfx_volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.sfx_volume_slider.resize(220, 15)
        self.sfx_volume_slider.move(14, 450)
        self.sfx_volume_slider.setRange(0, 100)
        self.sfx_volume_slider.setStyleSheet('color: white')
        self.sfx_volume_slider.setFocusPolicy(QtCore.Qt.NoFocus)

        self.shuffle_music_checkbox = QtWidgets.QCheckBox(self)
        self.shuffle_music_checkbox.move(14, 470)
        self.shuffle_music_checkbox.setFont(QtGui.QFont(FONT1, 15))
        self.shuffle_music_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.settings_skip_track_btn = QtWidgets.QPushButton(self)
        self.settings_skip_track_btn.resize(220, 30)
        self.settings_skip_track_btn.move(14, 505)
        self.settings_skip_track_btn.setFont(QtGui.QFont(FONT1, 14))
        self.settings_skip_track_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid orange}')
        self.settings_skip_track_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.back_settings_menu_btn = QtWidgets.QPushButton(self)
        self.back_settings_menu_btn.resize(220, 40)
        self.back_settings_menu_btn.move(14, 550)
        self.back_settings_menu_btn.setFont(QtGui.QFont(FONT1, 25))
        self.back_settings_menu_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # ABOUT-GAME MENU #

        self.aboutGame_lbl = QtWidgets.QLabel(self)
        self.aboutGame_lbl.move(14, 285)
        self.aboutGame_lbl.setFont(QtGui.QFont(FONT1, 15))

        # GAMEPLAY SCREEN #

        self.gameplay_background = QtWidgets.QLabel(self)
        self.gameplay_background.move(0, -50)

        self.gameplay_bar_background = QtWidgets.QLabel(self)
        self.gameplay_bar_background.setStyleSheet('background-color: black')
        self.gameplay_bar_background.resize(1280, 50)
        self.gameplay_bar_background.move(0, 670)

        self.score_lbl = QtWidgets.QLabel(self)
        self.score_lbl.resize(1265, 35)
        self.score_lbl.move(10, 680)
        self.score_lbl.setFont(QtGui.QFont(FONT1, 33))

        self.achievement_unlocked_notification = QtWidgets.QLabel(self)
        self.achievement_unlocked_notification.setPixmap(load_pixmap(resources['MISC']['ACHIEVEMENT_UNLOCKED']))
        self.achievement_unlocked_notification.resize(410, 80)
        self.achievement_unlocked_notification.move(1280, 0)

        # GAMEPLAY ENEMIES #

        self.enemy0 = QtWidgets.QPushButton(self)
        self.enemy0.resize(50, 50)
        self.enemy0.setIcon(QtGui.QIcon(load_pixmap(resources['ENEMIES'][0])))
        self.enemy0.setIconSize(QtCore.QSize(50, 50))
        self.enemy0.setStyleSheet('border: 0px')
        self.enemy0.setFocusPolicy(QtCore.Qt.NoFocus)

        self.enemy1 = QtWidgets.QPushButton(self)
        self.enemy1.resize(50, 50)
        self.enemy1.setIcon(QtGui.QIcon(load_pixmap(resources['ENEMIES'][1])))
        self.enemy1.setIconSize(QtCore.QSize(50, 50))
        self.enemy1.setStyleSheet('border: 0px')
        self.enemy1.setFocusPolicy(QtCore.Qt.NoFocus)

        self.enemy2 = QtWidgets.QPushButton(self)
        self.enemy2.resize(32, 90)
        self.enemy2.setIcon(QtGui.QIcon(load_pixmap(resources['ENEMIES'][2])))
        self.enemy2.setIconSize(QtCore.QSize(32, 90))
        self.enemy2.setStyleSheet('border: 0px')
        self.enemy2.setFocusPolicy(QtCore.Qt.NoFocus)

        # PAUSE SCREEN #

        self.pause_screen_background = QtWidgets.QLabel(self)
        self.pause_screen_background.setPixmap(load_pixmap(resources['BACKGROUNDS']['PAUSE_SCREEN']))

        self.pause_menu_background = QtWidgets.QLabel(self)
        self.pause_menu_background.setStyleSheet('background-color: black')
        self.pause_menu_background.resize(250, 720)
        self.pause_menu_background.move(1030, 0)

        self.pause_menu_title = QtWidgets.QLabel(self)
        self.pause_menu_title.setStyleSheet('color: red')
        self.pause_menu_title.resize(220, 60)
        self.pause_menu_title.move(1046, 170)
        self.pause_menu_title.setFont(QtGui.QFont(FONT1, 55))
        self.pause_menu_title.setAlignment(QtCore.Qt.AlignCenter)

        self.now_playing_track_bar = QtWidgets.QLabel(self)
        self.now_playing_track_bar.setStyleSheet('background-color: black')
        self.now_playing_track_bar.resize(1280, 50)
        self.now_playing_track_bar.move(0, 0)

        self.now_playing_track_lbl = QtWidgets.QLabel(self)
        self.now_playing_track_lbl.resize(855, 40)
        self.now_playing_track_lbl.move(175, 5)
        self.now_playing_track_lbl.setFont(QtGui.QFont(FONT1, 20))

        self.pauseScreen_skip_track_btn = QtWidgets.QPushButton(self)
        self.pauseScreen_skip_track_btn.resize(150, 30)
        self.pauseScreen_skip_track_btn.move(10, 10)
        self.pauseScreen_skip_track_btn.setFont(QtGui.QFont(FONT1, 14))
        self.pauseScreen_skip_track_btn.setStyleSheet('QPushButton:hover:!pressed{border: 1px solid orange}')
        self.pauseScreen_skip_track_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.back_gameplay_btn = QtWidgets.QPushButton(self)
        self.back_gameplay_btn.resize(220, 40)
        self.back_gameplay_btn.move(1046, 350)
        self.back_gameplay_btn.setFont(QtGui.QFont(FONT1, 25))
        self.back_gameplay_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.statistics_btn = QtWidgets.QPushButton(self)
        self.statistics_btn.resize(220, 40)
        self.statistics_btn.move(1046, 400)
        self.statistics_btn.setFont(QtGui.QFont(FONT1, 25))
        self.statistics_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.achievements_btn = QtWidgets.QPushButton(self)
        self.achievements_btn.resize(220, 40)
        self.achievements_btn.move(1046, 450)
        self.achievements_btn.setFont(QtGui.QFont(FONT1, 25))
        self.achievements_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.exit_gameplay_btn = QtWidgets.QPushButton(self)
        self.exit_gameplay_btn.resize(220, 40)
        self.exit_gameplay_btn.move(1046, 500)
        self.exit_gameplay_btn.setFont(QtGui.QFont(FONT1, 25))
        self.exit_gameplay_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # STATISTICS MENU #

        self.statistics_listwidget = QtWidgets.QListWidget(self)
        self.statistics_listwidget.resize(220, 240)
        self.statistics_listwidget.move(1046, 300)
        self.statistics_listwidget.setFont(QtGui.QFont(FONT1, 12))
        self.statistics_listwidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.statistics_listwidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.statistics_listwidget.setFocusPolicy(QtCore.Qt.NoFocus)

        # ACHIEVEMENTS MENU #

        self.achievements_lbl = QtWidgets.QLabel(self)
        self.achievements_lbl.resize(220, 30)
        self.achievements_lbl.move(1046, 270)
        self.achievements_lbl.setFont(QtGui.QFont(FONT1, 19))
        self.achievements_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.achievements_listwidget = QtWidgets.QListWidget(self)
        self.achievements_listwidget.resize(220, 130)
        self.achievements_listwidget.move(1046, 300)
        self.achievements_listwidget.setFont(QtGui.QFont(FONT1, 11))
        self.achievements_listwidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.achievements_listwidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.achievements_listwidget.setFocusPolicy(QtCore.Qt.NoFocus)

        LISTWIDGET_PALETTE = QtGui.QPalette()
        LISTWIDGET_PALETTE.setColor(QtGui.QPalette.Highlight, QtCore.Qt.darkRed)
        self.achievements_listwidget.setPalette(LISTWIDGET_PALETTE)

        self.achievement_info_viewer = QtWidgets.QTextBrowser(self)
        self.achievement_info_viewer.resize(220, 55)
        self.achievement_info_viewer.move(1046, 435)
        self.achievement_info_viewer.setFont(QtGui.QFont(FONT1, 11))
        self.achievement_info_viewer.setFocusPolicy(QtCore.Qt.NoFocus)
        self.achievement_info_viewer.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.achievement_info_viewer.setFocusPolicy(QtCore.Qt.NoFocus)

        self.achievements_switch_btn = QtWidgets.QPushButton(self)
        self.achievements_switch_btn.resize(220, 40)
        self.achievements_switch_btn.move(1046, 500)
        self.achievements_switch_btn.setFont(QtGui.QFont(FONT1, 25))
        self.achievements_switch_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        # BUTTON FOR BACK PAUSE MENU #
        self.back_pauseScreen_menu_btn = QtWidgets.QPushButton(self)
        self.back_pauseScreen_menu_btn.resize(220, 40)
        self.back_pauseScreen_menu_btn.move(1046, 550)
        self.back_pauseScreen_menu_btn.setFont(QtGui.QFont(FONT1, 25))
        self.back_pauseScreen_menu_btn.setFocusPolicy(QtCore.Qt.NoFocus)

    # PYQT-EVENTS #

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape: # key for pause the game
            if self.startScreen_status == False: # if player not in main-menu

                if self.pause_status == False: # if pause screen already is not opened
                    self.main.pause_gameplay_session()

                else: # if already opened - pause screen will be closed
                    self.main.continue_gameplay_session()

    def mouseReleaseEvent(self, event): # counting of non-target clicks in gameplay
        if (self.startScreen_status == False) and (self.pause_status == False):
            self.main.events.lose_points()

    def closeEvent(self, event):
        if not self.startScreen_status:
            self.main.overwrite_saves()
