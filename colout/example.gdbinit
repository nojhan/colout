
# Don't wrap line or the coloring regexp won't work.
set width 0

# Create a named pipe to get outputs from gdb
shell test -e /tmp/coloutPipe && rm /tmp/coloutPipe
shell mkfifo /tmp/coloutPipe

# A yellow prompt
set prompt \033[0;33mgdb>>>\033[0m 

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


define hook-continue
    shell cat /tmp/coloutPipe | colout "^Program received signal.*$" | colout "^(Breakpoint) ([0-9]+),*\s+(0x\S+ )*(in )*(\S+) (\(.*\)) at (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,none,green,cpp,none,white,white,yellow normal,bold,normal,normal,bold,normal,normal,bold,bold,bold | colout "^[0-9]+\s+(.*)$" Cpp &
    logging_on
end
define hookpost-continue
    logging_off
end


# Full syntax highlighting for the `list` command.
define hook-list
    shell cat /tmp/coloutPipe | colout --all --source Cpp &
    logging_on
end
# Don't forget the hookpost- or next coloring commands will fail.
define hookpost-list
    logging_off
end


define hook-backtrace
    # match the [path]file[.ext]: (.*/)?(?:$|(.+?)(?:(\.[^.]*)|))
    shell cat /tmp/coloutPipe | colout "^(#)([0-9]+)\s+(0x\S+ )*(in )*(\S+) (\(.*\)) at (.*/)?(?:$|(.+?)(?:(\.[^.]*)|)):([0-9]+)" red,red,blue,none,green,cpp,none,white,white,yellow normal,bold,normal,normal,bold,normal,normal,bold,bold,bold &
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


# Don't forget to clean the adhoc pipe.
define hook-quit
    shell rm -f /tmp/coloutPipe
end

