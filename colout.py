#!/usr/bin/env python
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
    import argparse

    parser = argparse.ArgumentParser(
        description="A regular expression based formatter that color up an arbitrary text output stream.")

    parser.add_argument("pattern", metavar="REGEX", type=str, nargs=1,
            help="A regular expression")

    parser.add_argument("color", metavar="COLOR", type=str, nargs='?',
            default="red",
            help="One of the following colors: "+" ".join(colors), choices = colors)

    parser.add_argument("style", metavar="STYLE", type=str, nargs='?',
            default="bold",
            help="One of the following styles: "+" ".join(styles), choices=styles)

    parser.add_argument("-e", "--stderr", action="store_true",
            help="Output on the stderr instead of stdout")

    args = parser.parse_args()

    for line in sys.stdin:
        if not args.stderr:
            print colorup( line, args.pattern[0], args.color, args.style ),
            sys.stdout.flush()
        else:
            print >> sys.stderr, colorup( line, args.pattern[0], args.color, args.style ),
            sys.stderr.flush()

