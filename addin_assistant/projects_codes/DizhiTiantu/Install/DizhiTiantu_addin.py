# -*- coding: utf-8 -*-
import arcpy
import pythonaddins
import os
class CreateAnnotation(object):
    """Implementation for CreateAnnotation_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        arcpy.env.overwriteOutput = True
        arcpy.CreateFileGDB_management(main_path,"Annotation.gdb")
        #Annotation = os.path.join(main_path,"Annotation.gdb")

        #mxd = arcpy.mapping.MapDocument('current')
        #dfs = arcpy.mapping.ListDataFrames(mxd)
        #lyrlist = arcpy.mapping.ListLayers(mxd,'',dfs[0])
        #for lyr in lyrlist:
        #    if lyr.name == u"等高线计曲线":
        #        arcpy.TiledLabelsToAnnotation_cartography(mxd,dfs[0],lyr,Annotation,"contour_Anno","Anno")
        #    elif lyr.name == u"乡镇":
        #        arcpy.TiledLabelsToAnnotation_cartography(mxd,dfs[0],lyr,Annotation,"Town_Anno","Anno")
        #    elif lyr.name == u"地名":
        #        arcpy.TiledLabelsToAnnotation_cartography(mxd,dfs[0],lyr,Annotation,"PlaceName_Anno","Anno")
        #    elif lyr.name == u"山":
        #        arcpy.TiledLabelsToAnnotation_cartography(mxd,dfs[0],lyr,Annotation,"Mountain_Anno","Anno")
        #arcpy.RefreshTOC()
        #arcpy.RefreshActiveView()
        #mxd.saveACopy(os.path.join(main_path,folderName + "layout.mxd"))
        pythonaddins.MessageBox("Create Annotation.gdb OK!","INFO",0)
        pythonaddins.MessageBox(u"请手动创建Annatation!","INFO",0)

class ExportMap(object):
    """Implementation for ExportMap_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        mxd = arcpy.mapping.MapDocument('current')
        picName = folderName + ".jpg"
        picPath = os.path.join(main_path,picName)

        arcpy.mapping.ExportToJPEG( mxd, picPath, '',5844, 4135, 400)
        pythonaddins.MessageBox("Picture Export OK!","INFO",0)
