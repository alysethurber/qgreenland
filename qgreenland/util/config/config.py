from functools import cache
from pathlib import Path
from typing import Optional

from qgreenland import exceptions as exc
from qgreenland.models.config import Config
from qgreenland.util.config.compile import compile_cfg


# Figure out the config dir locally to avoid importing anything unnecessary
THIS_DIR = Path(__file__).resolve().parent
CONFIG_DIR = THIS_DIR.parent.parent / 'config'
_CONFIG: Optional[Config] = None


def init_config(
    pattern: Optional[str] = None,
) -> None:
    global _CONFIG

    if _CONFIG is not None:
        raise RuntimeError(
            'Config already initialized. Config can only be initialized once!',
        )

    _CONFIG = compile_cfg(
        CONFIG_DIR.resolve(),
        pattern=pattern,
    )

    if not _CONFIG.layers:
        raise exc.QgrNoLayersFoundError(
            f'No layers found matching pattern "{pattern}".',
        )


@cache
def get_config() -> Config:
    if _CONFIG is None:
        raise RuntimeError('Config not initialized. Run `init_config` first!')

    return _CONFIG
