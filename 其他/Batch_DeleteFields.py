import arcpy

arcpy.env.workspace = r"D:\test2\SpatialJoinWithAttributes"

fcs = arcpy.ListFeatureClasses("*","Polygon","")
print "start"
for fc in fcs:
        print fc
        fields = arcpy.ListFields(fc)
        fieldNameList = []
        for field in fields:
                print field.name
                if field.name == "FID" or field.name == "Shape" or field.name == "ClassName" or field.name == "ClassID":
                        pass
                else:
                        fieldNameList.append(field.name)
                
        print fieldNameList
        arcpy.DeleteField_management(fc,fieldNameList)
                        
print "finish"
