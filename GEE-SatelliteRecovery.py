# import google earth engine python api
import ee
import time
# authentican and intialize GEE Python API
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
                                     description='RSX_export',
                                     folder='smp_folder',
                                     fileNamePrefix='RSX_export',
                                     scale=30,
                                     crs='EPSG:4326')

 #print(landsat)
task.start()
print(task.status())
print(task.state)
print(task.id)
time.sleep(120)
print(task.state)