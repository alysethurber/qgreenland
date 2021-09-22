from pathlib import Path
from typing import Any, Dict

import fiona
from pydantic import root_validator, validator

import qgreenland.exceptions as exc
from qgreenland.constants import ASSETS_DIR
from qgreenland.models.base_model import QgrBaseModel


class BoundingBox(QgrBaseModel):
    min_x: float
    min_y: float
    max_x: float
    max_y: float


class ConfigBoundariesInfo(QgrBaseModel):
    # Absolute filepath using `{assets_dir}` slug allows for diffing configs
    # across file systems. Steps often need absolute paths that are
    # filesystem-agnostic.
    filepath: str

    bbox: BoundingBox

    @validator('filepath')
    @classmethod
    def ensure_relative_to_assets(cls, value):
        # TODO: DRY this out? Same validator in assets module.
        full_path = Path(value.format(assets_dir=ASSETS_DIR))
        if not full_path.is_file():
            raise ValueError(f'No file found at {full_path}.')

        return value

    # TODO: Do we need a root validator? A regular validator, even with
    # `pre=True` and `always=True`, resulted in a "field not found" error for
    # "bbox".
    @root_validator(pre=True)
    @classmethod
    def calculate_bbox(cls, values) -> Dict[str, Any]:
        if 'filepath' not in values or not values['filepath']:
            raise RuntimeError('Filepath must be populated.')

        fp = Path(values['filepath'].format(assets_dir=ASSETS_DIR))

        with fiona.open(fp) as ifile:
            features = list(ifile)
            meta = ifile.meta
            bbox = ifile.bounds

        if (feature_count := len(features)) != 1:
            raise exc.QgrInvalidConfigError(
                f'Configured boundary {fp} contains the wrong'
                f' number of features. Expected 1, got {feature_count}.',
            )

        # NOTE: Import inside the method to avoid a cycle. The config subpackage
        # imports from the models subpackage, so the models can't import from
        # config.
        from qgreenland.config.constants import PROJECT_CRS  # noqa
        if (boundary_crs := meta['crs']['init'].upper()) != PROJECT_CRS.upper():
            raise exc.QgrInvalidConfigError(
                f'Expected CRS of boundary file {fp} ({boundary_crs}) to'
                f' match project CRS ({PROJECT_CRS}).',
            )

        return {
            'filepath': values['filepath'],
            'bbox': BoundingBox(
                min_x=bbox[0],
                min_y=bbox[1],
                max_x=bbox[2],
                max_y=bbox[3],
            ),
        }


class ConfigProject(QgrBaseModel):
    crs: str
    boundaries: Dict[str, ConfigBoundariesInfo]
