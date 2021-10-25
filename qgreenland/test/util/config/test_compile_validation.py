import pytest

# TODO: Write tests which exercise the compile_cfg function against directories
# with validation errors, ensuring that the correct errors are raised.
from qgreenland.test.constants import (
    TEST_CONFIG_W_EXTRA_SETTINGS_DIR,
    TEST_CONFIG_W_MISSING_SETTINGS_DIR,
)
from qgreenland.util.config.compile import compile_cfg


def test_missing_settings():
    with pytest.raises(...):
        compile_config(TEST_CONFIG_W_MISSING_SETTINGS_DIR)


def test_extra_settings():
    with pytest.raises(...):
        compile_config(TEST_CONFIG_W_MISSING_EXTRA_DIR)
