# -*- coding: cp936 -*-
import arcpy
print "��ʼ"
mxdPath = r"D:\����ũҵ�ղ�\���� - ����\��ͼ\����������.mxd"
PicSave_Folder = r"D:\����ũҵ�ղ�\���� - ����\��ͼ\����ͼƬ\\"
FileGetValue = "YFBHWY"
mxd = arcpy.mapping.MapDocument(mxdPath)
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    print mxd.dataDrivenPages.pageRow.getValue(FileGetValue)
    PicName = mxd.dataDrivenPages.pageRow.getValue(FileGetValue)
    PicPath = PicSave_Folder + str(PicName) + ".jpg"
    arcpy.mapping.ExportToJPEG(mxd, PicPath,"",2481,3509,300)
del mxd
print "����"