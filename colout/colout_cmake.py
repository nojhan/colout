
def theme():
    # CMake theme:
    #  actions performing in cyan
    performing="cyan"
    #  actions performed in green
    performed="green"

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
        # Link
        [ "^(Linking .* )(library|executable) (.*/)+(.+(\.[aso]+)*)$",
          performing, "normal,normal,bold" ],
        # [percent] Built
        [ "^\[\s*[0-9]+%\]\s(Built target)(\s.*)$",
          performed, "normal,bold" ],
        # [percent] Building
        [ "^\[\s*[0-9]+%\]\s(Building \w* object)(\s+.*/)([-\w]+.c.*)(.o)$",
            performing, "normal,normal,bold,normal"],
        # make errors
        [ "make\[[0-9]+\].*", "yellow"],
        [ "(make: \*\*\* \[.+\] )(.* [0-9]+)", "red", "normal,bold"],
        # progress percentage
        [ "^\[\s*([0-9]+)%\]","Scale" ]
    ]
