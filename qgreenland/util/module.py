import importlib
import inspect
from pathlib import Path
from types import ModuleType
from typing import Type, TypeVar


def module_from_path(module_path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(
        # TODO: Maybe `split` on `os.path.sep`?
        f'_generated_module.{module_path.stem}',
        str(module_path),
    )
    if not module_spec:
        raise RuntimeError(f'No module found at {module_path}')

    module = importlib.util.module_from_spec(module_spec)

    # https://github.com/python/typeshed/issues/2793
    if not isinstance(module_spec.loader, importlib.abc.Loader):
        raise RuntimeError(
            f'Module {module_path} failed to load:'
            ' (module_spec.loader=None)',
        )
    # TODO: Put a syntax error or runtime error (1/0) in the module. What
    # happens? Unit test this with a tempfile?
    module_spec.loader.exec_module(module)

    return module


T = TypeVar('T')
# TODO: Cache!
def load_objects_from_paths_by_class(
    module_paths: list[Path],
    *,
    target_class: Type[T],
) -> list[T]:
    """Return all objects of class `model_class` in `module_paths`."""
    found_models = []
    for module_path in module_paths:
        module = module_from_path(module_path)

        # TODO: Validate `id`s of each model, if present, are unique? Do that
        # afterwards? Probably after.

        models = _find_in_module_by_class(module, target_class=target_class)
        found_models.extend(models)

    return found_models


def _find_in_module_by_class(
    module: ModuleType,
    target_class: Type[T],
) -> list[T]:
    """Find all objects of class `model_class` among `module` members."""
    module_members = inspect.getmembers(module)
    return [
        m[1] for m in module_members
        if isinstance(m[1], target_class)
    ]
