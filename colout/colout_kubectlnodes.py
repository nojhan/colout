
def theme(context):

    return context, [
        ["(NAME|STATUS|ROLES|AGE|VERSION|INTERNAL-IP|EXTERNAL-IP|OS-IMAGE|KERNEL-VERSION|CONTAINER-RUNTIME)",
         "white", "underline"],
        ["^([^\s]+)", "blue"],
        ["(Ready)", "green"],
        ["(MemoryPressure|DiskPressure|PIDPressure|NetworkUnavailable|SchedulingDisabled)", "red"],
        ["^[^\s]+\s+[^\s]+\s+([^\s]+)", "yellow"],
        ["^[^\s]+\s+[^\s]+\s+([^\s]+)\s+([1-9]\d*)\s+", "red"],
    ]

