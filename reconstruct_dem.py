#!/usr/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import timeit

from include.functions import read_raster, mk_mask, reconstruct, write_raster

#5x5 kernel
kernel5=np.asarray([[1,0,1,0,1],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[1,0,1,0,1]])
#3x3 kernel
kernel3=np.asarray([[1,0,1],[0,1,0],[1,0,1]])

def usage():
    print("reconstruct_dem.py iname=[input dem in GDAL supported format] vname=[polyline for boundary reconstruction in OGR supported format] mname=[polygon for mask unmodified area]\n"
            "oname=[output name] kernel=<kernel size: 3 or 5, default 3> niter=<count of iterations, default 1> --clip_negative <set all negative values to 0>")

if __name__ == '__main__':
    tic=timeit.default_timer()
    kernel = kernel3
    niter = 1
    iname = None
    vname = None
    mname = None
    oname = None
    clip_neg = False
    #args parcing
    if len(sys.argv) < 4:
        print("Bad arguments")
        usage()
        sys.exit(-1)
    for arg in sys.argv:
        if arg.startswith("iname="):
            iname=arg.split("=")[1]
        elif arg.startswith("vname="):
            vname=arg.split("=")[1]
        elif arg.startswith("mname="):
            mname=arg.split("=")[1]
        elif arg.startswith("oname="):
            oname=arg.split("=")[1]
        elif arg.startswith("kernel="):
            try:
                k = int(float(arg.split("=")[1]))
            except:
                print("Wrong argument: %s must be numeric 3 or 5")
                sys.exit(-2)
            if k==3:
                kernel=kernel3
            elif k==5:
                kernel=kernel5
            else:
                print("Wrong argument: %s must be numeric 3 or 5")
                sys.exit(-2)
        elif arg.startswith("niter="):
            try:
                niter = int(float(arg.split("=")[1]))
            except:
                print("Wrong argument: %s must be positive integer > 0")
                sys.exit(-2)
            if niter<1:
                print("Wrong argument: %s must be positive integer > 0")
                sys.exit(-2)
        elif arg.startswith("--clip_negative"):
            clip_neg=True
    '''
    iname = "./data/dem_clip.tif"
    vname = "./data/rec_line.shp"
    mname = "./data/inside.shp"
    oname = "./data/reconstructed.tif"
    '''

    if (iname is None) or (vname is None) or (mname is None) or (oname is None):
        print("Bad arguments")
        usage()
        sys.exit(-1)

    #load input data
    try:
        print("Load input data")
        data = read_raster(iname)
        ln_mask = mk_mask(iname,vname)
        cmask = mk_mask(iname,mname)
    except Exception as e:
        print("Error while data loading with: %s"%(e))
        sys.exit(-3)
    #processing
    try:
        print("Reconstruction")
        rec0 =  reconstruct(data,data,ln_mask,cmask,kernel)
        for _ in range(niter-1):
            rec0 = reconstruct(data,rec0,ln_mask,cmask,kernel3)
        if clip_neg:
            rec0[rec0<0]=0
    except Exception as e:
        print("Error while data processing with: %s"%(e))
        sys.exit(-3)
    #save result
    try:
        print("Save result")
        write_raster(iname,oname,rec0)
    except Exception as e:
        print("Error while save result with: %s"%(e))
        sys.exit(-3)
    print("Processing done by %.2f"%(timeit.default_timer()-tic))
    sys.exit(0)
