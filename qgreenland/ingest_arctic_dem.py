import os

import gdal
from earthpy import spatial as eps
import geopandas
from shapely.geometry import Polygon
import rasterio as rio

import util
from tasks import DATA_WIP_DIR

data_path = os.path.join(DATA_WIP_DIR, 'arctic_dem.tif')

# TODO: parameterize the resampling algorithm. For example, the default
# `nearest` would be desirable for some datasets.
reproj_raster = os.path.join(DATA_WIP_DIR, 'arctic_dem_reproj.tif')
gdal.Warp(reproj_raster, data_path, dstSRS=util.PROJECT_CRS,
          resampleAlg='bilinear')

# Spatial subset
crop_raster = os.path.join(DATA_WIP_DIR, 'arctic_dem_cropped.tif')
with rio.open(reproj_raster, 'r') as ds:
    bb_poly = geopandas.GeoSeries([Polygon(util.BBOX_POLYGON)])
    img_out, meta_out = eps.crop_image(ds, bb_poly)

with rio.open(crop_raster, 'w', **meta_out) as c_ds:
    c_ds.write(img_out)
