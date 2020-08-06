import luigi

from qgreenland.tasks.common.fetch import FetchDataFiles
from qgreenland.tasks.common.misc import ExtractNcDataset
from qgreenland.tasks.common.raster import WarpRaster
from qgreenland.util.luigi import LayerPipeline


class VelocityMosaic(LayerPipeline):
    """Dataset VelocityMosaic.

    This is a NetCDF dataproduct with many distinct datasets representing
    distinct measurements.
    """

    extract_dataset = luigi.Parameter()

    def requires(self):
        source = self.cfg['source']

        fetch_data = FetchDataFiles(
            source_cfg=source,
            output_name='velocity_mosaic'
        )  # ->
        extract_nc_dataset = ExtractNcDataset(
            requires_task=fetch_data,
            layer_id=self.layer_id,
            dataset_name=self.extract_dataset
        )  # ->
        return WarpRaster(
            requires_task=extract_nc_dataset,
            layer_id=self.layer_id
        )
