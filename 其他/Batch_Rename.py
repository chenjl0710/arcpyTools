# -*- coding: cp936 -*-
#����arcpyģ��
'''

'''
import arcpy
arcpy.env.workspace = r"G:\�ζ��������óɹ�_���˼�������ܣ�1��16�ţ�\0����\�ζ�ϲ����\merge"
fcs = arcpy.ListFeatureClasses("*","All","")

for fc in fcs:
        print fc
        #length = len(str(fc))
        New_Name = str(fc[:-10])   #7
        print New_Name
        arcpy.Rename_management(fc,New_Name)
        print ""
print "finish"

