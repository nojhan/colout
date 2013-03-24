#!/usr/bin/env python
#encoding: utf-8

# Color Up Arbitrary Command Ouput
# Licensed under the GPL version 3
# 2012 (c) nojhan <nojhan@nojhan.net>

import re
import random
import os
import glob

###########
# Library #
###########

# Available styles
styles = {
    "normal": 0, "bold": 1, "faint": 2, "italic": 3, "underline": 4,
    "blink": 5, "rapid_blink": 6,
    "reverse": 7, "conceal": 8
}

# Available color names in 8-colors mode
colors = {
    "black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4,
    "magenta": 5, "cyan": 6, "white": 7
}

rainbow = ["red", "yellow", "green", "cyan", "blue", "magenta"]
colormap = rainbow  # default colormap to rainbow
colormap_idx = 0

# Escaped end markers for given color modes
endmarks = {8: ";", 256: ";38;5;"}

# load available themes
themes = {}
themes_dir=os.path.dirname(os.path.realpath(__file__))
os.chdir( themes_dir )
for f in glob.iglob("colout_*.py"):
    module = ".".join(f.split(".")[:-1])
    name = "_".join(module.split("_")[1:])
    themes[name] = __import__(module)

# load available pygments lexers
lexers = []
try:
    from pygments.lexers import get_all_lexers
    from pygments.lexers import get_lexer_by_name
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.formatters import TerminalFormatter
except ImportError:
    pass
else:
    for lexer in get_all_lexers():
        lexers.append(lexer[1][0])
    lexers.sort()


def colorin(text, color="red", style="normal"):
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
    global colormap_idx

    # Special characters.
    start = "\033["
    stop = "\033[0m"

    # Convert the style code
    if style == "random" or style == "Random":
        style = random.choice(list(styles.keys()))
    else:
        if style in styles:
            style_code = str(styles[style])

    if color == "random":
        mode = 8
        color_code = random.choice(list(colors.values()))
        color_code = str(30 + color_code)

    elif color == "Random":
        mode = 256
        color_nb = random.randint(0, 255)
        color_code = str(color_nb)

    elif color == "rainbow":
        mode = 8
        color = colormap[colormap_idx]
        color_code = str(30 + colors[color])

        if colormap_idx < len(colormap)-1:
            colormap_idx += 1
        else:
            colormap_idx = 0

    elif color == "colormap":
        color = colormap[colormap_idx]
        if color in colors:
            mode = 8
            color_code = str(30 + colors[color])
        else:
            mode = 256
            color_nb = int(color)
            assert(0 <= color_nb <= 255)
            color_code = str(color_nb)

        if colormap_idx < len(colormap)-1:
            colormap_idx += 1
        else:
            colormap_idx = 0

    # 8 colors modes
    elif color in colors:
        mode = 8
        color_code = str(30 + colors[color])

    # programming language
    elif color.lower() in lexers:
        lexer = get_lexer_by_name(color.lower())
        # Python => 256 colors, python => 8 colors
        ask_256 = color[0].isupper()
        if ask_256:
            try:
                formatter = Terminal256Formatter(style=style)
            except:  # style not found
                formatter = Terminal256Formatter()
        else:
            if style not in ("light","dark"):
                style = "dark" # dark color scheme by default
            formatter = TerminalFormatter(bg=style)
            # We should return all but the last character,
            # because Pygments adds a newline char.
        return highlight(text, lexer, formatter)[:-1]

    # 256 colors mode
    else:
        mode = 256
        color_nb = int(color)
        assert(0 <= color_nb <= 255)
        color_code = str(color_nb)

    return start + style_code + endmarks[mode] + color_code + "m" + text + stop


def colorout(text, match, prev_end, color="red", style="normal", group=0):
    """
    Build the text from the previous re.match to the current one,
    coloring up the matching characters.
    """
    start = match.start(group)
    colored_text = text[prev_end:start]
    end = match.end(group)

    colored_text += colorin(text[start:end], color, style)
    return colored_text, end


def colorup(text, pattern, color="red", style="normal", on_groups=False):
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
    global colormap_idx
    regex = re.compile(pattern)  # , re.IGNORECASE)

    # Prepare the colored text.
    colored_text = ""
    end = 0
    for match in regex.finditer(text):

        # If no groups are specified
        if not match.groups():
            # Color the previous partial line,
            partial, end = colorout(text, match, end, color, style)
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

            # If we want to iterate colormaps on groups instead of patterns
            if on_groups:
                # Reset the counter at the beginning of each match
                colormap_idx = 0

            # For each group index.
            # Note that match.groups returns a tuple (thus being indexed in [0,n[),
            # but that match.start(0) refers to the whole match, the groups being indexed in [1,n].
            # Thus, we need to range in [1,n+1[.
            for group in range(1, nb_groups+1):
                partial, end = colorout(text, match, end, group_colors[group-1], group_styles[group-1], group)
                colored_text += partial

    # Append the remaining part of the text, if any.
    colored_text += text[end:]

    return colored_text


