
def theme():
    # CMake theme:
    #  actions performing in cyan
    performing="cyan"
    #  actions performed in green
    performed="green"

    th = [
        # Configure...
        [ "^--.*works", performed ],
        [ "^--.*done", performed ],
        [ "^-- Found.*NO", "red" ],
        [ "^-- Found.*", performed ],
        [ "^--.*broken", "red" ],
        [ "^-- Coult NOT find.*", "red" ],
        [ "^-- Configuring incomplete, errors occurred!", "red" ],
        [ "^--.*", performing ],
        # Errors
        [ "CMake Error:", "red" ],
        [ "CMake Warning", "yellow" ],
        # Scan
        [ "^(Scanning dependencies of target)(.*)$",
          performing, "normal,bold" ],
        # Link
        [ "^(Linking .* (library|executable) )(.*/)+(.+(\.[aso]+)*)$",
          performing, "normal,normal,bold" ],
        # [percent] Built
        [ "^\[\s*[0-9]+%\]\s(Built target)(\s.*)$",
          performed, "normal,bold" ],
        # [percent] Building
        [ "^\[\s*[0-9]+%\]\s(Building \w* object)(\s.*/)(\w+.c.*)(.o)$",
            performing, "normal,normal,bold,normal"],
        # make errors
        [ "make\[[0-9]+\].*", "yellow"],
        [ "(make:.*)(Error [0-9]+)", "red", "normal,bold"]
    ]

    # Percentages: rainbow from magenta to red, depending on the number
    percs={
            "\s":("magenta","normal"),
            "1":("magenta","normal"),
            "2":("magenta","normal"),
            "3":("blue","normal"),
            "4":("blue","normal"),
            "5":("cyan","normal"),
            "6":("cyan","normal"),
            "7":("green","normal"),
            "8":("yellow","normal"),
            "9":("red","normal"),
            "10":("red","bold"),
            }
    for p in percs:
        th.append( [ "^(\[)\s*("+p+"[0-9]%)(\])", "black,"+percs[p][0]+",black", percs[p][1] ] )

    return th
