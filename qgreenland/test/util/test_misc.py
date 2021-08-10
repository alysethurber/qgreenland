from pathlib import Path

from qgreenland.constants import TaskType
from qgreenland.test.fixtures import (
    online_layer_cfg,  # noqa: F401
    raster_layer_cfg,  # noqa: F401
)
from qgreenland.util import misc


def test_final_layer_dir(raster_layer_cfg):  # noqa: F811
    expected = (
        Path(TaskType.FINAL.value)
        / 'group'
        / 'subgroup'
        / 'Example raster'
    )

    actual = misc.get_final_layer_dir(raster_layer_cfg)

    assert expected == actual


def test_vector_or_raster_gdal_remote(online_layer_cfg):  # noqa: F811
    assert misc.vector_or_raster(online_layer_cfg) == 'Raster'
