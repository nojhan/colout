#encoding: utf-8

def default_gettext( msg ):
    return msg

def theme(context):
    import os
    import gettext
    import locale

    section="blue"

    # get g++ version
    gv = os.popen("g++ -dumpversion").read().strip()

    # get the current translations of gcc
    try:
        t = gettext.translation("gcc-"+gv)
    except IOError:
        _ = default_gettext
    else:
        _ = t.gettext
    # _("msg") will return the given message, translated

    # if the locale is unicode
    enc = locale.getpreferredencoding()
    if "UTF" in enc:
        # gcc will use unicode quotes
        qo = "[‘`]"
        qc = "[’']"
    else:
        # rather than ascii ones
        qo = "['`]"
        qc = "'"

    return context,[
        # Command line
        [ r"[/\s]([cg]\+\+-*[0-9]*\.*[0-9]*)", "white", "bold" ],
        [ r"\s(\-D)(\s*[^\s]+)", "none,green", "normal,bold" ],
        [ r"\s(-g)", "green", "normal" ],
        [ r"\s-O[0-4]", "green", "normal" ],
        [ r"\s-[Wf][^\s]*", "magenta", "normal" ],
        [ r"\s-pedantic", "magenta", "normal" ],
        [ r"\s(-I)(/*[^\s]+/)([^/\s]+)", "none,blue", "normal,normal,bold" ],
        [ r"\s(-L)(/*[^\s]+/)([^/\s]+)", "none,cyan", "normal,normal,bold" ],
        [ r"\s(-l)([^/\s]+)", "none,cyan", "normal,bold" ],
        [ r"\s-[oc]", "red", "bold" ],
        [ r"\s(-+std(?:lib)?)=?([^\s]+)", "red", "normal,bold" ],

        # Important messages
        [ _("error: "), "red", "bold" ],
        [ _("fatal error: "), "red", "bold" ],
        [ _("warning: "), "magenta", "bold" ],
        [ _("undefined reference to "), "red", "bold" ],
        # [-Wflag]
        [ r"\[-W.*\]", "magenta"],

        # Highlight message start:
        #   path   file   ext     : line   :  col     …
        [ "(/.*?)/([^/:]+): (In .*)"+qo,
          section,
          "normal,normal,bold" ],

        [ "(/.*?)/([^/:]+): (At .*)",
          section,
          "normal,normal,bold" ],

        [ _("In file included from"), section ],

        # Highlight locations:
        #   path   file   ext     : line   :  col     …
        [ "(/.*?)/([^/:]+):([0-9]+):*([0-9]*)(.*)",
          "none,white,yellow,none,none",
          "normal,normal,normal,normal" ],

        # source code in single quotes
        [ qo+"(.*?)"+qc, "Cpp", "monokai" ],

        # source code after a "note: candidate are/is:"
        [ _("note: ")+"((?!.*("+qo+"|"+qc+")).*)$", "Cpp", "monokai" ],
        # [ _("note: ")+"(candidate:)(.*)$", "green,Cpp", "normal,monokai" ],
        # after the code part, to avoid matching ANSI escape chars
        [ _("note: "), "green", "normal" ]
    ]

