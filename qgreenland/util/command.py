import logging
import subprocess
from typing import Sequence

import qgreenland.exceptions as exc
from qgreenland.util.runtime_vars import EvalStr

logger = logging.getLogger('luigi-interface')


def interpolate_args(
    args: Sequence[EvalStr],
    **kwargs,
) -> list[str]:
    """Replace slugs in `args` with keys and values in `kwargs`."""
    return [arg.eval(**kwargs) for arg in args]


def run_qgr_command(cmd_list: list[str]):
    cmd = ['.', 'activate', 'qgreenland-cmd', '&&']
    cmd.extend(cmd_list)

    # Hack. The activation of the conda environment does not work as a list.
    # `subprocess.run(..., shell=True, ...)` enables running commands from
    # strings.
    cmd_str = ' '.join(cmd)

    logger.info('Running command:')
    logger.info(cmd_str)
    result = subprocess.run(
        cmd_str,
        shell=True,
        executable='/bin/bash',
        capture_output=True,
    )

    if result.returncode != 0:
        stdout = str(result.stdout, encoding='utf8')
        stderr = str(result.stderr, encoding='utf8')
        output = f'===STDOUT===\n{stdout}\n\n===STDERRR===\n{stderr}'
        raise exc.QgrSubprocessError(
            f'Subprocess failed with output:\n\n{output}',
        )

    return result
