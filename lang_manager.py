import configparser
import os

DEFAULT_LANG_CFG = configparser.ConfigParser()
DEFAULT_LANG_CFG.optionxform = str

DEFAULT_LANG_CFG.update({
    'LangInfo': {
        'Name': 'English',
        'Code': 'en',
        'TranslationAuthors': 'RinkLinky',
    },
    'Gui': {
        'NewGame': 'New Game',
        'ContinueGame': 'Continue',
        'QuitGame': 'Quit',
        'NameOfSave': 'Name of save',
        'CreateSave': 'Create',
        'RunSave': 'Run',
        'ChangeSave': 'Change',
        'DeleteSave': 'Delete',
        'DeleteSaveWarning': 'Save will be\npermanently deleted!',
        'BackgroundChangeDelay': 'Background delay',
        'BackgroundChangeDelay.SpinBox.Suffix': 's',
        'Autosaving': 'Autosaving',
        'AudioSettings': 'Audio',
        'MusicVolume': 'Music Volume',
        'SFXVolume': 'SFX Volume',
        'ShuffleMusic': 'Shuffle music',
        'SkipTrack': 'Skip track',
        'NowPlaying': 'Now playing: {}',
        'PauseTitle': 'PAUSE',
        'DefaultAchievements': 'Default',
        'CustomAchievements': 'Custom',
        'Cancel': 'Cancel',
        'Back': 'Back',
        'ExitToMainMenu': 'Save and exit',
    },
    'Other': {
        'Settings': 'Settings',
        'Language': 'Language',
        'GameMode': 'Game mode',
        'Difficulty': 'Difficulty',
        'Statistics': 'Statistics',
        'Achievements': 'Achievements',
        'Score': 'Score',
        'NewSave': 'New save',
        'MainMenu': 'Main menu',
    },
    'GameMode': {
        'EndlessMode': 'Endless mode',
    },
    'Difficulty': {
        'Easy': 'Easy',
        'Normal': 'Normal',
        'Hard': 'Hard',
        'VeryHard': 'Very hard',
    },
    'Statistics': {
        'time_played': 'Time played',
        'earned_points': 'Earned points',
        'lost_points': 'Lost points',
        'total_clicks': 'Total clicks count',
        'miss_clicks': 'Miss clicks count',
        'enemy_clicks': '<{}> clicks count',
    },
    'Enemies': {
        '0': 'BodyANM',
        '1': 'BCEM_XAXA',
        '2': 'Oil',
    },
})

CODES_FOR_STRINGS = {
    'Difficulty': ('Easy', 'Normal', 'Hard', 'VeryHard',),
    'GameMode': ('EndlessMode',),
}

