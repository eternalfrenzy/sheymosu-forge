import lupa
from lupa import LuaRuntime

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

    def run_code(self):
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

        if self.is_invalid:
            self.enabled = False
            return

        self.name = self.lua_state.globals().MOD_DATA["name"]
        
        if self.lua_state.globals().MOD_DATA["description"]:
            self.desc = self.lua_state.globals().MOD_DATA["description"]

        if self.lua_state.globals().MOD_DATA["version"]:
            self.version = self.lua_state.globals().MOD_DATA["version"]

    def enable(self):
        if self.is_invalid or self.enabled:
            return

        self.lua_state.globals().MOD_DATA["onEnable"]()
        self.enabled = True

    def disable(self):
        if self.is_invalid or not self.enabled:
            return

        self.lua_state.globals().MOD_DATA["onDisable"]()
        self.enabled = False