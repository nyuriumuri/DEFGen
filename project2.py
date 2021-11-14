from lef_parser import *
import pprint
def main():
    parser = LefParser('lef.lef')
    parser.parse()
    # pprint.pprint(parser.statements)
    # print(parser.stack)
    # pprint.pprint(parser.layer_dict)
    name = "lef"
    diearea = ( 98990, 109710 )
    print("""VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN """ +name+ """  ;
UNITS DISTANCE MICRONS 1000 ;"""+"\nDIEAREA ( 0 0 ) ( "+str(diearea[0])+" "+ str(diearea[1]) +") ;")

    printRows(parser)
    printTracks(parser)


def printRows(parser, start=10880, lim = 109710):
     i = 0
     height = int(parser.cell_height*1000)
     out = ""
     do = 191
     step = 460
     while (start+(i+1)*height) <= lim-start:
         out+="ROW ROW_{0} unithd 5520 {1} N DO {2} BY 1 STEP {3} 0 ; \n".format(i, start+i*height, do, step)
         i+=1
     print(out)
     return out
def printTracks(parser):
    for layer in parser.layer_dict.values():
        if layer.layer_type != "ROUTING":
            continue
        factor=1000
        numtrack = 200
        track = ""
        # print(layer.offset, layer.pitch)
        pitchx = 0
        pitchy = 0
        widthx= 0 
        widthy = 0
        if type(layer.pitch) is tuple:
            pitchx = int(layer.pitch[0] *factor)
            pitchy = int(layer.pitch[1]*factor)
        else:
            pitchx=pitchy=int(layer.pitch*factor)
        
        if type(layer.offset) is tuple:
            widthx = int(layer.offset[0]*factor)
            widthy = int(layer.offset[1]*factor)
        else:
            widthx=widthy = int(layer.offset*factor)
        track+="TRACKS X "+str(widthx)+" DO "+str(numtrack)+" STEP "+str(pitchx) + " LAYER "+ layer.name+"\n"
        track+="TRACKS Y "+str(widthy)+" DO "+str(numtrack)+" STEP "+str(pitchy) + " LAYER "+ layer.name
        
        # print(layer)
        print(track)
        return track
    # print(parser.via_dict)
    # print(parser.stack)
    # print(parser.macro_dict)
    # print(parser.cell_height)

if __name__ == "__main__":
    main()