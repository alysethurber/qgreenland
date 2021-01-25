import os
import shutil
import subprocess
import tempfile
from itertools import product
from pathlib import Path

from netCDF4 import Dataset
import numpy as np


BASE_DIR = Path('/share/appdata/qgreenland-private-archive/racmo_qgreenland_jan2021/')

# Filenames of "u" and "v" directional magnitude components of windspeed vectors
U_FN = 'u10m.1958-2019.BN_RACMO2.3p2_FGRN055_5.5km.YY-mean.nc'
V_FN = 'v10m.1958-2019.BN_RACMO2.3p2_FGRN055_5.5km.YY-mean.nc'


def _cmd(cmd: str):
    result = subprocess.run(
        cmd,
        shell=True,
        executable='/bin/bash',
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result

def copy_ncs(*, out_dir: Path):
    return _cmd(f'cp {BASE_DIR}/*.nc {out_dir}/.')


def write_csv(*, in_dir: Path, out_fp: Path) -> Path:
    u_ds = Dataset(in_dir / U_FN, 'r')
    v_ds = Dataset(in_dir / V_FN, 'r')

    u_data = u_ds.variables['u10m'][0, 0, :]
    v_data = v_ds.variables['v10m'][0, 0, :]

    lon_data = u_ds.variables['lon'][:]
    lat_data = u_ds.variables['lat'][:]

    with open(out_fp, 'w') as f:
        f.write(f'eastward_component,northward_component,magnitude,lon,lat\n')
        for i, j in product(range(u_data.shape[0]), range(u_data.shape[1])):
            u = u_data[i, j]
            if np.ma.is_masked(u):
                continue

            v = v_data[i, j]
            lon = lon_data[i, j]
            lat = lat_data[i, j]
            magnitude = np.sqrt(u**2 + v**2)

            f.write(f'{u},{v},{magnitude},{lon},{lat}\n')

    return out_fp 

def convert_to_gpkg(*, in_fp: Path, out_fp: Path):
    return _cmd(
        'ogr2ogr'
        ' -oo X_POSSIBLE_NAMES=lon'
        ' -oo Y_POSSIBLE_NAMES=lat'
        ' -oo AUTODETECT_TYPE=True'
        ' -s_srs "EPSG:4326" -t_srs "EPSG:3413"'
        f' {out_fp} {in_fp}'
    )


def u_v_to_magnitude_raster(*, in_dir: Path, out_fp: Path):
    u_fp = in_dir / U_FN
    v_fp = in_dir / V_FN

    tif_fp = out_fp.with_suffix('.tif')
    return _cmd(
        'gdal_calc.py'
        f' -A NETCDF:{u_fp}:u10m -B NETCDF:{v_fp}:v10m'
        f' --calc="sqrt(A**2 + B**2)" --outfile={tif_fp}'
        # NOTE: gdal_translate puts the data in variable "Band1"
        f' && gdal_translate -of NetCDF {tif_fp} {out_fp}'
    )

def zip_dir_contents(in_dir: Path, out_fp: Path):
    # NOTE: You may be asking "Why do we zip everything up?" Right now we can
    # only have 1 "source" per private dataset.
    shutil.make_archive(out_fp.with_suffix(''), 'zip', in_dir)

    return out_fp


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Copy fetched netcdf files from base location
        # TODO: Actually run the fetch and gunzip scripts to pull data directly
        # in to tempdir. No need to have all this junk laying around at the end.
        copy_ncs(out_dir=tmppath)

        # Generate magnitude.tif
        u_v_to_magnitude_raster(
            in_dir=tmppath,
            out_fp=tmppath / 'magnitudes.nc'
        )

        # Generate wind_vector_points.gpkg
        csv_fp = write_csv(
            in_dir=tmppath,
            out_fp=tmppath / 'wind_vector_points.csv'
        )
        convert_to_gpkg(
            in_fp=csv_fp,
            out_fp=tmppath / 'wind_vector_points.gpkg'
        )

        zip_fp = zip_dir_contents(
            tmpdir,
            out_fp=BASE_DIR / 'RACMO_QGreenland_Jan2021.zip'
        )

    print(f'Wrote zip: {zip_fp}')
