from osgeo import gdal

options_list = [
    '-ot Byte',
    '-of JPEG',
    '-scale'
]           

options_string = " ".join(options_list)
    
gdal.Translate(
    'C:/Users/Amaan-PC/Desktop/DatumCon/TEST8.jpg',
    'C:/Users/Amaan-PC/Desktop/DatumCon/s63_export.tif',
    options=options_string
)