def colorgen(stream, pattern, color="red", style="normal", on_groups=False):
    """
    A generator that colors the items given in an iterable input.

    >>> import math
    >>> list(colorgen([str(i) for i in [math.pi,math.e]],"1","red"))
    ['3.\x1b[0;31m1\x1b[0m4\x1b[0;31m1\x1b[0m59265359',
     '2.7\x1b[0;31m1\x1b[0m828\x1b[0;31m1\x1b[0m82846']
    """
    while True:
        try:
            item = stream.readline()
        except KeyboardInterrupt:
            break
        if not item:
            break
        yield colorup(item, pattern, color, style, on_groups)


def colortheme(item, theme):
    for args in theme:
        item = colorup(item, *args)
    return item


######################
# Command line tools #
######################

def __args_dirty__(argv, usage=""):
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
    if len(argv) < 2 \
       or len(argv) > 9 \
       or argv[1] == "--help" \
       or argv[1] == "-h":
        print(usage+"\n")
        print("Usage:", argv[0], "<pattern> <color(s)> [<style(s)>] [<print on stderr?>] [<iterate over groups?>]")
        print("\tAvailable colors:", " ".join(colors))
        print("\tAvailable styles:", " ".join(styles))
        print("Example:", argv[0], "'^(def)\s+(\w*).*$' blue,magenta italic,bold < colout.py")
        sys.exit(1)

    assert(len(argv) >= 2)
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
                if len(argv) == 6:
                    on_groups = bool(argv[5])
                    if len(argv) == 7:
                        as_colormap = bool(argv[6])
                        if len(argv) == 8:
                            as_theme = bool(argv[7])
                            if len(argv) == 9:
                                as_source = bool(argv[8])

    return pattern, color, style, on_stderr, on_groups, as_colormap, as_theme, as_source


def __args_parse__(argv, usage=""):
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
                        Available colors: "+", ".join(colors))

    parser.add_argument("style", metavar="STYLE", type=str, nargs='?',
            default="bold",
            help="One of the available styles or a comma-separated list of styles.\
                        Available styles: "+", ".join(styles))

    parser.add_argument("-e", "--stderr", action="store_true",
            help="Output on the stderr instead of stdout")

    parser.add_argument("-g", "--groups", action="store_true",
            help="For color maps (random, rainbow), iterate over matching groups in the pattern instead of over patterns")

    parser.add_argument("-c", "--colormap", action="store_true",
            help="Use the given colors as a colormap (cycle the colors at each match)")

    parser.add_argument("-t", "--theme", action="store_true",
            help="Interpret REGEX as a theme. \
                    Available themes: "+", ".join(themes.keys()))

    parser.add_argument("-s", "--source", action="store_true",
            help="Interpret REGEX as a source code readable by the Pygments library. \
            If the first letter of PATTERN is upper case, use the 256 colors mode, \
            if it is lower case, use the 8 colors mode. \
            In 256 colors, interpret COLOR as a Pygments style. \
            Available languages: "+", ".join(lexers))
    args = parser.parse_args()

    return args.pattern[0], args.color, args.style, args.stderr, args.groups, args.colormap, args.theme, args.source


def write(colored, on_stderr=False):
    """
    If on_stderr, write "colored" on sys.stderr, else write it on sys.stdout.
    Then flush.
    """
    if on_stderr:
        sys.stderr.write(colored)
        sys.stderr.flush()
    else:
        sys.stdout.write(colored)
        sys.stdout.flush()


if __name__ == "__main__":
    import sys

    usage = "A regular expression based formatter that color up an arbitrary text stream."

    try:
        import argparse

    # if argparse is not installed
    except ImportError:
        pattern, color, style, on_stderr, on_groups, as_colormap, as_theme, as_source = __args_dirty__(sys.argv, usage)

    # if argparse is available
    else:
        pattern, color, style, on_stderr, on_groups, as_colormap, as_theme, as_source = __args_parse__(sys.argv, usage)

    # use the generator: output lines as they come
    if as_colormap is True and color != "rainbow":
        colormap = color.split(",")  # replace the colormap by the given colors
        color = "colormap"  # use the keyword to switch to colormap instead of list of colors

    # if theme
    if as_theme:
        assert(pattern in themes.keys())
        while True:
            try:
                item = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            if not item:
                break
            th = themes[pattern].theme()
            colored = colortheme( item, th )
            write(colored)

    # if pygments
    elif as_source:
        assert(pattern.lower() in lexers)
        lexer = get_lexer_by_name(pattern.lower())
        # Python => 256 colors, python => 8 colors
        ask_256 = pattern[0].isupper()
        if ask_256:
            try:
                formatter = Terminal256Formatter(style=color)
            except:  # style not found
                formatter = Terminal256Formatter()
        else:
            formatter = TerminalFormatter()

        while True:
            try:
                item = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            if not item:
                break
            colored = highlight(item, lexer, formatter)
            write(colored)

    # if color
    else:
        for colored in colorgen(sys.stdin, pattern, color, style, on_groups):
            write(colored)
