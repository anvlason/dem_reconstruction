#!/usr/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.ndimage.morphology import grey_dilation, dilation
from osgeo import gdal, ogr, osr

gdal.AllRegister()
#from matplotlib import pyplot as plt 

def mk_mask(rname,vname):
    vds = ogr.Open(vname)
    vlr = vds.GetLayer()
    rds = gdal.Open(rname)
    drv = gdal.GetDriverByName('MEM')
    mds = drv.Create("",rds.RasterXSize,rds.RasterYSize,1,gdal.GDT_Byte)
    mds.SetProjection(rds.GetProjectionRef())
    mds.SetGeoTransform(rds.GetGeoTransform())
    gdal.RasterizeLayer(mds,[1],vlr,burn_values = [1])#,options = ["ATTRIBUTE=id"])#burn_values = [100])
    return mds.ReadAsArray()

def read_raster(rname):
    sds = gdal.Open(rname)
    return sds.ReadAsArray() 

def write_raster(rname,oname,data):
    sds=gdal.Open(rname)
    drv = gdal.GetDriverByName('GTiff')
    ods = drv.Create(oname,sds.RasterXSize,sds.RasterYSize,1,gdal.GDT_Float32)
    ods.SetProjection(sds.GetProjectionRef())
    ods.SetGeoTransform(sds.GetGeoTransform())
    ob = ods.GetRasterBand(1)
    ob.WriteArray(data)
    ob.SetNoDataValue(-9999)
    ob=None
    ods=None
    sds=None

def reconstruct(srs,prc,ln_mask,cmask,kernel):
    rec = grey_dilation(prc,structure=kernel)
    rec_m = rec + np.median((srs-rec)[ln_mask==1])
    min_val = -29#np.min(srs!=-9999)
    rec_m[rec_m<min_val]=-9999
    rec_m[cmask==1]=srs[cmask==1]
    return rec_m
'''
#cleanup source dem
iname="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0_dem_utm_egm2008.tif"
data = read_raster(iname)
#create sea mask
vname="/data/kolguev/shpindler/Shpindler_sea/Shpindler_sea_poly.shp"
sea_mask=mk_mask(iname,vname)
dmask=grey_dilation(sea_mask,size=1)
#set nodata
data[sea_mask==1]=-9999
#calc fill value 5% lowest
fill_val=np.percentile(data[(dmask)&(data>-9999)],5)
print(fill_val)
#correct sea by mask
data[sea_mask]=fill_val

'''


'''
kernel5=np.asarray([[1,0,1,0,1],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[1,0,1,0,1]])
kernel3=np.asarray([[1,0,1],[0,1,0],[1,0,1]])


rname = "/data/kolguev/dem_clip.tif"
vname = "/data/kolguev/rec_line.shp"
mname = "/data/kolguev/inside.shp"
data = read_raster(rname)
ln_mask = mk_mask(rname,vname)
cmask = mk_mask(rname,mname)

'''
'''
rec3 = grey_dilation(data,structure=kernel3)
rec3_m = rec3 + np.median((data-rec3)[ln_mask==1])

rec5 = grey_dilation(data,structure=kernel5)
rec5_m = rec5 + np.median((data-rec5)[ln_mask==1])

rec3_m[cmask==1]=data[cmask==1]
rec3_m[rec3_m<-29]=-9999

rec5_m[cmask==1]=data[cmask==1]
rec5_m[rec5_m<-29]=-9999

write_raster(rname,"/data/kolguev/wrk/reconstruct_k3.tif",rec3_m)
write_raster(rname,"/data/kolguev/wrk/reconstruct_k5.tif",rec5_m)
'''
'''
rec0 =  reconstruct(data,data,ln_mask,cmask,kernel3)
for _ in range(5):
    rec0 = reconstruct(data,rec0,ln_mask,cmask,kernel3)

write_raster(rname,"/data/kolguev/wrk/reconstruct_k3_5it.tif",rec0)
'''
