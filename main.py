"""THE BEST PYQT-GAME EVER"""

__title__   = 'SheymOsu'
__author__  = 'RinkLinky'
__version__ = 'Pre-Beta 0.5.1'

import pickle
import json
import os
import sys
import random
import datetime
import logging

from PyQt5 import QtWidgets, QtGui, QtCore

from gui_methods import GuiMethods
from gameplay_events import GameplayEvents
from audio_manager import GameAudio
from lang_manager import LanguageManager
from achievements_manager import AchievementsManager
from discord_rpc import DiscordRPCIntegration

DEFAULT_SETTINGS = {
    'language': 'en',
    'background_change_delay': 2,
    'autosaving': True,
    'autosaving_delay': 180000,
    'discord_rpc': True,

    'audio': {
        'music_volume': 30,
        'sfx_volume': 30,
        'notifications_volume': 40,
        'shuffle_music': True,
        'track_repeat_chance': False,
    }
}

APP_PALETTE = QtGui.QPalette()
APP_PALETTE.setColor(QtGui.QPalette.Window, QtCore.Qt.black)
APP_PALETTE.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
APP_PALETTE.setColor(QtGui.QPalette.Base, QtGui.QColor(19, 19, 19))
APP_PALETTE.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
APP_PALETTE.setColor(QtGui.QPalette.Button, QtCore.Qt.black)
APP_PALETTE.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
APP_PALETTE.setColor(QtGui.QPalette.Highlight, QtCore.Qt.red)
APP_PALETTE.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
APP_PALETTE.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(8, 8, 8))

DIFFICULTY_LEVELS = {
    0: {
        'ENEMIES_TIMEOUTS': (7, 4, 2),
        'ENEMIES_SCORES': (2, 5, 10),
        'LOSING_POINTS': 2,
    },
    1: {
        'ENEMIES_TIMEOUTS': (4, 2, 1.5),
        'ENEMIES_SCORES': (5, 10, 15),
        'LOSING_POINTS': 5,
    },
    2: {
        'ENEMIES_TIMEOUTS': (2, 1.5, 1),
        'ENEMIES_SCORES': (10, 15, 20),
        'LOSING_POINTS': 10,
    },
    3: {
        'ENEMIES_TIMEOUTS': (1.5, 1, 0.7),
        'ENEMIES_SCORES': (15, 20, 25),
        'LOSING_POINTS': 15,
    }
}

ABOUT_GAME_STRING = \
'''Game version:
%s

Author:
%s

Support:
eternalfrenzy
Garen

Source code on GitHub.''' % (__version__, __author__)

def extract_graphics():
    with open('resources/graphics.bin', 'rb') as resources_file:
        resources = pickle.load(resources_file)

    logger.info('RESOURCES EXTRACTED')

    return resources

def load_settings():
    if not os.path.isfile('settings.json'):
        logger.warning('SETTINGS-FILE NOT FOUND')

        with open('settings.json', 'w') as cfg_file:
            json.dump(DEFAULT_SETTINGS, cfg_file, ensure_ascii=False, indent=4)
        logger.info('DEFAULT SETTINGS-FILE SAVED')

    try:
        with open('settings.json', 'r') as cfg_file:
            settings = json.load(cfg_file)
        logger.info('SETTINGS LOADED')
    except Exception as e:
        logger.error('SETTINGS READING IS FAILED: %s', e)
        settings = DEFAULT_SETTINGS
        logger.info('DEFAULT SETTINGS LOADED')

    return settings

def read_saves():
    if not os.path.isfile('userdata/saves.sav'):
        logger.warning('SAVES-FILE NOT FOUND')

        if not os.path.exists('userdata'):
            os.makedirs('userdata')
            logger.info('DIR userdata CREATED')

        with open('userdata/saves.sav', 'wb') as saves_file:
            pickle.dump([], saves_file)
        logger.info('SAVES-FILE CREATED')

    try:
        with open('userdata/saves.sav', 'rb') as saves_file:
            saves = pickle.load(saves_file)
        logger.info('SAVES LOADED')
    except Exception as e:
        logger.error('SAVES READING IS FAILED: %s', e)

        try:
            with open('userdata/saves.old.sav', 'rb') as saves_file:
                saves = pickle.load(saves_file)
            logger.info('OLD SAVES LOADED')
        except Exception as e:
            logger.error('OLD SAVES READING IS FAILED: %s', e)
            saves = []

    return saves

