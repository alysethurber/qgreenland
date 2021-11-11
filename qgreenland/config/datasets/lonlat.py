import re

from qgreenland.constants.paths import ASSETS_DIR
from qgreenland.models.config.asset import ConfigDatasetRepositoryAsset
from qgreenland.models.config.dataset import ConfigDataset


lonlat_regex = re.compile(
    r'(?P<prefix>longitudes|latitudes)_(?P<res_id>.*)_degree.geojson',
)
geojson_files = ASSETS_DIR.glob('*.geojson')
lonlat_files = {}
for f in geojson_files:
    m = lonlat_regex.match(f.name)
    if not m:
        continue
    lonlat_files[f.name] = {
        'path': '{assets_dir}/' + str(f.relative_to(ASSETS_DIR)),
        'shortname': m.groupdict()['prefix'][0:3],
        'res_id': m.groupdict()['res_id'],
    }

lonlat = ConfigDataset(
    id='lonlat',
    assets=[
        ConfigDatasetRepositoryAsset(
            id=f"{params['shortname']}_{params['res_id']}_deg",
            filepath=params['path'],
        ) for params in lonlat_files.values()
    ],
    metadata={
        'title': 'Longitude and Latitude Lines',
        'abstract': 'Longitude and Latitude Lines.',
        'citation': {
            'text': 'Generated by QGreenland.',
            'url': '',
        },
    },
)
