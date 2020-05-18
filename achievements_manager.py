"""
SHEYMOSU ACHIEVEMENTS MANAGER

SUPPORTED ACHIEVEMENT TRIGGERS (GOALS):
- time
- earned_points
- lost_points
- clicks_count
- miss_clicks
- clicked_enemies
- enemies_clicks
- time_since_enemy_click
- time_since_miss_click

ACHIEVEMENT EXAMPLE:
{
    "goals": {
        "earned_points": 100
    },
    "total_goals": {},
    "reset": {
        "miss_clicks": 1
    },
    "info": {
        "name": {
            "en": "Earn points",
            "ru": "Заработать очков"
        },
        "description": {
            "en": "Earn 100 points without miss clicks",
            "ru": "Заработать 100 очков не промахнувшись"
        }
    },
    "id": "<RANDOM 25 ASCII-CHARACTER ID>"
}
"""

import json
import os

from PyQt5 import QtCore, QtMultimedia

from default_achievements import DEFAULT_ACHIEVEMENTS, DEFAULT_ACHIEVEMENT_IDS

CUSTOM_ACHIEVEMENTS_DIR = 'userdata/achievements/'

class AchievementsManager:

    def __init__(self, main):
        self.main = main
        self.achievements = self._load_achievements()

        file_url = QtCore.QUrl.fromLocalFile('resources/sounds/achievement_unlocked.mp3')
        achievement_sound = QtMultimedia.QMediaContent(file_url)
        self.main.audio.notifications_player.setMedia(achievement_sound)

        self.main.logger.info('ACHIEVEMENTS_MANAGER INITIALISED')

    def check_progress(self):
        for achievement in self.achievements:

            if achievement['id'] in self.main.current_save['completed_achievements']:
                continue

            completed_goals = []
            for goal_name in achievement['goals']:

                if isinstance(achievement['goals'][goal_name], list):
                    for e1, e2 in zip(achievement['goals'][goal_name], 
                                      achievement['progress'][goal_name]):
                        if e1 <= e2:
                            pass
                        else:
                            break
                    else:
                        completed_goals.append(goal_name)

                elif achievement['goals'][goal_name] <= achievement['progress'][goal_name]:
                    completed_goals.append(goal_name)

            for goal_name in achievement['total_goals']:

                if goal_name == 'score':
                    if achievement['total_goals']['score'] <= self.main.current_save['score']:
                        completed_goals.append(goal_name)

                elif isinstance(achievement['total_goals'][goal_name], list):
                    for e1, e2 in zip(achievement['total_goals'][goal_name],
                                      self.main.current_save['statistics'][goal_name]):
                        if e1 <= e2:
                            continue
                        else:
                            break
                    else:
                        completed_goals.append(goal_name)

                elif achievement['total_goals'][goal_name] <= self.main.current_save['statistics'][goal_name]:
                    completed_goals.append(goal_name)

            if len(completed_goals) == len(achievement['goals']) + len(achievement['total_goals']):
                self.main.current_save['completed_achievements'].append(achievement['id'])
                self.main.events.achievement_unlocked()

    def update_progress(self, goal, added_value, list_index=None):
        for achievement in self.achievements:

            if achievement['id'] in self.main.current_save['completed_achievements']:
                continue

            if goal not in achievement['progress']:
                continue

            if goal.startswith('time_since_'):
                if achievement['progress'][goal] is None:
                    if added_value == True:
                        achievement['progress'][goal] = 0.0
                else:
                    if isinstance(added_value, float):
                        updated_value = round(achievement['progress'][goal] + added_value, 1)
                        achievement['progress'][goal] = updated_value

            elif list_index is None:
                if isinstance(added_value, float):
                    updated_value = round(achievement['progress'][goal] + added_value, 1)
                    achievement['progress'][goal] = updated_value
                else:
                    achievement['progress'][goal] += added_value

            else:
                achievement['progress'][goal][list_index] += added_value

            if goal in achievement['reset']:

                if goal.startswith('time_since_'):

                    if achievement['progress'][goal] is None:
                        continue

                    if achievement['progress'][goal] >= achievement['reset'][goal]:
                        achievement['progress'] = self.reset_achievement_progress(achievement['goals'], achievement['reset'])

                elif list_index is not None:
                    for e1, e2 in zip(achievement['reset'][goal], achievement['progress'][goal]):
                        if e1 <= e2:
                            pass
                        else:
                            break
                    else:
                        achievement['progress'] = self.reset_achievement_progress(achievement['goals'], achievement['reset'])

                elif achievement['progress'][goal] >= achievement['reset'][goal]:
                    achievement['progress'] = self.reset_achievement_progress(achievement['goals'], achievement['reset'])

        self.check_progress()

    def reset_progress(self):
        for achievement in self.achievements:
            achievement['progress'] = self.reset_achievement_progress(achievement['goals'], achievement['reset'])

    def reset_achievement_progress(self, achievement_goals, achievement_reset_goals):
        items = set(tuple(achievement_goals.keys()) + tuple(achievement_reset_goals.keys()))
        progress = {}
        for item in items:
            if item == 'enemies_clicks':
                progress[item] = [0, 0, 0]
            elif item.startswith('time_since_'):
                progress[item] = None
            else:
                progress[item] = 0

        return progress

    def get_default_achievements_count(self):
        return len(DEFAULT_ACHIEVEMENTS)

    def get_completed_default_achievements_count(self):
        achievements_count = 0
        for achievement in self.achievements[:len(DEFAULT_ACHIEVEMENTS)]:
            if achievement['id'] in self.main.current_save['completed_achievements']:
                achievements_count += 1

        return achievements_count

    def get_completed_custom_achievements_count(self):
        achievements_count = 0
        for achievement in self.achievements[len(DEFAULT_ACHIEVEMENTS):]:
            if achievement['id'] in self.main.current_save['completed_achievements']:
                achievements_count += 1

        return achievements_count

    def _load_achievements(self):
        custom_achievements = self.load_custom_achievements()
        achievements = list(DEFAULT_ACHIEVEMENTS) + custom_achievements

        for achievement in achievements:
            achievement['progress'] = self.reset_achievement_progress(achievement['goals'], achievement['reset'])

        self.main.logger.info('%s ACHIEVEMENTS LOADED', len(achievements))

        return achievements

    def load_custom_achievements(self):
        custom_achievements = []

        if not os.path.exists(CUSTOM_ACHIEVEMENTS_DIR):
            return []

        for filename in os.listdir(CUSTOM_ACHIEVEMENTS_DIR):
            filepath = CUSTOM_ACHIEVEMENTS_DIR + filename

            if os.path.isfile(filepath) and filepath.endswith('.json'):
                try:
                    with open(filepath, 'r') as file:
                        custom_achievement = json.load(file)

                    if 'en' not in custom_achievement['info']['name']:
                        continue
                    if 'en' not in custom_achievement['info']['description']:
                        continue

                    if custom_achievement['id'] not in DEFAULT_ACHIEVEMENT_IDS:
                        custom_achievements.append(custom_achievement)

                except Exception as e:
                    self.main.logger.error('FAILED TO LOAD ACHIEVEMENT FROM %s: %s', filename, e)

        self.main.logger.info('%s CUSTOM ACHIEVEMENTS LOADED', len(custom_achievements))

        return custom_achievements
