<template>
    <el-table :data="tableData" border stripe :max-height="500">
        <el-table-column prop="itemName" label="明细">
            <template #default="scope">
                <el-input v-model="scope.row.itemName" placeholder="" clearable></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="itemCost" label="金额">
            <template #default="scope">
                <el-input v-model="scope.row.itemCost" placeholder="" clearable type="number"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注">
            <template #default="scope">
                <el-input v-model="scope.row.remark" placeholder="" clearable></el-input>
            </template>
        </el-table-column>
        <el-table-column label="操作">
            <template #default="scope">
                <el-button type="danger" @click="deleteRow(scope.$index)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-button type="primary" size="default" @click="addRow()">添加新一行</el-button>
</template>
<script>
export default {
    props: ["tableData", "outsourceInfoId"],
    methods: {
        addRow() {
            this.tableData.push(
                {
                    "itemName": "",
                    "itemCost": 0,
                    "remark": "",
                    "outsourceInfoId": this.$props.outsourceInfoId
                }
            )
        },
        deleteRow(index) {
            this.tableData.splice(index, 1)
        }
    }
}
</script>