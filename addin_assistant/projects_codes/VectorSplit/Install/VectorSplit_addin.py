import os
import arcpy
import pythonaddins

class FieldListCB(object):
    """Implementation for FieldListCB_addin.combobox (ComboBox)"""
    def __init__(self):
        self.items =[] 
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        floder = pythonaddins.OpenDialog("please select a floder",False,r"D:\test","Save")
        self.mxd = arcpy.mapping.MapDocument('current')
        layer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if isinstance(layer,arcpy.mapping.Layer):
            #arcpy.MakeFeatureLayer_management(layer, "lyr")
            icursor = arcpy.SearchCursor(layer)
            for row in icursor:
                igetvalue = row.getValue(selection)
                print "selection:",selection
                print "igetvalue:",igetvalue
                print """ "%s" = '%s' """%(selection,igetvalue)
                arcpy.SelectLayerByAttribute_management(layer,"NEW_SELECTION",""" "%s" = '%s' """%(selection,igetvalue))
                save_name = igetvalue + ".shp"
                outsave = os.path.join(floder,save_name)
                arcpy.CopyFeatures_management(layer,outsave)
                arcpy.SelectLayerByAttribute_management(layer,"CLEAR_SELECTION")
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        layer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if focused:
            if isinstance(layer,arcpy.mapping.Layer):
                fields = arcpy.ListFields(layer)
                self.items = []
                for f in fields:
                    self.items.append(f.name)
                print self.items
            else:
                pythonaddins.MessageBox("please select a layer!",'Message',0)
                pass
            
    def onEnter(self):
        pass
    def refresh(self):
        pass
