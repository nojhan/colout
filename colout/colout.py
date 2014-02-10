#!/usr/bin/env python3
#encoding: utf-8

# Color Up Arbitrary Command Ouput
# Licensed under the GPL version 3
# 2012 (c) nojhan <nojhan@nojhan.net>

import sys
import re
import random
import os
import glob
import math
import importlib
import logging
import signal
import string
import hashlib
import functools

# set the SIGPIPE handler to kill the program instead of
# ending in a write error when a broken pipe occurs
signal.signal( signal.SIGPIPE, signal.SIG_DFL )


###############################################################################
# Ressource parsing helpers
###############################################################################

def parse_gimp_palette( filename ):
    """
    Parse the given filename as a GIMP palette (.gpl)

    Return the filename (without path and extension) and a list of ordered
    colors.
    Generally, the colors are RGB triplets, thus this function returns:
        (name, [ [R0,G0,B0], [R1,G1,B1], ... , [RN,GN,BN] ])
    """

    logging.debug("parse GIMP palette file: %s" % filename)
    fd = open(filename)
    # remove path and extension, only keep the file name itself
    name = os.path.splitext( os.path.basename(filename ))[0]

    # The first .gpl line is a header
    assert( fd.readline().strip() == "GIMP Palette" )

    # Then the full name of the palette
    long_name = fd.readline().strip()

    # Then the columns number.
    # split on colon, take the second argument as an int
    line = fd.readline()
    if "Columns:" in line:
        columns = int( line.strip().split(":")[1].strip() )
        lines = fd.readlines()
    else:
        columns=3
        lines = [line] + fd.readlines()

    # Then the colors themselves.
    palette = []
    for line in lines:
        # skip lines with only a comment
        if re.match("^\s*#.*$", line ):
            continue
        # decode the columns-ths codes. Generally [R G B] followed by a comment
        colors = [ int(c) for c in line.split()[:columns] ]
        palette.append( colors )

    logging.debug("parsed %i RGB colors from palette %s" % (len(palette), name) )
    return name,palette


def uniq( lst ):
    """Build a list with uniques consecutive elements in the argument.

        >>> uniq([1,1,2,2,2,3])
        [1,2,3]
        >>> uniq([0,1,1,2,3,3,3])
        [0,1,2,3]
    """
    assert( len(lst) > 0 )
    uniq = [ lst[0] ]
    for i in range(1,len(lst)):
        if lst[i] != lst[i-1]:
            uniq.append(lst[i])
    return uniq


def rgb_to_ansi( r, g, b ):
    """Convert a RGB color to its closest 256-colors ANSI index"""
    # ansi_max is the higher possible RGB value for ANSI colors
    # limit RGB values to ansi_max
    red,green,blue = tuple([ansi_max if c>ansi_max else c for c in (r,g,b)])

    offset = 42.5
    is_gray = True
    while is_gray:
        if red < offset or green < offset or blue < offset:
            all_gray = red < offset and green < offset and blue < offset
            is_gray = False
        offset += 42.5

    if all_gray:
        val = ansi_max + round( (red + green + blue)/33.0 )
        res = int(val)
    else:
        val = ansi_min
        for color,modulo in zip( [red, green, blue], [6*6, 6, 1] ):
            val += round(6.0 * (color / 256.0)) * modulo
        res = int(val)

    return res


