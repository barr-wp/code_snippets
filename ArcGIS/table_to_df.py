import pandas as pd
import arcpy

# Modified from d-wasserman
def table_to_data_frame(in_table, input_fields=None, geometry=None, where_clause=None):
    """
    Convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor.

    :param in_table: The feature class, layer, table, or table view
    :param input_fields: A list (or tuple) of field names
    :param geometry: ESRI geometry token
    :param where_clause: An optional SQL expression that limits the records returned
    :return: Dataframe
    """

    OIDFieldName = arcpy.Describe(in_table).OIDFieldName

    if input_fields:
        cursor_fields = [OIDFieldName] + input_fields
    else:
        cursor_fields = [field.name for field in arcpy.ListFields(in_table)]

    if geometry:
        cursor_fields += [geometry]

    # Create array using search cursor
    data = [row for row in arcpy.da.SearchCursor(in_table, cursor_fields, where_clause=where_clause)]

    # Create df
    fc_dataframe = pd.DataFrame(data, columns=cursor_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=True)

    return fc_dataframe