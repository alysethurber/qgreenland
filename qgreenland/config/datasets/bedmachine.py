from qgreenland.models.config.asset import CmrAsset
from qgreenland.models.config.dataset import Dataset


bedmachine = Dataset(
    id='bedmachine',
    assets=[
        CmrAsset(
            id='only',
            granule_ur='SC:IDBMG4.004:212126987',
            collection_concept_id='C2050907241-NSIDC_ECS',
        ),
    ],
    metadata={
        'title': 'IceBridge BedMachine Greenland, Version 3',
        'abstract': """
This data set contains a bed topography/bathymetry map of Greenland based on
mass conservation, multi-beam data, and other techniques. It also includes
surface elevation and ice thickness data, as well as an ice/ocean/land mask.
""",
        'citation': {
            'text': """
Morlighem, M. et al. 2017, updated 2018. IceBridge BedMachine Greenland, Version
3. [Indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice
Data Center Distributed Active Archive Center. doi:
https://doi.org/10.5067/2CIX82HUV88Y. 2020/02/07.
""",
            'url': 'https://doi.org/10.5067/2CIX82HUV88Y',
        },
    },
)
