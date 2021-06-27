from osgeo import gdal
# import os
# from PIL import Image

# root_dir = 'C:/Users/Amaan-PC/Desktop/DatumCon/'
# for filename in os.listdir(root_dir):
#     infile = os.path.join(root_dir, filename)
#     print("file : " + infile)
#     if infile[-3:] == "tif" or infile[-3:] == "bmp" :
#        # print "is tif or bmp"
#        outfile = infile[:-3] + "jpeg"
#        im = Image.open(infile)
#        print("new filename : " + outfile)
#        out = im.convert("RGB")
#        out.save(outfile, "JPEG", quality=100)

options_list = [
    '-ot Byte',
    '-of JPEG',
    '-b 1',
    '-scale'
]           

options_string = " ".join(options_list)
    
gdal.Translate(
    'save_image_path.jpg',
    'C:\Users\Amaan-PC\Desktop\DatumCon\s63_export.tif',
    options=options_string
)