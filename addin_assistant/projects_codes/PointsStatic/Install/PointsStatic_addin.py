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
    #     Pnt�ǵ�Ҫ��
    #     Area����Ҫ��
        print Pnt
        if isinstance(Pnt,arcpy.mapping.Layer):
            print "yes"
            print arcpy.GetCount_management(Pnt)
            print Pnt.datasetName
        print Area
        print Field_Name
        #����Area��״Ҫ�ص��α�
        icursor = arcpy.UpdateCursor(Area)
    #     ������ʱlayer
#         arcpy.MakeFeatureLayer_management(Pnt,"Pntlyr")
#         arcpy.MakeFeatureLayer_management(Area,"Arealyr")
    #     ����ͼ��Pnt���ͳ�Ƶ�������ֶ�  Pnt_Count,Long��
        arcpy.AddField_management(Area,"Pnt_Count","LONG",9)
    #     �����α�
        print "Start"
        for row in icursor:
            name_txt = row.getValue(Field_Name)
            print name_txt
            express = '"' + Field_Name + '"' + "=" + "'" + name_txt + "'"
#             express = '"Name"=' + "'" + name_txt + "'"
            print express
    #         ��Area������ѡ��
            arcpy.SelectLayerByAttribute_management(Area,"NEW_SELECTION",express)
    #         ��Pnt��Area��λ��ѡ��ֻͳ��Pnt��ȫ����Area��ĵ㣬δͳ�����ڱ߽��ϵĵ�
            arcpy.SelectLayerByLocation_management(Pnt,"COMPLETELY_WITHIN",Area)
    #         ͳ��һ�������ڵ�ĸ���
            PntCount = arcpy.GetCount_management(Pnt)
    #         �ѵ�ĸ���д��Areaͼ���Pnt_Count�ֶ���
            row.setValue("Pnt_Count",PntCount)
            icursor.updateRow(row)
        
    #         ���ѡ��
            arcpy.SelectLayerByAttribute_management(Pnt,"CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(Area,"CLEAR_SELECTION")
        del icursor,row
    #     ɾ����������ʱlayer
        arcpy.Delete_management(Pnt)
        arcpy.Delete_management(Area)
        print "Finish"