class LanguageManager:

    def __init__(self, main):
        self.main = main
        self.languages = self._load_languages()
        self.selected_lang = self._get_lang(self.main.settings['language'])

        self.main.logger.info('LANGUAGE_MANAGER INITIALISED')

    def get_string(self, section, name):
        try:
            found_string = self.selected_lang[section][name]
            return found_string

        except KeyError:
            self.main.logger.warning('STRING [%s][%s] NOT FOUND FOR CURRENT LANGUAGE', section, name)

            return DEFAULT_LANG_CFG[section][name]

    def get_string_by_code(self, section, code):
        return CODES_FOR_STRINGS[section][code]

    def fill_with_languages(self):
        for lang in self.languages:
            self.main.gui.language_combobox.addItem(lang['LangInfo']['Name'])

    def apply_language(self):
        self.main.gui.newGame_btn.setText(self.get_string('Gui', 'NewGame'))
        self.main.gui.continueGame_btn.setText(self.get_string('Gui', 'ContinueGame'))
        self.main.gui.settings_btn.setText(self.get_string('Other', 'Settings'))
        self.main.gui.quitGame_btn.setText(self.get_string('Gui', 'QuitGame'))

        self.main.gui.saveName_lbl.setText(self.get_string('Gui', 'NameOfSave'))
        self.main.gui.change_gamemode_btn.setText(self.get_string('GameMode', 'EndlessMode'))
        self.main.gui.difficulty_lbl.setText(self.get_string('Other', 'Difficulty'))
        self.main.gui.change_difficulty_btn.setText(self.get_string('Other', 'Difficulty'))
        self.main.gui.create_save_btn.setText(self.get_string('Gui', 'CreateSave'))
        self.main.gui.continue_save_btn.setText(self.get_string('Gui', 'RunSave'))
        self.main.gui.change_save_btn.setText(self.get_string('Gui', 'ChangeSave'))
        self.main.gui.delete_save_btn.setText(self.get_string('Gui', 'DeleteSave'))

        self.main.gui.save_changedSave_btn.setText(self.get_string('Gui', 'ChangeSave'))

        self.main.gui.deleteSave_warning_lbl.setText(self.get_string('Gui', 'DeleteSaveWarning'))
        self.main.gui.confirm_deleteSave_btn.setText(self.get_string('Gui', 'DeleteSave'))

        self.main.gui.back_mods_menu_btn.setText(self.get_string('Gui', 'Back'))
        self.main.gui.mods_btn.setText(self.get_string('Gui', 'Mods'))
        self.main.gui.mod_desc.setText(self.get_string("Gui", "ModHint"))
        self.main.gui.toggle_mod_btn.setText(self.get_string("Gui", "Toggle"))

        self.main.gui.cancel_btn.setText(self.get_string('Gui', 'Cancel'))
        self.main.gui.settings_lbl.setText(self.get_string('Other', 'Settings'))
        self.main.gui.language_lbl.setText(self.get_string('Other', 'Language'))
        self.main.gui.background_changeDelay_lbl.setText(self.get_string('Gui', 'BackgroundChangeDelay'))
        self.main.gui.background_changeDelay_spinbox.setSuffix(self.get_string('Gui', 'BackgroundChangeDelay.SpinBox.Suffix'))
        self.main.gui.autosaving_checkbox.setText(self.get_string('Gui', 'Autosaving'))

        self.main.gui.audio_settings_btn.setText(self.get_string('Gui', 'AudioSettings'))
        self.main.gui.audio_settings_lbl.setText(self.get_string('Gui', 'AudioSettings'))
        self.main.gui.music_volume_lbl.setText(self.get_string('Gui', 'MusicVolume'))
        self.main.gui.sfx_volume_lbl.setText(self.get_string('Gui', 'SFXVolume'))
        self.main.gui.shuffle_music_checkbox.setText(self.get_string('Gui', 'ShuffleMusic'))
        self.main.gui.settings_skip_track_btn.setText(self.get_string('Gui', 'SkipTrack'))
        self.main.gui.back_settings_menu_btn.setText(self.get_string('Gui', 'Back'))

        self.main.gui.back_startScreen_menu_btn.setText(self.get_string('Gui', 'Back'))

        self.main.gui.pause_menu_title.setText(self.get_string('Gui', 'PauseTitle'))
        self.main.gui.back_gameplay_btn.setText(self.get_string('Gui', 'ContinueGame'))
        self.main.gui.statistics_btn.setText(self.get_string('Other', 'Statistics'))
        self.main.gui.achievements_btn.setText(self.get_string('Other', 'Achievements'))
        self.main.gui.exit_gameplay_btn.setText(self.get_string('Gui', 'ExitToMainMenu'))
        self.main.gui.pauseScreen_skip_track_btn.setText(self.get_string('Gui', 'SkipTrack'))

        if self.main.audio.music_player.state() == 1:
            currentTrack_name = self.main.audio.music_player.media().canonicalUrl().fileName()
            fmt_now_playing_track = self.get_string('Gui', 'NowPlaying').format(currentTrack_name)
            self.main.gui.now_playing_track_lbl.setText(fmt_now_playing_track)

        self.main.gui.back_pauseScreen_menu_btn.setText(self.get_string('Gui', 'Back'))

        self.main.gui.language_combobox.setCurrentText(self.selected_lang['LangInfo']['Name'])

        self.main.logger.info('%s LANGUAGE APPLIED', self.selected_lang['LangInfo']['Name'])

    def _load_languages(self):
        languages = []

        if not os.path.exists('languages'):
            self.main.logger.warning('LANGUAGES DIR NOT FOUND')
            return languages

        for filename in os.listdir('languages'):
            filepath = os.path.join('languages', filename)
            if filename.endswith('.ini') and os.path.isfile(filepath):
                try:
                    lang_cfg = configparser.ConfigParser()
                    lang_cfg.read(filepath, encoding='utf-8')

                    languages.append(lang_cfg)

                except Exception as e:
                    self.main.logger.error('FAILED TO LOAD LANGUAGE FROM %s: %s', filename, e)

        for lang in languages: # if english lang not found in langs dir
            if lang['LangInfo']['Name'] == 'English':
                break
        else:
            languages.append(DEFAULT_LANG_CFG)

        self.main.logger.info('%s LANGUAGES LOADED', len(languages))

        return languages

    def _get_lang(self, lang_code):
        for lang_cfg in self.languages:
            if lang_cfg['LangInfo']['Code'] == lang_code:
                return lang_cfg

        return DEFAULT_LANG_CFG
