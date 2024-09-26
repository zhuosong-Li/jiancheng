<template>
    <el-table :data="props.tableData" border>
        <el-table-column prop="rowId" label="序号" />
        <el-table-column prop="procedure" label="工序"></el-table-column>
        <el-table-column prop="price" label="单位价格"></el-table-column>
        <el-table-column prop="note" label="备注"></el-table-column>
    </el-table>
    <el-button type="primary" @click="handleExport">保存为Excel</el-button>
</template>
<script setup>
import { exportTableToExcel } from '@/Pages/ProductionManagementDepartment/utils';
const props = defineProps(['tableData'])

const handleExport = () => {
    exportTableToExcel(tableData.value, columns.value, currentTitle.value + ".xlsx")
}

const handleClose = () => {
    previewVis.value = false
    props.handleClose(1)
}
</script>