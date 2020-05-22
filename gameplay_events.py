import random

from PyQt5 import QtCore, QtMultimedia
from enemylib import DEFAULT_ENEMY_MAX_ID

class GameplayEvents:

    def __init__(self, main):
        self.main = main

        self.gameplay_timer = QtCore.QTimer()
        self.gameplay_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.gameplay_timer.setInterval(100)
        self.gameplay_timer.timeout.connect(self.gameplayTick)

        self.autosaving_timer = QtCore.QTimer()
        self.autosaving_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.autosaving_timer.setInterval(self.main.settings['autosaving_delay'])
        self.autosaving_timer.timeout.connect(self.main.overwrite_saves)

        self.achievement_animation_timer = QtCore.QTimer()
        self.achievement_animation_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.achievement_animation_timer.setInterval(2000)
        self.achievement_animation_timer.timeout.connect(self.hide_achievement_notification)

        self.show_achievement_animation = QtCore.QPropertyAnimation(self.main.gui.achievement_unlocked_notification, b'geometry')
        self.show_achievement_animation.setDuration(800)
        self.show_achievement_animation.setStartValue(QtCore.QRect(1280, 0, 410, 80))
        self.show_achievement_animation.setEndValue(QtCore.QRect(910, 0, 410, 80))
        self.show_achievement_animation.setEasingCurve(QtCore.QEasingCurve.OutBack)
        self.show_achievement_animation.finished.connect(self.achievement_animation_timer.start)

        self.hide_achievement_animation = QtCore.QPropertyAnimation(self.main.gui.achievement_unlocked_notification, b'geometry')
        self.hide_achievement_animation.setDuration(800)
        self.hide_achievement_animation.setStartValue(QtCore.QRect(910, 0, 410, 80))
        self.hide_achievement_animation.setEndValue(QtCore.QRect(1280, 0, 410, 80))
        self.hide_achievement_animation.setEasingCurve(QtCore.QEasingCurve.InOutBack)

        file_url = QtCore.QUrl.fromLocalFile('resources/sounds/enemy_click.mp3')
        enemy_click_sound = QtMultimedia.QMediaContent(file_url)
        self.main.audio.sfx_player.setMedia(enemy_click_sound)

        self.backgroundTime = 0
        self.enemy0_time = 0
        self.enemy1_time = 0
        self.enemy2_time = 0

        self.main.gui.enemy0.clicked.connect(self.enemy0_clicked)
        self.main.gui.enemy1.clicked.connect(self.enemy1_clicked)
        self.main.gui.enemy2.clicked.connect(self.enemy2_clicked)

        self.main.logger.info('EVENTS CLASS INITIALISED')

    def setup_custom_enemy_clicks(self):
        for enemy in self.main.enemylib.enemies:
            enemy.button.clicked.connect(enemy.clickevent)

    def enemy0_clicked(self):
        self.add_points(enemy_id=0)

        self.update_stats_for_enemy_click(enemy_id=0)
        self.main.gui.enemy0.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemy0_time = 0

        self.main.audio.sfx_player.play()

    def enemy1_clicked(self):
        self.add_points(enemy_id=1)

        self.update_stats_for_enemy_click(enemy_id=1)
        self.main.gui.enemy1.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemy1_time = 0

        self.main.audio.sfx_player.play()

    def enemy2_clicked(self):
        self.add_points(enemy_id=2)

        self.update_stats_for_enemy_click(enemy_id=2)
        self.main.gui.enemy2.move(random.randint(20, 1200), random.randint(20, 550))

        self.enemy2_time = 0

        self.main.audio.sfx_player.play()

    def gameplayTick(self):
        updated_timePlayed = round(self.main.current_save['statistics']['time_played'] + 0.1, 1)
        self.main.current_save['statistics']['time_played'] = updated_timePlayed
        self.backgroundTime = round(self.backgroundTime + 0.1, 1)
        self.enemy0_time = round(self.enemy0_time + 0.1, 1)
        self.enemy1_time = round(self.enemy1_time + 0.1, 1)
        self.enemy2_time = round(self.enemy2_time + 0.1, 1)

        for enemy in self.main.enemylib.enemies:
            enemy.time = round(enemy.time + 0.1, 1)

        self.main.achievements_manager.update_progress('time', 0.1)
        self.main.achievements_manager.update_progress('time_since_miss_click', 0.1)
        self.main.achievements_manager.update_progress('time_since_enemy_click', 0.1)

        if self.backgroundTime >= self.main.settings['background_change_delay']:
            self.main.gui.set_random_gameplayBackground()
            self.backgroundTime = 0

        if self.enemy0_time >= self.main.current_difficulty['ENEMIES_TIMEOUTS'][0]:
            self.main.gui.enemy0.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemy0_time = 0

        if self.enemy1_time >= self.main.current_difficulty['ENEMIES_TIMEOUTS'][1]:
            self.main.gui.enemy1.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemy1_time = 0

        if self.enemy2_time >= self.main.current_difficulty['ENEMIES_TIMEOUTS'][2]:
            self.main.gui.enemy2.move(random.randint(20, 1200), random.randint(20, 550))
            self.enemy2_time = 0

        for enemy in self.main.enemylib.enemies:
            if enemy.time >= enemy.timeout:
                enemy.button.move(random.randint(20, 1200), random.randint(20, 550))
                enemy.time = 0

        self.main.hookslib.call("onTick")

    def add_points(self, enemy_id):
        if enemy_id <= DEFAULT_ENEMY_MAX_ID:
            added_points = self.main.current_difficulty['ENEMIES_SCORES'][enemy_id]
        else:
            for enemy in self.main.enemylib.enemies:
                if enemy.id == enemy_id:
                    added_points = enemy.pts
                    break

        if not added_points:
            return

        newpts = self.main.hookslib.call("onAddPoints", enemy_id, added_points)
        if newpts:
            added_points = newpts

        self.main.current_save['score'] += added_points
        self.main.current_save['statistics']['earned_points'] += added_points
        self.main.achievements_manager.update_progress('earned_points', added_points)

        self.update_score()

    def lose_points(self):
        lost_points = self.main.current_difficulty['LOSING_POINTS']

        newpts = self.main.hookslib.call("onLosePoints", lost_points)
        if newpts:
            lost_points = newpts

        self.main.current_save['statistics']['lost_points'] += lost_points
        self.main.current_save['statistics']['total_clicks'] += 1
        self.main.current_save['statistics']['miss_clicks'] += 1
        self.main.current_save['score'] -= lost_points
        self.main.achievements_manager.update_progress('lost_points', lost_points)
        self.main.achievements_manager.update_progress('clicks_count', lost_points)
        self.main.achievements_manager.update_progress('miss_clicks', lost_points)
        self.main.achievements_manager.update_progress('time_since_miss_click', True)

        self.update_score()

    def update_score(self):
        score_name = self.main.lang_manager.get_string('Other', 'Score')
        self.main.gui.score_lbl.setText('%s: %s' % (score_name, self.main.current_save['score']))

    def update_stats_for_enemy_click(self, enemy_id):
        if enemy_id <= DEFAULT_ENEMY_MAX_ID:
            self.main.current_save['statistics']['enemies_clicks'][enemy_id] += 1
        self.main.current_save['statistics']['total_clicks'] += 1
        if enemy_id <= DEFAULT_ENEMY_MAX_ID:
            self.main.achievements_manager.update_progress('enemies_clicks', 1, list_index=enemy_id)
        self.main.achievements_manager.update_progress('clicked_enemies', 1)
        self.main.achievements_manager.update_progress('time_since_enemy_click', True)

    def achievement_unlocked(self):
        self.show_achievement_animation.start()
        self.main.audio.notifications_player.play()
        self.main.logger.info('GAMEPLAY: ACHIEVEMENT UNLOCKED')

    def hide_achievement_notification(self):
        self.achievement_animation_timer.stop()
        self.hide_achievement_animation.start()
