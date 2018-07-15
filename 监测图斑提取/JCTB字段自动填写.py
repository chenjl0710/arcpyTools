# -*- coding: cp936 -*-
'''
���jctb����ֶ��Զ�����
����ͼ�ߵ�����XZB��YZB����
����ͼ��������ǰʱ��ͺ�ʱ���ֵ
����ͼ�ߵ�˳���ţ����˳���մ������£������ҵ�˳��
'''
import arcpy,os


def CalcuZGDMJ(JCTBshp,GDTB,saveFolder):
    Input_Features = []
    Input_Features.append(JCTBshp)
    Input_Features.append(GDTB)
#     print Input_Features
    Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_GDTB" + "_intersect.shp")
#     print Output_Feature_Class
    arcpy.Intersect_analysis(Input_Features, Output_Feature_Class, "ALL", "", "INPUT")
    
    # Process: Add Field
    #arcpy.AddField_management(Output_Feature_Class, "ZJBNTMJ", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    # Process: Calculate Field
    arcpy.CalculateField_management(Output_Feature_Class, "ZGDMJ", "!SHAPE.AREA!", "PYTHON_9.3", "")
    
    # Process: Dissolve
    Dissolve_Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_GDTB" + "_intersect_Dissolve.shp")
    print "dissolving..."
    arcpy.Dissolve_management(Output_Feature_Class,Dissolve_Output_Feature_Class, "BSM", "ZGDMJ SUM", "MULTI_PART", "DISSOLVE_LINES")
    
    print "JoinFielding..."
    arcpy.JoinField_management(JCTBshp, "BSM",Dissolve_Output_Feature_Class, "BSM", "BSM;SUM_ZGDMJ")
    
    print "CalculateFielding..."
    arcpy.CalculateField_management(JCTBshp, "ZGDMJ", "!SUM_ZGDMJ!","PYTHON_9.3", "")
    arcpy.CalculateField_management(JCTBshp, "ZGDMJ", '!SUM_ZGDMJ!/666.7',"PYTHON_9.3", "")
    
    arcpy.DeleteField_management(JCTBshp,"BSM_1")
    arcpy.DeleteField_management(JCTBshp,"SUM_ZGDMJ")
    
def CalcuZJBNTMJ(JCTBshp,JBNTTB,saveFolder):
    Input_Features = []
    Input_Features.append(JCTBshp)
    Input_Features.append(JBNTTB)
#     print Input_Features
    Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_JBNTTB" + "_intersect.shp")
#     print Output_Feature_Class
    arcpy.Intersect_analysis(Input_Features, Output_Feature_Class, "ALL", "", "INPUT")
    
    # Process: Add Field
    #arcpy.AddField_management(Output_Feature_Class, "ZJBNTMJ", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    # Process: Calculate Field
    arcpy.CalculateField_management(Output_Feature_Class, "ZJBNTMJ", "!SHAPE.AREA!", "PYTHON_9.3", "")
    
    # Process: Dissolve
    Dissolve_Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_JBNTTB" + "_intersect_Dissolve.shp")
    print "dissolving..."
    arcpy.Dissolve_management(Output_Feature_Class,Dissolve_Output_Feature_Class, "BSM", "ZJBNTMJ SUM", "MULTI_PART", "DISSOLVE_LINES")
    
    print "JoinFielding..."
    arcpy.JoinField_management(JCTBshp, "BSM",Dissolve_Output_Feature_Class, "BSM", "BSM;SUM_ZJBNTM")
    
    print "CalculateFielding..."
    arcpy.CalculateField_management(JCTBshp, "ZJBNTMJ", "!SUM_ZJBNTM!","PYTHON_9.3", "")
    arcpy.CalculateField_management(JCTBshp, "ZJBNTMJ", '!SUM_ZJBNTM!/666.7',"PYTHON_9.3", "")
    
    arcpy.DeleteField_management(JCTBshp,"BSM_1")
    arcpy.DeleteField_management(JCTBshp,"SUM_ZJBNTM")