class UpdateLayers(object):
    """Implementation for UpdateLayers_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
            
    def onClick(self):
        global main_path
        global folderName
        main_path = pythonaddins.OpenDialog("Please Select Vectors Folder",False,"","OK")
        print "main_path:",main_path
        #name_txt = ''
        code_txt = ''
        moutain_txt = ''
        placename_txt = ''
        folderName = os.path.basename(main_path)
        print "folderName:",folderName
        #name_txt = folderName[:-10]
        code_txt = folderName[-10:]
        arcpy.env.workspace = main_path
        list_fc = arcpy.ListFeatureClasses()
        print "list_fc:",list_fc
        ras_list = arcpy.ListRasters()
        print "ras_list:",ras_list
        mxd = arcpy.mapping.MapDocument('current')
        df_list = arcpy.mapping.ListDataFrames(mxd)
        print "setting MapDocument DataSource"
        RAOLK = u''
        PlaceName = u''
        Town = u''
        Moutain = u''
        WaterBody = u''
        River = u''
        contour_B = u''
        contour = u''
        MapSheet = u''
        for fc in list_fc:
            print "fc:",fc
            if u"ROALK" in fc:
                RAOLK = fc
            elif u"PlaceName" in fc:
                PlaceName = fc
            elif u"Mountain" in fc:
                Moutain = fc
            elif u"WaterBody" in fc:
                WaterBody = fc
            elif u"River" in fc:
                River = fc
            elif u"contour_B" in fc:
                contour_B = fc
            elif u"contour" in fc and "_B" not in fc:
                contour = fc
            elif u"Town" in fc:
                Town = fc
            elif u"MapSheet" in fc:
                MapSheet = fc
        print "featurelayer is ready"

        def GetName(featureclass):
            cursor = arcpy.SearchCursor(featureclass)
            for row in cursor:
                if row.getValue("NAME") <> "" and len(row.getValue("NAME")) <= 4:
                    return row.getValue("NAME")
                    break   
                else:
                    continue   

        for df in df_list:
            lyrlist = arcpy.mapping.ListLayers(mxd,'',df)
            for lyr in lyrlist:
                print lyr.name
                if lyr.name == u"道路" and RAOLK <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", RAOLK[:-4])
                    #UniqueValuesSymbology(lyr)
                    arcpy.ApplySymbologyFromLayer_management(lyr, os.path.join(os.path.dirname(mxd.filePath),"road.lyr"))

                elif lyr.name == u"地名" and PlaceName <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", PlaceName[:-4])
                    placename_txt = GetName(lyr)##########
                    lyr.showLabels = True
                elif lyr.name == u"乡镇"and Town <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", Town[:-4])
                    lyr.showLabels = True
                elif lyr.name == u"山" and Moutain <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", Moutain[:-4])
                    moutain_txt = GetName(lyr) #########
                    lyr.showLabels = True
                elif lyr.name == u"水体" and WaterBody <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", WaterBody[:-4])

                elif lyr.name == u"单线河" and River <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", River[:-4])

                elif lyr.name == u"等高线计曲线" and contour_B <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", contour_B[:-4])
                    lyr.showLabels = True
                elif lyr.name == u"等高线" and contour <> "":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE", contour[:-4])
                    
                elif lyr.name == u"contour_Anno" or  lyr.name == u"Town_Anno" or lyr.name == u"PlaceName_Anno" or lyr.name == u"Mountain_Anno" or lyr.name == u"Default":
                    continue

                elif lyr.name == u"影像":
                    lyr.replaceDataSource(main_path, "RASTER_WORKSPACE", ras_list[0])

                elif lyr.name == u"MapSheet":
                    lyr.replaceDataSource(main_path, "SHAPEFILE_WORKSPACE",MapSheet[:-4])
                    lyr.showLabels = True
                else:
                    lyr.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()


            #设置dataframe的投影，将影像的投影信息赋给dataframe
            Spatial_ref = arcpy.Describe(contour).spatialReference
            #print "Spatial_ref:",Spatial_ref
            df_list[0].spatialReference = Spatial_ref
            #print "dataframe ref:",df_list[0].spatialReference
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()


        lyrlist0 = arcpy.mapping.ListLayers(mxd, '', df_list[0])
        for lyr0 in lyrlist0:
            if lyr0.name == u"影像":
                df_esxtent1 = lyr0.getExtent()
        df_list[0].panToExtent(df_esxtent1)
        df_list[0].scale = 20000
        arcpy.RefreshActiveView()

        lyrlist1 = arcpy.mapping.ListLayers( mxd, '', df_list[1])
        for lyr1 in lyrlist1:
            if lyr1.name == u"MapSheet":
                df_esxtent2 = lyr1.getExtent()
        df_list[1].extent = df_esxtent2
        df_list[1].scale = df_list[1].scale * 0.6
        arcpy.RefreshActiveView()

        ###########
        print "setting PageLayout properties"
        elm_txts = arcpy.mapping.ListLayoutElements( mxd, "TEXT_ELEMENT")
        print "placename_txt:",placename_txt
        print "placename_txt_length:",len(placename_txt)
        elm_txts[1].text = placename_txt
        print "elm_txts[1]:",elm_txts[1]
        elm_txts[0].text = moutain_txt
        elm_txts[7].text = code_txt
        #elm_txts[8].text = name_txt
        arcpy.RefreshActiveView()


        #print "setting txt_elem position"
        #item_count = 0
        #legend = arcpy.mapping.ListLayoutElements( mxd, "LEGEND_ELEMENT")
        #leg = legend[0]
        #item_count = len(leg.items)
        #height = leg.elementHeight
        #if "" in leg.items:
        #    item_count += 3
        #placeName_index = 0
        #if u"地名" in leg.items:
        #    placeName_index = leg.items.index(u"地名")
        #    elm_txts[1].elementPositionY = (9 - placeName_index) * height/10
        #if u"山" in leg.items:
        #    placeName_index = leg.items.index(u"山")
        #    elm_txts[2].elementPositionY = (9 - placeName_index) * height/10


        mxd.saveACopy(os.path.join(main_path,folderName + "layout.mxd"))
        pythonaddins.MessageBox("Data update ok!","INFO",0)
        pythonaddins.MessageBox(u"请修改图幅名称、图例!","INFO",0)
