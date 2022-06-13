import pandas as pd
import arcpy

# Modified from d-wasserman
def table_to_data_frame(in_table, input_fields=None, where_clause=None):
    """
    Convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor.
    """
    OIDFieldName = arcpy.Describe(in_table).OIDFieldName

    if input_fields:
        final_fields = [OIDFieldName] + input_fields
    else:
        final_fields = [field.name for field in arcpy.ListFields(in_table)]

    # Create array using search cursor
    data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]

    # Create df
    fc_dataframe = pd.DataFrame(data, columns=final_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=True)

    return fc_dataframe