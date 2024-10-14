
def theme(context):
    return context,[
            # LaTeX
            ["This is .*TeX.*$", "white", "bold"],
            ["(LaTeX Warning): (.*) `(.*)' on page [0-9] (.*) on input line [0-9]+.$",
                "magenta,magenta,white,magenta", "normal,bold,normal" ],
            ["(LaTeX Warning): (.*)", "magenta", "normal,bold" ],
            ["(LaTeX Error): (.*)", "red", "normal,bold" ],
            [r"^(.*\.tex):([0-9]+): (.*)", "white,yellow,red", "normal,normal,bold" ],
            # ["on (page [0-9]+)", "yellow", "normal" ],
            ["on input (line [0-9]+)", "yellow", "normal" ],
            ["^! .*$", "red", "bold"],
            [r"(.*erfull) ([^\s]+).* in [^\s]+ at (lines [0-9]+--[0-9]+)",
                "magenta,magenta,yellow", "normal"],
            [r"\\[^\s]+\s", "white", "bold"],
            [r"^l\.([0-9]+) (.*)", "yellow,tex"],
            [r"^\s+(.*)", "tex"],
            [r"(Output written on) (.*) \(([0-9]+ pages), [0-9]+ bytes\).",
                "blue,white,blue", "normal,bold,normal"],
            ["WARNING.*", "magenta", "normal"],
            ["[wW]arning.*", "magenta", "normal"],
            ["No pages of output", "red", "bold"],

            # BiBTeX
            ["^(I couldn't) (.*)", "red", "normal,bold"],
            ["(I found) no (.*)", "red"],
            ["^---(line [0-9]+) of file (.*)", "yellow,white", "normal"],
        ]

