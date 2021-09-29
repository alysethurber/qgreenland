import subprocess

import click

from qgreenland.constants import (
    INPUT_DIR,
    RELEASES_DIR,
    TaskType,
)
from qgreenland.util.cli.validate import (
    BOOLEAN_CHOICE,
    validate_ambiguous_command,
    validate_boolean_choice,
)


def _print_and_run(cmd, *, dry_run):
    print(cmd)
    if not dry_run:
        return subprocess.run(
            cmd,
            shell=True,
            check=True,
            executable='/bin/bash',  # /bin/sh doesn't support brace expansion
        )


@click.command()
@click.option('dry_run', '--dry-run', '-d',
              help="Print commands, but don't actually delete anything.",
              is_flag=True)
@click.option('delete_inputs_by_pattern', '--delete-inputs-by-pattern', '-i',
              help=(
                  'Bash glob/brace pattern used to delete input datasources by'
                  ' `<dataset_id>.<source_id>`'
              ),
              multiple=True)
@click.option('delete_wips_by_pattern', '--delete-wips-by-pattern', '-w',
              help=(
                  'Pattern used to delete WIP layers by layer ID'
              ), multiple=True)
@click.option('delete_all_input', '--delete-all-input', '-I',
              help=(
                  'Delete _ALL_ input-cached layers, ignoring LAYER_ID_PATTERN'
              ),
              type=BOOLEAN_CHOICE, callback=validate_boolean_choice,
              default='False', show_default=True)
@click.option('delete_all_wip', '--delete-all-wip', '-W',
              help=(
                  'Delete _ALL_ WIP layers, ignoring LAYER_ID_PATTERN'
              ),
              type=BOOLEAN_CHOICE, callback=validate_boolean_choice,
              default='False', show_default=True)
@click.option('delete_compiled', '--delete-compiled', '-C',
              help=(
                  'Delete compiled (but not zipped) QGreenland datapackage'
              ),
              type=BOOLEAN_CHOICE, callback=validate_boolean_choice,
              default='True', show_default=True)
# TODO: delete_all_wip_tmp: Deletes dirs like `transform-luigi-tmp-4765361527/`
#       from wip
# TODO: delete_all_dev_releases?
@click.option('delete_all_releases', '--delete-all-releases', '-R',
              help=(
                  'Delete all zipped QGreenland releases'
              ),
              type=BOOLEAN_CHOICE, callback=validate_boolean_choice,
              default='False', show_default=True)
# NOTE: Complexity check (C901) is disabled because this function is just a big
#       set of switches by design!
def cleanup(**kwargs):  # noqa: C901
    """Clean up input, WIP, and/or output data created by QGreenland.

    By default, clean up the compiled (but not zipped) datapackage.
    """
    validate_ambiguous_command(kwargs)

    if kwargs['dry_run']:
        print('WARNING: In DRY RUN mode. Nothing will be deleted.')
        print()

    if wip_patterns := kwargs['delete_wips_by_pattern']:
        for p in wip_patterns:
            _print_and_run(
                f'rm -rf {TaskType.WIP.value}/{p}',
                dry_run=kwargs['dry_run'],
            )
    if inp_patterns := kwargs['delete_inputs_by_pattern']:
        for p in inp_patterns:
            _print_and_run(
                f'rm -rf {INPUT_DIR}/{p}',
                dry_run=kwargs['dry_run'],
            )

    if kwargs['delete_all_input']:
        _print_and_run(
            f'rm -rf {INPUT_DIR}/*',
            dry_run=kwargs['dry_run'],
        )

    if kwargs['delete_all_wip']:
        _print_and_run(
            f'rm -rf {TaskType.WIP.value}/*',
            dry_run=kwargs['dry_run'],
        )

    if kwargs['delete_compiled']:
        _print_and_run(
            f'rm -rf {TaskType.FINAL.value}/*',
            dry_run=kwargs['dry_run'],
        )

    if kwargs['delete_all_releases']:
        _print_and_run(
            f'rm -rf {RELEASES_DIR}/*',
            dry_run=kwargs['dry_run'],
        )


if __name__ == '__main__':
    cleanup()
