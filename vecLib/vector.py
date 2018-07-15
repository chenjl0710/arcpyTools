# -*- coding: utf8 -*-
import os
import arcpy
import sys
import datetime
import setting
# sdefile = "vector.sde"
# # arcpy.env.workspace = sdefile
# project = os.path.join(sdefile,'SDE.PROJECT')
# fields = ['PRODUCT_TY','LOCATION','PRJ_ID','PRO_YEAR','RESOLUTION','PRJ_NAME','SHAPE@ ']
# cur = arcpy.da.SearchCursor(project,fields)
# for row in cur:

def currentPath():
    curpath = sys.argv[0]
    return curpath



class areaSearch():
    def __init__(self):
        self.current_path = os.path.dirname(sys.argv[0])
        self.sdefile = os.path.join(self.current_path,"vector.sde")
        self.project = os.path.join(self.sdefile, 'SDE.PROJECT')
        self.boundary = os.path.join(self.sdefile, 'SDE.Boundary')
        self.province = os.path.join(self.boundary,"SDE.全国省界")
        self.city = os.path.join(self.boundary,"SDE.全国市界")
        self.country = os.path.join(self.boundary,"SDE.全国区县界")
        self.fields = ['NAME',"ADMINCODE"]
        self.prj_fields = ['PRODUCT_TY', 'LOCATION', 'PRJ_ID', 'PRO_YEAR', 'RESOLUTION', 'PRJ_NAME', 'SHAPE@']

    def Province(self):
        """
        :return:省份中文名称及邮编，如：江苏省-320000
        """
        cur = arcpy.da.SearchCursor(self.province, self.fields)
        self.province_list = []
        for row in cur:
            self.province_name = row[0]+"-"+row[1]
            self.province_list.append(self.province_name)
        return self.province_list

    def City(self,pro_postcode):
        """
        postcode:
        :return:城市中文名称及邮编，如：伊春市-230722
        """
        pro_code = pro_postcode[:2]
        # ADMINCODE LIKE '31%'
        self.express = "ADMINCODE LIKE '{0}%'".format(pro_code)
        # arcpy.MakeFeatureLayer_management(self.city, "city_lyr")
        # arcpy.SelectLayerByAttribute_management("city_lyr","NEW_SELECTION",self.express)
        cur = arcpy.da.SearchCursor("city_lyr", self.fields,self.express)
        self.city_list = []
        for row in cur:
            self.city_name = row[0]+"-"+row[1]
            self.city_list.append(self.city_name)
        return self.city_list

    def Country(self,city_postcode):
        """
        :return:区县中文名称及邮编，如：广宗县-130531
        """
        city_code = city_postcode[:4]
        self.express =  "ADMINCODE LIKE '{0}%'".format(city_code)
        # arcpy.MakeFeatureLayer_management(self.country, "country_lyr")
        # arcpy.SelectLayerByAttribute_management("country_lyr", "NEW_SELECTION", self.express)
        cur = arcpy.da.SearchCursor("country_lyr", self.fields,self.express)
        self.country_list = []
        for row in cur:
            self.country_name = row[0]+"-"+row[1]
            self.country_list.append(self.country_name)
        return self.country_list

    def createGdb_post(self,outpath,area_postcode):
        """
        :param outpath: 输出文件路径，文件夹
        :param prj_id:项目编号
        :return:str ,file_GDB
        """
        gdb_name = "TQ" + area_postcode.split('-')[0] + area_postcode.split('-')[1]+".gdb"
        try:
            arcpy.CreateFileGDB_management(outpath,gdb_name)

        except:
            gdb_name = "TQ" + area_postcode.split('-')[0] + area_postcode.split('-')[1] + "_"+str(datetime.datetime.now()).split('.')[0].replace(' ','').replace('-','').replace(':','')+".gdb"
            arcpy.CreateFileGDB_management(outpath, gdb_name)
        file_GDB = os.path.join(outpath,gdb_name)
        return file_GDB

    def export_by_area_resolution(self,area_postcode,resolution,outdir):
        """
        :param area_postcode: 金山区-310116
        :param resolution: sdeSearch类的getResolution_producttype方法，如：0.8--亚米
        :return:
        """
        pro_type= resolution.split('--')[1]
        land_sde_lyr = os.path.join(self.sdefile, "SDE.Land","SDE." + pro_type)
        arcpy.MakeFeatureLayer_management(land_sde_lyr,"land_sde_lyr")
        postcode = area_postcode.split('-')[1]

        gdb_path = self.createGdb_post(outdir,area_postcode)

        # for area in [self.province,self.city,self.country]:
        area = self.country
        arcpy.MakeFeatureLayer_management(area,"area_lyr")
        self.express = '"ADMINCODE" =' + "'" + postcode + "'"
        arcpy.SelectLayerByAttribute_management("area_lyr", 'NEW_SELECTION', self.express)
        selectCount = arcpy.GetCount_management("area_lyr")
        if selectCount == 1:
            arcpy.SelectLayerByLocation_management("land_sde_lyr","intersect","area_lyr","","NEW_SELECTION")
        arcpy.Delete_management("area_lyr")
        export_fc = os.path.join(gdb_path,area_postcode.replace('-',''))
        arcpy.CopyFeatures_management("land_sde_lyr",export_fc)



