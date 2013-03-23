colout(1) -- Color Up Arbitrary Command Ouput
=============================================

## SYNOPSIS

`colout` [-h] [-e] PATTERN [COLOR(S)] [STYLE(S)]


## DESCRIPTION

`colout` read lines of text stream on the standard input and output characters 
matching a given regular expression *PATTERN* in given <COLOR> and *STYLE*.

If groups are specified in the regular expression pattern, only them are taken
into account, else the whole matching pattern is colored.

You can specify severall colors or styles when using groups by separating them
with commas. If you indicate more colors than groups, the last ones will be ignored.
If you ask for less colors, the last one will be duplicated across remaining
groups.

Available colors are: blue, black, yellow, cyan, green, magenta, white, red,
rainbow, random, Random or any number between 0 and 255.

Available styles are: normal, bold, faint, italic, underline, blink,
rapid_blink, reverse, conceal or random.

`Random` will color each matching pattern with a random color among the 255
available in the ANSI table. `random` will do the same in 8 colors mode.

`rainbow` will cycle over a 8 colors rainbow at each matching pattern.

When not specified, a *COLOR* defaults to _red_ and a *STYLE* defaults to _bold_.

`colout` comes with some predefined themes to rapidely color well-known outputs
(see the `-t` switch below).

If the python-pygments library is available, `colout` can be used as an interface
to it (see also the `-s` switch below).

`colout` is released under the GNU Public License v3.


## OPTIONS

* `-h`, `--help`:
  Show an help message and exit

* `-e`, `--stderr`:
  Output on the standard error instead of standard output.

* `-g`, `--groups`:
  For color maps (like "rainbow"), iterate over matching groups in the pattern instead of over patterns.

* `-c`, `--colormap`:
  Use the given list of comma-separated colors as a colormap (cycle the colors at each match).

* `-t`, `--theme`:
  Interpret PATTERN as a predefined theme (perm, cmake, g++, etc.)

* `-s`, `--source`:
  Interpret PATTERN as a source code readable by the Pygments library. If the first letter of PATTERN
  is upper case, use the 256 colors mode, if it is lower case, use the 8 colors mode.
  In 256 colors, interpret COLOR as a Pygments style (e.g. "default").


## REGULAR EXPRESSIONS

A regular expression (or _regex_) is a pattern that describes a set of strings
that matches it.

`colout` understands regex as specifed in the _re_ python module. Given that
`colout` is generally called by the command line, you may have to escape
special characters that would be recognize by your shell.


## EXAMPLES

* Color in bold red every occurence of the word _color_ in colout sources:
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
  begining of the command is just bash magic to repeat the string "(\\w+)\\W+":
  `L=$(seq 10) ; P=${L//??/(\\w+)\\W+} ; head /var/log/auth.log | colout -g "^${P}(.*)$" rainbow`

* Color each line of a file with a different color among a 256 color gradient from cyan to green:
  `head /var/log/auth.log | colout -c "^.*$" 39,38,37,36,35,34`

* Color a source code in 8 colors mode, without seeing comments:
  `cat colout.py | grep -v "#" | colout -s python`

* Color a source code in 256 colors mode:
  `cat colout.py | colout -s Python monokai`

* Color a JSON stream:
  `echo '{"foo": "lorem", "bar":"ipsum"}' | python -mjson.tool | colout -t json`

* Color a source code substring:
  `echo "There is an error in 'static void Functor::operator()( EOT& indiv ) { return indiv; }' you should fix it" | colout "'(.*)'" Cpp monokai`

