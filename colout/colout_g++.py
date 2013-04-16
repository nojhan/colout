#encoding: utf-8

def theme():
    import os
    import gettext
    import locale

    # get g++ version
    gv = os.popen("g++ -dumpversion").read().strip()

    # get the current translations of gcc
    t = gettext.translation("gcc-"+gv)
    _ = t.gettext
    # _("msg") will return the given message, translated

    # if the locale is unicode
    enc = locale.getpreferredencoding()
    if "UTF" in enc:
        # gcc will use unicode quotes
        qo = "‘"
        qc = "’"
    else:
        # rather than ascii ones
        qo = "'"
        qc = "'"

    return [
        [ _("error: "), "red", "bold" ],
        [ _("warning: "), "magenta", "bold" ],
        [ _("note: "), "blue", "bold" ],
        # [-Wflag]
        [ "\[-W.*\]", "magenta"],

        # Highlight message start:
        #   path   file   ext     : line   :  col     …
        [ "(/.*?)/([^/:]+): (In .*)"+qo,
          "green",
          "normal,normal,bold" ],

        # Highlight locations:
        #   path   file   ext     : line   :  col     …
        [ "(/.*?)/([^/:]+):([0-9]+):*([0-9]*)(.*)",
          "none,white,yellow,none,none",
          "normal,normal,normal,normal" ],

        # source code in single quotes
        [ qo+"(.*?)"+qc, "Cpp", "monokai" ]
    ]

