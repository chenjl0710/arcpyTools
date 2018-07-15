# -*- coding: cp936 -*-

import arcpy,os
 
# Set environment settings
arcpy.env.workspace = r"D:\0_PROJECTS\3_QingHai_MaDuo_Project\MaDuoNewBorderTask0107\Result\ToPo"
outFeaturePath = r"D:\0_PROJECTS\3_QingHai_MaDuo_Project\MaDuoNewBorderTask0107\Result\Eli"
temp = r"D:\0_PROJECTS\3_QingHai_MaDuo_Project\MaDuoNewBorderTask0107\Result\temp"
fcs = arcpy.ListFeatureClasses("*","All","")
print "start"
for fc in fcs:
    print fc
    # Set local variables
    inFeatures = fc
    tempLayer = os.path.join(temp,str(fc[:-4]) + "blocklayer")
    expression = '"SampleName" = \'1\''   #设置筛选条件,注意转义字符 用   \    转义

    #exclusionExpression = ''
     
    # Execute MakeFeatureLayer
    arcpy.MakeFeatureLayer_management(inFeatures, tempLayer)

    print "Step 1 finished!"
     
    # Execute SelectLayerByAttribute to define features to be eliminated
    arcpy.SelectLayerByAttribute_management(tempLayer, "NEW_SELECTION", expression)

    print "Step 2 finished!"
     
    # Execute Eliminate
    outFC_name = str(fc[:-4])
    outFeatureClass = os.path.join(outFeaturePath,outFC_name)
    arcpy.Eliminate_management(tempLayer, outFeatureClass, "AREA",)

    print ""
    
print "All finished"
