# -*- coding: cp936 -*-
import arcpy,os
arcpy.env.overwriteOutput = True
print "任务框图层里必须要有ImgName字段，并且该字段里填写的是任务框对应的影像的名称（不包括影像的后缀名），例如E114D4_N26D6_20131225_GF1_DOM_4_fus"

road_buffer = raw_input("请输入道路缓冲区图层：")
rwk = raw_input("请输入任务框图层：")
Bollen = raw_input("是否有水体参与掩膜 Y/N？请输入Y或者N：")

if Bollen == "Y" or Bollen == "y":
    water_shp = raw_input("请输入水体图层：")
    RoadMaskFolder = raw_input("请输入道路、水系掩膜存储路径：")
elif Bollen == "N" or Bollen == "n":
#     print "没有水体参与掩膜，开始计算......"
    RoadMaskFolder = raw_input("请输入道路掩膜存储路径：")
else :
    print "输入错误"
DefaultGDB = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"
print "开始计算掩膜图层······"
arcpy.MakeFeatureLayer_management(rwk,"rwklyr")
icursor = arcpy.SearchCursor(rwk)
for irow in icursor:
    mergeInput = []
    
    ImgNameValue = irow.getValue("imgName")
    expression = '"ImgName" = ' + "'" + ImgNameValue + "'"
    arcpy.SelectLayerByAttribute_management("rwklyr","NEW_SELECTION",expression)
    
    CopyFea = os.path.join(DefaultGDB,ImgNameValue + "_RWK")
    arcpy.CopyFeatures_management("rwklyr",CopyFea)
    if Bollen == "N" or Bollen == "n" :
        clip_ouput = os.path.join(DefaultGDB,ImgNameValue + "_Road")
        arcpy.Clip_analysis(road_buffer,CopyFea,clip_ouput)
#         
#         mergeInput[0] = clip_ouput
#         mergeInput[1] = CopyFea
        mergeInput.append(CopyFea)    
        mergeInput.append(clip_ouput)
#         mergeInput.append(CopyFea)        
        
        print "mergeInput:",mergeInput
        merge_output = os.path.join(RoadMaskFolder,ImgNameValue + ".shp")
        arcpy.Merge_management(mergeInput,merge_output)
    else:
        clip_ouput = os.path.join(DefaultGDB,ImgNameValue + "_Road")
        arcpy.Clip_analysis(road_buffer,CopyFea,clip_ouput)
        
        clip_ouput_water = os.path.join(DefaultGDB,ImgNameValue + "_Water")
        arcpy.Clip_analysis(water_shp,CopyFea,clip_ouput_water)        
        
#         mergeInput[0] = clip_ouput
#         mergeInput[1] = clip_ouput_water
#         mergeInput[2] = CopyFea
        mergeInput.append(CopyFea)
        mergeInput.append(clip_ouput)
        mergeInput.append(clip_ouput_water)
        
        
        print "mergeInput:",mergeInput
        merge_output = os.path.join(RoadMaskFolder,ImgNameValue + ".shp")
        arcpy.Merge_management(mergeInput,merge_output)
        
    
    
    
    
    