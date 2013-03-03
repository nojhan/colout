#!/usr/bin/env python
#encoding: utf-8

# Color Up Arbitrary Command Ouput 
# Licensed under the GPL version 3
# 2012 (c) nojhan <nojhan@nojhan.net>

import re
import random

###########
# Library #
###########

# Available styles
styles = {
    "normal":0, "bold":1, "faint":2, "italic":3, "underline":4,
    "blink":5, "rapid_blink":6,
    "reverse":7, "conceal":8
}

# Available color names in 8-colors mode
colors = {
    "black":0, "red":1, "green":2, "yellow":3, "blue":4,
    "magenta":5, "cyan":6, "white":7
}

rainbow = [ "red", "yellow", "green", "cyan", "blue", "magenta" ]
rainbow_idx = 0

# Escaped end markers for given color modes
endmarks = {8:";", 256:";38;5;"}

def colorin( text, color = "red", style = "normal" ):
    """
    Return the given text, surrounded by the given color ASCII markers.

    If the given color is a name that exists in available colors,
    a 8-colors mode is assumed, else, a 256-colors mode.

    The given style must exists in the available styles.

    >>> colorin("Fetchez la vache", "red", "bold")
    '\x1b[1;31mFetchez la vache\x1b[0m'
    >>> colout.colorin("Faites chier la vache", 41, "normal")
    '\x1b[0;38;5;41mFaites chier la vache\x1b[0m'
    """
    # Special characters.
    start = "\033["
    stop = "\033[0m"

    # Convert the style code
    if style == "random" or style == "Random":
        style = random.choice(list(styles.keys()))
    else:
        assert( style in styles)

    style_code = str(styles[style])

    if color == "random":
        mode = 8
        color_code = random.choice(list(colors.values()))
        color_code = str( 30 + color_code )

    elif color == "Random":
        mode = 256
        color_nb = random.randint(0,255)
        color_code = str( color_nb )

    elif color == "rainbow":
        global rainbow_idx
        mode = 8
        color = rainbow[rainbow_idx]
        color_code = str( 30 + colors[color] )

        if rainbow_idx < len(rainbow)-1:
            rainbow_idx += 1
        else:
            rainbow_idx = 0

    # 8 colors modes
    elif color in colors:
        mode = 8
        color_code = str( 30 + colors[color] )

    # 256 colors mode
    else:
        mode = 256
        color_nb = int( color )
        assert( 0 <= color_nb <= 255 )
        color_code = str( color_nb )

    return start + style_code + endmarks[mode] + color_code + "m" + text + stop


def colorout( text, match, prev_end, color = "red", style = "normal", group=0 ):
    """
    Build the text from the previous re.match to the current one,
    coloring up the matching characters.
    """
    start = match.start(group)
    colored_text = text[prev_end:start]
    end = match.end(group)

    colored_text += colorin(text[start:end], color, style )
    return colored_text,end


def colorup( text, pattern, color = "red", style = "normal" ):
    """
    Color up every characters that match the given regexp patterns.
    If groups are specified, only color up them and not the whole pattern.

    Colors and styles may be specified as a list of comma-separated values,
    in which case the different matching groups may be formatted differently.
    If there is less colors/styles than groups, the last format is used
    for the additional groups.

    >>> colorup("Fetchez la vache", "vache", "red", "bold")
    'Fetchez la \x1b[1;31mvache\x1b[0m'
    >>> colorup("Faites chier la vache", "[Fv]a", "red", "bold")
    '\x1b[1;31mFa\x1b[0mites chier la \x1b[1;31mva\x1b[0mche'
    >>> colorup("Faites Chier la Vache", "[A-Z](\S+)\s", "red", "bold")
    'F\x1b[1;31maites\x1b[0m C\x1b[1;31mhier\x1b[0m la Vache'
    >>> colorup("Faites Chier la Vache", "([A-Z])(\S+)\s", "red,green", "bold")
    '\x1b[1;31mF\x1b[0m\x1b[1;32maites\x1b[0m \x1b[1;31mC\x1b[0m\x1b[1;32mhier\x1b[0m la Vache'
    >>> colorup("Faites Chier la Vache", "([A-Z])(\S+)\s", "green")
    '\x1b[0;32mF\x1b[0m\x1b[0;32maites\x1b[0m \x1b[0;32mC\x1b[0m\x1b[0;32mhier\x1b[0m la Vache'
    >>> colorup("Faites Chier la Vache", "([A-Z])(\S+)\s", "blue", "bold,italic")
    '\x1b[1;34mF\x1b[0m\x1b[3;34maites\x1b[0m \x1b[1;34mC\x1b[0m\x1b[3;34mhier\x1b[0m la Vache'
    """
    regex = re.compile(pattern)#, re.IGNORECASE)

    # Prepare the colored text.
    colored_text = ""
    end = 0
    for match in regex.finditer(text):
        
        # If no groups are specified
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


