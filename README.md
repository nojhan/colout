colout(1) -- Color Up Arbitrary Command Output
==============================================

## SYNOPSIS

`colout` [-h] [-r]

`colout` [-g] [-c] [-l] [-a] [-t] [-T] [-P] [-s] PATTERN [COLOR(S) [STYLE(S)]]


## DESCRIPTION

`colout` read lines of text stream on the standard input and output characters
matching a given regular expression *PATTERN* in given <COLOR> and *STYLE*.

If groups are specified in the regular expression pattern, only them are taken
into account, else the whole matching pattern is colored.

You can specify several colors or styles when using groups by separating them
with commas. If you indicate more colors than groups, the last ones will be ignored.
If you ask for fewer colors, the last one will be duplicated across remaining
groups.

Available colors are: blue, black, yellow, cyan, green, magenta, white, red,
rainbow, random, Random, scale, none, an RGB hexadecimal triplet or any number
between 0 and 255.

Available styles are: normal, bold, faint, italic, underline, blink,
rapid_blink, reverse, conceal or random (some styles may have no effect, depending
on your terminal).

`rainbow` will cycle over a 8 colors rainbow at each matching pattern.
`Rainbow` will do the same over 24 colors (this requires a terminal that supports
the 256 color escape sequences).

`Random` will color each matching pattern with a random color among the 255
available in the ANSI table. `random` will do the same in 8 colors mode.

`scale` (8 colors) and `Scale` (36 colors) will parse the matching text as
a decimal number and apply the rainbow colormap according to its position
on the scale defined by the `-l` option (see below, "0,100" by default).

If the python-pygments library is installed, you can use the name of a
syntax-coloring "lexer" as a color (for example: "Cpp", "ruby", "xml+django", etc.).

If GIMP palettes files (*.gpl) are available, you can also use their names as a
colormap (see the `-P` switch below).

