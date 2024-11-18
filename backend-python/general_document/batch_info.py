import shutil
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter, column_index_from_string


# Function to load the Excel template and prepare for modification
def load_template(template_path, new_file_path):
    # Copy the template to a new file
    shutil.copy(template_path, new_file_path)
    # Load the new workbook
    wb = load_workbook(new_file_path)
    return wb


def get_next_column_name(current_column_name):
    # Convert column letter to index
    column_index = column_index_from_string(current_column_name)
    # Increment the index to get the next column
    next_column_index = column_index + 1
    # Convert the new index back to a column letter
    next_column_name = get_column_letter(next_column_index)
    return next_column_name


# Function to copy formatting and insert a new row
def insert_row_with_format(ws, row_to_copy, new_row_idx):
    # Insert a new row
    ws.insert_rows(new_row_idx)
    # Copy the formatting
    for col_idx, cell in enumerate(ws[row_to_copy], start=1):
        new_cell = ws.cell(row=new_row_idx, column=col_idx)
        if cell.has_style:
            new_cell.border = cell.border.copy()
            new_cell.alignment = cell.alignment.copy()


# Function to insert series data starting from row 6
def insert_series_data(wb: Workbook, series_data, start_row=6):
    ws = wb.active
    # un-merge cell
    ws.unmerge_cells('A8:U8')
    ws.unmerge_cells('A9:U9')
    for i, val in enumerate(series_data):           
        new_row = i + start_row
        if i > 0:
            insert_row_with_format(ws, start_row, new_row)
        ws[f"F{new_row}"] = val["colorName"]
        ws[f"G{new_row}"] = val["pairAmount"]
        column_name = "H"
        for j in range(34, 47):
            ws[f"{column_name}{new_row}"] = val[f"size{j}Amount"]
            column_name = get_next_column_name(column_name)
        ws[f"U{new_row}"] = val["batchName"]

    # merge cells
    ws.merge_cells(f'A{6+len(series_data) + 1}:U{6+len(series_data) + 1}')
    ws.merge_cells(f'A{6+len(series_data) + 2}:U{6+len(series_data) + 2}')

# Function to save the workbook after modification
def save_workbook(wb, new_file_path):
    wb.save(new_file_path)


# Main function to generate the Excel file
def generate_excel_file(template_path, new_file_path, data: dict):
    print(f"Generating Excel file")
    # Load template
    wb = load_template(template_path, new_file_path)

    table_data = data["batch_info"]
    insert_series_data(wb, table_data)

    ws = wb.active
    # insert meta data
    brand = '商标：' + data["customer_brand"]
    ws['U4'] = brand
    ws.column_dimensions['U'].width = len(brand) + 10

    ws.merge_cells(f"A6:A{6+len(table_data)-1}")
    ws["A6"] = data["order_rid"]

    ws.merge_cells(f"C6:C{6+len(table_data)-1}")
    ws["C6"] = data["shoe_rid"]

    ws.merge_cells(f"E6:E{6+len(table_data)-1}")
    ws["E6"] = data["customer_product_name"]

    column_name = "H"
    for i in range(0, 13):
        ws[f"{column_name}{5}"] = data["shoe_size_names"][i]["label"]
        column_name = get_next_column_name(column_name)

    # sum up the shoes
    ws[f"G{6+len(table_data)}"] = f"=SUM(G6:G{6+len(table_data)-1})"
    column_name = "H"
    for _ in range(0, 13):
        ws[f"{column_name}{6+len(table_data)}"] = f"=SUM({column_name}6:{column_name}{6+len(table_data)-1})"
        column_name = get_next_column_name(column_name)
    # Save the workbook
    save_workbook(wb, new_file_path)
    print(f"Workbook saved as {new_file_path}")
