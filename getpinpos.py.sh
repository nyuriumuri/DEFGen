
def Getpinposition (no_of_pins,totalW,totalL,directions):
        dictionary_pin={}
        Wdist_between_pins=totalW/(no_of_pins+2)
        Ldist_between_pins=totalL/(no_of_pins+2)
        i=1
        for pin in directions['N']:
            
            no_of_pins=len(directions['N'])
            Wdist_between_pins=totalW/(no_of_pins+2)
            Ldist_between_pins=0
            xpos=Wdist_between_pins*i
            dictionary_pin[pin]=(xpos,totalL)
            i=i+1
        i=1    
        for pin in directions['E']:
            no_of_pins=len(directions['E'])
            Ldist_between_pins=totalL/(no_of_pins+2)
            Wdist_between_pins=0
            ypos=Ldist_between_pins*i
            dictionary_pin[pin]=(totalW,ypos)
            i=i+1
        i=1    
        for pin in directions['S']:
            no_of_pins=len(directions['S'])
            Wdist_between_pins=totalW/(no_of_pins+2)
            Ldist_between_pins=0
            xpos=Wdist_between_pins*i
            dictionary_pin[pin]=(xpos,0)
            i=i+1
        i=1    
        for pin in directions['W']:
            no_of_pins=len(directions['W'])
            Ldist_between_pins=totalL/(no_of_pins+2)
            Wdist_between_pins=0
            ypos=Ldist_between_pins*i
            dictionary_pin[pin]=(0,ypos)
            i=i+1
        i=1
        return dictionary_pin