Note that the RGB colors (either the hex triplets or the palettes's colors) will
be converted to their nearest ANSI 256 color mode equivalents.

When not specified, a *COLOR* defaults to _red_ and a *STYLE* defaults to _bold_.

`colout` comes with some predefined themes to rapidly color well-known outputs
(see the `-t` switch below).

If the python-pygments library is available, `colout` can be used as an interface
to it (see also the `-s` switch below).

To have a list of all colors, styles, special colormaps, themes, palettes and lexers,
use the `-r` switch (see below).

`colout` is released under the GNU Public License v3.


## INSTALLATION

    sudo python setup.py install

and then soft link `/usr/local/bin/colout` to your colout.py under your installation
directory, which is usually something like

    /usr/local/lib/python2.7/dist-packages/colout-0.1-py2.7.egg/colout/colout.py


## OTHER INSTALLATION METHOD

Pypi (the Python Package Index)

    sudo pip install colout

or

    sudo easy_install colout

Ubuntu 13.04's ppa

    sudo add-apt-repository ppa:ciici123/colout
    sudo apt-get update
    sudo apt-get/aptitude install colout

Gentoo overlay

    1. Install layman
    
    echo "app-portage/layman git" >> $EPREFIX/etc/portage/package.Use
    sudo emerge layman
    
    2. Edit `$EPREFIX/etc/layman/layman.cfg`. Add a line after
    
    overlays   : http://www.gentoo.org/proj/en/overlays/repositories.xml
    
    so that it becomes
    
    overlays   : http://www.gentoo.org/proj/en/overlays/repositories.xml
                 file://$EPREFIX/var/lib/layman/my-list.xml

    3. Edit `$EPREFIX/var/lib/layman/my-list.xml`.  The content of this file should be:
    
    <?xml version="1.0" ?>
    <repositories version="1.0">
    <repo priority="50" quality="experimental" status="unofficial">
        <name>dongwm-overlay</name>
        <description>dongweiming's gentoo overlay</description>
        <homepage>https://github.com/dongweiming/dongwm-overlay.git</homepage>
        <owner>
            <email>ciici1234@hotmail.com</email>
        </owner>
        <source type="git">git://github.com/dongweiming/dongwm-overlay.git</source>
    </repo>
    </repositories>

    4. Add this overlay and installation
    
    layman -a dongwm-overlay && sudo emerge colout


## OPTIONS

* `-h`, `--help`:
  Show a help message and exit

* `-g`, `--groups`:
  For color maps (like "rainbow"), iterate over matching groups in the pattern instead of over patterns.

* `-c`, `--colormap`:
  Use the given list of comma-separated colors as a colormap (cycle the colors at each match).

* `-a`, `--all`
  Color the whole input at once instead of line by line (really useful
for coloring a source code file with strings on multiple lines).

* `-l min,max`, `--scale min,max`:
  When using the 'scale' colormap, parse matches as decimal numbers (taking your locale into account)
  and apply the rainbow colormap linearly between the given min,max (0,100, by default).

* `-a`, `--all`:
  Color the whole input at once instead of line per line
  (really useful for coloring a source code file with strings on multiple lines).

* `-t`, `--theme`:
  Interpret PATTERN as a predefined theme (perm, cmake, g++, etc.).

* `-T DIR`, `--themes-dir DIR`:
  Search for additional themes (colout_*.py files) in this directory.

* `-P DIR`, `--palettes-dir DIR`:
  Search for additional palettes (*.gpl files) in this directory.

* `-r`, `--resources`:
  Print the names of all available colors, styles, themes and palettes.

* `-s`, `--source`:
  Interpret PATTERN as source code readable by the Pygments library. If the first letter of PATTERN
  is upper case, use the 256 color mode, if it is lower case, use the 8 colors mode.
  In 256 color mode, interpret COLOR as a Pygments style (e.g. "default").

* `--debug`:
  Debug mode: print what's going on internally, if you want to check what features are available.


## REGULAR EXPRESSIONS

A regular expression (or _regex_) is a pattern that describes a set of strings
that matches it.

`colout` understands regex as specified in the _re_ python module. Given that
`colout` is generally called by the command line, you may have to escape
special characters that would be recognize by your shell.


## DEPENDENCIES

Recommended packages:

* `argparse` for a usable arguments parsing
* `pygments` for the source code syntax coloring
* `babel` for a locale-aware number parsing


## LIMITATIONS

Don't use nested groups or colout will duplicate the corresponding input text with each matching colors.


## EXAMPLES

* Color in bold red every occurrence of the word _color_ in colout sources:
  `cat colout.py | colout color red bold`

* Color in bold violet home directories in _/etc/passwd_:
  `colout '/home/[a-z]+' 135 < /etc/passwd`

* Use a different color for each line of the auth log
  `grep user /var/log/auth.log | colout "^.*$" rainbow`

* Color in yellow user/groups id, in bold green name and in bold red home directories in _/etc/passwd_:
  `colout ':x:([0-9]+:[0-9]+):([^:]+).*(/home/[a-z]+)' yellow,green,red normal,bold < /etc/passwd`

* Color in yellow file permissions with read rights for everyone:
  `ls -l | colout '.(r.-){3}' yellow normal`

* Color in green read permission, in bold red write and execution ones:
  `ls -l | colout '(r)(w*)(x*)' green,red normal,bold`

* Color permissions with a predefined template:
  `ls -l | colout -t perm`

* Color in green comments in colout sources:
  `colout '.*(#.*)$' green normal < colout.py`

* Color in light green comments in non-empty colout sources, with the sharp in bold green:
  `grep -v '^\s*$' colout.py | colout '.*(#)(.*)$' green,119 bold,normal`

* Color in bold green every numbers and in bold red the words _error_ in make output:
  `make 2>&1 | colout '[0-9]+' green normal | colout error`

* Color a make output, line numbers in yellow, errors in bold red, warning in magenta, pragma in green and C++ file base names in cyan:
  `make 2>&1 | colout ':([0-9]+):[0-9]*' yellow normal | colout error | colout warning magenta | colout pragma green normal | colout '/(\w+)*\.(h|cpp)' cyan normal`
  Or using themes:
  `make 2>&³ | colout -t cmake | colout -t g++`

* Color each word in the head of auth.log with a rainbow color map, starting a new colormap at each new line (the
  beginning of the command is just bash magic to repeat the string "(\\w+)\\W+":
  `L=$(seq 10) ; P=${L//??/(\\w+)\\W+} ; head /var/log/auth.log | colout -g "^${P}(.*)$" rainbow`

* Color each line of a file with a different color among a 256 color gradient from cyan to green:
  `head /var/log/auth.log | colout -c "^.*$" 39,38,37,36,35,34`

* Color source code in 8 colors mode, without seeing comments:
  `cat colout.py | grep -v "#" | colout -s python`

* Color source code in 256 color mode:
  `cat colout.py | colout -s Python monokai`

* Color a JSON stream:
  `echo '{"foo": "lorem", "bar":"ipsum"}' | python -mjson.tool | colout -t json`

* Color a source code substring:
  `echo "There is an error in 'static void Functor::operator()( EOT& indiv ) { return indiv; }' you should fix it" | colout "'(.*)'" Cpp monokai`

