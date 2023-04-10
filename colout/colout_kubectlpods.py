#encoding: utf-8

def theme(context):

    return context, [
        ["(NAME|READY|STATUS|RESTARTS|AGE|IP|NODE|NOMINATED|NODE|READINESS|GATES)",
         "white", "underline"],
        ["^([^\s]+)", "blue"],
        ["(\d+/\d+)", 
            context['Selectors']['percent'](r'(\d+)/(\d+)', groups=2, ranges=(30,80),  colors=("red", "yellow", "green"))
        ],
        ["(Running)", "green"],
        ["(CrashLoopBackOff|RunContainerError|Error)", "red"],
        ["^[^\s]+\s+[^\s]+\s+([^\s]+)", "yellow"],
        ["^[^\s]+\s+[^\s]+\s+([^\s]+)\s+([1-9]\d*)\s+", "red"],
    ]

