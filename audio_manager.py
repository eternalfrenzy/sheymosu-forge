import os
import random

from PyQt5 import QtCore, QtMultimedia

MUSIC_DIR = 'userdata/music'

class GameAudio:

    def __init__(self, main):
        self.main = main
        self.music_player = QtMultimedia.QMediaPlayer()
        self.sfx_player = QtMultimedia.QMediaPlayer()
        self.notifications_player = QtMultimedia.QMediaPlayer()

        self.music_player.stateChanged.connect(self._musicPlayer_state_changed)

        self.main.logger.info('GAME_AUDIO CLASS INITIALISED')

    def play_music(self):
        tracklist = self.get_music_tracklist()

        if not tracklist:
            return

        if self.main.settings['audio']['shuffle_music']:
            track_name = random.choice(tracklist)
        else:
            track_name = tracklist[0]

        file_url = QtCore.QUrl.fromLocalFile(os.path.join(MUSIC_DIR, track_name))
        track = QtMultimedia.QMediaContent(file_url)
        self.main.logger.info('AUDIO TRACK %s LOADED', track_name)

        self.music_player.setMedia(track)
        self.music_player.play()

    def play_next_track(self):
        tracklist = self.get_music_tracklist()

        if not tracklist:
            return

        if self.main.settings['audio']['shuffle_music']:
            while True:
                newTrack_name = random.choice(tracklist)

                if not self.main.settings['audio']['track_repeat_chance']:

                    if len(tracklist) == 1:
                        break

                    if self.music_player.media().canonicalUrl().fileName() == newTrack_name:
                        continue
                break

        else:
            current_track = self.music_player.media().canonicalUrl().fileName()
            try:
                current_track_index = tracklist.index(current_track)
                if current_track_index == len(tracklist) - 1:
                    newTrack_name = tracklist[0]
                else:
                    newTrack_name = tracklist[current_track_index + 1]
            except IndexError:
                newTrack_name = tracklist[0]

        file_url = QtCore.QUrl.fromLocalFile(os.path.join(MUSIC_DIR, newTrack_name))
        new_track = QtMultimedia.QMediaContent(file_url)
        self.main.logger.info('AUDIO TRACK %s LOADED', newTrack_name)

        self.music_player.setMedia(new_track)
        self.music_player.play()

    def skip_track(self):
        if self.music_player.state() == 0:
            self.play_next_track()
        else:
            self.music_player.stop()

    def _musicPlayer_state_changed(self, state):
        if state == 0:
            self.main.gui.now_playing_track_lbl.setText('')
            self.play_next_track()

        if state == 1:
            current_trackName = self.music_player.media().canonicalUrl().fileName()
            fmt_now_playing_info = self.main.lang_manager.get_string('Gui', 'NowPlaying').format(current_trackName)

            self.main.gui.now_playing_track_lbl.setText(fmt_now_playing_info)

    def get_music_tracklist(self):
        tracklist = []
        if os.path.exists(MUSIC_DIR):
            for file in os.listdir(MUSIC_DIR):
                if os.path.isfile(os.path.join(MUSIC_DIR, file)):
                    tracklist.append(file)

        tracklist.sort()

        return tracklist
