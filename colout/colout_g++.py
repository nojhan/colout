
def theme():
    import gettext
    import os

    # get g++ version
    gv = os.popen("g++ -dumpversion").read().strip()

    # get the current translations of gcc
    t = gettext.translation("gcc-"+gv)
    _ = t.ugettext
    # _("msg") will return the given message, translated


    return [
        [ _("error: "), "red", "bold" ],
        [ _("warning: "), "magenta", "bold" ],
        [ _("note: "), "blue", "bold" ],
        # [-Wflag]
        [ "\[-W.*\]", "magenta"],
        # Filename:line number
        [ "(/.*?)/([^/]+\.)(h|cp*):([0-9]+):*([0-9]*)(.*)",
          "white,white,white,yellow,yellow,none",
          "normal,bold,bold,bold,normal" ],
        # source code in single quotes
        [ "'(.*?)'", "Cpp", "monokai" ]
    ]

