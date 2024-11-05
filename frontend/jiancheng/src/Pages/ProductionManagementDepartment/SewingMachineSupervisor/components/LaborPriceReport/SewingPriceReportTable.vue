<template>
    <el-table :data="props.tableData" border stripe>
        <el-table-column prop="rowId" label="序号" />
        <el-table-column prop="procedure" label="工序">
            <template #default="scope">
                <el-autocomplete v-model="scope.row.procedure" :fetch-suggestions="querySearch" placeholder="输入工序"
                    @select="(args) => onProductSelect(args, scope.row)" clearable />
            </template>
        </el-table-column>
        <el-table-column prop="price" label="工价">
            <template #default="scope">
                <el-input v-model="scope.row.price" placeholder="" clearable></el-input>
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
import { ref } from 'vue';
const props = defineProps(['tableData', 'procedureInfo'])
const nameSuggestions = ref([])

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

const querySearch = (queryString, cb) => {
    const matchObj = queryString
        ? props.procedureInfo.filter(procedure =>
            procedure.procedureName.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        )
        : []
    // call callback function to return suggestions
    let result = []
    matchObj.forEach(row => {
        result.push({value: row.procedureName, price: row.price})
    })
    cb(result)
}

const onProductSelect = (info, row) => {
    row.procedureName = info.value
    row.price = info.price
}
// const handleClickEnter = (event) => {
//     if (event.key === 'Enter') {
//         addRow()
//     }
// }

</script>
