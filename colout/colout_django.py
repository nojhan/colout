
def theme(context):
    return context,[
            # Waiting
            ["^Waiting for .*$", "red", "bold"],
            [".*Sending.*", "green"],
            # Watches
            [r"^(Watching) (\S*) (.*)", "yellow", "bold,bold,normal"],
            [".*reloading.$","yellow"],
            # File from python/lib
            [r"^(File) (/.*/lib/python[^/]*/site-packages/)([^/]*)\S* (first seen) (with mtime [0-9]*.*)$",
                "blue,blue,white,blue,blue", "bold,normal,bold,bold,normal"],
            # File from app (last 3 name highlighted)
            [r"^(File) (/\S*/)(\S*/\S*/)(\S*) (first seen) (with mtime [0-9]*.*)$",
                "magenta,magenta,white,white,magenta,magenta", "bold,normal,normal,bold,bold,normal"],
            # SQL
            ["(.*)(SELECT)(.*)(FROM)(.*)",
                "green", "normal,bold,normal,bold,normal"],
            ["(.*)(SELECT)(.*)(FROM)(.*)(WHERE)(.*)",
                "green", "normal,bold,normal,bold,normal,bold,normal"],
            # HTTP
            [r"\"(GET) (\S*) (HTTP\S*)\" ([0-9]+) (.*)$",
                "green,white,green,green,green", "bold,bold,normal,bold,normal"],
            # Errors
            ["(Exception) (while .*) '(.*)' (in) (.*) '(.*)'", "red,red,white,red,red,white", "bold,normal,bold,bold,normal,bold"],
            ["(.*Error): (.*) '(.*)'", "red,red,white", "bold,normal,bold"],
            [r"(django[^:\s]*)\.([^.:\s]*): (.*)", "red","normal,bold,normal"],
            ["Traceback.*:","yellow"],
            ["During handling.*","yellow"],
            # File, line, in
            [
                r"^\s{2}(File \")(/*.*?/)*([^/:]+)(\", line) ([0-9]+)(, in) (.*)$",
                "blue,  none,  white,blue,  yellow,blue",
                "normal,normal,bold, normal,normal,bold"
            ],
    ]
