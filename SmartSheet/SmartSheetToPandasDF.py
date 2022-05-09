import smartsheet
import pandas as pd

token = 'your api token'

smartsheet_client = smartsheet.Smartsheet(token)
smartsheet_client.assume_user("you@email.com")

smartsheet_client.errors_as_exceptions(True)


def simple_sheet_to_dataframe(sheet):
    col_names = [col.title for col in sheet.columns]
    rows = []
    for row in sheet.rows:
        cells = []
        for cell in row.cells:
            cells.append(cell.value)
        rows.append(cells)
    data_frame = pd.DataFrame(rows, columns=col_names)

    return data_frame