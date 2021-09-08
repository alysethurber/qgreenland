import csv
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from qgreenland.util.config import export_config


@patch(
    'qgreenland.util.config.vector_or_raster',
    new=MagicMock(return_value='Raster'),
)
@patch(
    'qgreenland.util.config.get_final_layer_filepath',
    new=MagicMock(return_value=Path('/tmp')),
)
@patch(
    'qgreenland.util.config.directory_size_bytes',
    new=MagicMock(return_value=0),
)
def test_export_config(full_cfg):
    common = {
        'Data Source Abstract': 'Example abstract',
        'Data Source Citation': 'NSIDC 2020',
        'Data Source Citation URL': 'https://nsidc.org',
        'Data Source Title': 'Example Dataset',
        'Group': 'Group',
        'Layer Description': 'Example layer description',
        'Layer Size': '0 Bytes',
        'Layer Size Bytes': '0',
        'Subgroup': 'Subgroup',
    }
    with tempfile.NamedTemporaryFile('r') as tf:
        export_config(
            full_cfg,
            output_path=Path(tf.name),
        )

        actual = list(csv.DictReader(tf))

    expected = [
        {
            **common,
            'Layer Title': 'Example online',
            'Vector or Raster': 'Online',
        },
        {
            **common,
            'Layer Title': 'Example raster',
            'Vector or Raster': 'Raster',
        },
    ]
    assert actual == expected
