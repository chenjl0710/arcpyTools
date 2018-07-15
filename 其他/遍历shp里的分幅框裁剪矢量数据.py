# -*- coding: cp936 -*-
import arcpy
import os
input_shp = r"F:\PLA_Analysis2016\TestData\RoadLineLevel0\������·����\NavigationRoad.shp"
clip_fea = r"F:\PLA_Analysis2016\TestData\RoadLineLevel0\Ӱ����Ƕ��\360826_Taihexian_MosaicBoundary.shp"
#�����ļ���·��
save_floder = r"F:\PLA_Analysis2016\TestData\RoadLineLevel0\www"
arcpy.MakeFeatureLayer_management(clip_fea, "lyr") 
icursor = arcpy.SearchCursor(clip_fea)
for row in icursor:
    igetvalue = row.getValue("TaskID")
#     igetvalue2 = row.getValue("name")
    print igetvalue 
    sql = '"TaskID" =' + "'" + igetvalue + "'"   #'"TaskID" = %s'%igetvalue
    arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION",sql)
    #���������ļ�������
    #save_name = os.path.basename(os.path.splitext(input_shp)[0]) + "_" + '%s'%igetvalue2
    save_name = "360826_Taihexian_NavigationRoad" + "_part" +  str(igetvalue) + "_8.shp" #'%s'%igetvalue2 + ".shp"
    print save_name
    #outsave = os.path.join(save_floder,save_name)
    outsave = save_floder + "\\" + save_name
    arcpy.Clip_analysis(input_shp,"lyr",outsave)
    arcpy.SelectLayerByAttribute_management("lyr","CLEAR_SELECTION")
print "over"