# -*- coding: utf8 -*-
import os
import arcpy
from vector import areaSearch
import datetime
'''
# 4、根据输入矢量框、产品类型、分辨率检索，输出至文件数据库file geodatabase
'''
shpfile = arcpy.GetParameterAsText(0)
outdir = arcpy.GetParameterAsText(1)
area_search = areaSearch()
arcpy.MakeFeatureLayer_management(shpfile,"shpfile")
arcpy.MakeFeatureLayer_management(area_search.project,"project_lyr")
arcpy.SelectLayerByLocation_management("project_lyr","INTERSECT","shpfile")
cur = arcpy.da.SearchCursor("project_lyr",area_search.prj_fields)

for row in cur:
    prjid = row[2]
    prj_name = row[5]
    loca = row[1].replace('..', '').replace('/', '\SDE.')
    gdb_name = "TQ" + prjid+".gdb"
    file_GDB = os.path.join(outdir, gdb_name)
    try:
        arcpy.CreateFileGDB_management(outdir,gdb_name)
    except:
        pass
    prj_id_ = "prj_" + prjid
    location = area_search.sdefile + loca
    print "location:", location
    arcpy.MakeFeatureLayer_management(location, 'lacation_lyr')
    express = 'Prj_ID =' + "'" + prjid + "'"
    arcpy.SelectLayerByAttribute_management('lacation_lyr', 'NEW_SELECTION',express)
    export_path = os.path.join(file_GDB, prj_id_)
    arcpy.CopyFeatures_management('lacation_lyr', export_path)

