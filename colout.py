#!/usr/bin/env python
#encoding: utf-8

# Color Up Arbitrary Command Ouput 
# Licensed under the GPL version 3
# 2012 (c) nojhan <nojhan@gmail.com>

import re

styles = {"normal":0, "bold":1, "faint":2, "italic":3, "underline":4, "blink":5, "rapid_blink":6,
"reverse":7, "conceal":8 }
colors_mode8 = {"black":0, "red":1, "green":2, "yellow":3, "blue":4, "magenta":5, "cyan":6, "white":7}
modes = {8:";", 256:";38;5;"}


def colorin( text, color, style ):
    """Return the given text, surrounded by the given color ASCII markers."""
    # Special characters.
    start = "\033["
    stop = "\033[0m"
   
    # Convert the color code.
    cs = str(styles[style])

    # 8 colors modes
    if color in colors_mode8: 
        mode = 8
        cc = str( 30 + colors_mode8[color] )
    
    # 256 colors mode
    else: 
        mode = 256
        cc = str( color ) 

    return start + cs + modes[mode] + cc + "m" + text + stop


def colorout( text, match, prev_end, color, style, group=0 ):
    """Build the text from the previous match to the current one, coloring up the matching characters."""
    start = match.start(group)
    colored_text = text[prev_end:start]
    end = match.end(group)

    colored_text += colorin(text[start:end], color, style )
    return colored_text,end


def colorup( text, pattern, color, style = "normal" ):
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
            nb_groups = len(match.groups())

            # Build a list of colors that match the number of grouped,
            # if there is not enough colors, duplicate the last one.
            colors_l = color.split(",")
            group_colors = colors_l + [colors_l[-1]] * (nb_groups - len(colors_l))

            # Same for styles
            styles_l = style.split(",")
            group_styles = styles_l + [styles_l[-1]] * (nb_groups - len(styles_l))

            # For each group index.
            # Note that match.groups returns a tuple (thus being indexed in [0,n[),
            # but that match.start(0) refers to the whole match, the groups being indexed in [1,n].
            # Thus, we need to range in [1,n+1[.
            for group in range(1,nb_groups+1):
                partial,end = colorout( text, match, end, group_colors[group-1], group_styles[group-1], group )
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
            help="A number in [0…255] or one of the following colors: "+" ".join(colors_mode8) )

    parser.add_argument("style", metavar="STYLE", type=str, nargs='?',
            default="bold",
            help="One of the following styles: "+" ".join(styles) )

    parser.add_argument("-e", "--stderr", action="store_true",
            help="Output on the stderr instead of stdout")

    args = parser.parse_args()

    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        try:
            if not args.stderr:
                print colorup( line, args.pattern[0], args.color, args.style ),
                sys.stdout.flush()
            else:
                print >> sys.stderr, colorup( line, args.pattern[0], args.color, args.style ),
                sys.stderr.flush()
        except:
            pass

