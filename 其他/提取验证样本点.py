# -*- coding: cp936 -*-
#栅格转面
#面转中心点
import arcpy
#import os

input_Raster = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb\JiangXiPro_DOM_Clip"
create_Dataset = "dataset0"
DefaultDataBase = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"
save_Path = DefaultDataBase + "\\" +  create_Dataset

out_polygon_features = save_Path + "\\" + "Raster2Polygon"
arcpy.RasterToPolygon_conversion(input_Raster,out_polygon_features,"NO_SIMPLIFY","VALUE")

out_feature_class = save_Path + "\\" + "Fea2Pnt"
arcpy.FeatureToPoint_management (out_polygon_features, out_feature_class,"INSIDE")
