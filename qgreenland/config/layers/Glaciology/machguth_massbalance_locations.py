from qgreenland.config.datasets.machguth_massbalance import (
    machguth_etal_massbalance_obs_locations as dataset,
)
from qgreenland.config.helpers.steps.ogr2ogr import (
    STANDARD_OGR2OGR_ARGS,
)
from qgreenland.config.project import project
from qgreenland.models.config.layer import ConfigLayer, ConfigLayerInput
from qgreenland.models.config.step import ConfigLayerCommandStep


machguth_massbalance_locations = ConfigLayer(
    id='machguth_massbalance_locations',
    title='Mass balance glacier observation locations 1892-2020',
    description=(
        """Locations used in surface mass balance observations."""
    ),
    tags=[],
    style='labeled_point',
    input=ConfigLayerInput(
        dataset=dataset,
        asset=dataset.assets['only'],
    ),
    steps=[
        ConfigLayerCommandStep(
            args=[
                'ogr2ogr',
                *STANDARD_OGR2OGR_ARGS,
                '-clipdst', project.boundaries['background'].filepath,
                '-makevalid',
                '-s_srs', 'EPSG:4326',
                '-sql', (
                    """'SELECT
                        _ogr_geometry_,
                        fid,
                        glacier_id,
                        glacier_name,
                        glacier_type,
                        glacier_lat,
                        glacier_lon,
                        time_period,
                        sources_data,
                        sources_background,
                        CAST("#_points" AS INTEGER) as "#_points",
                        CAST("#_readings" AS INTEGER) as "#_readings",
                        CAST("#_readings_final" AS INTEGER) as "#_readings_final",
                        finished,
                        comments,
                        label
                    FROM foo'"""
                ),
                '{output_dir}/final.gpkg',
                '{input_dir}/locations.gpkg',
            ],
        ),
    ],
)
