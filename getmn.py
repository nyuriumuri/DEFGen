import math           
def getdim (aspectratio,totalarea,lmin,wmin,Util=0.6):
    print(totalarea)
    corearea= math.ceil(totalarea/Util)
    print(corearea)
    m=math.sqrt(corearea*aspectratio/(wmin*wmin))
    n=m/lmin*wmin/aspectratio
    print(corearea/(n*lmin))
    return math.ceil(m)*wmin,math.ceil(n)*lmin
 

""" input = [ xmax,
           ymax,
            directions =    {
                    'N' : [
                            pin1,
                            pin2,
                            ... 
                    ],

                    'W': [
                        pin1,
                        pin2,
                    ]
                }
 }
 """