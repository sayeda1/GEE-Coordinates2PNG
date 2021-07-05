from osgeo import gdal
import os 
import sys 
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
PathOfImages = os.path.join(dirname, "Images")
PathOfTiffs = os.path.join(dirname, "GeoTiffs")
def Converter(nfile):
    options_list = [
        '-ot Byte',
        '-of JPEG',
        '-scale'
    ]           

    options_string = " ".join(options_list)
        
    gdal.Translate(
        PathOfImages+'\\'+nfile+'.jpg',
        PathOfTiffs+'\\'+nfile+'.tif',
        options=options_string
    )
