from lef_parser.lef_parser import *
import pyverilog
import sys
import io
import math
from pyverilog.vparser.parser import parse as vparse
from collections import OrderedDict
import hdlparse.verilog_parser as vlog
from getmn import getdim
import pprint
import argparse


def main(vfile, leffile, pinfile, aspectRatio=1, xmargin = 5520, ymargin = 10880):
    # vfile = "tests/spm_synthesis.v"
    ast, directives = vparse([vfile])
    # leffile = 'tests/lef.lef'
    parser = LefParser(leffile)
    parser.parse()
    margins = (xmargin, ymargin)
    # pprint.pprint(parser.statements)
    # print(parser.stack)
    # pprint.pprint(parser.layer_dict)
    # aspectRatio = 0.8
    cellnames, cells,ports = getComponents(ast)
    diearea = getdim(aspectRatio,getCellAreas(cells, parser),parser.cell_height*1000,float(getMinWidth(leffile))*1000,Util=0.6)
    diearea = (int(diearea[0]+2*margins[0]),int(diearea[1]+2*margins[1]))
    name = ast.children()[0].children()[0].name
    # print(diearea)
    output="""VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN """ +name+ """  ;
UNITS DISTANCE MICRONS 1000 ;"""+"\nDIEAREA ( 0 0 ) ( "+str(diearea[0])+" "+ str(diearea[1]) +" ) ;\n"

    # output = ""
    output+=printRows(parser,start=margins[1], lim = diearea[1]-margins[1], do=math.floor((diearea[1]-2*margins[1])/(1000*getMinWidth(leffile))), step= int(1000*getMinWidth(leffile)))
    output+=printTracks(parser.layer_dict.values())
    
    
    output+=cellnames
    output+=getPins(ports, xmax=diearea[0],ymax=diearea[1],pinfile=pinfile)
    nets, netstr = getNets(cells)
    output+=netstr

    output+="END DESIGN"
    print(output)
    with open('def.def', 'w') as f:
        f.write(output)
    getCellAreas(cells, parser)
    
    astshow = io.StringIO()
    ast.show(attrnames=True, buf=astshow)
    with open('ast.txt','w') as f:
        f.write(astshow.getvalue())
    
    return




def getComponents(ast):  
    components = []
    ports =[]
    def getInstances(x):
        if isinstance(x,pyverilog.vparser.ast.Instance):
            components.append(x)
          
        else:
            for child in x.children():
                # print(child)
                width = None
                if isinstance(child, pyverilog.vparser.ast.Input):
                   
                    if child.width:
                        # pass
                        width=(child.width.lsb.value,child.width.msb.value)
                    ports.append({
                        "name" : child.name,
                        "direction" : 'INPUT',
                        "width" : width
                    })
                if isinstance(child, pyverilog.vparser.ast.Output):
                    if child.width:
                        # pass
                        width=(child.width.lsb.value,child.width.msb.value)
                    ports.append({
                        "name" : child.name,
                        "direction" : 'OUPUT',
                        "width" : width
                    })
                getInstances(child) 

    # print([(port.name,port.type) for port in ast.children()[0].children()[0].portlist.ports])            

    getInstances(ast)
    # modules = []
    output = "COMPONENTS {0} ;\n".format(len(components))
    for c in components:
        output+="\t- {0} {1} ;\n".format(c.name,c.module)
        # modules.append(c.module)
    # print(output)
    output+="END COMPONENTS\n"
    return output, components,ports

def printRows(parser, start=10880, lim = 109710, step = 460, do=191 ):
     i = 0
     height = int(parser.cell_height*1000)
     out = ""
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

def getMinWidth(file='tests/lef.lef'):
    with open(file,'r') as f:
        for line in f:
            if 'SITE'in line and 'unithd' in line:
                for line in f:
                    s = line.split()
                    if s[0] == "SIZE":
                        # print(s[1],s[2],s[3])
                        return float((s[1]))
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
        output+="\t - {0} ".format(net)
        for connection in nets[net]:
            output+="( {0} {1} ) ".format(connection[0],connection[1])
        output+=" + USE SIGNAL ;\n"
    # print(output)
    output+="END NETS\n"
    return nets, output

def getPins(ports, xmax=98990, ymax=109710, pinfile = "tests/pins.txt", ):
    pins = []
    direction = '#N'
    directions = {}
    with open(pinfile, 'r') as f:
        for line in f:
            line = line.strip()
            if any(line == x for x in ['#N', '#E', '#W', '#S']):
                direction = line
                continue 
            else:
                directions[line] = direction
    # pprint.pprint(directions)


    for port in ports:
        if port['width']:
            lsb = int(port['width'][0])
            msb = int(port['width'][1])
            for i in range(lsb,msb+1):
                name = port['name']+'['+str(i)+']'
                if name not in directions:
                    directions[name] = '#N'
        else:
            if port['name'] not in directions:
                directions[port['name']] = '#N'
   
    for port in ports:
        if port['width']:
            lsb = int(port['width'][0])
            msb = int(port['width'][1])
            for i in range(lsb,msb+1):
                line = "\t - {0}[{2}] + NET {0}[{2}] + DIRECTION {1} + USE SIGNAL \n\t\t+ PORT\n".format(port['name'],port['direction'],i)
                name = port['name']+'['+str(i)+']'
                layer = "\t\t\t + LAYER met2 ( -140 -2000 ) ( 140 2000 )\n"
                if name not in directions or directions[name] == '#N' or directions[name] == '#S':
                    layer = "\t\t\t + LAYER met3 ( -2000 -300 ) ( 2000 300 )\n"
                line += layer
                pins.append(line)
        else:
            line = "\t - {0} + NET {0} + DIRECTION {1} + USE SIGNAL \n\t\t + PORT\n".format(port['name'],port['direction'])
            name = port['name']
            layer = "\t\t\t + LAYER met2 ( -140 -2000 ) ( 140 2000 )\n"
            if name not in directions or directions[name] == '#N' or directions[name] == '#S':
                layer = "\t\t\t + LAYER met3 ( -2000 -300 ) ( 2000 300 )\n"
            line += layer
            pins.append(line)
    output = "PINS {0} ;\n".format(len(pins))
    for pin in pins:
        output+=pin
    output+="END PINS\n"
    # print(output)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vfile",
                     help="filepath of the synthesised verilog module")
    parser.add_argument("leffile",
                     help="filepath of the lef file")
    parser.add_argument("pinfile",
                     help="filepath of the pin file")
    parser.add_argument("--x",
                     help="x margin between the core and the die", type=int)
    parser.add_argument("--y",
                     help="y margin between the core and the die", type=int)    
    parser.add_argument("--aspect",
                     help="aspect ratio of the core", type=float)    
    aspectRatio=1
    xmargin = 5520
    ymargin = 10880
    args = parser.parse_args()   
    if args.aspect:
        aspectRatio = args.aspect
    if args.x:
        xmargin = args.x
    if args.y:
        ymargin = args.y
                
    main(args.vfile,args.leffile,args.pinfile, aspectRatio, xmargin, ymargin)