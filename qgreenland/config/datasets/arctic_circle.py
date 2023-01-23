from qgreenland.models.config.asset import RepositoryAsset
from qgreenland.models.config.dataset import Dataset

arctic_circle = Dataset(
    id="arctic_circle",
    assets=[
        RepositoryAsset(
            id="only",
            filepath="{assets_dir}/arctic_circle.geojson",
        ),
    ],
    metadata={
        "title": "Arctic Circle (66° 34' North)",
        "abstract": ("""Arctic Circle."""),
        "citation": {
            "text": (
                """Generated by QGreenland based on the definition of the Arctic
                Circle given by
                https://nsidc.org/cryosphere/arctic-meteorology/arctic.html"""
            ),
            "url": "https://nsidc.org/cryosphere/arctic-meteorology/arctic.html",
        },
    },
)
