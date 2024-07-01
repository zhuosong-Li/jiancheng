<template>
    <el-dialog title="针车工价表格" v-model="createVis" width="90%" :before-close="handleGenerateClose">
        <el-input v-model="searchOrder" placeholder="请输入工序名称" size="normal" style="width: 240px"
                :suffix-icon="Search" clearable @input="filterData"></el-input>
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
                    <!-- TODO: add a enter listener. Add row when click enter -->
                    <!-- 裁断工价定死
                    写状态详细点：生产多少双和剩余数量
                    放搜索栏在针车工价填报 
                    复制裁断到成型-->
                    <el-input v-model="scope.row.unitPrice" style="width: 100px" placeholder="" clearable @keypress="handleClickEnter"></el-input>
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
import { Search } from '@element-plus/icons-vue'
const props = defineProps(['tableInput', 'handleSave', 'handleClose'])

const tableData = ref(JSON.parse(JSON.stringify(props.tableInput)))
const rowId = ref(tableData.value.length + 1)
const createVis = ref(true)
const options = [
    {
        value: '后跟合缝处打酒精',
        label: 'Option1',
    },
    {
        value: '后跟合缝',
        label: 'Option2',
    },
    {
        value: '后跟压缝',
        label: 'Option3',
    },
    {
        value: '单针车后跟',
        label: 'Option4',
    },
    {
        value: '后跟上口修搭地4个/双',
        label: 'Option5',
    },
]
const priceOptions = {
    "后跟合缝处打酒精": [0.03],
    "后跟合缝": [0.45, 0.9],
    "后跟压缝": [1, 1.2],
    "单针车后跟": [0.9, 1.1],
    "后跟上口修搭地4个/双": [2, 2.5]
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

const handleClickEnter = (event) => {
    if (event.key === 'Enter') {
        addRow()
    }
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