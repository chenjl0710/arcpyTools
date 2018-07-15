# -*- coding: utf8 -*-
import arcpy
import os
import setting
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()
    self.current_path = setting.env[0]
    self.sdefile = os.path.join(self.current_path,"vector.sde")
    self.boundary = os.path.join(self.sdefile, 'SDE.Boundary')
    self.province = os.path.join(self.boundary,"SDE.全国省界")
    self.city = os.path.join(self.boundary,"SDE.全国市界")
    self.country = os.path.join(self.boundary,"SDE.全国区县界")
    self.project = os.path.join(self.sdefile, 'SDE.PROJECT')
    self.fields = ['NAME',"ADMINCODE",'SHAPE@']
    self.prj_fields = ['PRODUCT_TY','LOCATION','PRJ_ID','PRO_YEAR','RESOLUTION','PRJ_NAME','SHAPE@']

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    cur = arcpy.da.SearchCursor(self.province, self.fields)
    self.province_list = []
    for row in cur:
        self.province_name = row[0]+"-"+row[1]
        self.province_list.append(self.province_name)
    self.params[0].filter.list = self.province_list

    cur = arcpy.da.SearchCursor(self.city, self.fields)
    self.city_list = []

    for row in cur:
        self.city_name = row[0] + "-" + row[1]
        self.city_list.append(self.city_name)
    self.params[1].filter.list = self.city_list

    cur = arcpy.da.SearchCursor(self.country, self.fields)
    self.country_list = []
    for row in cur:
        self.country_name = row[0] + "-" + row[1]
        self.country_list.append(self.country_name)
    self.params[2].filter.list = self.country_list

    # cur = arcpy.da.SearchCursor(self.project, self.prj_fields)
    # self.project_list = []
    # for row in cur:
    #     self.project_name = row[2] + "-" + row[5]
    #     self.project_list.append(self.project_name)
    # self.params[3].filter.list = self.project_list

    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    self.city_list = []
    self.country_list = []
    if self.params[0].value:
        pro_code = self.params[0].value.split('-')[1][:2]
        self.expresscity = "ADMINCODE LIKE '{0}%'".format(pro_code)
        cur = arcpy.da.SearchCursor(self.city, self.fields,self.expresscity)
        for row in cur:
            self.city_name = row[0]+"-"+row[1]
            self.city_list.append(self.city_name)
        self.params[1].filter.list = self.city_list

    if self.params[1].value:
        city_code = self.params[1].value.split('-')[1][:4]
        self.expresscountry = "ADMINCODE LIKE '{0}%'".format(city_code)
        cur = arcpy.da.SearchCursor(self.country, self.fields,self.expresscountry)
        for row in cur:
            self.country_name = row[0]+"-"+row[1]
            self.country_list.append(self.country_name)
        self.params[2].filter.list = self.country_list

    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return