# -*- coding: utf8 -*-
import os
import arcpy
from vector import areaSearch

province = arcpy.GetParameterAsText(0)
city = arcpy.GetParameterAsText(1)
country = arcpy.GetParameterAsText(2)
outdir = arcpy.GetParameterAsText(3)
area_search = areaSearch()

# arcpy.AddMessage("city value:{0}".format(city))
if country <> "":
    express = "ADMINCODE = '{0}'".format(country.split('-')[1])
    arcpy.MakeFeatureLayer_management(area_search.country,"area_lyr",express)
elif city <> "":
    express = "ADMINCODE = '{0}'".format(city.split('-')[1])
    arcpy.MakeFeatureLayer_management(area_search.city, "area_lyr",express)
else:
    express = "ADMINCODE = '{0}'".format(province.split('-')[1])
    arcpy.MakeFeatureLayer_management(area_search.province, "area_lyr",express)

arcpy.MakeFeatureLayer_management(area_search.project, "project_lyr")
arcpy.SelectLayerByLocation_management("project_lyr", "INTERSECT", "area_lyr")
cur = arcpy.da.SearchCursor("project_lyr", area_search.prj_fields)
for row in cur:
    prjid = row[2]
    arcpy.AddMessage(prjid)
    prj_name = row[5]
    loca = row[1].replace('..', '').replace('/', '\SDE.')
    gdb_name = "TQ" + prjid.replace('.','')+".gdb"
    file_GDB = os.path.join(outdir, gdb_name)
    try:
        arcpy.CreateFileGDB_management(outdir,gdb_name)
    except:
        pass
    prj_id_ = "prj_" + prjid.replace('.','')
    location = area_search.sdefile + loca
    print "location:", location
    arcpy.MakeFeatureLayer_management(location, 'lacation_lyr')
    express = 'Prj_ID =' + "'" + prjid + "'"
    arcpy.SelectLayerByAttribute_management('lacation_lyr', 'NEW_SELECTION',express)
    export_path = os.path.join(file_GDB, prj_id_)
    arcpy.CopyFeatures_management('lacation_lyr', export_path)
    arcpy.Delete_management('lacation_lyr')