# -*- coding: cp936 -*-
#�Ƚ�����shp���ҳ�����Ĳ��֣�ɾ��shp���¼����Ϊ0��shp
# Import arcpy module
import arcpy,os

arcpy.env.workspace = r"D:\kekexili_LandUse_FinalResult"
merge_dir = r"C:\merge"
out_dir = r"D:\erase"
fcs = arcpy.ListFeatureClasses("*","All","")
print fcs
print "start"

for fc in fcs:
        print "��������" + str(fc)
        merge_name = str(fc[:-4]) + "_merge.shp"

        fc_merge = os.path.join(merge_dir,merge_name)      
        out_feature_class = os.path.join(out_dir,str(fc[:-4])+"_Erase")
        print u"��������..."
        arcpy.Erase_analysis(fc, fc_merge, out_feature_class)
        in_Fea = out_feature_class + ".shp"
        sumCount = int(arcpy.GetCount_management(in_Fea).getOutput(0))
        print sumCount
        if sumCount == 0:
                arcpy.Delete_management(in_Fea)
        
        print ""
        print ""

print "finish"
