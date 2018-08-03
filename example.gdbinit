
set confirm off

# Reversed yellow >>>, underlined green frame name, yellow »»»
set extended-prompt \[\e[7;33m\]>>>\[\e[0m\]\[\] \[\e[4;32m\]\f\[\e[0m\]\[\]\[\e[0;33m\] \n»»» \[\e[0m\]


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


define hook-break
    # Don't forget to run the command in the background
    shell cat /tmp/coloutPipe | colout "(Breakpoint) ([0-9]+) at (0x\S+): file (.+/)([^/]+), line ([0-9]+)." blue,red,cyan,none,white,yellow normal,bold,normal,normal,bold,normal &
  # You should start to consume the pipe before actually redirecting the command output into it.
    logging_on
end
define hookpost-break
    logging_off
end


define hook-run
    shell cat /tmp/coloutPipe | colout "^(Program received signal )(.+), (.+).$" yellow,red,yellow normal,bold | colout "^(Breakpoint) ([0-9]+),*\s+(0x\S+ )*(in )*(\S+) (\(.*\)) at (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,none,green,cpp,none,white,white,yellow normal,bold,normal,normal,bold,normal,normal,bold,bold,bold | colout "^(Starting program): (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" green,none,white,white,yellow normal,normal,bold,bold,bold | colout "^[0-9]+\s+(.*)$" Cpp  &
    logging_on
end
define hookpost-run
    logging_off
end


define hook-continue
    shell cat /tmp/coloutPipe | colout "^(Program received signal )(.*)(,.*)$" yellow,red,yellow bold | colout "^(Breakpoint) ([0-9]+),*\s+(0x\S+ )*(in )*(\S+) (\(.*\)) at (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,none,green,cpp,none,white,white,yellow normal,bold,normal,normal,bold,normal,normal,bold,bold,bold | colout "^[0-9]+\s+(.*)$" Cpp &
    logging_on
end
define hookpost-continue
    logging_off
end


# Full syntax highlighting for the `list` command.
define hook-list
    #shell cat /tmp/coloutPipe | colout --all --source cpp &
    shell cat /tmp/coloutPipe | colout "^([0-9]+)\s*(.*)$" red,Cpp &
    logging_on
end
# Don't forget the hookpost- or next coloring commands will fail.
define hookpost-list
    logging_off
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


define info hook-breakpoints
    shell cat /tmp/coloutPipe | colout "^([0-9]+)" red bold | colout "\sy\s" green | colout "\sn\s" red | colout "breakpoint" green normal | colout "watchpoint" orange normal | colout "\s0x\S+\s" blue normal | colout "(.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)$" none,white,white,yellow normal,bold &
    logging_on
end
define info hookpost-breakpoints
    logging_off
end


define info hook-line
    shell cat /tmp/coloutPipe | colout "^Line ([0-9]+) of \"(.*/)?(?:$|(.+?)(?:(\.[^.]*)|))\"" yellow,none,white,white bold | colout "(0x\S+) <(\S+)\+([0-9]+)>" blue,green,blue normal &
    logging_on
end
define info hookpost-line
    logging_off
end


define hook-frame
    #shell cat /tmp/coloutPipe | colout "^(#)([0-9]+)\s+(0x\S+ )*(in )*(.*) (at) (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,red,green,red,magenta,none,white,white,yellow normal,bold,normal,normal,bold,normal,normal,bold,bold,bold | colout "^([0-9]+)\s+(.*)$" yellow,Cpp &
    shell cat /tmp/coloutPipe | colout "^(#)([0-9]+)\s+(0x\S+ )*(in )*(.*) (\(.*\)) (at) (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,red,green,magenta,red,none,white,white,yellow normal,bold,normal,normal,normal,normal,normal,bold,bold,bold | colout "([\w\s]*?)(=)([^,]*?)([,\)])" yellow,blue,magenta,blue normal &
    logging_on
end
define hookpost-frame
    logging_off
end

# Don't forget to clean the adhoc pipe.
define hook-quit
    set confirm off
    shell rm -f /tmp/coloutPipe
end

define hook-display
    shell cat /tmp/coloutPipe | colout "^([0-9]+)(:) (.+?) (=) " red,blue,white,blue normal,normal,bold,normal | colout "(@)(0x\S+)(:)" red,blue,red normal &
    logging_on
end
define hookpost-display
    logging_off
end


