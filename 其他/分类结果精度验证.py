# -*- coding: cp936 -*-
import arcpy
from arcpy.sa import *
arcpy.env.workspace = r"Z:\样本\样本（第一批）\分类结果\栅格"

in_point_features = r"Z:\样本_验证\验证点数据（一级类）\jiangxi_2.shp"
print "have read  " + str(in_point_features)

fenlei_RST = arcpy.ListRasters("*","TIF")

arcpy.CheckOutExtension("Spatial")
i = 1
for in_raster in fenlei_RST:
    print "reading  " + str(in_raster)
    out_point_features = r"Z:\样本_验证\验证点数据（一级类）" + "\\" + "jiangxi_2_yanzheng" + str(i) + ".shp"
    ExtractValuesToPoints(in_point_features, in_raster, out_point_features,"NONE","VALUE_ONLY")
    print str(in_raster) + "  Processed"
    i = i + 1