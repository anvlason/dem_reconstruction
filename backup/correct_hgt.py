import numpy as np
from osgeo import gdal, osr, ogr
from scipy import stats
from scipy.ndimage.morphology import grey_dilation


gdal.AllRegister()

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

kernel5=np.asarray([[1,0,1,0,1],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[1,0,1,0,1]])
kernel3=np.asarray([[1,0,1],[0,1,0],[1,0,1]])


iname="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/merge.vrt"
oname="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0_dem_utm_egm2008_clip_fixed_1.tif"
onamep="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0_dem_utm_egm2008_clip_fixed_p_1.tif"
onamem="/data/kolguev/shpindler/SETSM_WV03_20150916_104001001167EB00_104001001181B600_seg1_2m_v3.0/merged.tif"
vname="/data/kolguev/shpindler/Shpindler_sea/Shpindler_sea_poly.shp"

data=read_raster(iname)
smask=mk_mask(iname,vname)
data[0,smask==1]=-9999
data[1,smask==1]=-9999

ndmask=np.maximum(data[0]==-9999,data[1]==-9999)
reg = stats.linregress(data[1,~ndmask],data[0,~ndmask])
print(reg)
fixed=data[1]*reg.slope+reg.intercept
fixed[data[1]==-9999]=-9999

vname="/data/kolguev/shpindler/Shpindler_2015_reconstruct/Shpindler_2015_reconstruct.shp"
mname="/data/kolguev/shpindler/Shpindler_2015_reconstruct/Shpindler_2015_reconstruct_poly.shp"
ln_mask = mk_mask(iname,vname)
cmask = mk_mask(iname,mname)

rec0 =  reconstruct(fixed,fixed,ln_mask,cmask,kernel3)
for _ in range(3):
    rec0 = reconstruct(fixed,rec0,ln_mask,cmask,kernel3)


rec0[data[1]==-9999]=9999
data[0,data[0]==-9999]=9999
result = np.minimum(rec0,data[0])
result[result==9999]=-9999
write_raster(iname,onamem,result)
'''
poly = np.polyfit(data[1,~ndmask],data[0,~ndmask],deg=2)
fixedp = np.polyval(poly,data[1])
fixedp[data[1]==-9999]=-9999
print(stats.linregress(fixedp[~ndmask],data[0,~ndmask]))

write_raster(iname,oname,fixed)
write_raster(iname,onamep,fixedp)
'''