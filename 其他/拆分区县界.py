# -*- coding: cp936 -*-
import arcpy,os


Proshp = raw_input("����ʡ�磺")
Cntyshp = raw_input("�������ؽ磺")
FolderPath = raw_input("����洢·����")
arcpy.MakeFeatureLayer_management(Proshp,"prolyr")
rows = arcpy.SearchCursor(Proshp)
for row in rows:
    ProName = row.getValue("NAME")
    path = FolderPath + "\\" + ProName 
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
     
