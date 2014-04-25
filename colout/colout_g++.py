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
        [ "[/\s]([cg]\+\+-*[0-9]*\.*[0-9]*)", "white", "bold" ],
        [ "\s(\-D)(\s*[^\s]+\s)", "none,green", "normal,bold" ],
        [ "\s-g\s", "green", "normal" ],
        [ "\s-O[0-4]*\s", "green", "normal" ],
        [ "\s-[Wf][^\s]*", "magenta", "normal" ],
        [ "\s(-I)(/*[^\s]+/)([^/\s]+)", "none,blue", "normal,normal,bold" ],
        [ "\s(-L)(/*[^\s]+/)([^/\s]+)", "none,cyan", "normal,normal,bold" ],
        [ "\s(-l)([^/\s]+)", "none,cyan", "normal,bold" ],
        [ "\s-[oc]", "red", "bold" ],
        [ "\s(-+std)=*([^s]+)", "red", "normal,bold" ],

        # Important messages
        [ _("error: "), "red", "bold" ],
        [ _("fatal error: "), "red", "bold" ],
        [ _("warning: "), "magenta", "bold" ],
        [ _("undefined reference to "), "red", "bold" ],
        # [-Wflag]
        [ "\[-W.*\]", "magenta"],

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
        [ _("note: ")+"((?!.*(candidate|"+qo+"|"+qc+")).*)$", "Cpp", "monokai" ],
        # after the code part, to avoid matching ANSI escape chars
        [ _("note: "), "green", "normal" ]
    ]

