import os
import shutil

from openpyxl import load_workbook
from openpyxl.styles import Border, Side
from openpyxl.utils import column_index_from_string, get_column_letter


# Function to load the Excel template and prepare for modification
def load_template(template_path, new_file_path):
    # Copy the template to a new file
    shutil.copy(template_path, new_file_path)
    # Load the new workbook
    wb = load_workbook(new_file_path)
    ws = wb.active
    return wb, ws
def add_borders(ws, start_cell, end_cell):
    thin = Side(border_style="thin", color="000000")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Iterate over the range and apply borders
    for row in ws[start_cell:end_cell]:
        for cell in row:
            cell.border = border

# Merge and add borders
def merge_cells(ws, row):
    ws.merge_cells(f"A{row+1}:C{row+1}")
    ws.merge_cells(f"B{row+2}:F{row+2}")
    ws.merge_cells(f"B{row+3}:F{row+3}")
    ws.merge_cells(f"B{row+4}:F{row+4}")
    ws.merge_cells(f"G{row+4}:S{row+4}")
    ws.merge_cells(f"A3:A{row}")
    add_borders(ws, f"A3", f"S{row+1}")
# Function to insert series data starting from row 4
def insert_series_data(ws, series_data, start_row=6):
    required_rows = 5  # Minimum rows to keep
    row = start_row - 1  # To calculate the last row after loop

    for i, item in enumerate(series_data):
        row = start_row + i
        print(f"Inserting series data into row {row}")
        ws[f"B{row}"] = i + 1
        ws[f"C{row}"] = item.get("物品名称", "")
        # insert shoe size names
        ws[f"E{row}"] = item.get("34", "")
        ws[f"F{row}"] = item.get("35", "")
        ws[f"G{row}"] = item.get("36", "")
        ws[f"H{row}"] = item.get("37", "")
        ws[f"I{row}"] = item.get("38", "")
        ws[f"J{row}"] = item.get("39", "")
        ws[f"K{row}"] = item.get("40", "")
        ws[f"L{row}"] = item.get("41", "")
        ws[f"M{row}"] = item.get("42", "")
        ws[f"N{row}"] = item.get("43", "")
        ws[f"O{row}"] = item.get("44", "")
        ws[f"P{row}"] = item.get("45", "")
        ws[f"Q{row}"] = item.get("46", "")
        ws[f"R{row}"] = item.get("合计", "")
        ws[f"S{row}"] = item.get("备注", "")

    # Add empty rows if seriesData length < required_rows
    for i in range(len(series_data), required_rows):
        row = start_row + i
        print(f"Adding empty row at {row}")
        ws[f"B{row}"] = i + 1  # Continue numbering for empty rows

    return row

# Function to save the workbook after modification
def save_workbook(wb, new_file_path):
    wb.save(new_file_path)


def get_next_column_name(current_column_name):
    # Convert column letter to index
    column_index = column_index_from_string(current_column_name)
    # Increment the index to get the next column
    next_column_index = column_index + 1
    # Convert the new index back to a column letter
    next_column_name = get_column_letter(next_column_index)
    return next_column_name

# Main function to generate the Excel file
def generate_size_excel_file(template_path, new_file_path, order_data: dict):
    print(f"Generating Excel file for order {order_data.get('订单信息', '')}")
    print(order_data)
    # Load template
    wb, ws = load_template(template_path, new_file_path)
    
    # Insert order details into specific cells
    ws["D2"] = order_data.get("订单信息", "")
    ws["B2"] = order_data.get("供应商", "")
    ws["L2"] = order_data.get("日期", "")

    # Insert shoe size names
    column = "E"
    shoe_size_names = order_data.get("shoe_size_names", "")
    for obj in shoe_size_names:
        ws[f"{column}4"] = obj["label"]
        column = get_next_column_name(column)
    
    # Insert series data from row 4 to 9
    row = insert_series_data(ws, order_data.get("seriesData", []))
    ws[f"A{row+1}"] = "合计"
    ws[f"R{row+1}"] = order_data.get("合计", "")
    ws[f"S{row+1}"] = order_data.get("备注", "")
    ws[f"A{row+2}"] = "环境要求:"
    ws[f"A{row+3}"] = "发货地址:"
    ws[f"A{row+4}"] = "交货期限:"
    ws[f"B{row+2}"] = order_data.get("环保要求", "")
    ws[f"B{row+3}"] = order_data.get("发货地址", "")
    ws[f"B{row+4}"] = order_data.get("交货期限", "")
    ws[f"G{row+4}"] = "如有特殊情况提前5天反馈，无故延期有贵公司承担后续责任。"
    ws[f"A{row+5}"] = "制表:"
    ws[f"G{row+5}"] = "审核:"

    merge_cells(ws, row)
    # Save the workbook
    save_workbook(wb, new_file_path)
    
    print(f"Workbook saved as {new_file_path}")
template_path = "D:/catSupermarket/jiancheng/backend-python/general_document/标准采购订单尺码版.xlsx"
new_file_path = "D:/catSupermarket/jiancheng/backend-python/general_document/size_test.xlsx"
def test_generate_excel_file():
    # Check if the template file exists
    if not os.path.exists(template_path):
        print(f"Template file '{template_path}' does not exist. Create a blank Excel file with this name for testing.")
        return

    # Call the function to generate the Excel file
    generate_size_excel_file(template_path, new_file_path, order_data)
    print("Test completed successfully. Check the generated Excel file.")
order_data = {
    "订单信息": "订单编号12345",
    "供应商": "供应商A",
    "日期": "2024-11-19",
    "seriesData": [
        {"物品名称": "商品1", "34": 10, "35": 20, "36": 30, "37": 40, "38": 50, "39": 60, "40": 70, "41": 80, "42": 90, "43": 100, "44": 110, "45": 120, "46": 130, "合计": 700, "备注": "无"},
        {"物品名称": "商品2", "34": 15, "35": 25, "36": 35, "37": 45, "38": 55, "39": 65, "40": 75, "41": 85, "42": 95, "43": 105, "44": 115, "45": 125, "46": 135, "合计": 800, "备注": "无"},
    ],
    "合计": 1500,
    "备注": "测试备注",
    "环保要求": "符合环保标准",
    "发货地址": "测试地址",
    "交货期限": "2024-12-01",
}