class Main:

    def __init__(self):
        self.resources = extract_graphics()
        self.settings = load_settings()
        self.logger = logger

        self.gui = GuiMethods(self)
        self.audio = GameAudio(self)
        self.events = GameplayEvents(self)
        self.lang_manager = LanguageManager(self)
        self.achievements_manager = AchievementsManager(self)
        self.discord_rpc = DiscordRPCIntegration(self)

        self.apply_settings()

        self.saves = read_saves()
        self.gui.fill_with_saves()

        self.gui.gameVersion_lbl.setText(__version__)
        self.gui.aboutGame_lbl.setText(ABOUT_GAME_STRING)

        self.gui.show()
        self.gui.open_startScreen()
        self.gui.close_pause_screen()
        self.gui.close_gameplay_screen()

        self.audio.play_music()

        # PYQT-SIGNALS CONNECTING #

        # START-SCREEN MENU #
        self.gui.newGame_btn.clicked.connect(self.gui.prepare_save_creating)
        self.gui.continueGame_btn.clicked.connect(self.gui.open_continueGame_menu)
        self.gui.settings_btn.clicked.connect(self.gui.open_settings_menu)
        self.gui.quitGame_btn.clicked.connect(app.quit)
        self.gui.aboutGame_btn.clicked.connect(self.gui.open_aboutGame_menu)
        self.gui.back_startScreen_menu_btn.clicked.connect(self.gui.back_startScreen_menu)
        # NEW-SAVE MENU #
        self.gui.create_save_btn.clicked.connect(self.new_save)
        self.gui.change_gamemode_btn.clicked.connect(self.gui.change_gamemodeLevel)
        self.gui.change_difficulty_btn.clicked.connect(self.gui.change_difficultyLevel)
        # CONTINUE-SAVES MENU #
        self.gui.savesList_edit.itemDoubleClicked.connect(self.continue_save)
        self.gui.continue_save_btn.clicked.connect(self.continue_save)
        self.gui.change_save_btn.clicked.connect(self.gui.change_save)
        self.gui.delete_save_btn.clicked.connect(self.gui.delete_save)
        # EDITING-SAVE MENU #
        self.gui.save_changedSave_btn.clicked.connect(self.save_changedSave)
        # DELETE-SAVE MENU #
        self.gui.confirm_deleteSave_btn.clicked.connect(self.confirm_save_deleting)
        # SETTINGS MENU #
        self.gui.language_combobox.currentIndexChanged.connect(self.gui.change_language)
        self.gui.background_changeDelay_spinbox.valueChanged.connect(self.gui.change_background_changeDelay)
        self.gui.autosaving_checkbox.stateChanged.connect(self.gui.switch_autosaving)
        self.gui.discord_rpc_checkbox.stateChanged.connect(self.gui.switch_discord_rpc)
        self.gui.audio_settings_btn.clicked.connect(self.gui.open_audio_settings_menu)
        # AUDIO-SETTINGS MENU #
        self.gui.music_volume_slider.valueChanged.connect(self.gui.change_music_volume)
        self.gui.sfx_volume_slider.valueChanged.connect(self.gui.change_sfx_volume)
        self.gui.back_settings_menu_btn.clicked.connect(self.gui.close_audio_settings_menu)
        self.gui.shuffle_music_checkbox.stateChanged.connect(self.gui.switch_shuffle_music)
        self.gui.settings_skip_track_btn.clicked.connect(self.audio.skip_track)
        # PAUSE MENU #
        self.gui.back_gameplay_btn.clicked.connect(self.continue_gameplay_session)
        self.gui.statistics_btn.clicked.connect(self.gui.open_statistics_menu)
        self.gui.achievements_btn.clicked.connect(self.gui.open_achievements_menu)
        self.gui.exit_gameplay_btn.clicked.connect(self.finish_gameplay)
        self.gui.pauseScreen_skip_track_btn.clicked.connect(self.audio.skip_track)
        self.gui.back_pauseScreen_menu_btn.clicked.connect(self.gui.back_pause_menu)
        # ACHIEVEMENTS MENU #
        self.gui.achievements_listwidget.currentRowChanged.connect(self.gui.show_achievement_description)
        self.gui.achievements_switch_btn.clicked.connect(self.gui.change_achievements_type)

        self.logger.info('MAIN CLASS INITIALISED')

    def new_save(self):
        """Create new save with user-settings"""
        saveName = self.gui.saveName_edit.text().strip() # Clearning the spaces on sides
        if saveName == '':
            saveName = self.lang_manager.get_string('Other', 'NewSave')

        self.current_save = { # Creating new save
            'name': saveName,
            'gamemode': self.gui.selected_gamemodeLevel,
            'difficulty': self.gui.selected_difficultyLevel,
            'score': 0,

            'statistics': {
                'time_played': 0,
                'earned_points': 0,
                'lost_points': 0,
                'total_clicks': 0,
                'miss_clicks': 0,
                'enemies_clicks': [0, 0, 0],
            },
            'completed_achievements': [],

            'created_at': datetime.datetime.now().timestamp(),
            'last_change': datetime.datetime.now().timestamp(),
            'client_version': __version__,
        }

        self.logger.info('NEW SAVE CREATED')

        self.saves.insert(0, self.current_save)

        self.overwrite_saves()
        self.gui.fill_with_saves()

        self.start_gameplay()

    def continue_save(self):
        """Continue the selected save by player"""
        currentSave_id = self.gui.savesList_edit.currentRow() # Getting the selected save
        if currentSave_id != -1:
            self.current_save = self.saves[self.gui.savesList_edit.currentRow()]
            self.current_save['client_version'] = __version__

            self.logger.info('SELECTED SAVE LOADED')

            del self.saves[currentSave_id]
            self.saves.insert(0, self.current_save)
            self.overwrite_saves()

            self.start_gameplay()

    def start_gameplay(self):
        """Prepare gameplay-screen for playing"""
        self.gui.close_startScreen()

        self.current_difficulty = DIFFICULTY_LEVELS[self.current_save['difficulty']]

        # zeroing the time values for time-outs work
        self.events.backgroundTime = 0
        self.events.enemy0_time = 0
        self.events.enemy1_time = 0
        self.events.enemy2_time = 0

        self.gui.set_random_gameplayBackground()

        score_name = self.lang_manager.get_string('Other', 'Score')
        self.gui.score_lbl.setText('%s: %s' % (score_name, self.current_save['score']))

        # random movement of enemies
        self.gui.enemy0.move(random.randint(20, 1200), random.randint(20, 620))
        self.gui.enemy1.move(random.randint(20, 1200), random.randint(20, 620))
        self.gui.enemy2.move(random.randint(20, 1200), random.randint(20, 620))

        self.gui.open_gameplay_screen()
        self.events.gameplay_timer.start()

        if self.settings['autosaving']:
            self.events.autosaving_timer.start()

        self.logger.info('GAMEPLAY SESSION STARTED')

    def finish_gameplay(self):
        """Finish gameplay and dump the updated saves"""
        self.gui.close_pause_screen()
        self.events.autosaving_timer.stop()

        # random movement of enemies
        self.gui.enemy0.move(random.randint(20, 1200), random.randint(20, 550))
        self.gui.enemy1.move(random.randint(20, 1200), random.randint(20, 550))
        self.gui.enemy2.move(random.randint(20, 1200), random.randint(20, 550))

        self.current_save['last_change'] = datetime.datetime.now().timestamp()

        self.saves[0] = self.current_save

        self.achievements_manager.reset_progress()

        self.logger.info('GAMEPLAY SESSION ENDED')

        self.overwrite_saves()

        self.gui.fill_with_saves()
        self.gui.open_startScreen()

    def continue_gameplay_session(self):
        """Close pause-screen and open gameplay-screen"""
        self.gui.close_pause_screen()
        self.gui.open_gameplay_screen()

        self.events.gameplay_timer.start()

        self.logger.info('GAMEPLAY SESSION RESUMED')

    def pause_gameplay_session(self):
        """Close gameplay-screen and open pause-screen"""
        self.gui.close_gameplay_screen()
        self.events.gameplay_timer.stop()

        self.gui.open_pause_screen()

        self.logger.info('GAMEPLAY SESSION PAUSED')

    def save_changedSave(self):
        """Save changes for selected save by player"""
        if self.gui.saveName_edit.text().strip() == '':
            self.gui.saveName_edit.clear()

        else:
            self.gui.hide_changeSave_menu()

            # if save-name was changed - change saving
            old_name = self.saves[self.gui.selected_save_row]['name']
            if self.gui.saveName_edit.text().strip() != old_name:
                new_name = self.gui.saveName_edit.text().strip()
                self.saves[self.gui.selected_save_row]['name'] = new_name

                self.logger.info('SELECTED SAVE EDITED WITH NEW NAME %s', new_name)

                self.overwrite_saves()
                self.gui.fill_with_saves()

            self.gui.show_continueGame_menu()

    def confirm_save_deleting(self):
        """Confirm deleting the selected save by player"""
        selected_save_row = self.gui.savesList_edit.currentRow()
        del self.saves[selected_save_row]

        self.logger.info('SELECTED SAVE DELETED')

        self.overwrite_saves()

        self.gui.fill_with_saves()

        self.gui.hide_deleteSave_menu()
        self.gui.show_continueGame_menu()

    def apply_settings(self):
        self.gui.background_changeDelay_spinbox.setValue(self.settings['background_change_delay'])

        if self.settings['autosaving']:
            self.gui.autosaving_checkbox.toggle()

        if self.settings['discord_rpc']:
            self.gui.discord_rpc_checkbox.toggle()
            try:
                self.discord_rpc.presence.connect()
            except Exception as e:
                self.logger.error('DISCORD_RPC CONNECTING IS FAILED: %s', e)

        self.gui.music_volume_slider.setValue(self.settings['audio']['music_volume'])
        self.gui.sfx_volume_slider.setValue(self.settings['audio']['sfx_volume'])
        self.audio.music_player.setVolume(self.settings['audio']['music_volume'])
        self.audio.sfx_player.setVolume(self.settings['audio']['sfx_volume'])
        self.audio.notifications_player.setVolume(self.settings['audio']['notifications_volume'])

        if self.settings['audio']['shuffle_music']:
            self.gui.shuffle_music_checkbox.toggle()

        self.lang_manager.fill_with_languages()
        self.lang_manager.apply_language()

        self.logger.info('SETTINGS APPLIED')

    def save_settings(self):
        with open('settings.json', 'w') as cfg_file:
            json.dump(self.settings, cfg_file, ensure_ascii=False, indent=4)
        self.logger.info('SETTINGS SAVED')

    def overwrite_saves(self):
        if not os.path.exists('userdata'):
            os.makedirs('userdata')
            self.logger.info('DIR userdata CREATED')

        try:
            with open('userdata/saves.sav', 'rb') as saves_file:
                old_saves = pickle.load(saves_file)

            with open('userdata/saves.old.sav', 'wb') as saves_file:
                pickle.dump(old_saves, saves_file)

        except Exception as e:
            self.logger.error('FAILED TO BACKUP THE SAVES: %s', e)

        with open('userdata/saves.sav', 'wb') as saves_file:
            pickle.dump(self.saves, saves_file)

        self.logger.info('SAVES OVERWRITTEN')

if __name__ == '__main__':
    logger = logging.getLogger('App')
    logger.setLevel(logging.INFO)
    logs_handler = logging.FileHandler('last.log')
    logs_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    logs_handler.setFormatter(logs_formatter)
    logger.addHandler(logs_handler)

    logger.info('/// APP STARTED ///')

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(APP_PALETTE)
    ex = Main()
    code = app.exec_()

    logger.info('/// APP CLOSED WITH CODE %s ///', code)
    sys.exit(code)
