# import google earth engine python api
import ee
import time
import GDrive2System
import GeoTiff2PNG
# authenticate and intialize GEE Python API
ee.Authenticate()
ee.Initialize()

# Load a landsat image and select three bands.
landsat = ee.ImageCollection('COPERNICUS/S2').filterDate('2020-01-01', '2020-02-28');

# Create a geometry representing an export region.
geometry = ee.Geometry.Rectangle([116.2634, 39.8412, 116.4849, 40.01236])
geometry = geometry['coordinates'][0]

BANDS = ['B4', 'B3', 'B2'];
landsat_mosaic =  landsat.median().select(BANDS);

task = ee.batch.Export.image.toDrive(image=landsat_mosaic,  # an ee.Image object.
                                     region=geometry,  # an ee.Geometry object.
                                     description='LANDCRUISER_export',
                                     folder='smp_folder',
                                     fileNamePrefix='LANDCRUISER_export',
                                     scale=10, 
                                     maxPixels=1e13, 
                                     crs='EPSG:4326')


task.start()
TaskSubmission = task.status()['state']
while TaskSubmission != 'COMPLETED':
    time.sleep(5)
    TaskSubmission = task.status()['state']

print('\nFile has finished uploading to drive...')
print('\nFile is now going to begin downloading from GDrive...')

obj = GDrive2System.DriveAPI()
i = int(input("Enter your choice:"
                  "1 - Download file, AnyKey- Exit.\n"))
   
if i == 1:
    f_id = input("Enter file id: ")
    f_name = input("Enter file name: ")
    obj.FileDownload(f_id, f_name)
      
else:
    exit()

print('\nFile is now being converted from GeoTiff to JPEG...')

GeoTiff2PNG.Converter('LANDCRUISER_export')



