#encoding: utf-8

def theme(context):
    style="monokai"
    return context,[
            [ "^(.*\.java):([0-9]+):\s*(warning:.*)$", "white,yellow,magenta", "normal,normal,bold" ],
            [ "^(.*\.java):([0-9]+):(.*)$", "white,yellow,red", "normal,normal,bold" ],
            [ "^(symbol|location)\s*:\s*(.*)$", "blue,Java", "bold,"+style ],
            [ "^(found)\s*:\s*(.*)", "red,Java", "bold,"+style ],
            [ "^(required)\s*:\s*(.*)", "green,Java", "bold,"+style ],
            [ "^\s*\^$", "cyan", "bold" ],
            [ "^\s+.*$", "Java", style ],
            [ "[0-9]+ error[s]*", "red", "bold" ],
            [ "[0-9]+ warning[s]*", "magenta", "bold" ],
        ]
