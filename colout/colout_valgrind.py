#encoding: utf-8

def theme(context):

    return context, [
            # section title
            [r"^(==[0-9]+==\s{1})(Memcheck|Copyright|Using)(.*)$","blue",""],
            [r"^(==[0-9]+==\s{1})(Warning)(.*)$","magenta",""],
            [r"^(==[0-9]+==\s{1}Command: )(\S*)(.*)$","green,white","normal,bold,normal"],
            [r"^(==[0-9]+==\s{1})(HEAP SUMMARY:)(.*)$","green",""],
            [r"^(==[0-9]+==\s{1})(All heap blocks were freed)(.*)$","green",""],
            [r"^(==[0-9]+==\s{1})(.*[rR]erun.*)$","blue",""],
            [r"^(==[0-9]+==\s{1})(Use --.*)$","blue",""],
            [r"^(==[0-9]+==\s{1}\S+.*)$","red",""],
            # section explanation
            [r"^==[0-9]+==\s{2}(\S+.*)$","orange",""],
            # locations adresses
            [r"^==[0-9]+==\s{4}([atby]{2}) (0x0): (\?{3})",
                "blue,yellow,red", "normal,normal,bold"],
            [r"^==[0-9]+==\s{4}([atby]{2}) (0x)([^:]*:) (\S+)",
                "blue,blue,blue,none", "normal"],
            # locations: library
            [r"\(in (.*)\)", "cyan", "normal"],
            # locations: file
            [r"\(([^\.]*\.[^:]+):([0-9]+)\)", "white,yellow", "bold,normal"],
            # leak summary
            [r"^==[0-9]+==\s{4}(definitely lost): .* (in) .*","red","bold"],
            [r"^==[0-9]+==\s{4}(indirectly lost): .* (in) .*","orange","bold"],
            [r"^==[0-9]+==\s{6}(possibly lost): .* (in) .*","yellow","bold"],
            [r"^==[0-9]+==\s{4}(still reachable): .* (in) .*","green","bold"],
            [r"^==[0-9]+==\s{9}(suppressed): .* (in) .*","cyan","bold"],
        ]

