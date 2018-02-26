
def theme(context):
    p="([-rwxsStT])"
    reg="^([-dpcCDlMmpPs?])"+p*9+"\s.*$"
    colors="blue"+",green"*3+",yellow"*3+",red"*3
    styles="normal"+ ",normal,italic,bold"*3
    return context,[ [reg, colors, styles] ]

