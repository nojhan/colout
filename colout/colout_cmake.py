
def theme(context):
    # CMake theme:
    #  actions performing in cyan
    performing="cyan"
    #  actions performed in green
    performed="green"
    #  actions taking an unknown time
    untimed="blue"

    # If the user do not ask for his own colormap
    if not context["user_defined_colormaps"]:
        # A palette that goes: purple, orange, white
        percs = [45, 39, 33, 27, 21, 57, 63, 62, 98, 97, 133, 132, 138, 173, 172, 208, 214, 220, 226, 228, 229, 230, 231, 255]
        context["colormaps"]["Scale"] = percs

    return context,[
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
        [ "CMake Error", "red" ],
        [ "CMake Warning", "magenta" ],
        [ "CMake Deprecation Warning", "magenta" ],
        # Scan
        [ "^(Scanning dependencies of target)(.*)$",
          performing, "normal,bold" ],
        # Link (make)
        # [ "^(Linking .* )(library|executable) (.*/)*(.+(\.[aso]+)*)$",
        [ "^(Linking .* )(library|executable) (.*)$",
          untimed, "normal,normal,bold" ],
        # [percent] Creating something
        [ r"^\[\s*[0-9/]+%?\]\s(.*Creating.*)$",
          performing, "normal" ],
        # [percent] Built
        [ r"^\[\s*[0-9/]+%?\]\s(Built target)(\s.*)$",
          performed, "normal,bold" ],
        # [percent] Building
        [ r"^\[\s*[0-9/]+%?\]\s(Building \w* object)\s+(.*)(\.dir)(.*/)([-\w]+).c.*.o$",
            performing+","+performing+","+performing+",Hash,"+performing, "normal,normal,normal,normal,bold"],
        # [percent] Generating
        [ r"^\[\s*[0-9/]+%?\]\s(Generating)(\s+.*)$",
            performing, "normal,bold"],
        # make errors
        [ r"make\[[0-9]+\].*", "yellow"],
        [ r"(make: \*\*\* \[.+\] )(.* [0-9]+)", "red", "normal,bold"],
        # progress percentage (make)
        [ r"^(\[\s*[0-9]+%\])","Scale" ]
    ]
