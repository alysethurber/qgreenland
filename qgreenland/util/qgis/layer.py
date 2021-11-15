import functools
from pathlib import Path
from typing import Callable, Union

import qgis.core as qgc
from osgeo import gdal

import qgreenland.exceptions as exc
from qgreenland.models.config.asset import OnlineAsset
from qgreenland.util.layer import (
    get_layer_compile_filepath,
    vector_or_raster,
)
from qgreenland.util.qgis.metadata import add_layer_metadata
from qgreenland.util.tree import LayerNode


def make_map_layer(layer_node: LayerNode) -> qgc.QgsMapLayer:
    layer_path = _layer_path(
        layer_node=layer_node,
    )
    layer_type = vector_or_raster(layer_node)
    if layer_type == 'Vector':
        provider = 'ogr'
        qgs_layer_creator = qgc.QgsVectorLayer
    elif layer_type == 'Raster':
        provider = 'gdal'
        qgs_layer_creator = qgc.QgsRasterLayer

    # For online layers, the provider is specified in the config.
    layer_cfg = layer_node.layer_cfg
    if type(layer_cfg.input.asset) is OnlineAsset:
        provider = layer_cfg.input.asset.provider

    creator = functools.partial(
        qgs_layer_creator,
        str(layer_path),
        layer_cfg.title,
        provider,
    )
    map_layer = _create_layer_with_side_effects(
        creator,
        layer_node=layer_node,
    )

    if not map_layer.isValid():
        raise exc.QgrRuntimeError(
            f'Invalid QgsMapLayer created for layer {layer_cfg.id}',
        )

    add_layer_metadata(map_layer, layer_cfg)

    if style_filepath := layer_cfg.style_filepath:
        _load_qml_style(map_layer, style_filepath)

    return map_layer


def _layer_path(
    layer_node: LayerNode,
) -> Union[Path, str]:
    layer_cfg = layer_node.layer_cfg
    if type(layer_cfg.input.asset) is OnlineAsset:
        return f'{layer_cfg.input.asset.url}'
    else:
        # Give the absolute path to the layer. We think project.addMapLayer()
        # automatically generates the correct relative paths. Using a relative
        # path causes statistics (nodata value, min/max) to not be generated,
        # resulting in rendering a gray rectangle.
        return get_layer_compile_filepath(layer_node)


def _offline_raster_side_effects(
    creator: Callable[..., qgc.QgsRasterLayer],
    *,
    layer_node: LayerNode,
) -> qgc.QgsRasterLayer:
    """Generate raster statistics on disk and in the layer object."""
    layer_path = _layer_path(layer_node)

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


def _create_layer_with_side_effects(
    creator: Callable[..., qgc.QgsMapLayer],
    *,
    layer_node: LayerNode,
) -> qgc.QgsMapLayer:
    """Apply special steps before/after creating a layer."""
    layer_cfg = layer_node.layer_cfg
    layer_type = vector_or_raster(layer_node)

    offline_raster = (
        layer_type == 'Raster'
        and type(layer_cfg.input.asset) is not OnlineAsset
    )

    if offline_raster:
        return _offline_raster_side_effects(creator, layer_node=layer_node)
    else:
        return creator()


def _load_qml_style(map_layer: qgc.QgsMapLayer, style_path: Path) -> None:
    msg, status = map_layer.loadNamedStyle(str(style_path))

    if not status:
        raise RuntimeError(f"Problem loading '{style_path}': '{msg}'")
