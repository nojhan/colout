
def theme(context):
    return context,[
            # traceback header
            ["^Traceback .*$", "blue" ],
            # File, line, in
            [
                "^\s{2}(File \")(/*.*?/)*([^/:]+)(\", line) ([0-9]+)(, in) (.*)$",
                "blue,  none,  white,blue,  yellow,blue",
                "normal,normal,bold, normal,normal,bold"
            ],
            # ["^\s{2}File \"(.*)\", line ([0-9]+), in (.*)$", "white,yellow,white", "normal,normal,bold" ],
            # Error name
            ["^([A-Za-z]*Error):*", "red", "bold" ],
            ["^([A-Za-z]*Exception):*", "red", "bold" ],
            # any quoted things
            ["Error.*['\"](.*)['\"]", "magenta" ],
            # python code
            ["^\s{4}.*$", "Python", "monokai" ],
        ]
