#encoding: utf-8
import colout
def theme( item ):
    item = colout.colorup( item, "error", "red", "bold" )
    item = colout.colorup( item, "warning", "magenta", "bold" )
    item = colout.colorup( item, "\[-W.*\]", "magenta", "normal" )
    item = colout.colorup( item, "note", "blue", "bold" )
    item = colout.colorup( item, ":([0-9]+):[0-9]*", "yellow", "normal" )
    item = colout.colorup( item, "^((/\w+)+)\.(h|cpp)", "white", "normal" )
    item = colout.colorup( item, "'(.*)'", "blue", "normal" )

    return item

