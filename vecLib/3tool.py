# -*- coding: utf8 -*-
import arcpy
import os
import sys
import setting
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()
    self.current_path = setting.env[0]
    self.sdefile = os.path.join(self.current_path,"vector.sde")
    self.project = os.path.join(self.sdefile, 'SDE.PROJECT')
    self.fields = ['PRODUCT_TY','LOCATION','PRJ_ID','PRO_YEAR','RESOLUTION','PRJ_NAME']

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened.
    return:
    """
    cur = arcpy.da.SearchCursor(self.project, self.fields)
    self.prj_list = []
    for row in cur:
        self.prj_id_name = row[0]
        if self.prj_id_name not in self.prj_list:
            self.prj_list.append(self.prj_id_name)
    self.params[0].filter.list = self.prj_list
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    self.pro_reso = []  # 产品分辨率
    self.pro_id_name = []#产品项目编号
    if self.params[0].value:
        typename = self.params[0].value
        self.express = '"PRODUCT_TY" =' + "'" + typename + "'"#"PRODUCT_TY = '{0}'".format(typename)
        cur = arcpy.da.SearchCursor(self.project, self.fields,self.express)
        for row in cur:
            reso = row[4]+"-" + row[1].split('/')[-1]
            if reso not in self.pro_reso:
                self.pro_reso.append(reso)
        self.params[1].filter.list = self.pro_reso
    if self.params[1].value:
        reso_value = self.params[1].value.split('-')[0]
        self.express2 =  '"PRODUCT_TY" =' + "'" + typename + "' AND " +'"RESOLUTION"='+ "'"+ reso_value + "'"
        cur = arcpy.da.SearchCursor(self.project, self.fields, self.express2)
        for row in cur:
            pro_idname = row[2] + "-" + row[5]
            self.pro_id_name.append(pro_idname)
        self.params[2].filter.list = self.pro_id_name
    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return