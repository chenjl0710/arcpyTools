# -*- coding: cp936 -*-
import arcpy
print "开始"
#样方lyr，必须要有CUNMD和CUNMC字段
yangfangshp = arcpy.GetParameterAsText(0)
yangfanglyr = arcpy.MakeFeatureLayer_management(yangfangshp,"yangfanglyr")
#村界lyr，必须要有CUNMC字段
cunjieshp = arcpy.GetParameterAsText(1)
cunjielyr = arcpy.MakeFeatureLayer_management(cunjieshp,"cunjielyr")
#村影像grouplyr，影像的 名称命名格式为：村名.tif，例如：和平村.tif
cunIMGgroup = arcpy.GetParameterAsText(2)

#新建字典，将样方shpCUNDM和CUNMC写入字典{村代码：村名称}
CUNDM = arcpy.GetParameterAsText(3)
CUNMC = arcpy.GetParameterAsText(4)
#输出图片文件夹
PicSave_Folder = arcpy.GetParameterAsText(5)
CUNDM_XZMC = {}
mxd = arcpy.mapping.MapDocument("CURRENT")
list_Layers = arcpy.mapping.ListLayers(mxd)

# arcpy.MakeFeatureLayer_management(cunIMGgroup,"cunIMGgrouplyrs")
cursor = arcpy.SearchCursor(yangfanglyr)
for row in cursor:
    #将村代码和村名称存入字典
    CUNDM_XZMC[row.getValue(CUNDM)] = row.getValue(CUNMC)
    
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    ##将所有影像设置为不可见
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
    
##将样方、村界、焦点村影像设置为可见，其他村影像不可见
#     iglyrs = arcpy.mapping.ListLayers(mxd)
#     for subLyr in iglyrs:
        if lyr.name == CUNDM_XZMC[PicName] + ".tif":
            lyr.visible = True
        else:
            lyr.visible = False
        if lyr.name[-4:] != ".tif":
            lyr.visible = True
        
    PicPath = PicSave_Folder + "\\" + str(PicName) + ".jpg"
    arcpy.mapping.ExportToJPEG(mxd, PicPath,"",2481,3509,300)   #300dpi  选择A4 Portrait.mxd模板
    arcpy.Delete_management(yangfanglyr)
    arcpy.Delete_management(cunjielyr)
del mxd
print "结束"