def hex_to_rgb(h):
    assert( h[0] == "#" )
    h = h.lstrip('#')
    lh = len(h)
    return tuple( int(h[i:i+lh//3], 16) for i in range(0, lh, lh//3) )


###############################################################################
# Global variables
###############################################################################

# Escaped end markers for given color modes
endmarks = {8: ";", 256: ";38;5;"}

ansi_min = 16
ansi_max = 234

# Available styles
styles = {
    "normal": 0, "bold": 1, "faint": 2, "italic": 3, "underline": 4,
    "blink": 5, "rapid_blink": 6,
    "reverse": 7, "conceal": 8
}

# Available color names in 8-colors mode
colors = {
    "black": 0, "red": 1, "green": 2, "yellow": 3, "orange":3, "blue": 4,
    "magenta": 5, "purple": 5, "cyan": 6, "white": 7, "none": -1
}

themes = {}

# pre-defined colormaps
# 8-colors mode should start with a lower-case letter (and can contains either named or indexed colors)
# 256-colors mode should start with an upper-case letter (and should contains indexed colors)
colormaps = {
    # Rainbows
    "rainbow" : ["magenta", "blue", "cyan", "green", "yellow", "red"],
    "Rainbow" : [92, 93, 57, 21, 27, 33, 39, 45, 51, 50, 49, 48, 47, 46, 82, 118, 154, 190, 226, 220, 214, 208, 202, 196],

    # from magenta to red, with white in the middle
    "spectrum" : ["magenta", "blue", "cyan", "white", "green", "yellow", "red"],
    "Spectrum" : [91, 92, 56, 57, 21, 27, 26, 32, 31, 37, 36, 35, 41, 40, 41, 77, 83, 84, 120, 121, 157, 194, 231, 254, 255, 231, 230, 229, 228, 227, 226, 220, 214, 208, 202, 196]
} # colormaps

colormap = colormaps["rainbow"]  # default colormap to rainbow
colormap_idx = 0

scale = (0,100)

class UnknownColor(Exception):
    pass

class DuplicatedPalette(Exception):
    pass

class DuplicatedTheme(Exception):
    pass


###############################################################################
# Load available extern resources
###############################################################################

def load_themes( themes_dir):
    global themes
    logging.debug("search for themes in: %s" % themes_dir)
    os.chdir( themes_dir )

    # load available themes
    for f in glob.iglob("colout_*.py"):
        module = ".".join(f.split(".")[:-1]) # remove extension
        name = "_".join(module.split("_")[1:]) # remove the prefix
        if name in themes:
            raise DuplicatedTheme(name)
        logging.debug("load theme %s" % name)
        themes[name] = importlib.import_module(module)


def load_palettes( palettes_dir ):
    global colormaps
    logging.debug("search for palettes in: %s" % palettes_dir)
    os.chdir( palettes_dir )

    # load available colormaps (GIMP palettes format)
    for p in glob.iglob("*.gpl"):
        try:
            name,palette = parse_gimp_palette(p)
        except Exception as e:
            logging.warning("error while parsing palette %s: %s" % ( p,e ) )
            continue
        if name in colormaps:
            raise DuplicatedPalette(name)
        # Convert the palette to ANSI
        ansi_palette = [ rgb_to_ansi(r,g,b) for r,g,b in palette ]
        # Compress it so that there isn't two consecutive identical colors
        compressed = uniq(ansi_palette)
        logging.debug("load %i ANSI colors in palette %s: %s" % (len(compressed), name, compressed))
        colormaps[name] = compressed


def load_lexers():
    global lexers
    # load available pygments lexers
    lexers = []
    try:
        global get_lexer_by_name
        from pygments.lexers import get_lexer_by_name

        global highlight
        from pygments import highlight

        global Terminal256Formatter
        from pygments.formatters import Terminal256Formatter

        global TerminalFormatter
        from pygments.formatters import TerminalFormatter

        from pygments.lexers import get_all_lexers
    except ImportError:
        logging.warning("the pygments module has not been found, syntax coloring is not available")
        pass
    else:
        for lexer in get_all_lexers():
            try:
                lexers.append(lexer[1][0])
            except IndexError:
                logging.warning("cannot load lexer: %s" % lexer[1][0])
                pass
            else:
                logging.debug("loaded lexer %s" % lexer[1][0])
        lexers.sort()


def load_resources( themes_dir, palettes_dir ):
    load_themes( themes_dir )
    load_palettes( palettes_dir )
    load_lexers()


###############################################################################
# Library
###############################################################################

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

    assert( type(color) is str )

    global colormap_idx
    global debug

    # Special characters.
    start = "\033["
    stop = "\033[0m"

    color_code = ""
    style_code = ""

    # Convert the style code
    if style == "random" or style == "Random":
        style = random.choice(list(styles.keys()))
    else:
        if style in styles:
            style_code = str(styles[style])

    color = color.strip()
    if color == "none":
        # if no color, style cannot be applied
        if not debug:
            return text
        else:
            return "<none>"+text+"</none>"

    elif color == "random":
        mode = 8
        color_code = random.choice(list(colors.values()))
        color_code = str(30 + color_code)

    elif color == "Random":
        mode = 256
        color_nb = random.randint(0, 255)
        color_code = str(color_nb)

    elif color in colormaps.keys():
        if color[0].islower(): # lower case first letter
            mode = 8
            c = colormaps[color][colormap_idx]
            if c.isdigit():
                color_code = str(30 + c)
            else:
                color_code = str(30 + colors[c])

        else: # upper case
            mode = 256
            color_nb = colormaps[color][colormap_idx]
            color_code = str( color_nb )

        if colormap_idx < len(colormaps[color])-1:
            colormap_idx += 1
        else:
            colormap_idx = 0

    elif color.lower() == "scale": # "scale" or "Scale"

        # filter out everything that does not seem to be necessary to interpret the string as a number
        # this permits to transform "[ 95%]" to "95" before number conversion,
        # and thus allows to color a group larger than the matched number
        chars_in_numbers = "-+.,e"
        allowed = string.digits + chars_in_numbers
        nb = "".join([i for i in filter(allowed.__contains__, text)])

        # interpret as decimal
        try:
            # babel is a specialized module
            import babel.numbers as bn
            f = float(bn.parse_decimal(nb))
        except ImportError:
            f = float(nb)

        # if out of scale, do not color
        if f < scale[0] or f > scale[1]:
            return text

        if color[0].islower():
            mode = 8
            cmap = colormaps["spectrum"]

            # normalize and scale over the nb of colors in cmap
            i = int( math.ceil( (f - scale[0]) / (scale[1]-scale[0]) * (len(cmap)-1) ) )

            color = cmap[i]
            color_code = str(30 + colors[color])

        else:
            mode = 256
            cmap = colormaps["Spectrum"]
            i = int( math.ceil( (f - scale[0]) / (scale[1]-scale[0]) * (len(cmap)-1) ) )
            color = cmap[i]
            color_code = str(color)

    # "hash" or "Hash"; useful to randomly but consistently color strings
    elif color.lower() == "hash":
        hasher = hashlib.md5()
        hasher.update(text.encode('utf-8'))
        hash = hasher.hexdigest()

        f = float(functools.reduce(lambda x, y: x+ord(y), hash, 0) % 101)

        if color[0].islower():
            mode = 8
            cmap = colormaps["rainbow"]

            # normalize and scale over the nb of colors in cmap
            i = int( math.ceil( (f - scale[0]) / (scale[1]-scale[0]) * (len(cmap)-1) ) )

            color = cmap[i]
            color_code = str(30 + colors[color])

        else:
            mode = 256
            cmap = colormaps["Rainbow"]
            i = int( math.ceil( (f - scale[0]) / (scale[1]-scale[0]) * (len(cmap)-1) ) )
            color = cmap[i]
            color_code = str(color)

    # Really useful only when using colout as a library
    # thus you can change the "colormap" variable to your favorite one before calling colorin
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

    # hexadecimal color
    elif color[0] == "#":
        mode = 256
        color_nb = rgb_to_ansi(*hex_to_rgb(color))
        assert(0 <= color_nb <= 255)
        color_code = str(color_nb)

    # 256 colors mode
    elif color.isdigit():
        mode = 256
        color_nb = int(color)
        assert(0 <= color_nb <= 255)
        color_code = str(color_nb)

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
        if not debug:
            return highlight(text, lexer, formatter)[:-1]
        else:
            return "<"+color+">"+ highlight(text, lexer, formatter)[:-1] + "</"+color+">"

    # unrecognized
    else:
        raise UnknownColor(color)

    if not debug:
        return start + style_code + endmarks[mode] + color_code + "m" + text + stop
    else:
        return start + style_code + endmarks[mode] + color_code + "m<" + color + ">" + text + "</" + color + ">" + stop


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

    if not debug:
        regex = re.compile(pattern)
    else:
        regex = re.compile(pattern, re.DEBUG)

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
                # If a group didn't match, there's nothing to color
                if match.group(group) is not None:
                    partial, end = colorout(text, match, end, group_colors[group-1], group_styles[group-1], group)
                    colored_text += partial

    # Append the remaining part of the text, if any.
    colored_text += text[end:]

    return colored_text


###########
# Helpers #
###########

def colortheme(item, theme):
    """
    Take a list of list of args to colorup, and color the given item with sequential calls to colorup.

    Used to read themes, which can be something like:
    [ [ pattern, colors, styles ], [ pattern ], [ pattern, colors ] ]
    """
    # logging.debug("use a theme with %i arguments" % len(theme))
    for args in theme:
        item = colorup(item, *args)
    return item


def write(colored, stream = sys.stdout):
    """
    Write "colored" on sys.stdout, then flush.
    """
    try:
        stream.write(colored)
        stream.flush()

    # Silently handle broken pipes
    except IOError:
        try:
            stream.close()
        except IOError:
            pass


def map_write( stream_in, stream_out, function, *args ):
    """
    Read the given file-like object as a non-blocking stream
    and call the function on each item (line),
    with the given extra arguments.

    A call to "map_write(sys.stdin, colorup, pattern, colors)" will translate to the
    non-blocking equivalent of:
        for item in sys.stdin.readlines():
            write( colorup( item, pattern, colors ) )
    """
    while True:
        try:
            item = stream_in.readline()
        except UnicodeDecodeError:
            continue
        except KeyboardInterrupt:
            break
        if not item:
            break
        write( function(item, *args), stream_out )


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

    # Use a dirty argument picker
    # Check for bad usage or an help flag
    if len(argv) < 2 \
       or len(argv) > 10 \
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
                on_groups = bool(argv[4])
                if len(argv) == 6:
                    as_colormap = bool(argv[5])
                    if len(argv) == 7:
                        as_theme = bool(argv[6])
                        if len(argv) == 8:
                            as_source = bool(argv[7])
                            if len(argv) == 9:
                                as_all = bool(argv[8])
                                if len(argv) == 10:
                                    scale = bool(argv[9])

    return pattern, color, style, on_groups, as_colormap, as_theme, as_source, as_all, scale


def __args_parse__(argv, usage=""):
    """
    Parse command line arguments with the argparse library.
    Returns a tuple of (pattern,color,style,on_stderr).
    """
    parser = argparse.ArgumentParser(
        description=usage)

    parser.add_argument("pattern", metavar="REGEX", type=str, nargs=1,
            help="A regular expression")

    pygments_warn=" You can also use a language name to activate syntax coloring (see `-r all` for a list)."
    try:
        import pygments
    except ImportError:
        pygments_warn=" (WARNING: python3-pygments is not available, \
                install it if you want to be able to use syntax coloring)"

    parser.add_argument("color", metavar="COLOR", type=str, nargs='?',
            default="red",
            help="A number in [0…255], a color name, a colormap name, \
            a palette or a comma-separated list of those values."+pygments_warn)

    parser.add_argument("style", metavar="STYLE", type=str, nargs='?',
            default="bold",
            help="One of the available styles or a comma-separated list of styles.")

    parser.add_argument("-g", "--groups", action="store_true",
            help="For color maps (random, rainbow), iterate over matching groups \
                in the pattern instead of over patterns")

    parser.add_argument("-c", "--colormap", action="store_true",
            help="Use the given colors as a colormap (cycle the colors at each match)")

    babel_warn=" (numbers will be parsed according to your locale)"
    try:
        # babel is a specialized module
        import babel.numbers
    except ImportError:
        babel_warn=" (WARNING: python3-babel is not available, install it \
        if you want to be able to parse numbers according to your locale)"

    parser.add_argument("-l", "--scale",
            help="When using the 'scale' colormap, parse matches as decimal numbers \
                and apply the rainbow colormap linearly between the given SCALE=min,max" + babel_warn)

    parser.add_argument("-a", "--all", action="store_true",
            help="Color the whole input at once instead of line per line \
                (really useful for coloring a source code file with strings \
                on multiple lines).")

    parser.add_argument("-t", "--theme", action="store_true",
            help="Interpret REGEX as a theme.")

    parser.add_argument("-T", "--themes-dir", metavar="DIR", action="append",
            help="Search for additional themes (colout_*.py files) in this directory")

    parser.add_argument("-P", "--palettes-dir", metavar="DIR", action="append",
            help="Search for additional palettes (*.gpl files) in this directory")

    # This normally should be an option with an argument, but this would end in an error,
    # as no regexp is supposed to be passed after calling this option,
    # we use it as the argument to this option.
    # The only drawback is that the help message lacks a metavar...
    parser.add_argument("-r", "--resources", action="store_true",
            help="Print the names of available resources. Use a comma-separated list of resources names \
            (styles, colors, special, themes, palettes, colormaps or lexers), \
            use 'all' to print everything.")

    parser.add_argument("--debug", action="store_true",
            help="Debug mode: print what's going on internally, useful if you want to check what features are available.")

    parser.add_argument("-s", "--source", action="store_true",
            help="Interpret REGEX as a source code readable by the Pygments library. \
                If the first letter of PATTERN is upper case, use the 256 colors mode, \
                if it is lower case, use the 8 colors mode. \
                Interpret COLOR as a Pygments style.")

    args = parser.parse_args()

    return args.pattern[0], args.color, args.style, args.groups, \
           args.colormap, args.theme, args.source, args.all, args.scale, args.debug, args.resources, args.palettes_dir, \
           args.themes_dir


def write_all( as_all, stream_in, stream_out, function, *args ):
    """
    If as_all, print function(*args) on the whole stream,
    else, print it for each line.
    """
    if as_all:
        write( function( stream_in.read(), *args ), stream_out )
    else:
        map_write( stream_in, stream_out, function, *args )


if __name__ == "__main__":

    global debug
    error_codes = {"UnknownColor":1, "DuplicatedPalette":2}

    usage = "A regular expression based formatter that color up an arbitrary text stream."

    #####################
    # Arguments parsing #
    #####################
    try:
        import argparse

    # if argparse is not installed
    except ImportError:
        pattern, color, style, on_groups, as_colormap, as_theme, as_source, as_all, myscale \
            = __args_dirty__(sys.argv, usage)

    # if argparse is available
    else:
        pattern, color, style, on_groups, as_colormap, as_theme, as_source, as_all, myscale, \
        debug, resources, palettes_dirs, themes_dirs \
            = __args_parse__(sys.argv, usage)

    if debug:
        lvl = logging.DEBUG
    else:
        lvl = logging.ERROR

    logging.basicConfig(format='[colout] %(levelname)s: %(message)s', level=lvl)


    ##################
    # Load resources #
    ##################
    try:
        # Search for available resources files (themes, palettes)
        # in the same dir as the colout.py script
        res_dir = os.path.dirname(os.path.realpath(__file__))

        # this must be called before args parsing, because the help can list available resources
        load_resources( res_dir, res_dir )

        # try additional directories if asked
        if palettes_dirs:
            for adir in palettes_dirs:
                try:
                    os.chdir( adir )
                except OSError as e:
                    logging.warning("cannot read palettes directory %s, ignore it" % adir)
                    continue
                else:
                    load_palettes( adir )

        if themes_dirs:
            for adir in themes_dirs:
                try:
                    os.chdir( adir )
                except OSError as e:
                    logging.warning("cannot read themes directory %s, ignore it" % adir)
                    continue
                else:
                    load_themes( adir )

    except DuplicatedPalette as e:
        logging.error( "duplicated palette file name: %s" % e )
        sys.exit( error_codes["DuplicatedPalette"] )

    if resources:
        asked=[r.lower() for r in pattern.split(",")]
        # print("Available resources:")
        for res in asked:
            if "style" in res or "all" in res:
                print("STYLES: %s" % ", ".join(styles) )

            if "color" in res or "all" in res:
                print("COLORS: %s" % ", ".join(colors) )

            if "special" in res or "all" in res:
                print("SPECIAL: %s" % ", ".join(["random", "Random", "scale", "Scale", "hash", "Hash", "colormap"]) )

            if "theme" in res or "all" in res:
                if len(themes) > 0:
                    print("THEMES: %s" % ", ".join(themes.keys()) )
                else:
                    print("NO THEME")

            if "colormap" in res or "all" in res:
                if len(colormaps) > 0:
                    print("COLORMAPS: %s" % ", ".join(colormaps) )
                else:
                    print("NO COLORMAPS")

            if "lexer" in res or "all" in res:
                if len(lexers) > 0:
                    print("SYNTAX COLORING: %s" % ", ".join(lexers) )
                else:
                    print("NO SYNTAX COLORING (check that python3-pygments is installed)")

        sys.exit(0) # not an error, we asked for help

    ############
    # Coloring #
    ############

    try:
        if myscale:
            scale = tuple([float(i) for i in myscale.split(",")])
            logging.debug("user-defined scale: %f,%f" % scale)

        # use the generator: output lines as they come
        if as_colormap is True and color != "rainbow":
            colormap = color.split(",")  # replace the colormap by the given colors
            color = "colormap"  # use the keyword to switch to colormap instead of list of colors
            logging.debug("used-defined colormap: %s" % ",".join(colormap) )

        # if theme
        if as_theme:
            logging.debug( "asked for theme: %s" % pattern )
            assert(pattern in themes.keys())
            write_all( as_all, sys.stdin, sys.stdout, colortheme, themes[pattern].theme() )

        # if pygments
        elif as_source:
            logging.debug("asked for lexer: %s" % pattern.lower())
            assert(pattern.lower() in lexers)
            lexer = get_lexer_by_name(pattern.lower())
            # Python => 256 colors, python => 8 colors
            ask_256 = pattern[0].isupper()
            if ask_256:
                logging.debug("256 colors mode")
                try:
                    formatter = Terminal256Formatter(style=color)
                except:  # style not found
                    logging.warning("style %s not found, fallback to default style" % color)
                    formatter = Terminal256Formatter()
            else:
                logging.debug("8 colors mode")
                formatter = TerminalFormatter()

            write_all( as_all, sys.stdin, sys.stdout, highlight, lexer, formatter )

        # if color
        else:
            write_all( as_all, sys.stdin, sys.stdout, colorup, pattern, color, style, on_groups )

    except UnknownColor as e:
        logging.error("unknown color: %s" % e )
        sys.exit( error_codes["UnknownColor"] )

