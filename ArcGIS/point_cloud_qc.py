import arcpy.management as mgmt
from os import path

def pointCloudStats(out_folder, las_dataset, sampling_val, count_limit):

    # Create statistics rasters
    las_file_name = path.basename(las_dataset).split('.')[0]
    print('')
    out_ras = path.join(out_folder, f'{las_file_name}_PULSE_COUNT.tif')
    print(out_ras)
    mgmt.LasPointStatsAsRaster(
        las_dataset,
        out_ras,
        method='PULSE_COUNT',
        sampling_type='CELLSIZE',
        sampling_value=sampling_val
    )

    low = ExtractByAttributes(out_ras, f"Value < {count_limit}")
    low.save(path.join(out_folder, f'{las_file_name}_POINT_COUNT_{count_limit}.tif'))
    del(low)


    # Create las statistics
    print('exporting statistics')
    out_stats = path.join(out_folder, f'{las_file_name}_stats.csv')
    mgmt.LasDatasetStatistics(
        las_dataset,
        calculation_type='SKIP_EXISTING_STATS',
        out_file=out_stats,
        summary_level='LAS_FILES',
        delimiter='COMMA'
    )