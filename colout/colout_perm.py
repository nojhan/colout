
def theme():
    p="([rwxs-])"
    reg="^([d-])"+p*9+"\s.*$"
    colors="blue"+",green"*3+",yellow"*3+",red"*3
    styles="normal"+ ",normal,italic,bold"*3
    return [ [reg, colors, styles] ]

