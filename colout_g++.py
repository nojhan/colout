
def theme():
    return [
        [ "error", "red", "bold" ],
        [ "warning", "magenta", "bold" ],
        [ "\[-W.*\]", "magenta", "normal" ],
        [ "note", "blue", "bold" ],
        [ ":([0-9]+):[0-9]*", "yellow", "normal" ],
        [ "^((/\w+)+)\.(h|cpp)", "white", "normal" ],
        [ "'(.*)'", "Cpp", "monokai" ],
    ]

