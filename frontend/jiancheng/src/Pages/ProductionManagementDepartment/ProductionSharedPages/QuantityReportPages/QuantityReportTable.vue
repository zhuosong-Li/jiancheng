<template>
    <el-table :data="props.tableData" border :style="{ marginBottom: '20px' }">
        <el-table-column prop="colorName" label="颜色"></el-table-column>
        <el-table-column label="生产数量">
            <template #default="scope">
                <el-input v-model="scope.row.reportAmount" style="width: 100px" type="number" min="0"
                    :max="scope.row.remainAmount" @blur="() => checkValue(scope.row)" :readonly="!props.editable"/>
            </template>
        </el-table-column>
        <el-table-column prop="remainAmount" label="目前剩余数量" />
    </el-table>
</template>

<script setup>
const props = defineProps(['tableData', 'orderShoeId', 'editable'])

const checkValue = (row) => {
    if (row.amount < 0) {
        row.amount = 0
    } else if (row.remainAmount < 0) {
        row.amount = Number(row.amount) + row.remainAmount
    }
}

</script>