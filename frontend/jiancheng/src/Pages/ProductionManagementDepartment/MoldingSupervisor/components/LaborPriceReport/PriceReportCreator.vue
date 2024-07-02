<template>
    <el-dialog title="工价表格" v-model="createVis" width="90%" :before-close="handleGenerateClose">
        <el-table :data="tableData" border>
            <el-table-column prop="rowId" label="序号" />
            <el-table-column prop="procedure" label="工序">
                <template #default="scope">
                    <el-select v-model="scope.row.procedure" filterable placeholder="请选择" style="width: 240px">
                        <el-option v-for="item in options" :value="item.value" />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="unitPrice" label="单位价格">
                <template #default="scope">
                    <p>{{ priceOptions[scope.row.procedure] }}</p>
                </template>
            </el-table-column>
            <el-table-column prop="note" label="备注">
                <template #default="scope">
                    <el-input v-model="scope.row.note" placeholder="" clearable></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="danger" @click="deleteRow(scope.$index)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="addRow">添加新一行</el-button>
        <template #footer>
            <span>
                <el-button @click="handleGenerateClose">取消</el-button>
                <el-button type="primary" @click="handleSaveData">保存</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
const props = defineProps(['tableInput', 'handleSave', 'handleClose'])

const tableData = ref(JSON.parse(JSON.stringify(props.tableInput)))
const rowId = ref(tableData.value.length + 1)
const createVis = ref(true)
const options = [
    {
        value: '单鞋E',
        label: 'Option1',
    },
    {
        value: '批-22片',
        label: 'Option2',
    }
]
const priceOptions = {
    "单鞋E": 0.03,
    "批-22片": 0.45
}

const addRow = () => {
    tableData.value.push(
        {
            "rowId": rowId.value,
            "procedure": "",
            "unitPrice": "",
            "note": ""
        }
    )
    rowId.value++
}

const deleteRow = (index) => {
    ElMessageBox.confirm('确定删除此行吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        tableData.value.splice(index, 1);
        ElMessage({
            type: 'success',
            message: '删除成功!'
        });
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '已取消删除'
        });
    });
    rowId.value--
}

const handleSaveData = () => {
    ElMessageBox.confirm('确定保存数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        ElMessage({
            type: 'success',
            message: '保存成功!'
        });
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '已取消保存'
        });
    });
    props.handleSave(tableData.value)
}
const handleGenerateClose = () => {
    ElMessageBox.confirm('确定退出编辑表格吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        createVis.value = false
        props.handleClose(0)
    }).catch(() => {})
}
</script>