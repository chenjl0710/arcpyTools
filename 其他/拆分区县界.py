# -*- coding: cp936 -*-
import arcpy,os


Proshp = raw_input("输入省界：")
Cntyshp = raw_input("输入区县界：")
FolderPath = raw_input("输入存储路径：")
arcpy.MakeFeatureLayer_management(Proshp,"prolyr")
rows = arcpy.SearchCursor(Proshp)
for row in rows:
    ProName = row.getValue("NAME")
    path = FolderPath + "\\" + ProName 
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
     
