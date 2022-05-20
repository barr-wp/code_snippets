import arcpy
import pandas as pd
from os import path

def tbl_geojson_to_features(csv, out_path, out_name, geometry_type, geom_field, in_sr, out_sr=None):
    """
    Converts table with geometry stored in geojson field to a feature class
    :param csv: csv table
    :param out_path: feature class path
    :param out_name: feature class name
    :param geometry_type: geometry type
    :param geom_field: field in csv with json string
    :param in_sr: in spatial reference
    :param out_sr: out spatial reference
    """
    out_fc = path.join(out_path, out_name)

    # Used to convert pd dtypes to esri
    # this is not complete - to be updated
    pandas_arc_dtypes = {
        'float64': 'FLOAT',
        'int64': 'LONG',
        'object': 'TEXT'
    }

    # Make the empty fc
    arcpy.CreateFeatureclass_management(
        out_path=out_path,
        out_name=out_name,
        geometry_type=geometry_type,
        spatial_reference=in_sr
    )

    # Add fields

    rb_csv = pd.read_csv(csv)

    # Rename because arc hates hyphens
    for f in list(rb_csv):
        new_c = f.replace('-', '_')
        rb_csv.rename(columns={f: new_c}, inplace=True)

    # List dataframe field and datatypes
    df_fields = zip(list(rb_csv), rb_csv.dtypes)
    esri_f_list = []

    # Create field dcitionary
    # Format as [[Field Name, Field Type, {Field Alias}, {Field Length}, {Default Value} {Field Domain}],...] for AddFields
    for f in df_fields:
        esri_f_list.append([f[0], pandas_arc_dtypes[str(f[1])]])

    arcpy.management.AddFields(out_fc, esri_f_list)

    # Insert rows
    i_fields = list(rb_csv) + ['SHAPE@']
    i_fields.remove(geom_field)  # remove this becasue we will write to geometry SHAPE@ token
                                 # also causes problems with sring field length limits in gdb

    with arcpy.da.InsertCursor(out_fc, i_fields) as iCursor:

        # Iterate through dataframe and insert rows
        for index, df_row in rb_csv.iterrows():
            i_row = []

            # Generate insert row except SHAPE@ token at end of list
            for f in i_fields[:-1]:
                i_row.append(df_row[f])

            # Append geom field
            line = arcpy.AsShape(df_row[geom_field])  # Convert GeoJASON string to shape object
            i_row.append(line)

            # Insert row
            iCursor.insertRow(i_row)

        # if out spatial reference is specified, project it and delete old fc
        if out_sr is not None:
            out_proj = path.join(out_path, 'proj_' + out_name)

            arcpy.Project_management(
                in_dataset=out_fc,
                out_dataset=out_proj,
                out_coor_system=out_sr
            )

            arcpy.Delete_management(out_fc)

# # Eample
# tbl_geojson_to_features(
#     csv=r'C:\Users\you\Downloads\Export_464_188.csv',
#     out_path=r'X:\Maps\data.gdb',
#     out_name='Export_464',
#     geometry_type='POLYLINE',
#     geom_field='geom',
#     in_sr='4326',
#     out_sr='26911'
# )