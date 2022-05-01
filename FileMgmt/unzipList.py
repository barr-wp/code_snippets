"""
Unzips a list of files and writes them to a folder
"""

import zipfile

def unzip_list(file_list, out_dir):
    """

    :param file_list: path containing zip files
    :param out_dir: path to write unzipped files
    :return: None
    """
    error_list = []

    for f in file_list:

        try:
            if f.endswith('.zip'):
                with zipfile.ZipFile(file_list + '\\' + f, 'r') as zipobj:
                    zipobj.extractall(out_dir)

        except zipfile.BadZipFile:
            error_list.append(f)

    print(f'\n{len(error_list)} Errors:')
    print(error_list)
    print('\nCOMPLETE')

    return

# # Example
# import os
#
# in_path = r'C:\in_path'
#
# file_List = os.listdir(in_path)
#
# # Add path to file names
# file_List = [os.path.join(in_path, s) for s in file_List]
#
# for f in file_List:
#     if f.endswith('.zip'):
#         unzip_list(file_list, r'C:\out_path')