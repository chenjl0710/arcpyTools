# -*- coding: utf-8 -*-
import arcpy,os
arcpy.env.overwriteOutput = True
# Local variables:
CurrentPath = os.getcwd()
print CurrentPath
arcpy.env.workspace = CurrentPath
# Output_File_GDB = r"F:\Test"
File_GDB_Name = "testMosaic.gdb"
Mosaic_Dataset_Name = "MosaicB"
tifs = arcpy.ListRasters()
tif = tifs[0]
spatial_ref = arcpy.Describe(tif).spatialReference
Coordinate_System = spatial_ref
# Coordinate_System = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;.001;.001;IsHighPrecision"
# Input_Data =  "F:\\江西GF2\\gf2"
Input_Data = CurrentPath
# Mosaicshp = r"F:\Test\Mosaicshp.shp"
Mosaicshp = os.path.join(CurrentPath,"Mosaicshp.shp")

print "Create File GDB"
arcpy.CreateFileGDB_management(CurrentPath, File_GDB_Name, "CURRENT")

print "Create Mosaic Dataset"

arcpy.CreateMosaicDataset_management(File_GDB_Name, Mosaic_Dataset_Name, Coordinate_System, "", "", "NONE", "")

print "Add Rasters To Mosaic Dataset"
md_name = File_GDB_Name + "\\" + Mosaic_Dataset_Name
arcpy.AddRastersToMosaicDataset_management(md_name, "Raster Dataset", Input_Data, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "", "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")

print "Build Footprints"
arcpy.BuildFootprints_management(md_name, "", "RADIOMETRY", "1", "65535", "80", "0", "NO_MAINTAIN_EDGES", "SKIP_DERIVED_IMAGES", "UPDATE_BOUNDARY", "2000", "100", "NONE", "", "20", ".05")

print "Export Mosaic Dataset Geometry"
arcpy.ExportMosaicDatasetGeometry_management(md_name, Mosaicshp, "", "FOOTPRINT")

print "Delete Mosaicshp Fields"
arcpy.DeleteField_management(Mosaicshp, "MinPS;MaxPS;LowPS;HighPS;Category;Tag;GroupName;CenterX;CenterY;ZOrder;TypeID;ItemTS;UriHash")

raw_input("finish Running")