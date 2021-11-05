
from qgreenland.config.datasets.geological_map import geological_map as dataset
from qgreenland.config.helpers.steps.compressed_vector import compressed_vector
from qgreenland.config.project import project
from qgreenland.models.config.layer import ConfigLayer, ConfigLayerInput


LAYER_PARAMS = {
    'onshore_planar_geological_map': {
        'title': 'Faults',
        'description': (
            """Onshore faults for the landmass and islands of Greenland."""
        ),
        'style': 'onshore_planar_geological_map',
        'input_filepath': 'data/shape/geology/Greenland_onshore_planar',
        'fn_mask': 'Greenland_onshore_Planar.*',
    },
    'onshore_geological_map': {
        'title': 'Rock types',
        'description': (
            """Geological unit polygon features for the onshore landmass and
            islands of Greenland."""
        ),
        'style': 'geological_map_polygons',
        'input_filepath': 'data/shape/geology/Greenland_onshore',
        'fn_mask': 'Greenland_onshore.*',
    },
    'greenland_ice': {
        'title': 'Ice isopachs',
        'description': (
            """This linear feature class contains onshore ice isopachs for the landmass of Greenland. 
        The isopochs illustrate the variation in ice thickness with a contour interval of 250 metres."""
        ),
        'style': 'Greenland_ice',
        'input_filepath': 'data/shape/base/Greenland_ice',
        'fn_mask': 'Greenland_ice.*',
    },
    'bathymetric_contours': {
        'title': 'Bathymetric contours',
        'description': (
            """This dataset includes linear features that represent bathymetric contours recorded in metres, 
        derived from the International Bathymetric Chart of the Arctic Ocean."""
        ),
        'style': 'bathymetry',
        'input_filepath': 'data/shape/base/bathymetry',
        'fn_mask': 'bathymetry.*',
        'dataset': dataset_geo,
    },
}

def make_layers() -> list[ConfigLayer]:
    return [
        ConfigLayer(
            id=layer_id,
            title=title,
            description=description,
            tags=[],
            style=style,
            input=ConfigLayerInput(
                dataset=dataset,
                asset=dataset.assets['only'],
            ),
            steps=[
                *compressed_vector(
                    input_file='{input_dir}/as_2159.zip',
                    output_file='{output_dir}/final.gpkg',
                    boundary_filepath=project.boundaries['background'].filepath,
                    decompress_step_kwargs={
                        'decompress_contents_mask':
                            params['input_filepath'] + '.*',
                    },
                    vector_filename=params['input_filepath'] + '.shp',
                ),
            ],
        )
        for key, params in _geoological_map_params.items()
    ]
