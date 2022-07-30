import arcpy.management as mgmt
from os import path

def pointCloudStats(out_folder, las_dataset, sampling_val, out_name):

    # Create statistics rasters
    # las_file_name = path.basename(las_dataset).split('.')[0]
    print('')
    out_ras = path.join(out_folder, f'{out_name}_PULSE_COUNT.tif')

    print(out_ras)
    mgmt.LasPointStatsAsRaster(
        las_dataset,
        out_ras,
        method='PULSE_COUNT',
        sampling_type='CELLSIZE',
        sampling_value=sampling_val
    )

    # Create las statistics
    print('exporting statistics')
    out_stats = path.join(out_folder, f'{out_name}_stats.csv')
    mgmt.LasDatasetStatistics(
        las_dataset,
        calculation_type='SKIP_EXISTING_STATS',
        out_file=out_stats,
        summary_level='LAS_FILES',
        delimiter='COMMA'
    )