"""
Downloads row attachments to folder named after the row's value in a specified cell.
For example all rows with file_id = ABC123 will be downloaded to root\\ABC123
If the root\\ABC123 folder doesn't exist it will be created.
This script will not download files of the same name and path, so updated attachment versions will NOT be downloaded
"""

import smartsheet
import urllib.request
import os


def check_create_dir(dir_path):
    if os.path.exists(dir_path):
        return
    else:
        os.mkdir(dir_path)


def get_collumn_map(sheet):
    column_map = {}
    for column in sheet.columns:
        column_map[column.title] = column.id
    return column_map


def get_cell_by_column_name(sheet, row, column_name):
    column_map = get_collumn_map(sheet)
    column_id = column_map[column_name]
    return row.get_column(column_id)


def get_latest_attch_version(sheet_id, attachment):
    """

    :param sheet_id:
    :param attachment:
    :return: attachment object
    """

    versions = smartsheet_client.Attachments.list_attachment_versions(
        sheet_id,
        attachment.id)

    latest_version = versions.data[0]

    latest_attachment = smartsheet_client.Attachments.get_attachment(
        sheet_id,  # sheet_id
        latest_version.id)

    return latest_attachment


def FileAttachByColAttr(sheet_id, root, file_collumn, file_prefix=''):

    problem_list = []

    # Get the sheet
    sheet = smartsheet_client.Sheets.get_sheet(sheet_id)

    # Get sheet rows
    rows = sheet.rows


    # Iterate over sheet rows
    for r in rows:

        cell = get_cell_by_column_name(sheet, r, file_collumn)
        site_id = cell.display_value

        # Get row attachements
        response = smartsheet_client.Attachments.list_row_attachments(
            sheet_id,  # sheet_id
            r.id,  # row_id
            include_all=True)

        attachments = response.data

        # Iterate over row attachments
        for a in attachments:

            # Get latest version of attachment to download b/c only version ids will return download url
            latest_attachment = get_latest_attch_version(sheet_id, a)

            url = latest_attachment.url

            attr_dir_path = os.path.join(root, file_prefix + site_id)
            check_create_dir(attr_dir_path)

            download_path = os.path.join(attr_dir_path, a.name)

            # Check folder and file exists then download
            try:

                if not os.path.exists(download_path):
                    print(f'DOWNLOAD {download_path} from {url}...')
                    urllib.request.urlretrieve(url, download_path)

                elif os.path.exists(download_path):
                    print(f'SKIP file exists {download_path}')

            except Exception:
                problem_list.append(f'{Exception} {download_path} from {url}')

    print('PROBLEM LIST:')
    for p in problem_list:
        print(p)

# Example
token = 'your api token'

smartsheet_client = smartsheet.Smartsheet(token)
smartsheet_client.assume_user("you@email.com")

smartsheet_client.errors_as_exceptions(True)

FileAttachByColAttr(
    sheet_id=427422951527412,
    root=r'E:\test_ss_to_folder',
    file_collumn='Site ID',
    file_prefix='Site '
)

print('DONE')