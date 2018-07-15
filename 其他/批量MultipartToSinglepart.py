# -*- coding: cp936 -*-

import arcpy,os

arcpy.env.workspace = r"G:\ToHQT\clip_result" 
feas = arcpy.ListFeatureClasses()
print str(feas)
savefolder = r"G:\ToHQT\clip_result_single"
for fc in feas:
    saveshp =  os.path.basename(os.path.splitext(fc)[0]) + ".shp"
    outsave = os.path.join(savefolder,saveshp)
    arcpy.MultipartToSinglepart_management (fc, outsave)
    print "ok"
print "完成"