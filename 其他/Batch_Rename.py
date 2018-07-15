# -*- coding: cp936 -*-
#导入arcpy模块
'''

'''
import arcpy
arcpy.env.workspace = r"G:\治多土地利用成果_拓扑检查结果汇总（1月16号）\0擦除\治多合并结果\merge"
fcs = arcpy.ListFeatureClasses("*","All","")

for fc in fcs:
        print fc
        #length = len(str(fc))
        New_Name = str(fc[:-10])   #7
        print New_Name
        arcpy.Rename_management(fc,New_Name)
        print ""
print "finish"