class sdeSearch():
    def __init__(self):
        self.current_path = setting.env[0]
        self.sdefile = os.path.join(self.current_path,"vector.sde")
        self.project = os.path.join(self.sdefile, 'SDE.PROJECT')
        self.fields = ['PRODUCT_TY','LOCATION','PRJ_ID','PRO_YEAR','RESOLUTION','PRJ_NAME']
        self.boundary = os.path.join(self.sdefile, 'SDE.Boundary')

    def getType(self):
        """
        :return: 产品类型   如：农普专题
        """
        cur = arcpy.da.SearchCursor(self.project, self.fields)
        self.prj_type = []
        for row in cur:
            self.prj_type_name= row[0]
            self.prj_type.append(self.prj_type_name)
        return self.prj_type




    def getProjects(self):
        """
        :return: 返回SDE.PROJECT中的项目编号和名称
        """
        cur = arcpy.da.SearchCursor(self.project, self.fields)
        self.prj_list = []
        for row in cur:
            self.prj_id_name = row[2] + "--" + row[5]
            self.prj_list.append(self.prj_id_name)
        return self.prj_list

    def getResolution_producttype(self):
        """

        :return:
        """
        cur = arcpy.da.SearchCursor(self.project, self.fields)
        self.reso_type_list = []
        for row in cur:
            resolution = row[4]
            protype = row[1].split('/')[-1]
            self.reso_type = resolution + "--" + protype
            self.reso_type_list.append(self.reso_type)
        return self.reso_type_list

    def searchBypeoject(self,prj_id):
        """
        :param prj_id:str,,项目编号,如：16.D63
        :return:str,项目的存储路径,如  /SDE.Land/SDE.亚米
        """
        loca = ""
        # self.express = '"PRJ_ID" =' + "'" + prj_id + "'"
        self.express = "PRJ_ID = '{0}'".format(prj_id)
        # arcpy.MakeFeatureLayer_management(self.project,'projectlayer')
        # arcpy.SelectLayerByAttribute_management('projectlayer','NEW_SELECTION',self.express)
        cur = arcpy.SearchCursor(self.project,self.express)
        try:
            for row in cur:
                if row.getValue("PRJ_ID") == prj_id:
                    loca = row.getValue("LOCATION").replace('..','').replace('/','\SDE.')
                    return loca
        except:
            loca = None
            return loca

    def createGdb(self,outpath,prj_id):
        """
        :param outpath: 输出文件路径，文件夹
        :param prj_id:项目编号
        :return:str ,file_GDB
        """
        gdb_name = "TQ" + prj_id.replace('.','')+".gdb"
        try:
            arcpy.CreateFileGDB_management(outpath,gdb_name)

        except:
            gdb_name = "TQ" + prj_id.replace('.','')+"_"+str(datetime.datetime.now()).split('.')[0].replace(' ','').replace('-','').replace(':','')+".gdb"
            arcpy.CreateFileGDB_management(outpath, gdb_name)
        file_GDB = os.path.join(outpath,gdb_name)
        return file_GDB

    def exportByloca(self,loca,prj_id,export):
        """
        :param loca: SDE.PROJECT中LOCATION的值，如  /SDE.Land/SDE.亚米
        :param export:输出file gdb文件夹路径
        :return:file geodatabase
        """
        prj_id_ = "prj_"+ prj_id.replace('.','')
        gdb_file = self.createGdb(export,prj_id)
        location = self.sdefile + loca
        print "location:",location
        arcpy.MakeFeatureLayer_management(location,'lacation_lyr')
        self.express = 'Prj_ID =' + "'" + prj_id + "'"
        arcpy.SelectLayerByAttribute_management('lacation_lyr','NEW_SELECTION',self.express)
        export_path = os.path.join(gdb_file ,prj_id_)
        arcpy.CopyFeatures_management('lacation_lyr',export_path)

        arcpy.MakeFeatureLayer_management(self.project,"project_lyr")
        self.express_prj = 'PRJ_ID =' + "'" + prj_id + "'"
        arcpy.SelectLayerByAttribute_management('project_lyr','NEW_SELECTION',self.express_prj)
        export_path = os.path.join(gdb_file ,prj_id_+"_meta")
        arcpy.CopyFeatures_management('project_lyr',export_path)
