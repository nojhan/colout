
def theme():
    # CMake theme:
    #  actions performing in cyan
    performing="cyan"
    #  actions performed in green
    performed="green"
    #  actions taking an unknown time
    untimed="blue"

    return [
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
        # Link (make)
        [ "^(Linking .* )(library|executable) (.*/)*(.+(\.[aso]+)*)$",
          untimed, "normal,normal,bold" ],
        # Link (ninja)
        [ "^\[[0-9/]+\]\s?(Linking .* )(library|executable) (.*/)*(.+(\.[aso]+)*)$",
          untimed, "normal,normal,bold" ],
        # [percent] Built
        [ "^\[\s*[0-9/]+%?\]\s(Built target)(\s.*)$",
          performed, "normal,bold" ],
        # [percent] Building
        [ "^\[\s*[0-9/]+%?\]\s(Building \w* object)(\s+.*/)([-\w]+.c.*)(.o)$",
            performing, "normal,normal,bold,normal"],
        # [percent] Generating
        [ "^\[\s*[0-9/]+%?\]\s(Generating)(\s+.*)$",
            performing, "normal,bold"],
        # make errors
        [ "make\[[0-9]+\].*", "yellow"],
        [ "(make: \*\*\* \[.+\] )(.* [0-9]+)", "red", "normal,bold"],
        # progress percentage (make)
        [ "^(\[\s*[0-9]+%\])","Scale" ],
        # progress percentage (ninja)
        [ "^(\[[0-9]+/[0-9]+\])","Scale" ]
    ]
