
def theme():
    th = [
        [ "^(Scanning dependencies of target)(.*)$",
          "magenta,blue", "normal,bold" ],
        [ "^(Linking \w+ \w+ library)(\s.*/)(\w+.[aso]+)$",
          "magenta", "normal,normal,bold" ],
        [ "^\[\s*[0-9]+%\]\s(Built target)(\s.*)$",
          "cyan,blue", "normal,bold" ],
        [ "^\[\s*[0-9]+%\]\s(Building \w* object)(\s.*/)(\w+.cpp)(.o)$",
            "green", "normal,normal,bold,normal"]
    ]

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
