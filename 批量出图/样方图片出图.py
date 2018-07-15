# -*- coding: cp936 -*-
import arcpy
print "开始"
mxdPath = r"D:\江苏农业普查\泗洪 - 副本\作图\耕作区泗洪.mxd"
PicSave_Folder = r"D:\江苏农业普查\泗洪 - 副本\作图\样方图片\\"
FileGetValue = "YFBHWY"
mxd = arcpy.mapping.MapDocument(mxdPath)
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    print mxd.dataDrivenPages.pageRow.getValue(FileGetValue)
    PicName = mxd.dataDrivenPages.pageRow.getValue(FileGetValue)
    PicPath = PicSave_Folder + str(PicName) + ".jpg"
    arcpy.mapping.ExportToJPEG(mxd, PicPath,"",2481,3509,300)
del mxd
print "结束"