def GetOBJECTID_BSM(JCTBshp):
    arcpy.CalculateField_management(JCTBshp,"OBJECTID","!FID!+1","PYTHON_9.3")
    arcpy.CalculateField_management(JCTBshp,"BSM","!FID!+1","PYTHON_9.3")

def GetXZQ(JCTBshp,XZQBM,XZQMC):
    cursor = arcpy.UpdateCursor(JCTBshp)
    for row in cursor:
        row.setValue("XZQBM",XZQBM)
        row.setValue("XZQMC",XZQMC)
        cursor.updateRow(row)
    del cursor, row

def GetQSX(QSXshp,JCTBshp):
    #��ȡǰʱ���ֵ
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
    #��ȡ��ʱ���ֵ
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
    #��ȡXY�����������ֵ
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
    arcpy.CalculateField_management(JCTBshp,"JCMJ", '!SHAPE.AREA!',"PYTHON_9.3")
    cur = arcpy.UpdateCursor(JCTBshp)
    for row in cur:
        NewJCMJ = float(row.getValue("JCMJ"))/666.7
        row.setValue("JCMJ",NewJCMJ)
        cur.updateRow(row)
    del cur,row       

def SortField(JCTBshp):
    #������TBLX���ֶ�˳��
    arcpy.AddField_management(JCTBshp,"tblx_T","TEXT","","","10")
    arcpy.CalculateField_management(JCTBshp,"tblx_T","!TBLX!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"TBLX")
    arcpy.AddField_management(JCTBshp,"TBLX","TEXT","","","10")
    arcpy.CalculateField_management(JCTBshp,"TBLX","!tblx_T!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"tblx_T")
    
    #������BHCD���ֶ�˳��
    arcpy.AddField_management(JCTBshp,"BHCD_T","TEXT","","","20")
    arcpy.CalculateField_management(JCTBshp,"BHCD_T","!BHCD!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"BHCD")
    arcpy.AddField_management(JCTBshp,"BHCD","TEXT","","","20")
    arcpy.CalculateField_management(JCTBshp,"BHCD","!BHCD_T!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"BHCD_T")
    
    #������BZ���ֶ�˳��
    arcpy.AddField_management(JCTBshp,"BZ_T","TEXT","","","100")
    arcpy.CalculateField_management(JCTBshp,"BZ_T","!BZ!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"BZ")
    arcpy.AddField_management(JCTBshp,"BZ","TEXT","","","100")
    arcpy.CalculateField_management(JCTBshp,"BZ","!BZ_T!","PYTHON_9.3")  
    arcpy.DeleteField_management(JCTBshp,"BZ_T")   
    
    #���ռ���������ռ����ũ�����
    arcpy.AddField_management(JCTBshp,"ZGDMJ","Double","15","4","")
    arcpy.AddField_management(JCTBshp,"ZJBNTMJ","Double","15","4","")
    
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
    dic = {"1":"���Ʊ仯","2":"ȷ���仯"}
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

#����ͼ����Ӿ������Ͻǵ�����λ�ü���JCBH

def JCBH(JCTBshp):
    XY_list = []
#     try:
#         arcpy.AddField_management(fc,"JCBH","LONG")
#         print "Add field successfully"
#     except IOError,e:
#         print "already have the field"
#     print JCTBshp
    cur  = arcpy.da.SearchCursor(JCTBshp,["SHAPE@"])  # @UndefinedVariable
    for row in cur:
        ext = row[0].extent
#         print "X_min",ext.XMin,"Y_Max",ext.YMax#���������ε����y�������Сx����
        XY_list.append([round(ext.XMin,1),round(ext.YMax,1)])#�����½���1λС��
    del cur,row
#          ��������
    for i in range(len(XY_list)):
        for j in range(len(XY_list)):
            if (XY_list[i][1] > XY_list[j][1]) or (XY_list[i][1] == XY_list[j][1] and XY_list[i][0] < XY_list[j][0]):
                a = XY_list[i]
                XY_list[i] = XY_list[j]
                XY_list[j] = a
#     print "list is in order"
#   shp�ļ���ֵ
    for i in range(len(XY_list)):
        cur = arcpy.da.UpdateCursor(JCTBshp,["SHAPE@","JCBH"])
        for row in cur:
            X = row[0].extent.XMin
            Y = row[0].extent.YMax
            if(XY_list[i][0] == round(X,1) and XY_list[i][1] == round(Y,1)):
                row[1] = i + 1
                cur.updateRow(row)

#����ͼ������λ�ü���JCBH   ��ʱ����
def JCBH_Zhixin(JCTBshp):
    XY_list = []
#     try:
#         arcpy.AddField_management(JCTBshp,"BH","LONG")
#         print "Add field successfully"
#     except IOError,e:
#         print "already have the field"
#     print JCTBshp
    cur  = arcpy.da.SearchCursor(JCTBshp)  # @UndefinedVariable
    for row in cur:
        ext = row[0].centroid
        print "X",ext.X,"Y",ext.Y#��������Ҫ�ص����������X��Y����
        XY_list.append([round(ext.XMin,1),round(ext.YMax,1)])#�����½���1λС��
    del cur,row
        #��������
    for i in range(len(XY_list)):
        for j in range(len(XY_list)):
            if (XY_list[i][1] > XY_list[j][1]) or (XY_list[i][1] == XY_list[j][1] and XY_list[i][0] < XY_list[j][0]):
                a = XY_list[i]
                XY_list[i] = XY_list[j]
                XY_list[j] = a
    print "list is in order"
        #shp�ļ���ֵ
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
    FolderPath = r"C:\Users\Administrator\Desktop\�½��ļ���"
    JBNTTB= r"C:\Users\Administrator\Desktop\test2\GD_JBNT\JBNTBHTB.SHP"
    GDTB = r"C:\Users\Administrator\Desktop\test2\GD_JBNT\Ϋ��2013����.shp"
    Folders = os.listdir(FolderPath)
    for Folder in Folders:
        print "Folder�ǣ�",Folder
        XZQBM = Folder[0:6]
        print "XZQBM�ǣ�",XZQBM
        XZQMC = Folder[6:]
        print "XZQMC�ǣ�",XZQMC
        shpFolder = os.path.join(FolderPath,Folder)
        QSXshpName = XZQBM + "2014xq.shp"
        HSXshpName = XZQBM + "2015xq.shp"
        JCTBshpName = Folder + "jctb.shp"
        QSXshp = os.path.join(shpFolder,QSXshpName)
        HSXshp = os.path.join(shpFolder,HSXshpName)
        JCTBshp =os.path.join(shpFolder,JCTBshpName)
        #���ú���
#         print "����deleteFields����"
#         deleteFields(JCTBshp)
#         print "����addNewField����"
#         addNewField(JCTBshp)
        arcpy.CalculateField_management(JCTBshp, "ZJBNTMJ", "0", "PYTHON_9.3", "")
        arcpy.CalculateField_management(JCTBshp, "ZGDMJ", "0", "PYTHON_9.3", "")        
    
        print "����GetQSX����"
#         GetQSX(QSXshp,JCTBshp)
        
        print "����GetHSX����"
#         GetHSX(HSXshp,JCTBshp)
#         arcpy.CalculateField_management(JCTBshp, "HSX", "20150823", "PYTHON_9.3", "")
        
        
        
        print "����GetX_YZB����"
#         GetX_YZB(JCTBshp)
        
        print "����GetJCMJ����"
#         GetJCMJ(JCTBshp)
        
        print "����GetXZQ����"
#         GetXZQ(JCTBshp,XZQBM,XZQMC)
        
#         print "����SortField����"
#         SortField(JCTBshp)
        print "����JCBH����"
#         JCBH(JCTBshp)
        
        print "����OBJECTID��BSM"
#         GetOBJECTID_BSM(JCTBshp)
        
#         print "����ChangeBHCD����"
#         ChangeBHCD(JCTBshp)
        

        print "����ռ����ũ�����"
        CalcuZJBNTMJ(JCTBshp,JBNTTB,FolderPath)
        print "����ռ�������"
        CalcuZGDMJ(JCTBshp,GDTB,FolderPath)
        
        
        print "---------------------------\n"
    print "=================Finish=================="