def colorgen( items, pattern, color = "red", style = "normal" ):
    """
    A generator that colors the items given in an iterable input.

    >>> import math
    >>> list(colorgen([str(i) for i in [math.pi,math.e]],"1","red"))
    ['3.\x1b[0;31m1\x1b[0m4\x1b[0;31m1\x1b[0m59265359',
     '2.7\x1b[0;31m1\x1b[0m828\x1b[0;31m1\x1b[0m82846']
    """
    for item in items:
        yield colorup( item, pattern, color, style )


######################
# Command line tools #
######################

def __args_dirty__(argv,usage=""):
    """
    Roughly extract options from the command line arguments.
    To be used only when argparse is not available.

    Returns a tuple of (pattern,color,style,on_stderr).

    >>> colout.__args_dirty__(["colout","pattern"],"usage")
    ('pattern', 'red', 'normal', False)
    >>> colout.__args_dirty__(["colout","pattern","colors","styles"],"usage")
    ('pattern', 'colors', 'styles', False)
    >>> colout.__args_dirty__(["colout","pattern","colors","styles","True"],"usage")
    ('pattern', 'colors', 'styles', True)
    """
    import sys

    # Use a dirty argument picker
    # Check for bad usage or an help flag 
    if    len(argv) < 2 \
       or len(argv) > 5 \
       or argv[1] == "--help" \
       or argv[1] == "-h":
        print(usage+"\n")
        print("Usage:",argv[0],"<pattern> <color(s)> [<style(s)>] [<print on stderr?>]")
        print("\tAvailable colors:"," ".join(colors))
        print("\tAvailable styles:"," ".join(styles))
        print("Example:",argv[0],"'^(def)\s+(\w*).*$' blue,magenta italic,bold < colout.py")
        sys.exit(1)
    
    assert( len(argv) >= 2 )
    # Get mandatory arguments
    pattern = argv[1]

    # default values for optional args
    color = "red"
    style = "normal"
    on_stderr = False

    if len(argv) >= 3:
        color = argv[2]
        if len(argv) >= 4:
            style = argv[3]
            if len(argv) == 5:
                on_stderr = bool(argv[4])
    
    return pattern,color,style,on_stderr


def __args_parse__(argv,usage=""):
    """
    Parse command line arguments with the argparse library.
    Returns a tuple of (pattern,color,style,on_stderr).
    """
    parser = argparse.ArgumentParser(
        description=usage)

    parser.add_argument("pattern", metavar="REGEX", type=str, nargs=1,
            help="A regular expression")

    parser.add_argument("color", metavar="COLOR", type=str, nargs='?',
            default="red",
            help="A number in [0…255], one of the available colors or a comma-separated list of values. \
                        Available colors: "+" ".join(colors) )

    parser.add_argument("style", metavar="STYLE", type=str, nargs='?',
            default="bold",
            help="One of the available styles or a comma-separated list of styles.\
                        Available styles: "+" ".join(styles) )

    parser.add_argument("-e", "--stderr", action="store_true",
            help="Output on the stderr instead of stdout")

    args = parser.parse_args()

    return args.pattern[0], args.color, args.style, args.stderr


if __name__ == "__main__":
    import sys

    usage="A regular expression based formatter that color up an arbitrary text stream."

    try:
        import argparse

    # if argparse is not installed
    except ImportError:
        pattern,color,style,on_stderr = __args_dirty__(sys.argv,usage)
        
    # if argparse is available
    else:
        pattern,color,style,on_stderr = __args_parse__(sys.argv,usage)

    # use the generator: output lines as they come
    for colored in colorgen( sys.stdin, pattern, color, style ):
        if on_stderr:
            sys.stderr.write(colored)
            sys.stderr.flush()
        else:
            sys.stdout.write(colored)
            sys.stdout.flush()
