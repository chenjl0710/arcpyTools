# -*- coding: cp936 -*-
import arcpy
import pythonaddins

class AreaField(object):
    """Implementation for PointsStatic_addin.combobox_2 (ComboBox)"""
    def __init__(self):
#         AreaLayer.__init__(self)
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        global Field_Name 
        Field_Name = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        
#         AreaLayer.onSelChange(self, selection)
        if isinstance(Area,arcpy.mapping.Layer):
            fields = arcpy.ListFields(Area)
            self.items = []
            for f in fields:
                self.items.append(f.name)
            print self.items
    def onEnter(self):
        pass
    def refresh(self):
        pass

class AreaLayer(object):
    """Implementation for AreaLayer_addin.combobox (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        global Area
        Area = selection
        
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        dfs = arcpy.mapping.ListDataFrames(self.mxd)
        for df in dfs:
            lyrs = arcpy.mapping.ListLayers(self.mxd, '', df)
            self.items = []
            for lyr in lyrs:
                if isinstance(lyr,arcpy.mapping.Layer):
                    self.items.append(lyr)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class PointLayer(object):
    """Implementation for PointsStatic_addin.combobox (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        global Pnt
        Pnt = selection
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        dfs = arcpy.mapping.ListDataFrames(self.mxd)
        for df in dfs:
            lyrs = arcpy.mapping.ListLayers(self.mxd, '', df)
            self.items = []
            for lyr in lyrs:
                if isinstance(lyr,arcpy.mapping.Layer):
                    self.items.append(lyr)
            
    def onEnter(self):
        pass
    def refresh(self):
        pass

class PointsStatic(object):
    """Implementation for PointsStatic_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
    #     Pnt是点要素
    #     Area是面要素
        print Pnt
        if isinstance(Pnt,arcpy.mapping.Layer):
            print "yes"
            print arcpy.GetCount_management(Pnt)
            print Pnt.datasetName
        print Area
        print Field_Name
        #设置Area面状要素的游标
        icursor = arcpy.UpdateCursor(Area)
    #     创建临时layer
#         arcpy.MakeFeatureLayer_management(Pnt,"Pntlyr")
#         arcpy.MakeFeatureLayer_management(Area,"Arealyr")
    #     给点图层Pnt添加统计点个数的字段  Pnt_Count,Long。
        arcpy.AddField_management(Area,"Pnt_Count","LONG",9)
    #     遍历游标
        print "Start"
        for row in icursor:
            name_txt = row.getValue(Field_Name)
            print name_txt
            express = '"' + Field_Name + '"' + "=" + "'" + name_txt + "'"
#             express = '"Name"=' + "'" + name_txt + "'"
            print express
    #         对Area按属性选择
            arcpy.SelectLayerByAttribute_management(Area,"NEW_SELECTION",express)
    #         对Pnt和Area按位置选择，只统计Pnt完全落在Area里的点，未统计落在边界上的点
            arcpy.SelectLayerByLocation_management(Pnt,"COMPLETELY_WITHIN",Area)
    #         统计一个区域内点的个数
            PntCount = arcpy.GetCount_management(Pnt)
    #         把点的个数写进Area图层的Pnt_Count字段里
            row.setValue("Pnt_Count",PntCount)
            icursor.updateRow(row)
        
    #         清空选择集
            arcpy.SelectLayerByAttribute_management(Pnt,"CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(Area,"CLEAR_SELECTION")
        del icursor,row
    #     删除创建的临时layer
        arcpy.Delete_management(Pnt)
        arcpy.Delete_management(Area)
        print "Finish"