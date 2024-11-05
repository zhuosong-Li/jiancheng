import * as XLSX from 'xlsx';
import axios from 'axios';
import { saveAs } from 'file-saver';
import app from '@/main';

export const productionLines = {
    "cutting": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17],
    "preSewing": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17],
    "sewing": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17],
    "molding": [1, 2, 3, 5],
}

export const outsourceOutboundStatus = ["材料出库", "外包生产中", "成品入库", "外包结束"]
export const outsourceReadOnlyStatus = ["已提交", "材料出库", "外包生产中", "成品入库", "外包结束"]
export const outsourceEditStatus = ["未提交", "被驳回", "已审批"]

export const getShoeSizesName = async (orderShoeId) => {
    let params = { "orderShoeId": orderShoeId }
    let response = await axios.get(`${app.config.globalProperties.$apiBaseUrl}/batchtype/getorderbatchtype`, { params })
    return response.data
}

export const handleRowClick = (row) => {
    let url = ""
    const queryString = new URLSearchParams(row).toString();
    if (row.statusId === 20) {
        url = `${window.location.origin}/fabriccutting/pricereport?${queryString}`;
    } else if (row.statusId === 23) {
        url = `${window.location.origin}/fabriccutting/ordershoelist?${queryString}`;
    }
    if (url) {
        window.open(url, '_blank');
    }
}


export function exportTableToExcel(data, columns, filename = 'table.xlsx') {
    const headers = columns.map(col => col.label);
    const keys = columns.map(col => col.prop);
    const formattedData = data.map(row => {
        const formattedRow = {};
        keys.forEach(key => {
            formattedRow[key] = row[key];
        });
        return formattedRow;
    });
    const ws = XLSX.utils.json_to_sheet(formattedData, { header: keys });
    XLSX.utils.sheet_add_aoa(ws, [headers], { origin: 'A1' });
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    saveAs(new Blob([wbout], { type: 'application/octet-stream' }), filename);
}

export function shoeBatchInfoTableSpanMethod(tableData) {
    return function spanMethod({ row, column, rowIndex, columnIndex }) {
        // Merging 'colorName' and 'totalAmount' columns
        if (columnIndex === 0 || columnIndex === 1) { // colorName and totalAmount columns
            const currentColor = tableData[rowIndex].colorName;

            // Skip rows already merged
            if (rowIndex > 0 && tableData[rowIndex - 1].colorName === currentColor) {
                return [0, 0]; // Skip this cell
            }

            // Calculate the rowspan for the current 'colorName'
            let rowspan = 1;
            for (let i = rowIndex + 1; i < tableData.length; i++) {
                if (tableData[i].colorName === currentColor) {
                    rowspan++;
                } else {
                    break;
                }
            }

            return [rowspan, 1]; // Set the rowspan for merging, and colspan = 1
        }
    }
}

export function checkProductionStatus(array) {
    let result = -1
    if (array.includes("18")) {
        result = 0
    }
    else if (array.includes("23")) {
        result = 1
    }
    else if (array.includes("24")) {
        result = 2
    }
    else if (array.includes("30")) {
        result = 3
    }
    else if (array.includes("31")) {
        result = 4
    }
    else if (array.includes("32")) {
        result = 5
    }
    else if (array.includes("33")) {
        result = 6
    }
    else if (array.includes("40")) {
        result = 7
    }
    else if (array.includes("41")) {
        result = 8
    }
    else if (array.includes("42")) {
        result = 9
    }
    return result
}

export function checkOutsourceStatus(status) {
    console.log(status, typeof (status))
    let result = -1
    if (status < 4) {
        result = 0
    }
    else if (status == 4) {
        result = 1
    }
    else if (status == 5) {
        result = 2
    }
    else if (status == 6) {
        result = 3
    }
    else if (status == 7) {
        result = 4
    }
    return result
}
