# -*- coding: cp936 -*-
import os
import arcpy
import pythonaddins

class ButtonClass1(object):
    """Implementation for Add_ShpsFromFolder_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        folder_path = pythonaddins.OpenDialog('Select Folder', False, r'C:\Program Files (x86)\ArcGIS','Add')
        Ext = [".shp"]
        if folder_path == None:
            pythonaddins.MessageBox("请选择一个文件夹",'消息',0)
            exit
        else:
            shpsList = []
            for root,dirs,files in os.walk(folder_path):
                for file in files:
                    filepath = os.path.join(root,file)
                    if os.path.splitext(filepath)[1] in Ext:
                        shpsList.append(filepath)
            mxd = arcpy.mapping.MapDocument('current')
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            i = 1
            for fc in shpsList:
                layer_name = os.path.basename(fc).replace(".shp","") + str(i)
                print layer_name
                arcpy.MakeFeatureLayer_management(fc, layer_name)
                del layer_name
                i = i + 1
                arcpy.RefreshTOC()
            pythonaddins.MessageBox("矢量数据加载完成",'消息',0)
class ButtonClass7(object):
    """Implementation for Add_ImagesFromFolder.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        folder_path = pythonaddins.OpenDialog('Select Folder', False, r'C:\Program Files (x86)\ArcGIS','Add')
        #Ext = [".shp"]
        Ext = [".tif",".img",".pix",".dat"]
        if folder_path == None:
            pythonaddins.MessageBox("请选择一个文件夹",'消息',0)
            exit
        else:
            shpsList = []
            for root,dirs,files in os.walk(folder_path):
                for file in files:
                    filepath = os.path.join(root,file)
                    if os.path.splitext(filepath)[1] in Ext:
                        shpsList.append(filepath)
            mxd = arcpy.mapping.MapDocument('current')
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            i = 1
            for fc in shpsList:
                layer_name = os.path.splitext(os.path.basename(fc))[0] + str(i)
                print layer_name
                arcpy.MakeRasterLayer_management(fc, layer_name)
                del layer_name
                i = i + 1
                arcpy.RefreshTOC()
            pythonaddins.MessageBox("栅格影像数据加载完成",'消息',0)
