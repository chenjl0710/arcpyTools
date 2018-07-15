# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Batch_dissolve.py
#-------------------------------------------------------------

# Import arcpy module
import arcpy,os

arcpy.env.workspace = r"G:\治多土地利用成果_拓扑检查结果汇总（1月16号）\0擦除\外部"
outPut_dir = r"G:\治多土地利用成果_拓扑检查结果汇总（1月16号）\0擦除\外部\merge"
fcs = arcpy.ListFeatureClasses()
print "start"
i = 0
for fc in fcs:
        print str(fc)
        # Local variables:
        Input_Features = fc
        i = i + 1
        Dissolve_Fields = ["ClassName","ClassID"]
        Output_Feature_Class = os.path.join(outPut_dir,str(fc[:-4]))

        # Process: Dissolve
        arcpy.Dissolve_management(Input_Features, Output_Feature_Class, Dissolve_Fields, "", "SINGLE_PART", "DISSOLVE_LINES")

        print i
print "finish"
