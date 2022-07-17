import arcpy
import pandas as pd
from os import path

def df_to_features(df, out_fc, geometry_type, geom_field, spatial_reference, field_description=None):
    """
    Dataframe with geometry stored in geojson field to a feature class
    :param out_fc: feature class path
    :param geometry_type: geometry type
    :param geom_field: field in csv with json string
    :param spatial_reference: in spatial reference
    :param field_description: [[Field Name, Field Type, {Field Alias}, {Field Length}, {Default Value} {Field Domain}],...]
    """

    file_path = path.split(path.abspath(out_fc))
    arcpy.CreateFeatureclass_management(
        out_path=file_path[0],
        out_name=file_path[1],
        geometry_type=geometry_type,
        spatial_reference=spatial_reference
    )
    dtype_map = {
        pd.dtype('float64'): 'DOUBLE',
        pd.dtype('bool'): 'SHORT',
        pd.dtype('datetime64'): 'DATE',
        pd.dtype('int64'): 'LONG',
        pd.dtype('object'): 'TEXT'
    }

    # Create field lists for AddFields and InsertCursor
    if field_description:
        iFields = [f[0] for f in field_description]
    else:
        iFields = list(df)
        iFields.remove(geom_field)  # Don't need a field for this. It will be held in SHAPE@
        field_description = [(dField, dtype_map[df.dtypes[dField]]) for dField in iFields]

    arcpy.management.AddFields(out_fc, field_description)

    iFields.append(['SHAPE@']) # Add to write geometry

    with arcpy.da.InsertCursor(out_fc, iFields) as iCursor:
        for index, df_row in df.iterrows():
            iRow = [df_row[f] for f in iFields[:-1]]   # Generate insert row except SHAPE@ token at end of list
            iRow.append(arcpy.AsShape(df_row[geom_field]))
            iCursor.insertRow(iRow)