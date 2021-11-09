from pathlib import Path

from qgreenland.constants.project import PROJECT
from qgreenland.util.version import (
    get_build_version,
    version_is_full_release,
)


PACKAGE_DIR = Path(__file__).parent.parent
PROJECT_DIR = PACKAGE_DIR.parent

CONFIG_DIR = PACKAGE_DIR / 'config'
LAYERS_CFG_DIR = CONFIG_DIR / 'layers'

PRIVATE_ARCHIVE_DIR = Path('/private-archive')

FETCH_DATASETS_DIR = Path('/rw/fetch-dataset')

WIP_LAYERS_DIR = Path('/rw/wip-layers')
WIP_PACKAGE_DIR = Path('/rw/wip-package')

RELEASE_LAYERS_DIR = Path('/rw/release-layers')
RELEASE_PACKAGES_DIR = Path('/rw/release-packages')

COMPILE_PACKAGE_DIR = WIP_PACKAGE_DIR / PROJECT

ANCILLARY_DIR = PACKAGE_DIR / 'ancillary'
TEMPLATES_DIR = ANCILLARY_DIR / 'templates'
ASSETS_DIR = PACKAGE_DIR / 'assets'
SCRIPTS_DIR = PROJECT_DIR / 'scripts'

OUTPUT_DIRS = (
    FETCH_DATASETS_DIR,
    WIP_LAYERS_DIR,
    WIP_PACKAGE_DIR,
    RELEASE_LAYERS_DIR,
    RELEASE_PACKAGES_DIR,
)

# TODO: Extract to function in another module to remove constants dependency on
# get_build_version, version_is_full_release
if version_is_full_release(version := get_build_version()):
    VERSIONED_PACKAGE_DIR = RELEASE_PACKAGES_DIR / version
else:
    VERSIONED_PACKAGE_DIR = RELEASE_PACKAGES_DIR / 'dev' / version
