# Collect land cover data from CropSpace- [Cropland Data Layer](https://nassgeodata.gmu.edu/CropScape/)
library(CropScapeR)

# State of Colorado, FIPS code: 08 , years: 2013, 2015, 2017, 2019, 2021   
CO14 <- GetCDLData(aoi = '08', year = 2014, type = 'f')

#Save the raster
library(raster)
writeRaster(CO14, filename = "cdl-2014.tif", format = "GTiff")

