
def theme(context):
    # This theme expect a formatted JSON input, with items spread across lines.
    # See tools like "python -m json.tool" or "json_xs"
    return context,[
        [ r'[\[\]{}],*\s*\n' ],
        [ '" (:) ', "yellow" ],
        [ r'[\]}"](,)', "yellow" ],
        [ r"\"(-*[0-9]+\.*[0-9]*e*-*[0-9]*)\"", "blue" ],
        [ '"(.*)"', "green" ],
        [ """["']""", "cyan" ]
    ]

