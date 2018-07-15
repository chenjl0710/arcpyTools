# -*- coding:utf-8 -*-
import arcpy
import os
import shutil
import time
import multiprocessing
def currentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

# function
#Monitoring变化监测数据集Monitor图层批量添加字段
# inShp：Monitor_AddFields函数输入参数，必须为矢量数据图层
def Monitor_AddFields(inShp):
    print inShp
    fields = arcpy.ListFields(inShp)
    Flds = []
    for f in fields:
        Flds.append(f.name)
    print Flds
    print "创建字段。"
    if "Prj_ID" not in Flds:
        arcpy.AddField_management(inShp, "Prj_ID", "TEXT", "", "", "10")
        arcpy.AddMessage("Add field Prj_ID successfully!")

    if "QSX" not in Flds:
        arcpy.AddField_management(inShp, "QSX", "TEXT", "", "", "10")
        arcpy.AddMessage("Add field QSX successfully!")

    if "HSX" not in Flds:
        arcpy.AddField_management(inShp, "HSX", "TEXT", "", "", "10")
        arcpy.AddMessage("Add field HSX successfully!")

    if "TBLX" not in Flds:
        arcpy.AddField_management(inShp, "TBLX", "TEXT", "", "", "4")
        arcpy.AddMessage("Add field TBLX successfully!")

    if "BZ" not in Flds:
        arcpy.AddField_management(inShp, "BZ", "TEXT", "", "", "50")
        arcpy.AddMessage("Add field BZ successfully!")

    if "TBMJ" not in Flds:
        arcpy.AddField_management(inShp, "TBMJ", "FLOAT", 8, 2)
        arcpy.AddMessage("Add field TBMJ successfully!")

    if "Dist_Name" not in Flds:
        arcpy.AddField_management(inShp, "Dist_Name", "TEXT", "", "", "50")
        arcpy.AddMessage("Add field Dist_Name successfully!")


    if "Dist_Code" not in Flds:
        arcpy.AddField_management(inShp, "Dist_Code", "TEXT", "", "", "6")
        arcpy.AddMessage("Add field Dist_Code successfully!")

    if "Unique_Cod" not in Flds:
        arcpy.AddField_management(inShp, "Unique_Cod", "TEXT", "", "", "25")
        arcpy.AddMessage("Add field Unique_Code successfully!")

# function
# Landuse数据集批量添加字段
# inShp：Landuse_AddFields函数输入参数，必须为矢量数据图层
def Landuse_AddFields(inShp):
    print "创建字段。"
    try:
        arcpy.AddField_management(inShp, "Prj_ID", "TEXT", "", "", "10")
        arcpy.AddMessage("Add field Prj_ID successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Prj_ID")

    try:
        arcpy.AddField_management(inShp, "Phase", "TEXT", "", "", "10")
        arcpy.AddMessage("Add field Phase successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Phase")

    try:
        arcpy.AddField_management(inShp, "ID_src", "TEXT", "", "", "4")
        arcpy.AddMessage("Add field ID_src successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:ID_src")

    try:
        arcpy.AddField_management(inShp, "Name_src", "TEXT", "", "", "50")
        arcpy.AddMessage("Add field Name_src successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Name_src")

    try:
        arcpy.AddField_management(inShp, "ID_db", "TEXT", "", "", "4")
        arcpy.AddMessage("Add field ID_db successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:ID_db")

    try:
        arcpy.AddField_management(inShp, "Name_db", "TEXT", "", "", "50")
        arcpy.AddMessage("Add field Name_db successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Name_db")

    try:
        arcpy.AddField_management(inShp, "Image_src", "TEXT", "", "", "50")
        arcpy.AddMessage("Add field Image_src successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Image_src")

    try:
        arcpy.AddField_management(inShp, "Dist_Code", "TEXT", "", "", "6")
        arcpy.AddMessage("Add field Dist_Code successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Dist_Code")

    try:
        arcpy.AddField_management(inShp, "Unique_Cod", "TEXT", "", "", "25")
        arcpy.AddMessage("Add field Dist_Code successfully!")
    except IOError, e:
        arcpy.AddMessage("already have the field:Dist_Code")

    arcpy.AddMessage("Add fields finished!")
    print "finish"

