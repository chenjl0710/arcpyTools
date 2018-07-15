
import os,sys
import arcpy
import pythonaddins

class AddBaseMap2ArcMap(object):
    """Implementation for TQ_AddBaseMap2ArcMapV1_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        #Ding Yi Chang Liang
        Ext = [".tif",".pix",".img"]
        ImgNameField = "NAME"
        
        #Ding Yi Kong ZiDian / LieBiao
        Image_Dic = {}
        ImagesAdd2Arcmap_List = []
        imageList = []
        
        #Ding Yi Hanshu
        def addImagesFromFolder(foderName):
            DOM_folders = os.path.join(BaseMapFolder,foderName)
            for rootdir,dirs,files in os.walk(DOM_folders):
                for file in files:
                    filepath = os.path.join(rootdir,file)
                    if os.path.splitext(filepath)[1] in Ext:
                        imageList.append(filepath)
        def GetEN_Time(L):
            E_pos = L.find("E")
            L_name = L[E_pos:]
            index  = L_name.find("_")
            index2 = L_name.find("_",index + 1)
            index3 = L_name.find("_",index2 + 2)
            Name = L_name[:index3]
            return Name
        #Ding Yi mxd / df / Check_Box / BaseMap_Box
        mxd = arcpy.mapping.MapDocument("current")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        Check_Box   = arcpy.mapping.ListLayers(mxd, '',df)[0]
        BaseMap_Box = arcpy.mapping.ListLayers(mxd, '',df)[1]
        
        #Ding Yi Wen Jian Jia
        BaseMapFolder = pythonaddins.OpenDialog("Please Select BaseMap Folder",False,r"D:\\","Open")
        
        if BaseMapFolder == None:
            sys.exit()
        else:
            #Qiu Check_Box Yu BaseMap_Box de Kong Jian Xiang Jiao Guan Xi
            arcpy.SelectLayerByLocation_management(BaseMap_Box,"INTERSECT",Check_Box,"","NEW_SELECTION")
            
            #Ba gongzuo kongjian li de suoyou yingxiang dou tianjia dao [imageList] liebiao li.
            arcpy.env.workspace = BaseMapFolder
            folders = arcpy.ListWorkspaces("*", "Folder")
            for folder in folders:
                foderName = os.path.basename(folder).encode('UTF-8')
                addImagesFromFolder(foderName)
            print "imageList length:",len(imageList)
            print "\n"
            
            #ba imageList liebiao zhuan cheng zidian,
            #zidian de KEY shi jingdu_weidu_shijain,
            #zidian de  VALUE shi yingxiang de mingcheng.
            for Image in imageList:
                print "Image:",Image
                Image_key = GetEN_Time(Image.encode('UTF-8'))
                print "Image_key:",Image_key
                Image_Dic[Image_key] = Image.encode('UTF-8')
            print "Image_Dic length:",len(Image_Dic)
            print "\n"
            
            #Duqu xuanzhong de yingxiangkuang de shuxingbiao "NAME" ziduan,
            #ruguo NAME zai zidian li ,ba yingxiang append dao [ImagesAdd2Arcmap_List] liebiao li ,
            #ruguo meiyou ,jiu pass
            iRows = arcpy.SearchCursor(BaseMap_Box)
            for row in iRows:
                row_name = row.getValue(ImgNameField).encode('UTF-8') #E115D2_N24D6_20151016
                print "row_name:",row_name
                if row_name in Image_Dic:
                    Image_name = Image_Dic[row_name]
                    print "Image_name:",Image_name
                    ImagesAdd2Arcmap_List.append(Image_name)
                else:
                    pass
            print "ImagesAdd2Arcmap_List lenth:",len(ImagesAdd2Arcmap_List)
            print "\n"
            
            #ba ImagesAdd2Arcmap_List liebiao li de yingxiang yici jiazai dao arcmap li.
            for Image in ImagesAdd2Arcmap_List:
                add_layer = os.path.basename(Image) + "_BaseMap"
                print add_layer
                arcpy.MakeRasterLayer_management(Image,add_layer)
                del add_layer
            arcpy.RefreshTOC()
