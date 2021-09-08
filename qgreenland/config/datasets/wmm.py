from qgreenland.models.config.dataset import (
    ConfigDataset,
    ConfigDatasetHttpAsset,
)

wmm = ConfigDataset(
    id='world_magnetic_model',
    assets=[
        ConfigDatasetHttpAsset(
            id='geomagnetic_north_pole',
            urls=[
                'https://www.ngdc.noaa.gov/geomag/data/poles/WMM2020_NP.xy',
            ],
        ),
        ConfigDatasetHttpAsset(
            id='igrf_geomagnetic_north_pole',
            urls=[
                'https://www.ngdc.noaa.gov/geomag/data/poles/NP.xy',
            ],
        ),
        ConfigDatasetHttpAsset(
            id='geomagnetic_coordinates',
            urls=[
                'ftp://ftp.ngdc.noaa.gov/geomag/wmm/wmm2020/shapefiles/WMM2020_geomagnetic_coordinate_shapefiles.zip',  # noqa:E501
            ],
        ),
        ConfigDatasetHttpAsset(
            id='blackout_zones',
            urls=[
                'ftp://ftp.ngdc.noaa.gov/geomag/wmm/wmm2020/shapefiles/WMM2020-2025_BoZ_Shapefile.zip',  # noqa:E501
            ],
        ),
        *[
            ConfigDatasetHttpAsset(
                id=str(year),
                urls=[
                    f'ftp://ftp.ngdc.noaa.gov/geomag/wmm/wmm2020/shapefiles/{year}/WMM_{year}_all_shape_geographic.zip',  # noqa:E501
                ],
            )
            for year in range(2020, 2025 + 1)
        ],
    ],
    metadata={
        'title': 'The World Magnetic Model',
        'abstract': """
The World Magnetic Model (WMM) is a joint product of the United States’
National Geospatial-Intelligence Agency (NGA) and the United Kingdom’s
Defence Geographic Centre (DGC). The WMM was developed jointly by the
National Centers for Environmental Information (NCEI, Boulder CO, USA)
(formerly National Geophysical Data Center (NGDC)) and the British
Geological Survey (BGS, Edinburgh, Scotland).

The World Magnetic Model is the standard model used by the U.S. Department
of Defense, the U.K. Ministry of Defence, the North Atlantic Treaty
Organization (NATO) and the International Hydrographic Organization (IHO),
for navigation, attitude and heading referencing systems using the
geomagnetic field. It is also used widely in civilian navigation and
heading systems. The model, associated software, and documentation are
distributed by NCEI on behalf of NGA. The model is produced at 5-year
intervals, with the current model expiring on December 31, 2024.

Changes of the fluid flow in the Earth's outer core lead to unpredictable
changes in the Earth's magnetic field. Fortunately, the system has large
inertia, so that these changes take place over time scales of many
years. By surveying the field for a few years, one can precisely map the
present field and its rate of change and then linearly extrapolate it out
into the future. Provided that suitable satellite magnetic observations
are available, the prediction of the WMM is highly accurate on its release
date and then subsequently deteriorates towards the end of the 5 year
epoch, when it has to be updated with revised values of the model
coefficients.

It is important to recognize that the WMM and the charts produced from
this model characterize only the long-wavelength portion of the Earth's
internal magnetic field, which is primarily generated in the Earth's fluid
outer core. The portions of the geomagnetic field generated by the Earth's
crust and upper mantle, and by the ionosphere and magnetosphere, are
largely unrepresented in the WMM. Consequently, a magnetic sensor such as
a compass or magnetometer may observe spatial and temporal magnetic
anomalies when referenced to the WMM. In particular, certain local,
regional, and temporal magnetic declination anomalies can exceed 10
degrees. Anomalies of this magnitude are not common but they do
exist. Declination anomalies of the order of 3 or 4 degrees are not
uncommon but are usually of small spatial extent.
""",
        'citation': {
            'text': """
NCEI Geomagnetic Modeling Team and British Geological Survey. 2019.
World Magnetic Model 2020. NOAA National Centers for Environmental
Information. doi: 10.25921/11v3-da71, 2020, Date accessed:
{{date_accessed}}.
""",
            'url': 'https://doi.org/10.25921/11v3-da71',
        },
    },
)
