import math           
def getdim (aspectratio,totalarea,lmin,wmin,Util=0.6):
    corearea= totalarea/Util
    
    m=math.sqrt(corearea/(lmin*lmin*aspectratio))
    n=aspectratio*m*lmin/wmin
    return m,n
 