![SheymOsu](https://img.shields.io/badge/SheymOsu-Pre--Beta%200.5.1-orange) ![Forge](https://img.shields.io/badge/Forge-0.0.1-red)

# The best game on PyQT ever, now with mod support!
Sheymosu Forge (registered trademark by the laws of United States of America) introduses lua scripting api. Currently WIP.
Will update readme when the barebones are ready.

# An example mod

```
MOD_DATA = {}
MOD_DATA["name"] = "Leet mod" -- Necessary field
MOD_DATA["version"] = "1.3.3.7" -- Optional field
MOD_DATA["description"] = "It does cool stuff" -- Optional field

function onAddPointsHandler(args)
    enemyid = args[0]
    pointstoadd = args[1]

    print("You just killed an enemy id ", enemyid, ", and got ", pointstoadd, " points.")
end

function onEnable()
    print("enable")
    hooks.add("onAddPoints", MOD_DATA["name"].."onAddPoints", onAddPointsHandler) -- aka event handlers
    enemy.add("clown", 30, "myenemy.jpg", 2) -- The actual path to the texture is: <game executable>/userdata/resources/myenemy.jpg.
    enemy.add("frenzy", 100, "frenzy.jpg", 0.5) -- Fast AF boiiiiiiiiiiii
end
MOD_DATA["onEnable"] = onEnable -- Let the mod know. Both onEnable and onDisable fields are necessary.

function onDisable()
    print("disable")
    hooks.remove("onAddPoints", MOD_DATA["name"].."onAddPoints")
end
MOD_DATA["onDisable"] = onDisable
```
