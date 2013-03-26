
def theme():
    return [
        [ "(fatal )*(error)", "red", "bold" ],
        [ "warning", "magenta", "bold" ],
        [ "note", "blue", "bold" ],
        # [-Wflag]
        [ "\[-W.*\]", "magenta"],
        # Filename:line number
        [ "(/.*?)/([^/]+\.)(h|cp*):([0-9]+):*[0-9]*(.*)", "white,white,white,yellow,none", "normal,bold,bold,normal"],
        # source code in single quotes
        [ "'(.*)'", "Cpp", "monokai" ]
    ]

