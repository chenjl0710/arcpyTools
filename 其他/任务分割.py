# -*- coding: cp936 -*-
'''
按照任务框划定的范围将总任务划分成若干块任务。
'''


import arcpy
import os
arcpy.env.overwriteOutput = True 
#输入数据
#1
gdbshpname = r"F:\XinFeng_Result20151016.gdb\XinFeng_Result20151016"         #分割结果
#2
areaTaskshp = r"F:\信丰任务框.shp"     #任务框

#保存文件夹路径
Output_GDB = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"
#3
save_floder = r"F:\XinFeng_result"

#赋值allTaskshp到默认数据库
allTaskshp = os.path.join(Output_GDB,os.path.basename(os.path.splitext(gdbshpname)[0]) + "_Copy")
arcpy.CopyFeatures_management(gdbshpname,allTaskshp)
print str(allTaskshp)

arcpy.MakeFeatureLayer_management(allTaskshp, "lyr0")
arcpy.MakeFeatureLayer_management(areaTaskshp, "lyr")
icursor = arcpy.SearchCursor(areaTaskshp)
for row in icursor:
    igetvalue = row.getValue("FID")
    #FZRname = row.getValue("负责人")
    print igetvalue
    arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION",'"FID" = %s'%igetvalue)
    arcpy.SelectLayerByLocation_management("lyr0","INTERSECT","lyr","","NEW_SELECTION")
    #保存结果的文件名命名
    #save_name = os.path.basename(os.path.splitext(gdbshpname)[0]) + "_" + '%s'%igetvalue
    #save_name = "临朐县_" + '%s'%igetvalue
    save_name = os.path.basename(gdbshpname)[0:-4] + '%s'%igetvalue
    outsave = os.path.join(save_floder,save_name)
    arcpy.CopyFeatures_management("lyr0",outsave)
    arcpy.DeleteFeatures_management("lyr0")
    arcpy.SelectLayerByAttribute_management("lyr","CLEAR_SELECTION")
    
    #判断featureclass是不是空的
    Cursorshp = outsave + ".shp"
    lyrCursor = arcpy.SearchCursor(Cursorshp)
    row = lyrCursor.next()
    if row:
        print "保留"
    else:
        arcpy.Delete_management(Cursorshp)
arcpy.Delete_management(allTaskshp)
print "ok"



