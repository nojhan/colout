#encoding: utf-8

def theme(context):

    return context, [
            ["^(checking .*)(yes|found|ok)$","green", "normal,bold"],
            ["^(checking .*)(no|none)$", "yellow",   "normal,bold"],
            ["^(configure:) (error:)(.*)",   "red","normal,bold"],
            ["^(configure:)(.*)",   "magenta","normal,bold"],
            ["^(checking .*)",      "blue",""],
            ["^(config.status:) (creating )(.*)",  "cyan,blue","normal,normal,bold"],
            ["^(config.status:) (executing )(.*)", "cyan,green","normal,normal,bold"],
        ]
