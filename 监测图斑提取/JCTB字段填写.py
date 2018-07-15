# -*- coding: cp936 -*-
'''
OBJECTID
BSM
JCBH
XZQBM
XZQMC
QXS
HSX
XZB
YZB
JCMJ
TBLX
'''
import arcpy,os



def GetXZQ(JCTBshp,XZQBM,XZQMC):
    cursor = arcpy.UpdateCursor(JCTBshp)
    for row in cursor:
        row.setValue("XZQBM",XZQBM)
        row.setValue("XZQMC",XZQMC)
        cursor.updateRow(row)
    del cursor, row

def GetQSX(QSXshp,JCTBshp):
    #获取前时相的值
    arcpy.MakeFeatureLayer_management(QSXshp, "QSX_lyr")
    arcpy.MakeFeatureLayer_management(JCTBshp, "QJCTB_lyr")
    icursor = arcpy.SearchCursor(QSXshp)
    for row in icursor:
        igetFID = row.getValue("FID")
#         print igetFID
        igetQSX = row.getValue("SX")
#         print igetQSX
        arcpy.SelectLayerByAttribute_management("QSX_lyr","NEW_SELECTION",'"FID" = %s'%igetFID)
        arcpy.SelectLayerByLocation_management("QJCTB_lyr","HAVE_THEIR_CENTER_IN","QSX_lyr","","NEW_SELECTION")##
        icursor_QSX = arcpy.UpdateCursor("QJCTB_lyr")
        for row_QSX in icursor_QSX:
            row_QSX.setValue("QSX",igetQSX)
            icursor_QSX.updateRow(row_QSX)
        #del icursor_QSX,row_QSX
        arcpy.SelectLayerByAttribute_management("QJCTB_lyr","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("QSX_lyr","CLEAR_SELECTION")
    arcpy.Delete_management("QSX_lyr")
    arcpy.Delete_management("QJCTB_lyr")
    
def GetHSX(HSXshp,JCTBshp):  
    #获取后时相的值
    arcpy.MakeFeatureLayer_management(HSXshp, "HSX_lyr")
    arcpy.MakeFeatureLayer_management(JCTBshp, "HJCTB_lyr")
    icursor = arcpy.SearchCursor(HSXshp)
    for row in icursor:
        igetFID = row.getValue("FID")
#         print igetFID
        igetHSX = row.getValue("SX")
#         print igetHSX
        arcpy.SelectLayerByAttribute_management("HSX_lyr","NEW_SELECTION",'"FID" = %s'%igetFID)
        arcpy.SelectLayerByLocation_management("HJCTB_lyr","HAVE_THEIR_CENTER_IN","HSX_lyr","","NEW_SELECTION")
        icursor_HSX = arcpy.UpdateCursor("HJCTB_lyr")
        for row_HSX in icursor_HSX:
            row_HSX.setValue("HSX",igetHSX)
            icursor_HSX.updateRow(row_HSX)
        #del icursor_QSX,row_QSX
        arcpy.SelectLayerByAttribute_management("HJCTB_lyr","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("HSX_lyr","CLEAR_SELECTION")
    arcpy.Delete_management("HSX_lyr")
    arcpy.Delete_management("HJCTB_lyr")
    
def GetX_YZB(JCTBshp):
    #获取XY的质心坐标的值
    arcpy.CalculateField_management(JCTBshp,"XZB","!SHAPE.CENTROID.X!","PYTHON_9.3")
    arcpy.CalculateField_management(JCTBshp,"YZB","!SHAPE.CENTROID.Y!","PYTHON_9.3")

def addNewField(JCTBshp):
    arcpy.AddField_management(JCTBshp,"OBJECTID","Double","10","","")
    arcpy.AddField_management(JCTBshp,"BSM","Double","18","10","")
    arcpy.AddField_management(JCTBshp,"JCBH","Double","10","","")
    arcpy.AddField_management(JCTBshp,"XZQBM","TEXT","","","10")
    arcpy.AddField_management(JCTBshp,"XZQMC","TEXT","","","20")
    arcpy.AddField_management(JCTBshp,"QSX","TEXT","","","20")
    arcpy.AddField_management(JCTBshp,"HSX","TEXT","","","20")
    arcpy.AddField_management(JCTBshp,"XZB","Double","18","5","")
    arcpy.AddField_management(JCTBshp,"YZB","Double","18","5","")
    arcpy.AddField_management(JCTBshp,"JCMJ","Double","15","4","")

def deleteFields(JCTBshp):
    fields = arcpy.ListFields(JCTBshp)
    for field in fields:
#         print field.name
        if (field.name != "TBLX" and field.name != "FID" and field.name != "Shape"):
            arcpy.DeleteField_management(JCTBshp,field.name)
        
        
def GetJCMJ(JCTBshp):
    arcpy.CalculateField_management(JCTBshp,"JCMJ", '!SHAPE.AREA!',"PYTHON_9.3")  #@Square Meters
    cur = arcpy.UpdateCursor(JCTBshp)
    for row in cur:
        NewJCMJ = float(row.getValue("JCMJ"))/666.7
        row.setValue("JCMJ",NewJCMJ)
        cur.updateRow(row)
    del cur,row       

def SortField(JCTBshp):
    arcpy.AddField_management(JCTBshp,"tblx_T","TEXT","","","10")
    arcpy.CalculateField_management(JCTBshp,"tblx_T","!TBLX!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"TBLX")
    arcpy.AddField_management(JCTBshp,"TBLX","TEXT","","","10")
    arcpy.CalculateField_management(JCTBshp,"TBLX","!tblx_T!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"tblx_T")

def LanduseShpDeal(LanduseShp):
    arcpy.CalculateField_management(LanduseShp,"DLBM","!F15DLBM!","PYTHON_9.3")
    arcpy.CalculateField_management(LanduseShp,"DLMC","!F15DLMC!","PYTHON_9.3")  
    arcpy.DeleteField_management(LanduseShp,"F15DLBM")
    arcpy.DeleteField_management(LanduseShp,"F15DLMC")
    arcpy.DeleteField_management(LanduseShp,"F14DLBM")
    arcpy.DeleteField_management(LanduseShp,"TBLX")
    arcpy.DeleteField_management(LanduseShp,"TZ")
    arcpy.DeleteField_management(LanduseShp,"SHAPE_Leng")
    arcpy.DeleteField_management(LanduseShp,"SHAPE_Area")

def ChangeBHCD(LanduseShp):
    dic = {"1":"疑似变化","2":"确定变化"}
    iCursor = arcpy.UpdateCursor(LanduseShp)
    for iRow in iCursor:
        iValue = iRow.getValue("BHCD")
        if iValue in dic:
            iRow.setValue("BHCD",dic[iValue])
#         else :
#             iRow.setValue("BHCD","")
#             print iRow.getValue("FID")
        iCursor.updateRow(iRow)
    del iCursor,iRow

#根据图斑外接矩形左上角的坐标位置计算JCBH
def JCBH(JCTBshp):
    XY_list = []
#     try:
#         arcpy.AddField_management(fc,"JCBH","LONG")
#         print "Add field successfully"
#     except IOError,e:
#         print "already have the field"
#     print JCTBshp
    cur  = arcpy.da.SearchCursor(JCTBshp,["SHAPE@"])
    for row in cur:
        ext = row[0].extent
#         print "X_min",ext.XMin,"Y_Max",ext.YMax#读出外界矩形的最大y坐标和最小x坐标
        XY_list.append([round(ext.XMin,1),round(ext.YMax,1)])#精度下降到1位小数
    del cur,row
#          排序数组
    for i in range(len(XY_list)):
        for j in range(len(XY_list)):
            if (XY_list[i][1] > XY_list[j][1]) or (XY_list[i][1] == XY_list[j][1] and XY_list[i][0] < XY_list[j][0]):
                a = XY_list[i]
                XY_list[i] = XY_list[j]
                XY_list[j] = a
#     print "list is in order"
#   shp文件赋值
    for i in range(len(XY_list)):
        cur = arcpy.da.UpdateCursor(JCTBshp,["SHAPE@","JCBH"])
        for row in cur:
            X = row[0].extent.XMin
            Y = row[0].extent.YMax
            if(XY_list[i][0] == round(X,1) and XY_list[i][1] == round(Y,1)):
                row[1] = i + 1
                cur.updateRow(row)


#根据图斑质心位置计算JCBH   暂时不用
def JCBH_Zhixin(JCTBshp):
    XY_list = []
    try:
        arcpy.AddField_management(JCTBshp,"BH","LONG")
        print "Add field successfully"
    except IOError,e:
        print "already have the field"
    print JCTBshp
    cur  = arcpy.da.SearchCursor(JCTBshp)
    for row in cur:
        ext = row[0].centroid
        print "X",ext.X,"Y",ext.Y#读出集合要素的质心坐标的X，Y坐标
        XY_list.append([round(ext.XMin,1),round(ext.YMax,1)])#精度下降到1位小数
    del cur,row
        #排序数组
    for i in range(len(XY_list)):
        for j in range(len(XY_list)):
            if (XY_list[i][1] > XY_list[j][1]) or (XY_list[i][1] == XY_list[j][1] and XY_list[i][0] < XY_list[j][0]):
                a = XY_list[i]
                XY_list[i] = XY_list[j]
                XY_list[j] = a
    print "list is in order"
        #shp文件赋值
    for i in range(len(XY_list)):
        cur = arcpy.da.UpdateCursor(JCTBshp,["SHAPE@","BH"])
        for row in cur:
            X = row[0].extent.XMin
            Y = row[0].extent.YMax
            if(XY_list[i][0] == round(X,1) and XY_list[i][1] == round(Y,1)):
                row[1] = i + 1
                cur.updateRow(row)





if __name__ == "__main__":
    print "=================Start=================="
    FolderPath = r"C:\Users\Administrator\Desktop\test"
    Folders = os.listdir(FolderPath)
    for Folder in Folders:
        print "Folder是：",Folder
        XZQBM = Folder[0:6]
        print "XZQBM是：",XZQBM
        XZQMC = Folder[6:]
        print "XZQMC是：",XZQMC
        shpFolder = os.path.join(FolderPath,Folder)
#         print "shpFolder是：",shpFolder 
        QSXshpName = XZQBM + "2014xq.shp"
        HSXshpName = XZQBM + "2015xq.shp"
        JCTBshpName = XZQBM + "jctb.shp"
#         LanduseShpName = XZQBM + "2015landuse.shp"      #Landuse
        QSXshp = os.path.join(shpFolder,QSXshpName)
        HSXshp = os.path.join(shpFolder,HSXshpName)
        JCTBshp =os.path.join(shpFolder,JCTBshpName)
#         LanduseShp =os.path.join(shpFolder,LanduseShpName)      #Landuse
        #调用函数
        print "调用deleteFields函数"
        deleteFields(JCTBshp)
        print "调用addNewField函数"
        addNewField(JCTBshp)
        print "调用GetQSX函数"
        GetQSX(QSXshp,JCTBshp)
        print "调用GetHSX函数"
        GetHSX(HSXshp,JCTBshp)
        print "调用GetX_YZB函数"
        GetX_YZB(JCTBshp)
        print "调用GetJCMJ函数"
        GetJCMJ(JCTBshp)
        print "调用GetXZQ函数"
        GetXZQ(JCTBshp,XZQBM,XZQMC)
        print "调用SortField函数"
        SortField(JCTBshp)
        print "调用JCBH函数"
        JCBH(JCTBshp)
        
#         print "调用LanduseShpDeal函数"
#         LanduseShpDeal(LanduseShp)
#         print "调用ChangeBHCD函数"
#         ChangeBHCD(LanduseShp)
  
        print "---------------------------\n"
    print "=================Finish=================="