<template>
    <el-table :data="props.tableData" border stripe>
        <el-table-column prop="rowId" label="序号" />
        <el-table-column prop="procedure" label="工序">
            <template #default="scope">
                <el-select v-model="scope.row.procedure" filterable placeholder="请选择" style="width: 240px">
                    <el-option v-for="(value, key) in props.procedureInfo" :value="key" />
                </el-select>
            </template>
        </el-table-column>
        <el-table-column prop="price" label="单位价格">
            <template #default="scope">
                <p>{{ props.procedureInfo[scope.row.procedure] ? props.procedureInfo[scope.row.procedure]["price"] : '' }}</p>
            </template>
        </el-table-column>
        <el-table-column prop="note" label="备注">
            <template #default="scope">
                <el-input v-model="scope.row.note" placeholder="" clearable></el-input>
            </template>
        </el-table-column>
        <el-table-column label="操作">
            <template #default="scope">
                <el-button type="danger" @click="deleteRow(props.tableData, scope.$index)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-button type="primary" size="default" @click="addRow(props.tableData)">添加新一行</el-button>
</template>
<script setup>
const props = defineProps(['tableData', 'procedureInfo'])

const addRow = (arrRef) => {
    const newRowId = arrRef.length + 1;
    arrRef.push(
        {
            "rowId": newRowId,
            "procedure": "",
            "price": "",
            "note": ""
        }
    )
}

const deleteRow = (tableData, index) => {
    tableData.splice(index, 1)
    tableData.forEach((row, index) => {
        row.rowId = index + 1
    })
}

// const handleClickEnter = (event) => {
//     if (event.key === 'Enter') {
//         addRow()
//     }
// }

</script>
