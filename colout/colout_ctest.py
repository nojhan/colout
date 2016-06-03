
def theme(context):
    # CTest theme:
    passed="green"
    notpassed="red"

    # If the user do not ask for his own colormap
    # if not context["user_defined_colormaps"]:
    #     # A palette that goes: purple, orange, white
    #     percs = [45, 39, 33, 27, 21, 57, 63, 62, 98, 97, 133, 132, 138, 173, 172, 208, 214, 220, 226, 228, 229, 230, 231, 255]
    #     context["colormaps"]["Scale"] = percs

    return context,[
        # Passed
        [ "^\s*[0-9]+/[0-9]+ Test\s+#[0-9]+: (.*)\s+\.+\s+(Passed)", passed],
        [ "^\s*[0-9]+/[0-9]+ Test\s+#[0-9]+: (.*)\s+\.+(\*{3}.*)\s+.*", notpassed]
    ]
