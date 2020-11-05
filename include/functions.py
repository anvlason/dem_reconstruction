#!/usr/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.ndimage.morphology import grey_dilation
from osgeo import gdal, ogr, osr

gdal.AllRegister()
gdal.UseExceptions()

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
def mk_mask(rname,vname):
    '''
    rasterize vector layer to raster extent
    rname - input raster name
    vname - input vector name
    '''
    vds = ogr.Open(vname)
    vlr = vds.GetLayer()
    rds = gdal.Open(rname)
    drv = gdal.GetDriverByName('MEM')
    mds = drv.Create("",rds.RasterXSize,rds.RasterYSize,1,gdal.GDT_Byte)
    mds.SetProjection(rds.GetProjectionRef())
    mds.SetGeoTransform(rds.GetGeoTransform())
    gdal.RasterizeLayer(mds,[1],vlr,burn_values = [1])#,options = ["ATTRIBUTE=id"])#burn_values = [100])
    return mds.ReadAsArray()

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
def read_raster(rname):
    '''
    read Gdal rater tto numpy array
    rname - input raster name
    '''
    sds = gdal.Open(rname)
    return sds.ReadAsArray() 

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
def write_raster(rname,oname,data):
    '''
    save single band numpy array to GTiff file
    rname - file name to take projection and geotransform
    oname - output name
    data - numpy array
    '''
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

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
def reconstruct(srs,prc,ln_mask,cmask,kernel):
    '''
    reconstruct coast line by dilation
    src - source dem
    prc - dem for processing
    lm_mask - mask with correction boundary
    cmask - mask with unmodified boundary
    kernel - structure element for dilation operation
    kernel5=np.asarray([[1,0,1,0,1],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[1,0,1,0,1]])
    kernel3=np.asarray([[1,0,1],[0,1,0],[1,0,1]])
    '''
    rec = grey_dilation(prc,structure=kernel)
    rec_m = rec + np.median((srs-rec)[ln_mask==1])
    min_val = -29#np.min(srs!=-9999)
    rec_m[rec_m<min_val]=-9999
    rec_m[cmask==1]=srs[cmask==1]
    return rec_m

'''
kernel5=np.asarray([[1,0,1,0,1],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[1,0,1,0,1]])
kernel3=np.asarray([[1,0,1],[0,1,0],[1,0,1]])


rname = "/data/kolguev/dem_clip.tif"
rname = "/data/kolguev/SETSM_W1W1_20110904_1020010014625A00_1020010015411700_seg1_2m_v3.0/SETSM_W1W1_20110904_1020010014625A00_1020010015411700_seg1_2m_v3.0_dem_egm2008_cor.tif"
vname = "/data/kolguev/rec_line.shp"
mname = "/data/kolguev/inside.shp"

rname ="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0_dem_utm_egm2008_clip_fixed_1.tif"
oname ="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0_dem_utm_egm2008_clip_fixed_1_rec4.tif"
vname="/data/kolguev/shpindler/Shpindler_2015_reconstruct/Shpindler_2015_reconstruct.shp"
mname="/data/kolguev/shpindler/Shpindler_2015_reconstruct/Shpindler_2015_reconstruct_poly.shp"

rname = "/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/merged_fill.tif"
vname = "/data/kolguev/shpindler/Shpindler_DEM_cut/Shpindler_DEM_cut.shp"
mname = "/data/kolguev/shpindler/Shpindler_DEM_cut/Shpindler_DEM_cut_reg.shp"
oname = "/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/merged_fill_recon_10.tif"

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

for _ in range(10):
    rec0 = reconstruct(data,rec0,ln_mask,cmask,kernel3)
rec0[rec0<0]=0
write_raster(rname,oname,rec0)
'''
