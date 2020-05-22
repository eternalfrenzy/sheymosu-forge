import random
import datetime

from PyQt5 import QtGui, QtWidgets, QtCore

from gui import Gui, load_pixmap

class GuiMethods(Gui):

    def __init__(self, main):
        super().__init__(main.resources)
        main.logger.info('GUI INITIALISED')
        self.main = main

        self.startScreen_status = True
        self.pause_status = False
        self.selected_gamemodeLevel = 0
        self.selected_difficultyLevel = 1
        self.selected_achievements_type_view = 0

        self.main.logger.info('GUI METHODS INITIALISED')

    def setup_custom_enemies(self):
        for enemy in self.main.enemylib.enemies:
            enemy.button = QtWidgets.QPushButton(self)
            enemy.button.resize(50, 50)
            enemy.button.move(230, 230)
            try:
                fi = open(enemy.texture, "rb")
                texturedata = fi.read()
                fi.close()
                enemy.button.setIcon(QtGui.QIcon(load_pixmap(texturedata)))
            except Exception as e:
                pass
            enemy.button.setIconSize(QtCore.QSize(50, 50))
            enemy.button.setStyleSheet('border: 0px')
            enemy.button.setFocusPolicy(QtCore.Qt.NoFocus)
            enemy.button.hide()

    def prepare_save_creating(self):
        """Prepare new-game menu for creating the new save"""
        self.hide_startScreen_menu()

        newSave_name = self.main.lang_manager.get_string('Other', 'NewSave')
        difficulty_name = self.main.lang_manager.get_string('Difficulty', 'Normal')

        self.saveName_edit.setText(newSave_name)
        self.change_difficulty_btn.setText(difficulty_name)

        self.selected_gamemodeLevel = 0
        self.selected_difficultyLevel = 1

        self.show_newGame_menu()

    def open_continueGame_menu(self):
        """Show continue-game menu and hide start-screen menu"""
        self.hide_startScreen_menu()
        self.show_continueGame_menu()

    def open_settings_menu(self):
        """Show settings menu and hide start-screen menu"""
        self.hide_startScreen_menu()
        self.show_settings_menu()

    def open_mods_menu(self):
        """Shows the mod list and mod utilities"""
        self.hide_startScreen_menu()
        self.show_mods_menu()

    def close_mods_menu(self):
        """Closes the mod list and mod utilities"""
        self.hide_mods_menu()
        self.show_startScreen_menu()

    def show_mods_menu(self):
        self.back_mods_menu_btn.show()
        self.toggle_mod_btn.show()
        self.mod_desc.show()
        self.modsList.show()

    def hide_mods_menu(self):
        self.back_mods_menu_btn.hide()
        self.toggle_mod_btn.hide()
        self.mod_desc.hide()
        self.modsList.hide()

    def open_audio_settings_menu(self):
        """Show audio settings menu and hide standard settings menu"""
        self.hide_settings_menu()
        self.show_audio_settings_menu()

    def close_audio_settings_menu(self):
        """Show audio settings menu and hide standard settings menu"""
        self.hide_audio_settings_menu()
        self.show_settings_menu()

    def toggle_mod(self):
        """Toggles a selected mod on or off"""
        selected = self.modsList.currentRow()
        if selected != -1:
            mod = self.main.mod_manager.mods[selected]
            if not mod.is_invalid:
                mod.enable() if not mod.enabled else mod.disable()
                self.fill_with_mods()

    def change_save(self):
        """Show change-save menu for selected save"""
        self.selected_save_row = self.savesList_edit.currentRow()
        if self.selected_save_row != -1: # -1 index means that not selected
            self.saveName_edit.setText(self.main.saves[self.selected_save_row]['name'])
            self.cancel_btn.clicked.connect(self.cancel_saveEditing)
            self.hide_continueGame_menu()
            self.show_changeSave_menu()

    def delete_save(self):
        """Show delete-save menu for selected save"""
        selected_save_row = self.savesList_edit.currentRow()
        if selected_save_row != -1:
            self.cancel_btn.clicked.connect(self.cancel_saveDeleting)
            self.hide_continueGame_menu()
            self.show_deleteSave_menu()

    def cancel_saveEditing(self):
        """Hide save-change menu and show continue-game menu"""
        self.hide_changeSave_menu()
        self.show_continueGame_menu()

    def cancel_saveDeleting(self):
        """Hide save-delete menu and show continue-game menu"""
        self.hide_deleteSave_menu()
        self.show_continueGame_menu()

    def open_aboutGame_menu(self):
        """Show information about the game and hide start-screen menu"""
        self.hide_startScreen_menu()
        self.show_aboutGame_menu()

    def open_statistics_menu(self):
        """Show statistics menu and hide pause-screen menu"""
        self.hide_pause_menu()
        self.fill_with_statistics()
        self.show_statistics_menu()

    def open_achievements_menu(self):
        """Show achievements menu and hide pause-screen menu"""
        self.hide_pause_menu()

        default_achievements_count = self.main.achievements_manager.get_default_achievements_count()

        if default_achievements_count == len(self.main.achievements_manager.achievements):
            self.achievements_switch_btn.setEnabled(False)
        else:
            self.achievements_switch_btn.setEnabled(True)

        self.show_default_achievements()

        self.show_achievements_menu()

    def back_startScreen_menu(self):
        """Hide all start-screen submenus and show start-screen menu"""
        self.hide_newGame_menu()
        self.hide_continueGame_menu()
        self.hide_changeSave_menu()
        self.hide_deleteSave_menu()
        self.hide_settings_menu()
        self.hide_audio_settings_menu()
        self.hide_aboutGame_menu()
        self.show_startScreen_menu()

    def back_pause_menu(self):
        """Hide all pause submenus and show pause menu"""
        self.hide_statistics_menu()
        self.hide_achievements_menu()
        self.show_pause_menu()

    def change_difficultyLevel(self):
        """Changing the difficulty by button pressing"""
        if self.selected_difficultyLevel == 0:
            self.selected_difficultyLevel = 1

            difficulty_name = self.main.lang_manager.get_string('Difficulty', 'Normal')
            self.change_difficulty_btn.setText(difficulty_name)

        elif self.selected_difficultyLevel == 1:
            self.selected_difficultyLevel = 2

            difficulty_name = self.main.lang_manager.get_string('Difficulty', 'Hard')
            self.change_difficulty_btn.setText(difficulty_name)

        elif self.selected_difficultyLevel == 2:
            self.selected_difficultyLevel = 3

            difficulty_name = self.main.lang_manager.get_string('Difficulty', 'VeryHard')
            self.change_difficulty_btn.setText(difficulty_name)

        elif self.selected_difficultyLevel == 3:
            self.selected_difficultyLevel = 0

            difficulty_name = self.main.lang_manager.get_string('Difficulty', 'Easy')
            self.change_difficulty_btn.setText(difficulty_name)

    def change_gamemodeLevel(self):
        """Changing the gamemode by button pressing"""
        pass

    def change_achievements_type(self):
        if self.selected_achievements_type_view == 0:
            self.show_custom_achievements()

        elif self.selected_achievements_type_view == 1:
            self.show_default_achievements()

    def change_language(self, lang_index):
        """Apply changed game language"""
        selected_language = self.main.lang_manager.languages[lang_index]
        self.main.lang_manager.selected_lang = selected_language

        self.main.settings['language'] = selected_language['LangInfo']['Code']
        self.main.save_settings()

        self.main.logger.info('CURRENT LANGUAGE CHANGED')

        self.main.lang_manager.apply_language()
        self.fill_with_saves()
        self.fill_with_mods()

    def change_background_changeDelay(self, delay):
        """Save the changed 'background_change_delay' in game settings"""
        self.main.settings['background_change_delay'] = delay
        self.main.save_settings()

    def switch_autosaving(self, state):
        """Update 'autosaving' setting after checkbox switch"""
        self.main.settings['autosaving'] = bool(state)
        self.main.save_settings()

    def switch_discord_rpc(self, state):
        """Update 'discord_rpc' setting after checkbox switch"""
        self.main.settings['discord_rpc'] = bool(state)

        if state == 2:
            try:
                self.main.discord_rpc.presence.connect()
                self.main.logger.info('DISCORD PRESENCE CONNECTED')
            except Exception as e:
                self.main.logger.error('DISCORD_RPC CONNECTING IS FAILED: %s', e)
            self.main.discord_rpc.update_for_startScreen()

        else:
            try:
                self.main.discord_rpc.presence.clear()
                self.main.logger.info('DISCORD PRESENCE DISABLED')
            except:
                self.main.logger.error('DISCORD PRESENCE CLEANUP IS FAILED')

        self.main.logger.info('DISCORD_RPC SETTING CHANGED')

        self.main.save_settings()

    def switch_shuffle_music(self, state):
        """Update 'shuffle_music' setting by checkbox switch"""
        self.main.settings['audio']['shuffle_music'] = bool(state)
        self.main.save_settings()

    def change_music_volume(self, value):
        """Update music volume by slider moving"""
        self.main.settings['audio']['music_volume'] = value
        self.main.save_settings()

        self.main.audio.music_player.setVolume(value)

    def change_sfx_volume(self, value):
        """Update SFX volume by slider moving"""
        self.main.settings['audio']['sfx_volume'] = value
        self.main.save_settings()

        self.main.audio.sfx_player.setVolume(value)

    def fill_with_saves(self):
        """Fill the QListWidget with saves"""
        self.savesList_edit.clear()

        for save in self.main.saves: # format displying information of save in QListWidget

            gamemode_name = self.main.lang_manager.get_string_by_code('GameMode', save['gamemode'])
            gamemode_name = self.main.lang_manager.get_string('GameMode', gamemode_name)

            difficulty_name = self.main.lang_manager.get_string_by_code('Difficulty', save['difficulty'])
            difficulty_name = self.main.lang_manager.get_string('Difficulty', difficulty_name)

            score_name = self.main.lang_manager.get_string('Other', 'Score')

            new_item = f"{save['name']}\n{difficulty_name} / {score_name}: {save['score']}"

            self.savesList_edit.addItem(new_item)

        if self.savesList_edit.count() == 0:
            self.continueGame_btn.setEnabled(False) # if saves not found - continue-menu will be disabled
        else:
            self.continueGame_btn.setEnabled(True)

    def fill_with_mods(self):
        """Fill the QListWidget with mod list"""
        self.modsList.clear()

        for mod in self.main.mod_manager.mods:

            if mod.is_invalid:
                state = self.main.lang_manager.get_string("Gui", "Invalid")
            else:
                state = self.main.lang_manager.get_string("Gui", "Enabled") if mod.enabled else self.main.lang_manager.get_string("Gui", "Disabled")

            version_localize = self.main.lang_manager.get_string("Gui", "Version")

            item = "%s - %s\n%s %s" % (mod.name, state, version_localize, mod.version)
            self.modsList.addItem(item)

    def mod_select(self):
        """Handle mod selection in the list"""
        selected = self.modsList.currentRow()
        if selected != -1:
            mod = self.main.mod_manager.mods[selected]
            if mod:
                self.main.gui.mod_desc.setText(mod.desc) if not mod.is_invalid else self.main.gui.mod_desc.setText(self.main.lang_manager.get_string("Gui", "Invalid")+": "+str(mod.exception))
                # Retarded way of updating the aligment, ikr
                self.main.gui.mod_desc.hide() 
                self.main.gui.mod_desc.show()

    def fill_with_statistics(self):
        """Fill the QListWidget with player statistics"""
        self.statistics_listwidget.clear()

        NOT_STANDARD_ITEMS = 'time_played', 'enemies_clicks',

        time_played = int(self.main.current_save['statistics']['time_played'])
        format_time = str(datetime.timedelta(seconds=time_played))
        item_name = self.main.lang_manager.get_string('Statistics', 'time_played')
        self.statistics_listwidget.addItem('%s\n- %s' % (item_name, format_time))

        for item in self.main.current_save['statistics']:

            if item in NOT_STANDARD_ITEMS:
                continue

            item_name = self.main.lang_manager.get_string('Statistics', item)
            item_value = self.main.current_save['statistics'][item]

            self.statistics_listwidget.addItem('%s\n- %s' % (item_name, item_value))

        item_name = self.main.lang_manager.get_string('Statistics', 'enemy_clicks')
        for element in enumerate(self.main.current_save['statistics']['enemies_clicks']):
            enemy_name = self.main.lang_manager.get_string('Enemies', str(element[0]))

            format_item_name = item_name.format(enemy_name)
            item_value = element[1]

            self.statistics_listwidget.addItem('%s\n- %s' % (format_item_name, item_value))

    def fill_with_achievements(self, start_index=None, end_index=None):
        """Fill the QListWidget with player achievements progress"""
        self.achievements_listwidget.clear()
        self.achievement_info_viewer.clear()

        if start_index is None:
            start_index = 0

        if end_index is None:
            end_index = len(self.main.achievements_manager.achievements)

        selected_lang_code = self.main.lang_manager.selected_lang['LangInfo']['Code']
        for achievement in self.main.achievements_manager.achievements[start_index:end_index]:

            if selected_lang_code in achievement['info']['name']:
                achievement_name = achievement['info']['name'][selected_lang_code]
            else:
                achievement_name = achievement['info']['name']['en']

            item = QtWidgets.QListWidgetItem()
            item.setText(achievement_name)
            if achievement['id'] in self.main.current_save['completed_achievements']:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.main.resources['MISC']['CHECKMARK'])
                item.setIcon(QtGui.QIcon(pixmap))
            else:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(self.main.resources['MISC']['CROSSMARK'])
                item.setIcon(QtGui.QIcon(pixmap))

            self.achievements_listwidget.addItem(item)

    def show_default_achievements(self):
        """Update achievements menu for default achievements"""
        self.selected_achievements_type_view = 0

        default_achievements_count = self.main.achievements_manager.get_default_achievements_count()
        self.fill_with_achievements(end_index=default_achievements_count)

        completed_achievements_count = self.main.achievements_manager.get_completed_default_achievements_count()
        achievements_name = self.main.lang_manager.get_string('Other', 'Achievements')
        self.achievements_lbl.setText('%s %s/%s' % (
            achievements_name, completed_achievements_count, default_achievements_count))

        achievements_type_name = self.main.lang_manager.get_string('Gui', 'CustomAchievements')
        self.achievements_switch_btn.setText(achievements_type_name)

    def show_custom_achievements(self):
        """Update achievements menu for custom achievements"""
        self.selected_achievements_type_view = 1

        default_achievements_count = self.main.achievements_manager.get_default_achievements_count()
        self.fill_with_achievements(start_index=default_achievements_count)

        custom_achievements_count = len(self.main.achievements_manager.achievements) - default_achievements_count
        completed_achievements_count = self.main.achievements_manager.get_completed_custom_achievements_count()
        achievements_name = self.main.lang_manager.get_string('Other', 'Achievements')
        self.achievements_lbl.setText('%s %s/%s' % (
            achievements_name, completed_achievements_count, custom_achievements_count))

        achievements_type_name = self.main.lang_manager.get_string('Gui', 'DefaultAchievements')
        self.achievements_switch_btn.setText(achievements_type_name)

    def show_achievement_description(self, index):
        """Show achievement description in 'achievement_info_viewer' by achievement index"""
        if self.selected_achievements_type_view == 1:
            index += self.main.achievements_manager.get_default_achievements_count()

        achievement = self.main.achievements_manager.achievements[index]

        selected_lang_code = self.main.lang_manager.selected_lang['LangInfo']['Code']

        if selected_lang_code in achievement['info']['description']:
            achievement_description = achievement['info']['description'][selected_lang_code]
        else:
            achievement_description = achievement['info']['description']['en']

        self.achievement_info_viewer.setText(achievement_description)

    def set_random_gameplayBackground(self):
        """Set random background to gameplay screen"""
        new_pixmap = QtGui.QPixmap()
        new_pixmap.loadFromData(random.choice(self.main.resources['BACKGROUNDS']['GAMEPLAY']))

        self.gameplay_background.setPixmap(new_pixmap)

    # NAVIGATION METHODS #

    # START-SCREEN METHODS #

    def open_startScreen(self):
        """Open start-screen"""
        self.startScreen_menu_background.show()
        self.startScreen_background.show()
        self.startScreen_menu_logo.show()
        self.gameVersion_lbl.show()

        self.back_startScreen_menu()

        self.startScreen_background_gif.setPaused(False)

        self.startScreen_status = True

        self.main.discord_rpc.update_for_startScreen()

    def close_startScreen(self):
        """Close start-screen"""
        self.startScreen_menu_background.hide()
        self.startScreen_background.hide()
        self.startScreen_menu_logo.hide()
        self.gameVersion_lbl.hide()

        self.hide_startScreen_menu()
        self.hide_newGame_menu()
        self.hide_continueGame_menu()
        self.hide_settings_menu()
        self.hide_aboutGame_menu()

        self.startScreen_background_gif.setPaused(True)

        self.startScreen_status = False

    def show_startScreen_menu(self):
        """Show start-screen menu"""
        self.newGame_btn.show()
        self.continueGame_btn.show()
        self.settings_btn.show()
        self.mods_btn.show()
        self.quitGame_btn.show()
        self.aboutGame_btn.show()

    def hide_startScreen_menu(self):
        """Hide start-screen menu"""
        self.newGame_btn.hide()
        self.continueGame_btn.hide()
        self.settings_btn.hide()
        self.mods_btn.hide()
        self.quitGame_btn.hide()
        self.aboutGame_btn.hide()

    def show_newGame_menu(self):
        """Show menu for creating the new save"""
        self.saveName_lbl.show()
        self.saveName_edit.show()
        self.change_gamemode_btn.show()
        self.difficulty_lbl.show()
        self.change_difficulty_btn.show()
        self.create_save_btn.show()

        self.back_startScreen_menu_btn.show()

    def hide_newGame_menu(self):
        """Hide menu for creating the new save"""
        self.saveName_lbl.hide()
        self.saveName_edit.hide()
        self.change_gamemode_btn.hide()
        self.difficulty_lbl.hide()
        self.change_difficulty_btn.hide()
        self.create_save_btn.hide()

        self.back_startScreen_menu_btn.hide()

    def show_continueGame_menu(self):
        """Show menu for continue saves"""
        self.savesList_edit.show()
        self.continue_save_btn.show()
        self.change_save_btn.show()
        self.delete_save_btn.show()

        self.back_startScreen_menu_btn.show()

    def hide_continueGame_menu(self):
        """Hide menu for continue saves"""
        self.savesList_edit.hide()
        self.continue_save_btn.hide()
        self.change_save_btn.hide()
        self.delete_save_btn.hide()

        self.back_startScreen_menu_btn.hide()

    def show_changeSave_menu(self):
        """Show menu for changing the save"""
        self.saveName_lbl.show()
        self.saveName_edit.show()
        self.save_changedSave_btn.show()
        self.cancel_btn.show()

    def hide_changeSave_menu(self):
        """Hide menu for changing the save"""
        self.saveName_lbl.hide()
        self.saveName_edit.hide()
        self.save_changedSave_btn.hide()
        self.cancel_btn.hide()

    def show_deleteSave_menu(self):
        """Show menu for confirm save deleting"""
        self.deleteSave_warning_lbl.show()
        self.confirm_deleteSave_btn.show()
        self.cancel_btn.show()

    def hide_deleteSave_menu(self):
        """Hide menu for confirm save deleting"""
        self.deleteSave_warning_lbl.hide()
        self.confirm_deleteSave_btn.hide()
        self.cancel_btn.hide()

    def show_settings_menu(self):
        """Show settings-menu"""
        self.settings_lbl.show()
        self.language_lbl.show()
        self.language_combobox.show()
        self.background_changeDelay_lbl.show()
        self.background_changeDelay_spinbox.show()
        self.autosaving_checkbox.show()
        self.discord_rpc_checkbox.show()
        self.audio_settings_btn.show()

        self.back_startScreen_menu_btn.show()

    def hide_settings_menu(self):
        """Hide settings-menu"""
        self.settings_lbl.hide()
        self.language_lbl.hide()
        self.language_combobox.hide()
        self.background_changeDelay_lbl.hide()
        self.background_changeDelay_spinbox.hide()
        self.autosaving_checkbox.hide()
        self.discord_rpc_checkbox.hide()
        self.audio_settings_btn.hide()

        self.back_startScreen_menu_btn.hide()

    def show_audio_settings_menu(self):
        self.audio_settings_lbl.show()
        self.music_volume_lbl.show()
        self.music_volume_slider.show()
        self.sfx_volume_lbl.show()
        self.sfx_volume_slider.show()
        self.shuffle_music_checkbox.show()
        self.settings_skip_track_btn.show()
        self.back_settings_menu_btn.show()

    def hide_audio_settings_menu(self):
        self.audio_settings_lbl.hide()
        self.music_volume_lbl.hide()
        self.music_volume_slider.hide()
        self.sfx_volume_lbl.hide()
        self.sfx_volume_slider.hide()
        self.shuffle_music_checkbox.hide()
        self.settings_skip_track_btn.hide()
        self.back_settings_menu_btn.hide()

    def show_aboutGame_menu(self):
        self.aboutGame_lbl.show()

        self.back_startScreen_menu_btn.show()

    def hide_aboutGame_menu(self):
        self.aboutGame_lbl.hide()

        self.back_startScreen_menu_btn.hide()

    # GAMEPLAY SCREEN METHODS #

    def open_gameplay_screen(self):
        """Open gameplay screen"""
        self.show_gameplay_screen()

        self.enemy0.show()
        self.enemy1.show()
        self.enemy2.show()

        for enemy in self.main.enemylib.enemies:
            enemy.button.show()

        self.main.discord_rpc.update_for_gameplayScreen()

    def close_gameplay_screen(self):
        """Close gameplay screen"""
        self.hide_gameplay_screen()

        self.enemy0.hide()
        self.enemy1.hide()
        self.enemy2.hide()

        for enemy in self.main.enemylib.enemies:
            enemy.button.hide()

    def show_gameplay_screen(self):
        """Show gameplay GUI only"""
        self.gameplay_background.show()
        self.gameplay_bar_background.show()
        self.score_lbl.show()
        self.achievement_unlocked_notification.show()

    def hide_gameplay_screen(self):
        """Hide Gameplay GUI only"""
        self.gameplay_background.hide()
        self.gameplay_bar_background.hide()
        self.score_lbl.hide()
        self.achievement_unlocked_notification.hide()

    # PAUSE SCREEN METHODS #

    def open_pause_screen(self):
        """Open pause-screen"""
        self.pause_screen_background.show()
        self.pause_menu_background.show()
        self.pause_menu_title.show()
        self.now_playing_track_bar.show()
        self.now_playing_track_lbl.show()
        self.pauseScreen_skip_track_btn.show()

        self.back_pause_menu()

        self.pause_status = True

    def close_pause_screen(self):
        """Close pause-screen"""
        self.pause_screen_background.hide()
        self.pause_menu_background.hide()
        self.pause_menu_title.hide()
        self.now_playing_track_bar.hide()
        self.now_playing_track_lbl.hide()
        self.pauseScreen_skip_track_btn.hide()

        self.hide_pause_menu()
        self.hide_statistics_menu()
        self.hide_achievements_menu()

        self.pause_status = False

    def show_pause_menu(self):
        """Show pause-screen menu"""
        self.back_gameplay_btn.show()
        self.statistics_btn.show()
        self.achievements_btn.show()
        self.exit_gameplay_btn.show()

    def hide_pause_menu(self):
        """Hide pause-screen menu"""
        self.back_gameplay_btn.hide()
        self.statistics_btn.hide()
        self.achievements_btn.hide()
        self.exit_gameplay_btn.hide()

    def show_statistics_menu(self):
        self.statistics_listwidget.show()

        self.back_pauseScreen_menu_btn.show()

    def hide_statistics_menu(self):
        self.statistics_listwidget.hide()

        self.back_pauseScreen_menu_btn.hide()

    def show_achievements_menu(self):
        self.achievements_lbl.show()
        self.achievements_listwidget.show()
        self.achievement_info_viewer.show()
        self.achievements_switch_btn.show()

        self.back_pauseScreen_menu_btn.show()

    def hide_achievements_menu(self):
        self.achievements_lbl.hide()
        self.achievements_listwidget.hide()
        self.achievement_info_viewer.hide()
        self.achievements_switch_btn.hide()

        self.back_pauseScreen_menu_btn.hide()
