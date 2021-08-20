package Layers

import "nsidc.org/qgreenland:Datasets"
// local warpAndCut = import "step_templates/warp_and_cut.libsonnet";

layers:{
  background: {
    id: "background",
    title: "Background (500m)",
    hierarchy: ["Basemaps"],
    description: "Stylized shaded-relief map for providing a general sense of geography.",
    show: true,
    input: {
      dataset: Datasets.datasets.background,
      asset: Datasets.datasets.background.assets.high_res,
    },
    steps: [
      #CommandStep & {
        args: [ 
          "unzip",
          "{input_dir}/*.zip",
          "-d",
          "{output_dir}",
        ],
      },
      // ]+
      // warpAndCut.warpAndCut {
      //   inputFile: "{input_dir}/NE2_HR_LC_SR_W/NE2_HR_LC_SR_W.tif",
      //   outputFile: "{output_dir}/warped_and_cut.tif",
      //   crs: "EPSG:3413",
      //   targetExtent: "-5774572.727595 -5774572.727595 5774572.727595 5774572.727595",
      //   cutFilePath: "{assets_dir}/latitude_shape_40_degrees.geojson",
      // }.steps+
      // [
      #CommandStep & {
        args: [ 
          "cp",
          "{input_dir}/warped_and_cut.tif",
          "{output_dir}/overviews.tif",
          "&&",
          "gdaladdo",
          "-r",
          "average",
          "{output_dir}/overviews.tif",
          "2",
          "4",
          "8",
          "16",
        ],
      },
    ],
  }
}
