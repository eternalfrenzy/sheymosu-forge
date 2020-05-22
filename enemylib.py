import random

DEFAULT_ENEMY_MAX_ID = 2
ENEMY_TEXTURE_PATH = "userdata/mods/resources/"

class EnemyObj:

    def __init__(self, main, id, name, pts, texture, timeout):
        self.main = main
        self.id = id
        self.name = name
        self.pts = pts
        self.texture = ENEMY_TEXTURE_PATH+texture
        self.timeout = timeout

        self.time = 0
        self.button = None

    def clickevent(self):
        self.main.events.add_points(enemy_id=self.id)

        self.main.events.update_stats_for_enemy_click(enemy_id=self.id)
        self.button.move(random.randint(20, 1200), random.randint(20, 550))

        self.time = 0

        self.main.audio.sfx_player.play()

class EnemyLib:

    def __init__(self, main):
        self.enemies = []
        self.main = main
    
    def add(self, name, pts, texture, timeout):
        newid = DEFAULT_ENEMY_MAX_ID + len(self.enemies) + 1
        enemy = EnemyObj(self.main, newid, name, pts, texture, timeout)
        self.enemies.append(enemy)
        return enemy

    def removeByName(self, name):
        pass

    def removeById(self, id):
        pass

    def getByName(self, name):
        pass

    def getById(self, id):
        pass

class _EnemyLibInterface: # This is exposed to lua

    add = None
    removeByName = None
    removeById = None
    getByName = None
    getById = None