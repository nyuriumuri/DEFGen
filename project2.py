from lef_parser import *
import pyverilog
import sys
import io
from pyverilog.vparser.parser import parse as vparse
from collections import OrderedDict

import pprint
def main():
    ast, directives = vparse(["spm.synthesis.v"])
    parser = LefParser('lef.lef')
    parser.parse()
    # pprint.pprint(parser.statements)
    # print(parser.stack)
    # pprint.pprint(parser.layer_dict)
    name = "lef"
    diearea = ( 98990, 109710 )
    output="""VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN """ +name+ """  ;
UNITS DISTANCE MICRONS 1000 ;"""+"\nDIEAREA ( 0 0 ) ( "+str(diearea[0])+" "+ str(diearea[1]) +" ) ;\n"

    # output = ""
    output+=printRows(parser)
    output+=printTracks(parser.layer_dict.values())
    cellnames, cells = getComponents(ast)
    output+=cellnames
    nets, netstr = getNets(cells)
    output+=netstr
    output+="END DESIGN"
    print(output)
    with open('def.def', 'w') as f:
        f.write(output)
    getCellAreas(cells, parser)
    getMinWidth()
    
    return





def getComponents(ast):  
    components = []
    def getInstances(x):
        if isinstance(x,pyverilog.vparser.ast.Instance):
            components.append(x)
          
        else:
            for child in x.children():
                getInstances(child) 
    
    getInstances(ast)
    # modules = []
    output = "COMPONENTS {0} ;\n".format(len(components))
    for c in components:
        output+="\t\t- {0} {1} ;\n".format(c.name,c.module)
        # modules.append(c.module)
    # print(output)
    output+="END COMPONENTS\n"
    return output, components

def printRows(parser, start=10880, lim = 109710):
     i = 0
     height = int(parser.cell_height*1000)
     out = ""
     do = 191
     step = 460
     while (start+(i+1)*height) <= lim-start:
         out+="ROW ROW_{0} unithd 5520 {1} {4} DO {2} BY 1 STEP {3} 0 ; \n".format(i, start+i*height, do, step, ('FS' if i%2 else 'N'))
         i+=1
    #  print(out)
     return out


def printTracks(layers):
    track = ""
    
    for layer in layers:
    
        # layer = parser.layer_dict[layer]
        if layer.layer_type == "ROUTING":
                
            factor=1000
            numtrack = 200
           
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
            track+="TRACKS X "+str(widthx)+" DO "+str(numtrack)+" STEP "+str(pitchx) + " LAYER "+ layer.name+" ;\n"
            track+="TRACKS Y "+str(widthy)+" DO "+str(numtrack)+" STEP "+str(pitchy) + " LAYER "+ layer.name+" ;\n"
        
        # print(layer)
    # print(track)
    return track
   

def getCellAreas(cells, parser, factor=1000):
    area = 0
    for cell in cells:
        size = parser.macro_dict[cell.module].info["SIZE"]
        area += size[0]*size[1]*factor*factor
        # print(size)
    # print(area)
    return area

def getMinWidth(file='lef.lef'):
    with open(file,'r') as f:
        for line in f:
            if 'SITE'in line and 'unithd' in line:
                for line in f:
                    s = line.split()
                    if s[0] == "SIZE":
                        # print(s[1],s[2],s[3])
                        return (s[1])
    return 1



def getNets(components):
    nets = {}
    for c in components:
        for p in c.portlist:
            netname = p.argname
            if isinstance(netname, pyverilog.vparser.ast.Pointer):
                # print(netname.var,netname.ptr)
                # netname = netname.var
                netname = str(netname.var)+"["+str(netname.ptr)+"]"
            else:
                netname = netname.name
            if netname not in nets:
                # print(netname)
                nets[netname] = []
            nets[netname].append((c.name,p.portname))
    output = "NETS {0} ;\n".format(len(nets))
    for net in sorted(nets):
        output+="\t \t- {0} ".format(net)
        for connection in nets[net]:
            output+="( {0} {1} ) ".format(connection[0],connection[1])
        output+=" + USE SIGNAL ;\n"
    # print(output)
    output+="END NETS\n"
    return nets, output
if __name__ == "__main__":
    main()