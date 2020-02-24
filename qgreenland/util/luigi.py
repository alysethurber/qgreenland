import os

import luigi

from qgreenland.constants import TaskType
from qgreenland.util.misc import get_layer_config


class LayerConfigMixin(luigi.Task):
    layer_name = luigi.Parameter()
    task_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_cfg = get_layer_config(self.layer_name)

    @property
    def short_name(self):
        return self.layer_cfg['short_name']

    @property
    def outdir(self):
        if self.task_type not in TaskType:
            msg = (f"This class defines self.task_type as '{self.task_type}'. "
                   f'Must be one of: {list(TaskType)}.')
            raise RuntimeError(msg)

        if self.task_type is TaskType.FINAL:
            outdir = (f"{TaskType.FINAL.value}/{self.layer_cfg['layer_group']}/"
                      f'{self.short_name}')
        else:
            outdir = f'{self.task_type.value}/{self.short_name}'

        os.makedirs(outdir, exist_ok=True)
        return outdir
