# -*- coding: cp936 -*-
import arcpy
arcpy.env.workspace = r"G:\����ʡ��Ŀ\����������\�������\�������" 
feas = arcpy.ListFeatureClasses()
print str(feas)
for feasc in feas:
    #arcpy.DeleteField_management(feasc,"shpname")
    #arcpy.MakeFeatureLayer_management(feasc, "lyr") 
    arcpy.AddField_management(feasc,"shpname","TEXT")
    feadec = arcpy.Describe(feasc)
    feasc_name = feadec.baseName
    print feasc_name
    iCursor = arcpy.UpdateCursor(feasc)
    
    for iRow in iCursor:
        iRow.setValue("shpname",'%s'%feasc_name)
        iCursor.updateRow(iRow)
    del iCursor,iRow
print "ok"