import luigi

from qgreenland.util.luigi import LayerTask
from qgreenland.util.misc import run_ogr_command


def interpolate_args(
    args: List[str],
    **kwargs,
) -> List[str]:
    """Replace slugs in `args` with keys and values in `kwargs`."""
    return [arg.format(**kwargs)
            for arg in args]


def command_runner(
    step: Step,
    *,
    input_dir: str,
    output_dir: str,
):
    """Run a shell command in the "gdal" conda environment.

    `kwargs` are string-interpolated for each of the command's arguments.
    """
    # TODO: Some better data structure; this access is confusing.
    command_args = step[0]

    breakpoint()
    interpolate_args(
        command_args,
        input_dir=input_dir,
        output_dir=output_dir,
    )

    # TODO: What's an "ogr" command? Any command will work, this just runs the
    # command in our special "gdal" conda environment. Rename the "gdal"
    # environment to the "command" environment? Rename the function to
    # "run_conda_command"? ¯\_(ツ)_/¯
    run_ogr_command(command_args)
