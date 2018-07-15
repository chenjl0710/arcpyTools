# -*- coding: cp936 -*-
'''
��������򻮶��ķ�Χ�������񻮷ֳ����ɿ�����
'''


import arcpy
import os
arcpy.env.overwriteOutput = True 
#��������
#1
gdbshpname = r"F:\XinFeng_Result20151016.gdb\XinFeng_Result20151016"         #�ָ���
#2
areaTaskshp = r"F:\�ŷ������.shp"     #�����

#�����ļ���·��
Output_GDB = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"
#3
save_floder = r"F:\XinFeng_result"

#��ֵallTaskshp��Ĭ�����ݿ�
allTaskshp = os.path.join(Output_GDB,os.path.basename(os.path.splitext(gdbshpname)[0]) + "_Copy")
arcpy.CopyFeatures_management(gdbshpname,allTaskshp)
print str(allTaskshp)

arcpy.MakeFeatureLayer_management(allTaskshp, "lyr0")
arcpy.MakeFeatureLayer_management(areaTaskshp, "lyr")
icursor = arcpy.SearchCursor(areaTaskshp)
for row in icursor:
    igetvalue = row.getValue("FID")
    #FZRname = row.getValue("������")
    print igetvalue
    arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION",'"FID" = %s'%igetvalue)
    arcpy.SelectLayerByLocation_management("lyr0","INTERSECT","lyr","","NEW_SELECTION")
    #���������ļ�������
    #save_name = os.path.basename(os.path.splitext(gdbshpname)[0]) + "_" + '%s'%igetvalue
    #save_name = "������_" + '%s'%igetvalue
    save_name = os.path.basename(gdbshpname)[0:-4] + '%s'%igetvalue
    outsave = os.path.join(save_floder,save_name)
    arcpy.CopyFeatures_management("lyr0",outsave)
    arcpy.DeleteFeatures_management("lyr0")
    arcpy.SelectLayerByAttribute_management("lyr","CLEAR_SELECTION")
    
    #�ж�featureclass�ǲ��ǿյ�
    Cursorshp = outsave + ".shp"
    lyrCursor = arcpy.SearchCursor(Cursorshp)
    row = lyrCursor.next()
    if row:
        print "����"
    else:
        arcpy.Delete_management(Cursorshp)
arcpy.Delete_management(allTaskshp)
print "ok"



