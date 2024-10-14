
def theme(context):
    # Theme for coloring AMD/Xilinx Vivado IDE synthesis and implementation output
    return context,[
        [ r"^\s*\*+.+$", "green" ],
        [ "^#.+", "green" ],

        [ "^.+ Checksum: .+$", "green" ],

        [ r"^.+Time \(s\).+", "green" ],
        [ r"^Time \(s\).+", "green" ],

        [ r"Estimated Timing Summary \|.+\|.+\|", "cyan", "bold" ],
        [ r"Intermediate Timing Summary \|.+\|.+\|", "cyan", "bold" ],

        [ "^INFO:", "white", "bold" ],
        [ "^WARNING:.+$", "yellow" ],
        [ "^CRITICAL WARNING:.+$", "red" ],
        [ "^ERROR:.+$", "red" ],

        [ "^Phase [0-9]+.[0-9]+.[0-9]+.[0-9]+.+$", "magenta", "bold" ],
        [ "^Phase [0-9]+.[0-9]+.[0-9]+.+$",        "magenta", "bold" ],
        [ "^Phase [0-9]+.[0-9]+.+$",               "magenta", "bold" ],
        [ "^Phase [0-9]+.+$",                      "magenta", "bold" ]
    ]

