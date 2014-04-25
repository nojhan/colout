
def theme(context):
    # This theme expect a formatted JSON input, with items spread across lines.
    # See tools like "python -m json.tool" or "json_xs"
    return context,[
        [ '[\[\]{}],*\s*\n' ],
        [ '" (:) ', "yellow" ],
        [ '[\]}"](,)', "yellow" ],
        [ "\"(-*[0-9]+\.*[0-9]*e*-*[0-9]*)\"", "blue" ],
        [ '"(.*)"', "green" ],
        [ """["']""", "cyan" ]
    ]

