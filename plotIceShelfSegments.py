import netCDF4
import sys
sys.path.append('/Users/imerino/Documents/NEMO_Glacial_Freshwater_Files')
import numpy as np
from NEMO_ICB_File import *
from pylab import *


#--Define a discrete sequence of numColors colors
def colormapDef(numColors,colormap):
    NUM_COLORS = numColors
    
    cm = get_cmap(colormap)
    colors=[]
    for i in range(NUM_COLORS):
        colors.append(cm(1.*i/NUM_COLORS))  # color will now be an RGBA tuple
    
    return colors
    
    
colors=colormapDef(31,'Set1')

#List of Ice shelves to consider#
listShelf=['lbc','fris','brl','jf','ar','ne','ais','w','sha','van','tot','mu','por','ade','mer','nin','coo','ren','dry','ris','sul','lan'
            ,'getz','cd','thw','pig','cosg','abb','ven','geo','wor']

listSectors=['westIndian','eastIndian','rossSea','amundsen','bellingshausen','weddell']


#First coastal point, needed to use extractCoastNew. It is an ocean point with land at (x,y-1)
xinit=28
yinit=863

#Open needed Files
ncfile = netCDF4.Dataset('/Users/imerino/Documents/Freshwater_Orca12/AA12_bathymetry_v2.4.nc','a')
var = np.array(ncfile.variables['Bathymetry'])[:,:]
ncfile.close()

ncfile = netCDF4.Dataset('/Users/imerino/Documents/Freshwater_Orca12/AA12_coordinates.nc','a')
varLon = np.array(ncfile.variables['glamt'])[:,:]
varLat = np.array(ncfile.variables['gphit'])[:,:]
e1t = np.array(ncfile.variables['e1t'])[:,:]
e2t = np.array(ncfile.variables['e2t'])[:,:]
ncfile.close()
###########
area=e1t*e1t

[ydim,xdim]=var.shape

#######1Clean the Bathymetry, 0->land, 1000->ocean
var=cleanBathy(var,1000)
########

######## Extract the list of consecutive coastal points
listP=extractCoast(var,xinit,yinit)
#List of X and Y values in the grid referencial
xP=zip(*listP)[0]
yP=zip(*listP)[1]
#####


plt.figure(1)

#Default plot
ax=plt.imshow(var,cmap='Greys_r')

#Plot individualy each ice shelf
indexShelf=0
for shelf in listShelf:
    limits=globals()[shelf]#Get geospatial limits of the iceshelf i from data.py. It may be made by segments, check data.py
    XIceShelf,YIceShelf,PointsPerSegment,NumOfSegments = getIceShelfSegmentPoints(limits,xP,yP,varLon,varLat) #Extract (x,y)
    im=plt.scatter(XIceShelf, YIceShelf #Scatter plot over previous imshow plot
        ,s=100
        ,c=colors[indexShelf]
        ,edgecolor='none'
        #,zorder=0
    )
    indexShelf=indexShelf+1


plt.gca().invert_yaxis()
plt.show()
