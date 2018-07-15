# -*- coding: cp936 -*-
import arcpy
import os
import shutil
import pythonaddins
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 


class AddImages(object):
    """Implementation for AddImages_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
      
    def onClick(self):
        global rootPath
        global imageList
        global Ext
        rootPath = r"\\172.17.2.34\homes\003"
        Ext = [".tif"]
        mxd = arcpy.mapping.MapDocument('current')
        df = arcpy.mapping.ListDataFrames(mxd)[0]

        def addImagesFromFolder(foderName):
            DOM_folders = os.path.join(rootPath,foderName,r'projectGlobalBuffer\ProductDOM')
            for rootdir,dirs,files in os.walk(DOM_folders):
                for file in files:
                    filepath = os.path.join(rootdir,file)
                    if os.path.splitext(filepath)[1] in Ext:
                        imageList.append(filepath)
        def addImagesFromXML(foderName):
            xml_path = os.path.join(rootPath,foderName,r'projectGlobalBuffer\Project\AT\ATMCH\AtMatch.xml')
            try: 
                tree = ET.parse(xml_path)     #打开xml文档 
                #root = ET.fromstring(country_string) #从字符串传递xml 
                root = tree.getroot()         #获得root节点  
            except Exception, e: 
                print "Error:cannot parse file:%s."%xml_path
                sys.exit(1) 
             
#             print root.tag, "---", root.attrib  
            for child in root: 
#                 print child.tag, "---", child.attrib 
                if child.tag == "File":
                    for Image in child.findall('Image'): #找到root节点下的所有country节点 
                        Path = Image.find('Path').text     #子节点下属性name的值 
                        GeoType = Image.find('GeoType').text   #子节点下节点rank的值 
                        ID = Image.find('ID').text
                        if 'ctrl' in ID  and GeoType == 'TFW':
#                             print GeoType,Path
                            imageList.append(Path)
        
        
        
        
        arcpy.env.workspace = rootPath
        folders = arcpy.ListWorkspaces("*", "Folder")
        for folder in folders:
            imageList = []
            foderName = os.path.basename(folder)
            
            addImagesFromFolder(foderName)
            addImagesFromXML(foderName)
            
#             print imageList
            
            for image1 in imageList:
                if os.path.exists(image1):
                    layer_name = os.path.basename(image1)
                    print image1
                    arcpy.MakeRasterLayer_management(image1, layer_name)
                    del layer_name
                else:
                    print u"%s 没有找到该数据，请核查！"%image1
                
                arcpy.RefreshTOC()
