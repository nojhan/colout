#encoding: utf-8

def theme(context):
    style="monokai"
    return context,[
            [ r"^(.*\.java):([0-9]+):\s*(warning:.*)$", "white,yellow,magenta", "normal,normal,bold" ],
            [ r"^(.*\.java):([0-9]+):(.*)$", "white,yellow,red", "normal,normal,bold" ],
            [ r"^(symbol|location)\s*:\s*(.*)$", "blue,Java", "bold,"+style ],
            [ r"^(found)\s*:\s*(.*)", "red,Java", "bold,"+style ],
            [ r"^(required)\s*:\s*(.*)", "green,Java", "bold,"+style ],
            [ r"^\s*\^$", "cyan", "bold" ],
            [ r"^\s+.*$", "Java", style ],
            [ "[0-9]+ error[s]*", "red", "bold" ],
            [ "[0-9]+ warning[s]*", "magenta", "bold" ],
        ]