def Image_src_sde(landuse, image):
    icursor = arcpy.SearchCursor(image)
    arcpy.MakeFeatureLayer_management(image, "imlyr")
    arcpy.MakeFeatureLayer_management(landuse, "lulyr")
    for row in icursor:
        gpid = row.getValue("Name")
        #         print gpid
        gpidV = '"' + gpid + '"'
        #     print gpidV
        express = '"Name" =' + "'" + gpid + "'"
        print express
        arcpy.SelectLayerByAttribute_management("imlyr", "NEW_SELECTION", express)
        arcpy.SelectLayerByLocation_management("lulyr", "INTERSECT", "imlyr","","NEW_SELECTION")
        arcpy.SelectLayerByAttribute_management("lulyr", "SUBSET_SELECTION", "\"PRJ_ID\" = '15.A90'")
        arcpy.CalculateField_management("lulyr", "IMAGE_SRC", gpidV, "PYTHON_9.3", "")
        arcpy.CalculateField_management("lulyr", "Phase", "!Image_src![13:21]", "PYTHON_9.3", "")
        arcpy.SelectLayerByAttribute_management("imlyr", "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("lulyr", "CLEAR_SELECTION")
    arcpy.Delete_management("imlyr")
    arcpy.Delete_management("lulyr")



# function
# Image_src函数是计算输入landuse图层的“Image_src”字段
# landuse：Image_src函数输入参数，是Landuse数据集的图层，必须为矢量数据图层
# image：Image_src函数输入参数，是影像的矢量框，其属性表含name字段，属性值表示影像的名称，必须为矢量数据图层
def Image_src(landuse, image):
    icursor = arcpy.SearchCursor(image)
    arcpy.MakeFeatureLayer_management(image, "imlyr")
    arcpy.MakeFeatureLayer_management(landuse, "lulyr")
    for row in icursor:
        gpid = row.getValue("Name")
        #         print gpid
        gpidV = '"' + gpid + '"'
        #     print gpidV
        express = '"Name" =' + "'" + gpid + "'"
        print currentTime(),"-",express
        arcpy.SelectLayerByAttribute_management("imlyr", "NEW_SELECTION", express)
        arcpy.SelectLayerByLocation_management("lulyr", "HAVE_THEIR_CENTER_IN", "imlyr")
        arcpy.CalculateField_management("lulyr", "Image_src", gpidV, "PYTHON_9.3", "")
        # arcpy.CalculateField_management("lulyr", "Phase", "!Image_src![13:21]", "PYTHON_9.3", "")  # Mid( [IMAGE_SRC],13,4 )+"-"+Mid( [IMAGE_SRC],17,2 )+"-"+Mid( [IMAGE_SRC],19,2 )
        arcpy.SelectLayerByAttribute_management("imlyr", "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("lulyr", "CLEAR_SELECTION")
    # arcpy.Delete_management("imlyr")
    # arcpy.Delete_management("lulyr")

# function
# Phase函数是计算landuse图层的“Phase”字段
# landuse：Phase函数输入参数，是Landuse数据集的图层，必须为矢量数据图层
# "!Image_src![13:21]":是函数输入参数的Image_src字段的13位至21位的字符串，13、21可以根据实际作调整
def Phase(landuse):
    arcpy.MakeFeatureLayer_management(landuse, "lulyr")
    arcpy.CalculateField_management("lulyr", "Phase", "!Image_src![13:21]", "PYTHON_9.3", "")




def UniqueCode_new(landuse,intufu):
    tufu_count = arcpy.GetCount_management(intufu)
    arcpy.MakeFeatureLayer_management(landuse, "dikuai_lyr")
    arcpy.MakeFeatureLayer_management(intufu, "intufulyr")
    curs = arcpy.SearchCursor(intufu)
    j = 1
    for row in curs:
        # NUMBER = row[0]
        # shp = row[1]

        gpid = row.getValue("NUMBER_1W")
        #         print gpid
        gpidV = '"' + gpid + '"'
        #     print gpidV
        express = '"NUMBER_1W" =' + "'" + gpid + "'"
        # print currentTime(),"-",express

        try:
            arcpy.SelectLayerByAttribute_management("intufulyr", "NEW_SELECTION", express)
            arcpy.SelectLayerByLocation_management("dikuai_lyr", "HAVE_THEIR_CENTER_IN", "intufulyr", "", "NEW_SELECTION")
            count = int(arcpy.GetCount_management("dikuai_lyr").getOutput(0))
            print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), ":", gpid, ":", str(j), "/", tufu_count, "---", count
            if count > 0:
                i = 1
                u_cur = arcpy.da.UpdateCursor("dikuai_lyr", ["Unique_Cod", "Dist_Code"])
                for u_row in u_cur:
                    # if u_row[0] is None:
                    # Cal_Value = "086" + str(u_row[1]) + gpid
                    if i <= 9 and i <= count:
                        u_row[0] =  "0" * 5 + str(i)
                    elif i <= 99 and i <= count:
                        u_row[0] =  "0" * 4 + str(i)
                    elif i <= 999 and i <= count:
                        u_row[0] = "0" * 3 + str(i)
                    elif i <= 9999 and i <= count:
                        u_row[0] =  "0" * 2 + str(i)
                    elif i <= 99999 and i <= count:
                        u_row[0] =  "0" * 1 + str(i)
                    elif i <= 999999 and i <= count:
                        u_row[0] =  "0" * 0 + str(i)
                    i = i + 1
                    u_cur.updateRow(u_row)
            arcpy.SelectLayerByAttribute_management("dikuai_lyr", "CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management("intufulyr", "CLEAR_SELECTION")
            j = j + 1
        except IOError, e:
            print "TopoEngine Error", gpid
# function
# UniqueCode函数是计算landuse图层的“Unique_Code”字段
# landuse：UniqueCode函数输入参数，是Landuse数据集的图层，必须为矢量数据图层，且“Dist_Code”字段值必须预先填写。
# intufu:函数输入参数，是1比10000的分幅框，
def UniqueCode(landuse,intufu):
    tufu_count = arcpy.GetCount_management(intufu)
    arcpy.MakeFeatureLayer_management(landuse, "dikuai_lyr")
    arcpy.MakeFeatureLayer_management(intufu, "intufulyr")
    curs = arcpy.SearchCursor(intufu)
    j = 1
    for row in curs:
        # NUMBER = row[0]
        # shp = row[1]

        gpid = row.getValue("NUMBER_1W")
        #         print gpid
        gpidV = '"' + gpid + '"'
        #     print gpidV
        express = '"NUMBER_1W" =' + "'" + gpid + "'"
        # print currentTime(),"-",express

        try:
            arcpy.SelectLayerByAttribute_management("intufulyr", "NEW_SELECTION", express)
            arcpy.SelectLayerByLocation_management("dikuai_lyr", "HAVE_THEIR_CENTER_IN", "intufulyr", "", "NEW_SELECTION")
            count = int(arcpy.GetCount_management("dikuai_lyr").getOutput(0))
            print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), ":", gpid, ":", str(j), "/", tufu_count, "---", count
            if count > 0:
                i = 1
                u_cur = arcpy.da.UpdateCursor("dikuai_lyr", ["Unique_Cod", "Dist_Code"])
                for u_row in u_cur:
                    # if u_row[0] is None:
                    Cal_Value = "086" + str(u_row[1]) + gpid
                    if i <= 9 and i <= count:
                        u_row[0] = Cal_Value + "0" * 5 + str(i)
                    elif i <= 99 and i <= count:
                        u_row[0] = Cal_Value + "0" * 4 + str(i)
                    elif i <= 999 and i <= count:
                        u_row[0] = Cal_Value + "0" * 3 + str(i)
                    elif i <= 9999 and i <= count:
                        u_row[0] = Cal_Value + "0" * 2 + str(i)
                    elif i <= 99999 and i <= count:
                        u_row[0] = Cal_Value + "0" * 1 + str(i)
                    elif i <= 999999 and i <= count:
                        u_row[0] = Cal_Value + "0" * 0 + str(i)
                    i = i + 1
                    u_cur.updateRow(u_row)
            arcpy.SelectLayerByAttribute_management("dikuai_lyr", "CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management("intufulyr", "CLEAR_SELECTION")
            j = j + 1
        except IOError, e:
            print "TopoEngine Error", gpid


# function
# srcFields2dbFields函数是根据ID_src、Name_src及矢量入库分类体系转换成ID_db、Name_db。
#根据实际情况，['11','12']、['21','22']······需要作调整。
# landuse：srcFields2dbFields函数的输入参数。
def srcFields2dbFields(landuse):
    icursor = arcpy.UpdateCursor(landuse)
    for row in icursor:
        tempID = str(row.getValue("ID_src"))
        if tempID in ['100']:
            row.setValue("ID_db","100")
            row.setValue("Name_db","耕地")
        elif tempID in ['200']:
            row.setValue("ID_db","200")
            row.setValue("Name_db","园地")
        elif tempID in ['300']:
            row.setValue("ID_db","300")
            row.setValue("Name_db","林地")
        elif tempID in ['400']:
            row.setValue("ID_db","400")
            row.setValue("Name_db","草地")
        elif tempID in ['600']:
            row.setValue("ID_db","500")
            row.setValue("Name_db","城乡建设用地")
        elif tempID in ['700']:
            row.setValue("ID_db","600")
            row.setValue("Name_db","交通运输用地")
        elif tempID in ['500']:
            row.setValue("ID_db","700")
            row.setValue("Name_db","水域及水利设施用地")
        elif tempID in ['800','900']:
            row.setValue("ID_db","800")
            row.setValue("Name_db","其他土地")
        icursor.updateRow(row)
    del icursor,row



def Copy_children2Parent(root,target):
    for parent, dirnames, filenames in os.walk(root):
        for file in filenames:
            img_path = os.path.join(parent, file)
            if not os.path.exists(os.path.join(root,file)) :
                print currentTime(),os.path.basename(img_path)
                shutil.copy(img_path, target)
            else:
                print currentTime(),os.path.basename(img_path),"already exists in ", target


if __name__ == "__main__":
    # landuse = r"D:\Chenjl_Data\矢量入库原始数据\26上海农普\一类测量\YLDCTB310000.shp"
    # intufu = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb\Export_Output1b1w"
    # UniqueCode(landuse, intufu)
    landuse = r"C:\test\四川landuse.shp"
    image = r"C:\test\四川landuse_fenfu.shp"
    # p = multiprocessing.Process(target=UniqueCode,args=(landuse, image))
    # p.start()
    # print p.pid

    UniqueCode_new(landuse, image)