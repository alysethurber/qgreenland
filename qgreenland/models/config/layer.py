from typing import List, Optional

from pydantic import Field

from qgreenland.models.config.dataset import AnyAsset, ConfigDataset
from qgreenland.models.config.step import ConfigLayerStep
from qgreenland.models.immutable_model import ImmutableBaseModel


class ConfigLayerInput(ImmutableBaseModel):
    # TODO: just maintain ids here?
    dataset: ConfigDataset
    asset: AnyAsset


class ConfigLayer(ImmutableBaseModel):
    id: str

    # The layer name in QGIS layers panel:
    title: str

    # Descriptive text:
    description: str = Field(..., min_length=1)

    hierarchy: List[str]
    # in_package: bool

    # Is this layer initially "checked" as visible in QGIS?:
    show: bool = False

    # Which style (.qml) file to use for this layer?
    style: Optional[str] = Field(None, min_length=1)

    input: ConfigLayerInput

    steps: List[ConfigLayerStep]
