import arcpy,os

shp_folder = r""
img = r""
clip_outsave = r""
arcpy.env.workspace = shp_folder
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    print fc
    arcpy.Clip_management(img,"",os.path.join(clip_outsave,fc.replace(".shp",".tif")),fc,"NoData","ClippingGeometry")