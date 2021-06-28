from osgeo import gdal

def Converter(nfile):
    options_list = [
        '-ot Byte',
        '-of JPEG',
        '-scale'
    ]           

    options_string = " ".join(options_list)
        
    gdal.Translate(
        'C:/Users/Amaan-PC/Desktop/DatumCon/'+nfile+'.jpg',
        'C:/Users/Amaan-PC/Desktop/DatumCon/'+nfile+'.tif',
        options=options_string
    )
