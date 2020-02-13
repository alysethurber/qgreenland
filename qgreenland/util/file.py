import os
import shutil
from contextlib import contextmanager

import yaml

from qgreenland.constants import (DATA_DIR,
                                  DATA_RELEASE_DIR,
                                  THIS_DIR,
                                  TaskType,
                                  ZIP_TRIGGERFILE)


@contextmanager
def temporary_path_dir(target):
    with target.temporary_path() as p:
        try:
            os.makedirs(p, exist_ok=True)
            yield p
        finally:
            pass
    return


def cleanup_output_dirs(delete_fetch_dir=False):
    """Delete output dirs.

    $DATA_DIR/{wip,qgreenland,release,tmp*,READY_TO_ZIP}
    """
    dirs_to_delete = []

    for task_type in TaskType:
        if task_type != TaskType.FETCH or delete_fetch_dir:
            dirs_to_delete.append(
                os.path.join(DATA_DIR, task_type.value)
            )

    dirs_to_delete.append(DATA_RELEASE_DIR)
    dirs_to_delete.extend(
        [os.path.join(DATA_DIR, x)
         for x in os.listdir(DATA_DIR)
         if x.startswith('tmp')]
    )

    if os.path.isfile(ZIP_TRIGGERFILE):
        os.remove(ZIP_TRIGGERFILE)

    for d in dirs_to_delete:
        if os.path.isdir(d):
            shutil.rmtree(d)


def load_layer_config(layername=None):
    LAYERS_CONFIG = os.path.join(THIS_DIR, 'layers.yml')
    with open(LAYERS_CONFIG, 'r') as f:
        config = yaml.safe_load(f)

    if not layername:
        return config

    # TODO: Add error handling
    try:
        return config[layername]
    except KeyError:
        raise NotImplementedError(
            f"Configuration for layer '{layername}' not found."
        )
