import qgis.core as qgc

from qgreenland.util.qgis import QgsApplicationContext


if __name__ == '__main__':
    with QgsApplicationContext():
        url = 'crs=EPSG:4326&format=image/png&layers=continents&styles&url=https://demo.mapserver.org/cgi-bin/wms'
        layer = qgc.QgsRasterLayer(url, 'Foo', 'wms')

        if not layer.isValid():
            raise RuntimeError('NO! BAD!')

        project = qgc.QgsProject.instance()
        project.write('/tmp/wms_example.qgs')
        project.addMapLayer(layer)
        project.write()

        print('Done')
