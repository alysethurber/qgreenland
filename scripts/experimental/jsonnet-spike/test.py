import json

from compile import JSONNET_DICT, THIS_DIR

OLD_CFG_DIR = THIS_DIR / 'old_cfg'
OLD_CFG = OLD_CFG_DIR / 'config.json'


def test_jsonnet():
    old_config = json.load(open(OLD_CFG, 'r'))

    expected_layer_config = old_config['layers']['background']
    expected_layer_config.pop('steps')

    expected_config = {
        'layers': {'background': expected_layer_config},
        'datasets': {
            'background': old_config['datasets']['background']
        }
    }

    assert expected_config == JSONNET_DICT
