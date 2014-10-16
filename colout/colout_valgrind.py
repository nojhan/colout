#encoding: utf-8

def theme(context):

    return context, [
            # section title
            ["^(==[0-9]+==\s{1})(Memcheck|Copyright|Using)(.*)$","blue",""],
            ["^(==[0-9]+==\s{1})(Warning)(.*)$","magenta",""],
            ["^(==[0-9]+==\s{1}Command: )(\S*)(.*)$","green,white","normal,bold,normal"],
            ["^(==[0-9]+==\s{1})(HEAP SUMMARY:)(.*)$","green",""],
            ["^(==[0-9]+==\s{1})(All heap blocks were freed)(.*)$","green",""],
            ["^(==[0-9]+==\s{1})(.*[rR]erun.*)$","blue",""],
            ["^(==[0-9]+==\s{1})(Use --.*)$","blue",""],
            ["^(==[0-9]+==\s{1}\S+.*)$","red",""],
            # section explanation
            ["^==[0-9]+==\s{2}(\S+.*)$","orange",""],
            # locations adresses
            ["^==[0-9]+==\s{4}([atby]{2}) (0x0): (\?{3})",
                "blue,yellow,red", "normal,normal,bold"],
            ["^==[0-9]+==\s{4}([atby]{2}) (0x)([^:]*:) (\S+)",
                "blue,blue,blue,none", "normal"],
            # locations: library
            ["\(in (.*)\)", "cyan", "normal"],
            # locations: file
            ["\(([^\.]*\.[^:]+):([0-9]+)\)", "white,yellow", "bold,normal"],
            # leak summary
            ["^==[0-9]+==\s{4}(definitely lost): .* (in) .*","red","bold"],
            ["^==[0-9]+==\s{4}(indirectly lost): .* (in) .*","orange","bold"],
            ["^==[0-9]+==\s{6}(possibly lost): .* (in) .*","yellow","bold"],
            ["^==[0-9]+==\s{4}(still reachable): .* (in) .*","green","bold"],
            ["^==[0-9]+==\s{9}(suppressed): .* (in) .*","cyan","bold"],
        ]

