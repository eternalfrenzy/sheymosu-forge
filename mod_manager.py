import os

from base_mod import *

MODS_DIR = "userdata/mods"

class ModManager:

    def __init__(self, main):
        self.mods = []
        self.main = main

    def run_mods(self):
        for m in self.mods:
            m.run_code()

            if not m.is_invalid:
                m.enable()

    def get_modlist(self):
        modfiles = []
        if os.path.exists(MODS_DIR):
            for file in os.listdir(MODS_DIR):
                if os.path.isfile(os.path.join(MODS_DIR, file)):
                    modfiles.append(file)
        
        for f in modfiles:
            fi = open(MODS_DIR+"/%s" % f, "r", encoding="utf-8")
            code = fi.read()
            fi.close()

            mod = BaseMod(code, self.main)
            self.mods.append(mod)