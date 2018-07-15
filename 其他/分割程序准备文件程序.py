# -*- coding: cp936 -*-
import arcpy,os
arcpy.env.overwriteOutput = True
print "�����ͼ�������Ҫ��ImgName�ֶΣ����Ҹ��ֶ�����д����������Ӧ��Ӱ������ƣ�������Ӱ��ĺ�׺����������E114D4_N26D6_20131225_GF1_DOM_4_fus"

road_buffer = raw_input("�������·������ͼ�㣺")
rwk = raw_input("�����������ͼ�㣺")
Bollen = raw_input("�Ƿ���ˮ�������Ĥ Y/N��������Y����N��")

if Bollen == "Y" or Bollen == "y":
    water_shp = raw_input("������ˮ��ͼ�㣺")
    RoadMaskFolder = raw_input("�������·��ˮϵ��Ĥ�洢·����")
elif Bollen == "N" or Bollen == "n":
#     print "û��ˮ�������Ĥ����ʼ����......"
    RoadMaskFolder = raw_input("�������·��Ĥ�洢·����")
else :
    print "�������"
DefaultGDB = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"
print "��ʼ������Ĥͼ�㡤����������"
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
        
    
    
    
    
    