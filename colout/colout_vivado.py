
def theme(context):
    # Theme for coloring AMD/Xilinx Vivado IDE synthesis and implementation output
    return context,[
        [ "^#.+", "green" ],
        [ "^.+ Checksum: .+$", "green" ],

        [ "^.+Time \(s\).+", "green" ],
        [ "^Time \(s\).+", "green" ],

        [ "Estimated Timing Summary \|.+\|.+\|", "cyan", "bold" ],
        [ "Intermediate Timing Summary \|.+\|.+\|", "cyan", "bold" ],

        [ "^INFO:", "white", "bold" ],
        [ "^WARNING:.+$", "yellow" ],
        [ "^CRITICAL WARNING:.+$", "red" ],
        [ "^ERROR:.+$", "red" ],

        [ "^Phase [0-9]+.[0-9]+.[0-9]+.[0-9]+.+$", "magenta", "bold" ],
        [ "^Phase [0-9]+.[0-9]+.[0-9]+.+$",        "magenta", "bold" ],
        [ "^Phase [0-9]+.[0-9]+.+$",               "magenta", "bold" ],
        [ "^Phase [0-9]+.+$",                      "magenta", "bold" ]
    ]

