# -*- coding: cp936 -*-
import arcpy
print "��ʼ"
#����lyr������Ҫ��CUNMD��CUNMC�ֶ�
yangfangshp = arcpy.GetParameterAsText(0)
yangfanglyr = arcpy.MakeFeatureLayer_management(yangfangshp,"yangfanglyr")
#���lyr������Ҫ��CUNMC�ֶ�
cunjieshp = arcpy.GetParameterAsText(1)
cunjielyr = arcpy.MakeFeatureLayer_management(cunjieshp,"cunjielyr")
#��Ӱ��grouplyr��Ӱ��� ����������ʽΪ������.tif�����磺��ƽ��.tif
cunIMGgroup = arcpy.GetParameterAsText(2)

#�½��ֵ䣬������shpCUNDM��CUNMCд���ֵ�{����룺������}
CUNDM = arcpy.GetParameterAsText(3)
CUNMC = arcpy.GetParameterAsText(4)
#���ͼƬ�ļ���
PicSave_Folder = arcpy.GetParameterAsText(5)
CUNDM_XZMC = {}
mxd = arcpy.mapping.MapDocument("CURRENT")
list_Layers = arcpy.mapping.ListLayers(mxd)

# arcpy.MakeFeatureLayer_management(cunIMGgroup,"cunIMGgrouplyrs")
cursor = arcpy.SearchCursor(yangfanglyr)
for row in cursor:
    #�������ʹ����ƴ����ֵ�
    CUNDM_XZMC[row.getValue(CUNDM)] = row.getValue(CUNMC)
    
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    ##������Ӱ������Ϊ���ɼ�
#     cunIMGgrouplyrs = arcpy.mapping.ListLayers("cunIMGgrouplyrs")
#     for subLyr in cunIMGgrouplyrs:
#         subLyr.visible = False
        
    PicName = mxd.dataDrivenPages.pageRow.getValue(CUNDM)
    for lyr in list_Layers:
#         Query = '"' + CUNDM + '" =' + "'" + PicName + "'"
        Query = '"CUNDM"  =' + "'" + PicName + "'"
        print Query
        yangfanglyr.definitionQuery = Query
        cunjielyr.definitionQuery = Query
        print  CUNDM_XZMC[PicName],PicName
    
##����������硢�����Ӱ������Ϊ�ɼ���������Ӱ�񲻿ɼ�
#     iglyrs = arcpy.mapping.ListLayers(mxd)
#     for subLyr in iglyrs:
        if lyr.name == CUNDM_XZMC[PicName] + ".tif":
            lyr.visible = True
        else:
            lyr.visible = False
        if lyr.name[-4:] != ".tif":
            lyr.visible = True
        
    PicPath = PicSave_Folder + "\\" + str(PicName) + ".jpg"
    arcpy.mapping.ExportToJPEG(mxd, PicPath,"",2481,3509,300)   #300dpi  ѡ��A4 Portrait.mxdģ��
    arcpy.Delete_management(yangfanglyr)
    arcpy.Delete_management(cunjielyr)
del mxd
print "����"
