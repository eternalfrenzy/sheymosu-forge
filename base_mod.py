import lupa
from lupa import LuaRuntime
from hookslib import _HooksLibInterface
from enemylib import _EnemyLibInterface

class BaseMod:

    def __init__(self, code, main):
        self.code = code
        self.main = main
        self.name = "Unknown"
        self.desc = "Generic mod"
        self.version = "1.0"
        self.lua_state = LuaRuntime(unpack_returned_tuples=True)
        self.is_invalid = False
        self.enabled = False
        self.exception = None

    def add_libs(self):
        hooks = _HooksLibInterface()
        hooks.add = self.main.hookslib.add
        hooks.remove = self.main.hookslib.remove
        hooks.get = self.main.hookslib.get
        hooks.call = self.main.hookslib.call

        enemy = _EnemyLibInterface()
        enemy.add = self.main.enemylib.add
        enemy.getById = self.main.enemylib.getById
        enemy.getByName = self.main.enemylib.getByName
        enemy.removeById = self.main.enemylib.removeById
        enemy.removeByName = self.main.enemylib.removeByName

        self.lua_state.globals().enemy = enemy
        self.lua_state.globals().hooks = hooks

    def run_code(self):
        self.add_libs()

        try:
            self.lua_state.execute(self.code)
        except Exception as e:
            self.main.logger.error("Mod %s caused an exception: %s", self.name, e)
            self.exception = e
            self.is_invalid = True
            self.enabled = False
            return

        self.validate()

    def validate(self):
        if not self.lua_state.globals().MOD_DATA:
            self.is_invalid = True
            self.exception = "The 'MOD_DATA' constant was not declared."
        if not self.lua_state.globals().MOD_DATA["onEnable"]:
            self.is_invalid = True
            self.exception = "'onEnable' field in MOD_DATA is abscent or nil."
        if not self.lua_state.globals().MOD_DATA["onDisable"]:
            self.is_invalid = True
            self.exception = "'onDisable' field in MOD_DATA is abscent or nil."
        if not self.lua_state.globals().MOD_DATA["name"]:
            self.is_invalid = True
            self.exception = "'name' field in MOD_DATA is abscent or nil."
        else:
            self.name = self.lua_state.globals().MOD_DATA["name"]

        if self.is_invalid:
            self.enabled = False

        if self.lua_state.globals().MOD_DATA["description"]:
            self.desc = self.lua_state.globals().MOD_DATA["description"]

        if self.lua_state.globals().MOD_DATA["version"]:
            self.version = self.lua_state.globals().MOD_DATA["version"]

    def enable(self):
        if self.is_invalid or self.enabled:
            return

        try:
            self.lua_state.globals().MOD_DATA["onEnable"]()
        except Exception as e:
            pass
        
        self.enabled = True

    def disable(self):
        if self.is_invalid or not self.enabled:
            return

        try:
            self.lua_state.globals().MOD_DATA["onDisable"]()
        except Exception as e:
            pass

        self.enabled = False