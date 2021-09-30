from typing import Generator, Type

import luigi

from qgreenland.models.config.asset import (
    AnyAsset,
    ConfigDatasetCmrAsset,
    ConfigDatasetHttpAsset,
    ConfigDatasetManualAsset,
    ConfigDatasetOnlineAsset,
    ConfigDatasetRepositoryAsset,
)
from qgreenland.models.config.dataset import ConfigDataset
from qgreenland.models.config.layer import ConfigLayer
from qgreenland.util.config.config import CONFIG
from qgreenland.util.luigi.tasks.fetch import (
    FetchCmrGranule,
    FetchDataFiles,
    FetchLocalDataFiles,
    FetchTask,
)
from qgreenland.util.luigi.tasks.main import ChainableTask, FinalizeTask


# TODO: Make "fetch" tasks into Python "steps"?
ASSET_TYPE_TASKS: dict[Type[AnyAsset], Type[FetchTask]] = {
    ConfigDatasetHttpAsset: FetchDataFiles,
    ConfigDatasetCmrAsset: FetchCmrGranule,
    # TODO: rename `FetchLocalDataFiles`, split in two!
    ConfigDatasetManualAsset: FetchLocalDataFiles,
    ConfigDatasetRepositoryAsset: FetchLocalDataFiles,
}


def _fetch_task(
    dataset_cfg: ConfigDataset,
    asset_cfg: AnyAsset,
) -> FetchTask:
    # TODO: Unit test!
    fetch_task = ASSET_TYPE_TASKS[type(asset_cfg)](
        dataset_id=dataset_cfg.id,
        asset_id=asset_cfg.id,
    )

    return fetch_task


def fetch_task_from_layer(
    layer_cfg: ConfigLayer,
) -> FetchTask:
    # TODO: Unit test!
    dataset_cfg = layer_cfg.input.dataset
    asset_cfg = layer_cfg.input.asset

    return _fetch_task(dataset_cfg, asset_cfg)


def fetch_tasks_from_dataset(
    dataset_cfg: ConfigDataset,
) -> Generator[FetchTask, None, None]:
    # TODO: Unit test!
    for asset_cfg in dataset_cfg.assets.values():
        yield _fetch_task(dataset_cfg, asset_cfg)


# TODO: Rename? generate_layer_pipelines?
# TODO: Accept an optional pattern?
# TODO: Fetch-only boolean option?
def generate_layer_tasks():
    """Generate a list of pre-configured tasks based on layer configuration.

    Instead of calling tasks now, we return a list of callables with the
    arguments already populated.
    """
    tasks: list[luigi.Task] = []

    for layer_cfg in CONFIG.layers.values():
        # Check if it's an online layer; those have no processing pipeline.
        if isinstance(layer_cfg.input.asset, ConfigDatasetOnlineAsset):
            continue

        # Create tasks, making each task dependent on the previous task.
        task = fetch_task_from_layer(layer_cfg)

        # If the layer has no steps, it's just fetched and finalized.
        if layer_cfg.steps:
            for step_number, _ in enumerate(layer_cfg.steps):
                task = ChainableTask(
                    requires_task=task,
                    layer_id=layer_cfg.id,
                    step_number=step_number,
                )

        # We only need the last task in the layer pipeline to run all
        # "required" tasks in a layer pipeline.
        task = FinalizeTask(
            requires_task=task,
            layer_id=layer_cfg.id,
        )

        tasks.append(task)

    return tasks
