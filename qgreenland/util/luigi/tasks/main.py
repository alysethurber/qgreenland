"""Responsible for task orchestration.

Manages input and output directories and various ways of running pipeline steps.
Doesn't care about what files end up in the output directory, that's the
responsibility of the step configuration.
"""
import copy
import os
import shutil
from pathlib import Path
from typing import List

import luigi

from qgreenland.config import CONFIG
from qgreenland.constants import TaskType
from qgreenland.models.config.step import AnyStep
from qgreenland.runners import step_runner
from qgreenland.util.misc import get_final_layer_dir, get_layer_fp, temporary_path_dir


# TODO: Rename... QgrTask? ChainableLayerTask? ChainableLayerStep?
class ChainableTask(luigi.Task):
    """Define dependencies at instantiation-time.

    Each chainable task is specific to a single step in creation of a single
    layer (for now).

    TODO: Consider multiple inheritance to separate layer/step repsonsibility
    from dependency-specification responsibility?
    """

    requires_task = luigi.Parameter()
    layer_id = luigi.Parameter()
    step_number = luigi.IntParameter()

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'layer_id={self.layer_id},'
            f' step_number={self.step_number})'
        )

    def requires(self):
        """Dynamically specify task this task depends on."""
        return self.requires_task

    @property
    def layer_cfg(self):
        return copy.deepcopy(
            CONFIG.layers[self.layer_id],
        )

    @property
    def step(self):
        return self.layer_cfg.steps[self.step_number]

    @property
    def step_identifier(self):
        """Generate a short string uniquely identifying a step within a layer.

        WARNING: Only uniquely identifies a _step_ in the context of a layer;
        does not uniquely ID a step + layer combination.
        """
        first_part = f'{self.step_number:02}-{self.step.type}'
        last_part = (
            f'-{self.step.args[0]}'
            if self.step.type == 'command'
            else 'TODO'
        )
        return f'{first_part}{last_part}'

    def output(self):
        """Define a directory for the step's behavior to write things into.

        We don't care what those files are or what directory structure lies
        within.

        NOTE: As soon as this directory exists, Luigi will consider this Task
        complete. _Always_ wrap behaviors in a temporary directory for outputs.
        """
        output_dir = (
            Path(TaskType.WIP.value)
            / self.layer_id
            / self.step_identifier
        )
        return luigi.LocalTarget(output_dir)

    def run(self):
        """Execute the step with a temporary directory.

        Enables Luigi to trigger the next job at the right time.

        NOTE: If jobs fail, temporary directory is not cleaned up. The WIP dir
        is ephemeral and will be cleaned up in a more wholesale manner.
        """
        with temporary_path_dir(self.output()) as temp_path:
            step_runner(
                self.step,
                input_dir=self.input().path,
                output_dir=temp_path,
            )


class FinalizeTask(luigi.Task):
    """Allow top-level layer tasks to lookup config from class attr layer_id.

    Also standardizes output directory for top-level layer tasks.

    TODO: Expect a .gpkg or a .tif file in its input directory. If none (or >1?)
    exists, throw an exception so the pipeline developer knows. If one exists,
    create the appropriate type of QGIS Layer.

    TODO: How to handle "extra" layers that aren't in the zip, but are exposed
    for use with plugin? Separate "Final" step? Or make this one handle both
    cases?
    """

    # TODO: DRY
    requires_task = luigi.Parameter()
    layer_id = luigi.Parameter()

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'layer_id={self.layer_id})'
        )

    # TODO: DRY
    @property
    def cfg(self):
        return CONFIG.layers[self.layer_id]

    # TODO: DRY
    def requires(self):
        """Dynamically specify task this task depends on."""
        return self.requires_task

    def output(self):
        return luigi.LocalTarget(get_final_layer_dir(self.cfg))

    def run(self):
        if not os.path.isdir(self.input().path):
            # TODO: better err
            raise RuntimeError(
                'Expected final output to be a directory, not'
                f' {self.input().path}!',
            )

        source_dir = Path(self.input().path)

        # find compatible layer in dir (gpkg | tif)
        input_fp = get_layer_fp(source_dir)

        # TODO: have `temporary_path_dir` return a `Path`.
        with temporary_path_dir(self.output()) as temp_path:
            with open(Path(temp_path) / 'provenance.txt', 'w') as provenance_file:
                provenance_file.write(
                    steps_to_provenance_text(self.cfg.steps),
                )

            output_tmp_fp = Path(temp_path) / f'{self.cfg.id}{input_fp.suffix}'
            shutil.copy2(input_fp, output_tmp_fp)


def steps_to_provenance_text(steps: List[AnyStep]) -> str:
    steps_as_text = [step.provenance for step in steps]

    return '\n\n'.join(steps_as_text)
