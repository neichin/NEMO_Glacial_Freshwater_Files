import netCDF4
import sys
sys.path.append('/Users/imerino/Documents/NEMO_Glacial_Freshwater_Files')
import numpy as np
from NEMO_ICB_File import *


#List of Ice shelves to consider#
listShelf=['lbc','fris','brl','jf','ar','ne','ais','w','sha','van','tot','mu','por','ade','mer','nin','coo','ren','dry','ris','sul','lan'
            ,'getz','cd','thw','pig','cosg','abb','ven','geo','wor']

listSectors=['westIndian','eastIndian','rossSea','amundsen','bellingshausen','weddell']

#First coastal point, needed to use extractCoastNew. It is an ocean point with land at (x,y-1)
xinit=28
yinit=863

#Distance between calving sources in shelves
distSourcesShelf = 50
#Distance between calving sources in sectors
distSourcesSectors = 150
#########


#Open needed Files
ncfile = netCDF4.Dataset('/Users/imerino/Documents/Freshwater_Orca12/AA12_bathymetry_v2.4.nc','a')
var = np.array(ncfile.variables['Bathymetry'])[:,:]
ncfile.close()

ncfile = netCDF4.Dataset('/Users/imerino/Documents/Freshwater_Orca12/AA12_coordinates.nc','a')
varLon = np.array(ncfile.variables['glamt'])[:,:]
varLat = np.array(ncfile.variables['gphit'])[:,:]
ncfile.close()
###########

[ydim,xdim]=var.shape

#######1Clean the Bathymetry, 0->land, 1000->ocean
var=cleanBathy(var,1000)
########

######## Create rmpty calving flux variable
CalvingFlux=np.zeros(var.shape)
########

######## Extract the list of consecutive coastal points
listP=extractCoast(var,xinit,yinit)
#List of X and Y values in the grid referencial
xP=zip(*listP)[0]
yP=zip(*listP)[1]
#####

####### Fill calving flux variable with data from the list of shelves and sectors   
createCalvingFile(CalvingFlux,listShelf,distSourcesShelf,xP,yP,varLon,varLat)
createCalvingFile(CalvingFlux,listSectors,distSourcesSectors,xP,yP,varLon,varLat)

ncfile = netCDF4.Dataset('/Users/imerino/Documents/Freshwater_Orca12/calvingORCA12_Depoorter2013.nc','a')
calv = ncfile.variables['calvingFlux']
calv[:,:]=CalvingFlux[:,:]
ncfile.close()