# TODO: DELETE ME
from qgreenland.models.config.step import AnyStep, CommandStep


def compress_raster(
    *,
    input_file: str,
    output_file: str,
) -> list[AnyStep]:
    predictor_value = 3 if dtype_is_float else 2

    return [CommandStep(
        args=[
            'gdal_translate',
            '-co', 'COMPRESS=DEFLATE',
            '-co', f'PREDICTOR={predictor_value}',
            # TODO: `-co TILED=yes`
            input_file,
            output_file,
        ],
    )]
