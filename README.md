colout — Color Up Arbitrary Command Output
==========================================

![Colout logo](https://raw.githubusercontent.com/nojhan/colout/master/colout_logo.svg")

## Synopsis

`colout [-h] [-r RESOURCE]`

`colout [-g] [-c] [-l min,max] [-a] [-t] [-T DIR] [-P DIR] [-d COLORMAP] [-s] [-e CHAR] [-E CHAR] [--debug] PATTERN [COLOR(S) [STYLE(S)]]`

## Description

`colout` read lines of text stream on the standard input and output characters
matching a given regular expression *PATTERN* in given *COLOR* and *STYLE*.

If groups are specified in the regular expression pattern, only them are taken
into account, else the whole matching pattern is colored.

You can specify several colors or styles when using groups by separating them
with commas. If you indicate more colors than groups, the last ones will be ignored.
If you ask for fewer colors, the last one will be duplicated across remaining
groups.

Available colors are: blue, black, yellow, cyan, green, magenta, white, red,
rainbow, random, Random, Spectrum, spectrum, scale, Scale, hash, Hash, none, an
RGB hexadecimal triplet (`#11aaff`, for example) or any number between 0 and 255.

Available styles are: normal, bold, faint, italic, underline, blink,
rapid_blink, reverse, conceal or random (some styles may have no effect, depending
on your terminal).

In some case, you can indicate a foreground and a background color, by indicating both colors
separated by a period (for example: `red.blue`). You can also use this system to combine two styles
(for example, for a bold style that also blinks: `bold.blink`).

`rainbow` will cycle over a the default colormap at each matching pattern.
`Rainbow` will do the same over the default colormap for the 256-colors mode
(this requires a terminal that supports the 256 color escape sequences).

`Random` will color each matching pattern with a random color among the default colormap
(the 255 available in the ANSI table, by default).
`random` will do the same in 8 colors mode.

`spectrum` and `Spectrum` are like rainbows, but with more colors (8 and 36
colors).

`scale` (8 colors) and `Scale` (256 colors) will parse the numbers characters in
the matching text as a decimal number and apply the default colormap according
to its position on the scale defined by the `-l` option (see below, "0,100" by
default).

`hash` (8 colors) and `Hash` (256 colors) will take a fingerprint of the matching
text and apply the default colormap according to it. This ensure that matching
texts appearing several times will always get the same color.

Before interpreting the matched string as a number, colout will remove any
character not supposed to be used to write down numbers. This permits to apply
this special color on a large group, while interpreting only its numerical part.

You can use the name of a syntax-coloring ["lexer"](http://pygments.org/docs/lexers/)
as a color (for example: "Cpp", "ruby", "xml+django", etc.).

If GIMP palettes files (*.gpl) are available, you can also use their names as a
colormap (see the `-P` switch below).

Note that the RGB colors (either the hex triplets or the palettes's colors) will
be converted to their nearest ANSI 256 color mode equivalents.

When not specified, a *COLOR* defaults to _red_ and a *STYLE* defaults to _bold_.

`colout` comes with some predefined themes to rapidly color well-known outputs
(see the `-t` switch below).

`colout` can be used as an interface to pygments (see also the `--source` switch below).

To have a list of all colors, styles, special colormaps, themes, palettes and lexers,
use the `-r` switch (see below).

`colout` is released under the GNU Public License v3.


## Installation

The recomended method is using pip to install the package for the local user:

```console
$ pip install --user colout
```

Another method is using [pipsi](https://github.com/mitsuhiko/pipsi)
(_pipsi is no longer maintained, <https://github.com/mitsuhiko/pipsi/blob/db3e3fccbe4f8f9ed1104ed7293ec8fec6579efc/README.md#L3>_)
```console
$ pipsi install colout
```

There is also a PPA for Ubuntu 16.04 (Xenial)/18.04 (Bionic) (@`0.6.1-3~dist7`, not actively maintained)

```console
$ sudo add-apt-repository ppa:csaba-kertesz/random
$ sudo apt-get update
$ sudo apt-get/aptitude install colout
```

## Options

* `-h`, `--help`:
  Show a help message and exit

* `-g`, `--groups`:
  For color maps (like "rainbow"), iterate over matching groups in the pattern instead of over patterns.

* `-c`, `--colormap`:
  Use the given list of comma-separated colors as a colormap (cycle the colors at each match).

* `-l min,max`, `--scale min,max`:
  When using the 'scale' colormap, parse matches as decimal numbers (taking your locale into
  account) or as arithmetic expression (like "1+2/0.9*3") and apply the rainbow colormap linearly
  between the given min,max (0,100, by default).

* `-a`, `--all`:
  Color the whole input at once instead of line per line
  (really useful for coloring a source code file with strings on multiple lines).

* `-t`, `--theme`:
  Interpret PATTERN as a predefined theme (perm, cmake, g++, etc.).

* `-T DIR`, `--themes-dir DIR`:
  Search for additional themes (colout_*.py files) in this directory.

* `-P DIR`, `--palettes-dir DIR`:
  Search for additional palettes (*.gpl files) in this directory.

* `-d COLORMAP`, `--default COLORMAP`:
  When using special colormaps (`random`, `scale` or `hash`), use this COLORMAP instead of the default one.
  This can be either one of the available colormaps or a comma-separated list of colors.
  WARNING: be sure to specify a default colormap that is compatible with the special colormap's mode,
  or else the colors may not appear the same.
  Also, external palettes are converted from RGB to 256-ANSI and will thus not work if you use
  them as default colormaps for a 8-colors mode special color.

* `-r TYPE(S)`, `--resources TYPE(S)`:
  Print the names of available resources. Use a comma-separated list of resources names
  (styles, colors, special, themes, palettes, colormaps or lexers),
  use 'all' to print everything.

* `-s`, `--source`:
  Interpret PATTERN as source code readable by the Pygments library. If the first letter of PATTERN
  is upper case, use the 256 color mode, if it is lower case, use the 8 colors mode.
  In 256 color mode, interpret COLOR as a Pygments style (e.g. "default").

* `-e CHAR`, `--sep-list CHAR`:
  Use this character as a separator for list of colors/resources/numbers (instead of comma).

* `-E CHAR`, `--sep-pair CHAR`:
  Use this character as a separator for foreground/background pairs (instead of period).

* `--debug`:
  Debug mode: print what's going on internally, if you want to check what features are available.


## Regular expressions

A regular expression (or _regex_) is a pattern that describes a set of strings
that matches it.

`colout` understands regex as specified in the _re_ python module. Given that
`colout` is generally called by the command line, you may have to escape
special characters that would be recognize by your shell.


## Dependencies

Necessary Python modules:

* `pygments` for the source code syntax coloring
* `babel` for a locale-aware number parsing


## Limitations

Don't use nested groups or colout will duplicate the corresponding input text
with each matching colors.

Using a default colormap that is incompatible with the special colormap's mode
(i.e. number of colors) will end badly.

Color pairs (`foreground.background`) work in 8-colors mode for simple coloring, but may fail with `--colormap`.

## Examples

### Simple

* Color in bold red every occurrence of the word _color_ in colout sources:
  `cat colout.py | colout color red bold`

* Color in bold violet home directories in _/etc/passwd_:
  `colout '/home/[a-z]+' 135 < /etc/passwd`

* Color in yellow user/groups id, in bold green name and in bold red home directories in `/etc/passwd`:
  `colout ':x:([0-9]+:[0-9]+):([^:]+).*(/home/[a-z]+)' yellow,green,red normal,bold < /etc/passwd`

* Color in yellow file permissions with read rights for everyone:
  `ls -l | colout '.(r.-){3}' yellow normal`

* Color in green read permission, in bold red write and execution ones:
  `ls -l | colout '(r)(w*)(x*)' green,red normal,bold`

* Color in green comments in colout sources:
  `colout '.*(#.*)$' green normal < colout.py`

* Color in bold green every numbers and in bold red the words _error_ in make output:
  `make 2>&1 | colout '[0-9]+' green normal | colout error`


### Somewhat useful

* Use a different color for each line of the auth log
  `grep user /var/log/auth.log | colout "^.*$" rainbow`

* Color each line of a file with a different color among a 256 color gradient from cyan to green:
  `head /var/log/auth.log | colout -c "^.*$" 39,38,37,36,35,34`

* Color permissions with a predefined template:
  `ls -l | colout -t perm`

* Color in light green comments in non-empty colout sources, with the sharp in bold green:
  `grep -v '^\s*$' colout.py | colout '.*(#)(.*)$' green,119 bold,normal`

* Color a make output, line numbers in yellow, errors in bold red, warning in magenta, pragma in green and C++ file base names in cyan:
  `make 2>&1 | colout ':([0-9]+):[0-9]*' yellow normal | colout error | colout warning magenta | colout pragma green normal | colout '/(\w+)*\.(h|cpp)' cyan normal`
  Or using themes:
  `make 2>&1 | colout -t cmake | colout -t g++`

* Color each word in the head of auth.log with a rainbow color map, starting a new colormap at each new line (the
  beginning of the command is just bash magic to repeat the string "(\\w+)\\W+":
  `L=$(seq 10) ; P=${L//??/(\\w+)\\W+} ; head /var/log/auth.log | colout -g "^${P}(.*)$" rainbow`

* Color source code in 8 colors mode, without seeing comments:
  `cat colout.py | grep -v "#" | colout -s python`

* Color source code in 256 color mode:
  `cat colout.py | colout -s Python monokai`

* Color a JSON stream:
  `echo '{"foo": "lorem", "bar":"ipsum"}' | python -mjson.tool | colout -t json`

* Color a source code substring:
  `echo "There is an error in 'static void Functor::operator()( EOT& indiv ) { return indiv; }' you should fix it" | colout "'(.*)'" Cpp monokai`

* Color the percent of progress part of a CMake's makefile output, with a color
  related to the value of the progress (from 0%=blue to 100%=red):
  `cmake .. && make | colout "^(\[\s*[0-9]+%\])" Scale`

* Color hosts and users in `auth.log`, with consistent colors:
  `cat /var/log/auth.log | colout "^(\S+\s+){3}(\S+)\s(\S+\s+){3}(\S+)\s+(\S+\s+){2}(\S+)\s*" none,hash,none,hash,none,hash`


### Bash alias

The following bash function color the output of any command with the
cmake and g++ themes:

```bash
function cm()
{
    set -o pipefail
    $@ 2>&1  | colout -t cmake | colout -t g++
}
```

You then can use the `cm` alias as a prefix to your build command,
for example: `cm make test`


### GDB integration

You can use `colout` within the GNU debuger (`gbd`) to color its output.
For example, the following script `.gdbinit` configuration will color
the output of the backtrace command:

```gdb
set confirm off

# Don't wrap line or the coloring regexp won't work.
set width 0

# Create a named pipe to get outputs from gdb
shell test -e /tmp/coloutPipe && rm /tmp/coloutPipe
shell mkfifo /tmp/coloutPipe

define logging_on
  # Instead of printing on stdout only, log everything...
  set logging redirect on
  # ... in our named pipe.
  set logging on /tmp/coloutPipe
end

define logging_off
  set logging off
  set logging redirect off
  # Because both gdb and our commands are writing on the same pipe at the same
  # time, it is more than probable that gdb will end before our (higher level)
  # commands.  The gdb prompt will thus render before the result of the command,
  # which is highly akward. To prevent this, we need to wait before displaying
  # the prompt again.  The more your commands are complex, the higher you will
  # need to set this.
  shell sleep 0.4s
end

define hook-backtrace
    # Note: match path = [path]file[.ext] = (.*/)?(?:$|(.+?)(?:(\.[^.]*)|))
    # This line color highlights:
    # – lines that link to source code,
    # – function call in green,
    # – arguments names in yellow, values in magenta,
    # — the parent directory in bold red (assuming that the debug session would be in a "project/build/" directory).
    shell cat /tmp/coloutPipe | colout "^(#)([0-9]+)\s+(0x\S+ )*(in )*(.*) (\(.*\)) (at) (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,red,green,magenta,red,none,white,white,yellow normal,bold,normal,normal,normal,normal,normal,bold,bold,bold | colout "([\w\s]*?)(=)([^,]*?)([,\)])" yellow,blue,magenta,blue normal | colout "/($(basename $(dirname $(pwd))))/" red bold &
    logging_on
end
define hookpost-backtrace
    logging_off
end

# Don't forget to clean the adhoc pipe.
define hook-quit
    set confirm off
    shell rm -f /tmp/coloutPipe
end
```

Take a look at the `example.gdbinit` file distributed with colout for more gdb commands.



### Themes

You can easily add your own theme to colout.
A theme is basically a module with a function named `theme` that take the configuration context as
an argument and return back the (modified) context and a list of triplets.
Each triplet figures the same arguments than those of the command line interface.

```python
def theme(context):
    return context,[ [regexp, colors, styles] ]
```

With the context dictionary at hand, you have access to the internal configuration of colout, you
can thus change colormaps for special keywords, the scale, even the available colors, styles or
themes.

See the cmake them for how to modify an existing colormap if (and only if) the user didn't ask for an alternative one.
See the ninja theme for how to extend an existing theme with more regexps and a different configuration.
See the gcc theme for an example of how to use the localization of existing softwares to build translated regexp.


### Buffering

Note that when you use colout within real time streams (like `tail -f X | grep Y | colout Z`) of
commands, you may observe that the lines are printed by large chunks and not one by one, in real
time.
This is not due to colout but to the buffering behavior of your shell.

To fix that, use `stdbuf`, for example: `tail -f X | stdbuf -o0 grep Y | colout Z`.

## Authors

* nojhan <nojhan@nojhan.net>: original idea, main developer, maintainer.
* Adrian Sadłocha <adrian.adek@gmail.com>
* Alex Burka <aburka@seas.upenn.edu>
* Brian Foley <bpfoley@gmail.com>
* Charles Lewis <noodle@umich.edu>
* DainDwarf <daindwarf@gmail.com>
* Dimitri Merejkowsky <dmerejkowsky@aldebaran-robotics.com>
* Dong Wei Ming <ciici123@gmail.com>
* Fabien MARTY <fabien.marty@gmail.com>
* Jason Green <jason@green.io>
* John Anderson <sontek@gmail.com>
* Jonathan Poelen <jonathan.poelen@gmail.com>
* Louis-Kenzo Furuya Cahier <louiskenzo@gmail.com>
* Mantas <sirexas@gmail.com>
* Martin Ueding <dev@martin-ueding.de>
* Nicolas Pouillard <nicolas.pouillard@gmail.com>
* Nurono <while0pass@yandex.ru>
* Oliver Bristow <obristow@mintel.com>
* orzrd <61966225@qq.com>
* Philippe Daouadi <p.daouadi@free.fr>
* Piotr Staroszczyk <piotr.staroszczyk@get24.org>
* Scott Lawrence <oz@lindenlab.com>
* Xu Di <xudifsd@gmail.com>
* https://github.com/stdedos: maintainer.
