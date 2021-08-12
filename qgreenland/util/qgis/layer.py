import functools
import os
from pathlib import Path
from typing import Callable, Union

import qgis.core as qgc
from osgeo import gdal

import qgreenland.exceptions as exc
from qgreenland.constants import ASSETS_DIR
from qgreenland.models.config.dataset import ConfigDatasetOnlineAsset
from qgreenland.models.config.layer import ConfigLayer
from qgreenland.util.misc import (
    get_final_layer_filepath,
    vector_or_raster,
)
from qgreenland.util.qgis.metadata import add_layer_metadata


def make_map_layer(layer_cfg: ConfigLayer) -> qgc.QgsMapLayer:
    layer_path = _layer_path(layer_cfg)
    layer_type = vector_or_raster(layer_cfg)
    if layer_type == 'Vector':
        provider = 'ogr'
        qgs_layer_creator = qgc.QgsVectorLayer
    elif layer_type == 'Raster':
        provider = 'gdal'
        qgs_layer_creator = qgc.QgsRasterLayer

    # For online layers, the provider is specified in the config.
    if type(layer_cfg.input.asset) is ConfigDatasetOnlineAsset:
        provider = layer_cfg.input.asset.provider

    creator = functools.partial(
        qgs_layer_creator,
        str(layer_path),
        layer_cfg.title,
        provider,
    )
    map_layer = _create_layer_with_side_effects(
        creator,
        layer_cfg=layer_cfg,
    )

    if not map_layer.isValid():
        raise exc.QgrRuntimeError(
            f'Invalid QgsMapLayer created for layer {layer_cfg.id}'
        )

    add_layer_metadata(map_layer, layer_cfg)

    if style := layer_cfg.style:
        _load_qml_style(map_layer, style)

    return map_layer


def _layer_path(layer_cfg: ConfigLayer) -> Union[Path, str]:
    if type(layer_cfg.input.asset) is ConfigDatasetOnlineAsset:
        return f'{layer_cfg.input.asset.url}'
    else:
        # Give the absolute path to the layer. We think project.addMapLayer()
        # automatically generates the correct relative paths. Using a relative
        # path causes statistics (nodata value, min/max) to not be generated,
        # resulting in rendering a gray rectangle.
        return get_final_layer_filepath(layer_cfg)


def _create_layer_with_side_effects(
    creator: Callable[..., qgc.QgsMapLayer],
    *,
    layer_cfg: ConfigLayer,
) -> qgc.QgsMapLayer:
    """Apply special steps before/after creating a layer."""
    layer_path = _layer_path(layer_cfg)
    layer_type = vector_or_raster(layer_cfg)

    if (
        layer_type == 'Vector':
        or type(layer_cfg.input.asset) is ConfigDatasetOnlineAsset
    ):
        map_layer = creator()

    elif layer_type == 'Raster':
        # Create .aux.xml metadatafile with raster band statistics; useful
        # for styling and accurate min/max/stdev/mean in QGIS layer info
        # panel
        gdal.Info(str(layer_path), stats=True)

        map_layer = creator()

        # Set the min/max render accuracy to 'Exact'. Usually qgis estimates
        # statistics for e.g., generating the default colormap.
        mmo = map_layer.renderer().minMaxOrigin()
        mmo.setStatAccuracy(0)  # 0 == 'Exact'
        map_layer.renderer().setMinMaxOrigin(mmo)

    return map_layer


def _load_qml_style(map_layer: qgc.QgsMapLayer, style_name: str) -> None:
    style_path = os.path.join(ASSETS_DIR, 'styles', style_name + '.qml')
    # If you pass a path to nothing, it will silently fail
    if not os.path.isfile(style_path):
        raise RuntimeError(f"Style '{style_path}' not found.")

    msg, status = map_layer.loadNamedStyle(style_path)

    if not status:
        raise RuntimeError(f"Problem loading '{style_path}': '{msg}'")
