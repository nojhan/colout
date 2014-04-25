
def theme(context):
    return context,[
            # LaTeX
            ["This is .*TeX.*$", "white", "bold"],
            ["(LaTeX Warning): (.*) `(.*)' on page [0-9] (.*) on input line [0-9]+.$",
                "magenta,magenta,white,magenta", "normal,bold,normal" ],
            ["(LaTeX Warning): (.*)", "magenta", "normal,bold" ],
            # ["on (page [0-9]+)", "yellow", "normal" ],
            ["on input (line [0-9]+)", "yellow", "normal" ],
            ["^! .*$", "red", "bold"],
            ["(.*erfull) ([^\s]+).* in [^\s]+ at (lines [0-9]+--[0-9]+)",
                "magenta,magenta,yellow", "normal"],
            ["\\[^\s]+\s", "white", "bold"],
            ["^l\.([0-9]+) ", "yellow"],
            ["(Output written on) (.*) \(([0-9]+ pages), [0-9]+ bytes\).",
                "blue,white,blue", "normal,bold,normal"],
            ["WARNING.*", "magenta", "normal"],
            ["warning.*", "magenta", "normal"],

            # BiBTeX
            ["^(I couldn't) (.*)", "red", "normal,bold"],
            ["(I found) no (.*)", "red"],
            ["^---(line [0-9]+) of file (.*)", "yellow,white", "normal"],
        ]

