
import colout
def theme( item ):
    item = colout.colorup( item, '[{}]' )
    item = colout.colorup( item, '[:,]', "blue" )
    item = colout.colorup( item, '".*"', "green" )
    return item

