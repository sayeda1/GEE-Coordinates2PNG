# import google earth engine python api
import ee
import os
import time
import GDrive2System
import GeoTiff2PNG
# authenticate and intialize GEE Python API
ee.Authenticate()
ee.Initialize()

C1 = (str(input('\nEnter First Coordinate, put the x coordinate first, then place a comma and then place the y coordinate\n'))).replace(" ", "")
C2 = (str(input('\nEnter Second Coordinate, put the x coordinate first, then place a comma and then place the y coordinate\n'))).replace(" ", "")
C3 = (str(input('\nEnter Third Coordinate, put the x coordinate first, then place a comma and then place the y coordinate\n'))).replace(" ", "")
C4 = (str(input('\nEnter Fourth Coordinate, put the x coordinate first, then place a comma and then place the y coordinate\n'))).replace(" ", "")
NameOfFile = str(input('\nPlease input a suitable file name for your PNG, please dont use special character/White spaces\n'))
NameOfFile_img1 = NameOfFile + '_IMG1'
NameOfFile_img2 = NameOfFile + '_IMG2'

C1X, C1Y = C1.split(',')
C2X, C2Y = C2.split(',')
C3X, C3Y = C3.split(',')
C4X, C4Y = C4.split(',')

C1X = float(C1X)
C2X = float(C2X)
C3X = float(C3X)
C4X = float(C4X)

C1Y = float(C1Y)
C2Y = float(C2Y)
C3Y = float(C3Y)
C4Y = float(C4Y)
# Load a landsat image and select three bands.
#landsat = ee.ImageCollection('COPERNICUS/S2').filterDate('2020-01-01', '2020-02-28');
landsat = ee.ImageCollection('COPERNICUS/S2')
landsat_img1 = landsat.filterDate('2020-01-01', '2020-02-28');
landsat_img2 = landsat.filterDate('2016-01-01', '2016-02-28');
#-----> We can use FilterDate, at the batch export stage eliminating the need to do multiple uploads
#landsat = ee.ImageCollection('LANDSAT/LT05/C01/T1').filterDate('2011-01-01', '2011-02-28');
#change in detect blah blah  doesnt like rectangles
# Create a geometry representing an export region.
#ee.Geometry.Rectangle( xMin, yMin, xMax, yMax.)
#geometry = ee.Geometry.Rectangle([min(C1X,C2X,C3X,C4X), min(C1Y,C2Y,C3Y,C4Y),max(C1X,C2X,C3X,C4X), max(C1Y,C2Y,C3Y,C4Y)])
geometry = ee.Geometry.Rectangle([116.2621, 39.8412, 116.43326, 40.01236]);
geometry = geometry['coordinates'][0]

BANDS = ['B4', 'B3', 'B2'];
#BANDS = ['B3', 'B2', 'B1'];
landsat_mosaic_img1 =  landsat_img1.median().select(BANDS);
landsat_mosaic_img2 =  landsat_img2.median().select(BANDS);

print('\nstarting export of first image to drive\n')
task = ee.batch.Export.image.toDrive(image=landsat_mosaic_img1,  # an ee.Image object.
                                     region=geometry,  # an ee.Geometry object.
                                     description=NameOfFile_img1,
                                     folder='smp_folder',
                                     fileNamePrefix=NameOfFile_img1,
                                     scale=10, 
                                     maxPixels=1e13, 
                                     crs='EPSG:4326')


task.start()
TaskSubmission = task.status()['state']
while TaskSubmission != 'COMPLETED':
    time.sleep(5) #add a check for failed uploads, wasting alot of time by checking earth engine code editor
    TaskSubmission = task.status()['state']
    if(TaskSubmission == 'FAILED'):
        print('Image Upload Error')
        quit()


print('\nFile has finished uploading to drive...')
print('\nFile is now going to begin downloading from GDrive...')

obj = GDrive2System.DriveAPI()


print('\nstarting export of second image to drive\n')
task = ee.batch.Export.image.toDrive(image=landsat_mosaic_img2,  # an ee.Image object.
                                     region=geometry,  # an ee.Geometry object.
                                     description=NameOfFile_img2,
                                     folder='smp_folder',
                                     fileNamePrefix=NameOfFile_img2,
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


print('\nFiles are now being converted from GeoTiff to JPEG...')

GeoTiff2PNG.Converter(NameOfFile_img1)
GeoTiff2PNG.Converter(NameOfFile_img2)

#args based line of code, really good to run command based scripts
os.system('python C:/Users/Amaan-PC/Desktop/Change-detection-in-multitemporal-satellite-images-master/scripts/DetectChange.py -io C:/Users/Amaan-PC/Desktop/DatumCon/'+NameOfFile_img1+'.jpg -it C:/Users/Amaan-PC/Desktop/DatumCon/'+ NameOfFile_img2+'.jpg -o C:/Users/Amaan-PC/Desktop/DatumCon/')

print('\n finished')
# import os, sys
# dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
# print os.path.join(dirname, "b.txt")