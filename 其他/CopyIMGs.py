# -*- coding: cp936 -*-
import arcpy,os
from shutil import copy
imgshp = r"F:\test\imgs1.shp"
imgsourceFolder = r"W:\4bands\第四批影像（12.21）\FUS"
targetFolder = r"E:\JiangXi_IMG1221"
imglist = []
cursor = arcpy.SearchCursor(imgshp)
for row in cursor:
    imgname = row.getValue("name") + "_GF1_DOM_4_fus.tif"
    print imgname
    imglist.append(imgname)
for imglyr  in imglist:
    print imglyr
    sourcefile = os.path.join(imgsourceFolder,imglyr)
    targetfile = os.path.join(targetFolder,imglyr)
    copy(sourcefile,targetfile)
print "ok"
    


    