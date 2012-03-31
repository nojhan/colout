#!/usr/bin/env python3
#encoding: utf-8

import re

styles = {"standard":0, "bold":1, "reverse":2}
colors = {"black":30, "red":31, "green":32, "yellow":33, "blue":34, "magenta":35, "cyan":36, "white":37}


def colorin( text, color, style ):
    """Return the given text, surrounded by the given color ASCII markers."""
    # Special characters.
    start = "\033["
    stop = "\033[0m"
    
    # Convert the color code.
    cs = str(styles[style])
    cc = str(colors[color])

    return start + cs + ";" + cc + "m" + text + stop


def colorout( text, match, prev_end, color, style, group=0 ):
    """Build the text from the previous match to the current one, coloring up the matching characters."""
    start = match.start(group)
    colored_text = text[prev_end:start]
    end = match.end(group)
    colored_text += colorin(text[start:end], color, style)
    return colored_text,end


def colorup( text, pattern, color, style = "standard" ):
    """Color up every characters that match the given patterns.
    If groups are specified, only color up them and not the whole pattern."""
    regex = re.compile(pattern, re.IGNORECASE)

    # Prepare the colored text.
    colored_text = ""
    end = 0
    for match in regex.finditer(text):
        
        # If not groups are specified
        if not match.groups():
            # Color the previous partial line,
            partial,end = colorout( text, match, end, color, style )
            # add it to the final text.
            colored_text += partial
        else:
            # For each group index.
            # Note that match.groups returns a tuple (thus being indexed in [0,n[),
            # but that match.start(0) refers to the whole match, the groups being indexed in [1,n].
            # Thus, we need to range in [1,n+1[.
            for group in range(1,len(match.groups())+1):
                partial,end = colorout( text, match, end, color, style, group )
                colored_text += partial
   
    # Append the remaining part of the text, if any.
    colored_text += text[end:]

    return colored_text


if __name__ == "__main__":
    import sys

    pattern = ".*"
    color= "red"
    style = "bold"

    nargs = len(sys.argv)

    if nargs <= 1 or nargs >= 5:
        msg = "Usage: colorout pattern [color] [style]"
        msg += "\n\tAvailable colors: "+" ".join(colors)
        msg += "\n\tAvailable styles: "+" ".join(styles)
        sys.exit(msg)
    else:
        if nargs > 1:
             pattern = sys.argv[1]
        if nargs > 2:
            color = sys.argv[2]
        if nargs > 3:
            style = sys.argv[3]

    for line in sys.stdin:
        print( colorup( line, pattern, color, style ), end="" )

