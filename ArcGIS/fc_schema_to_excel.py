"""
exports feature class field attributes, domains, and first 5 rows of fc into excel file
"""

import arcpy
import pandas as pd
from os import path

def get_geodatabase_path(input_table):
    '''Return the Geodatabase path from the input table or feature class.
    :param input_table: path to the input table or feature class
    '''

    workspace = path.dirname(input_table)
    if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in path.splitext(workspace)]:
        return workspace
    else:
        return path.dirname(workspace)

def schema_to_excel(fc, out_path, file_name):

    database = get_geodatabase_path(fc)
    domain_dict = {d.name: d for d in arcpy.da.ListDomains(database)}
    data = []

    for f in arcpy.ListFields(fc):

        dname = f.domain
        if f.domain in domain_dict.keys():

            if domain_dict[dname].domainType == 'CodedValue':
                dtype = domain_dict[dname].domainType
                dvalue = []
                for k in domain_dict[dname].codedValues.keys():
                    dvalue.append(f'{k}:{domain_dict[dname].codedValues[k]}')

            elif domain_dict[dname].domainType == 'Range':
                dtype = domain_dict[dname].domainType
                for t in domain_dict[dname].range:
                    dvalue.append(t)
            else:
                dvalue = ''
                dtype = ''

        row = {
            'Name':f.name,
            'Alias':f.aliasName,
            'Type':f.type,
            'domain':dname,
            'Domain_type':dtype,
            'Domain_values':dvalue
        }

        data.append(row)

        df = pd.DataFrame.from_records(data)
        df_head = pd.DataFrame.spatial.from_featureclass(fc).head(20)

        s_name = file_name
        with pd.ExcelWriter(path.join(out_path, f'{s_name}.xlsx'), engine="openpyxl") as writer:


            df.to_excel(writer, index=False, sheet_name=s_name)
            df_head.to_excel(writer, index=False, sheet_name=f'sample')

            writer.save()