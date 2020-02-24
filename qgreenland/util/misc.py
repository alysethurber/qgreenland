import os
import shutil
import time
from contextlib import contextmanager

from qgreenland.constants import (CONFIG,
                                  DATA_RELEASE_DIR,
                                  REQUEST_TIMEOUT,
                                  TaskType,
                                  WIP_DIR,
                                  ZIP_TRIGGERFILE)
from qgreenland.util.edl import create_earthdata_authenticated_session


def fetch_file(url):
    # TODO: Share the session across requests somehow?
    s = create_earthdata_authenticated_session(hosts=[url])

    return s.get(url, timeout=REQUEST_TIMEOUT)


@contextmanager
def temporary_path_dir(target):
    with target.temporary_path() as p:
        try:
            os.makedirs(p, exist_ok=True)
            yield p
        finally:
            pass
    return


def _rmtree(directory, *, retries=3):
    """Add robustness to shutil.rmtree.

    Retries in case of intermittent issues, e.g. with network storage.
    """
    if os.path.isdir(directory):
        for i in range(retries):
            try:
                shutil.rmtree(directory)
                return
            except OSError as e:
                print(f'WARNING: shutil.rmtee failed for path: {directory}')
                print(f'Exception: {e}')
                print(f'Retrying in {i} seconds...')
                time.sleep(i)

        # Allow caller to receive exceptions raised on the final try
        shutil.rmtree(directory)


def cleanup_intermediate_dirs(delete_fetch_dir=False):
    """Delete all intermediate data, except maybe 'fetch' dir."""
    if delete_fetch_dir:
        _rmtree(WIP_DIR)
        return

    if os.path.isfile(ZIP_TRIGGERFILE):
        os.remove(ZIP_TRIGGERFILE)

    for task_type in TaskType:
        if task_type != TaskType.FETCH:
            _rmtree(task_type.value)

    if os.path.isdir(WIP_DIR):
        for x in os.listdir(WIP_DIR):
            if x.startswith('tmp'):
                _rmtree(x)


def cleanup_output_dirs(delete_fetch_dir=False):
    """Delete all output dirs (intermediate and release).

    Defaults to leaving only the 'fetch' dir in place.
    """
    cleanup_intermediate_dirs(delete_fetch_dir=delete_fetch_dir)
    if os.path.isdir(DATA_RELEASE_DIR):
        for directory in os.listdir(DATA_RELEASE_DIR):
            _rmtree(directory)


def get_layer_config(layername=None):
    config = CONFIG['layers']

    if not layername:
        return config

    try:
        return config[layername]
    except KeyError:
        raise NotImplementedError(
            f"Configuration for layer '{layername}' not found."
        )


def get_layer_fs_path(layer_name, layer_cfg):
    layer_group_list = layer_cfg.get('path', '').split('/')

    return os.path.join(TaskType.FINAL.value,
                        *layer_group_list,
                        layer_name,
                        f'{layer_name}.{layer_cfg["file_type"]}')
