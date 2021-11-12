from lef_parser import *
import pprint
parser = LefParser('lef.lef')
parser.parse()
# pprint.pprint(parser.layer_dict)
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
# print(parser.via_dict)
# print(parser.stack)
# print(parser.macro_dict)
# print(parser.cell_height)