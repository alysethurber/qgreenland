import qgreenland.config.datasets.coastlines as dataset
from qgreenland.config.helpers.steps.compressed_vector import compressed_vector
from qgreenland.models.config.layer import ConfigLayer, ConfigLayerInput


bas_greenland_coastlines = ConfigLayer(
    id='bas_greenland_coastlines',
    title='Greenland coastlines 2017',
    description=(
        """This layer should be used as the 'reference coastline' for
        Greenland."""
    ),
    tags=[],
    show=True,
    style='greenland_coastline',
    input=ConfigLayerInput(
        dataset=dataset.bas_coastlines,
        asset=dataset.bas_coastlines.assets['only'],
    ),
    steps=[
        *compressed_vector(
            input_file='{input_dir}/Greenland_coast.zip',
            output_file='{output_dir}/greenland_coastline.gpkg',
        ),
    ],
)

coastlines = ConfigLayer(
    id='coastlines',
    title='Global coastlines',
    description=(
        """Note that the 'Greenland coastlines 2017' layer is preferred for
        Greenland."""
    ),
    tags=[],
    style='coastline-IHOECDIS',
    input=ConfigLayerInput(
        dataset=dataset.coastlines,
        asset=dataset.coastlines.assets['only'],
    ),
    steps=[
        *compressed_vector(
            input_file='{input_dir}/ne_10m_coastline.zip',
            output_file='{output_dir}/global_coastline.gpkg',
        ),
    ],
)
