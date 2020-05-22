class HookObj:

    def __init__(self, eventname, identifier, handlerfunc):
        self.handlerfunc = handlerfunc
        self.eventname = eventname
        self.identifier = identifier

class HooksLib:

    def __init__(self, main):
        self.hooks = []
        self.main = main

    def add(self, eventname, identifier, handlerfunc):
        h = HookObj(eventname, identifier, handlerfunc)
        self.hooks.append(h)
        return h

    def remove(self, eventname, identifier):
        for h in self.hooks:
            if h.eventname == eventname and h.identifier == identifier:
                self.hooks.remove(h)

    def call(self, eventname, *varargs):
        for h in self.hooks:
            if h.eventname == eventname:
                try:
                    return h.handlerfunc(varargs)
                except Exception as e:
                    self.main.logger.error("Hook %s of event %s caused an exception: %s", h.identifier, h.eventname, e)

    def get(self, eventname, identifier):
        returnstuff = []

        for h in self.hooks:
            if h.eventname == eventname and h.identifier == identifier:
                returnstuff.append(h)

        if len(returnstuff) == 1:
            return returnstuff[0]
        elif len(returnstuff) <= 0:
            return None
        else:
            return returnstuff

class _HooksLibInterface: # This is exposed to lua

    add = None
    remove = None
    call = None
    get = None