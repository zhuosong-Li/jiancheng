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
    <el-row :gutter="20">
        <el-button style="position: fixed; right: 90px;" type="primary" @click="handleSaveData">保存</el-button>
        <el-button style="position: fixed; right: 20px;" type="success" @click="handleSubmit">提交</el-button>
    </el-row>
</template>

<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import { useRouter } from 'vue-router';
const props = defineProps(['orderId', 'orderShoeId', 'reportId', 'tableData', 'procedureInfo'])
const proxy = getCurrentInstance()
const router = useRouter();
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
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

const handleSaveData = () => {
    ElMessageBox.confirm('确定保存数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        // insert price to table data
        props.tableData.forEach(row => {
            row["price"] = props.procedureInfo[row.procedure]["price"]
            row["procedureId"] = props.procedureInfo[row.procedure]["id"]
        })
        await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
            { reportId: props.reportId, newData: props.tableData })
        ElMessage({
            type: 'success',
            message: '保存成功!'
        });
        window.location.reload()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '已取消保存'
        });
        window.location.reload()
    });
}
const handleSubmit = async (rowData) => {
    const response = await axios.post(`${apiBaseUrl}/production/submitpricereport`, 
    { "orderId": props.orderId, "orderShoeId": props.orderShoeId, "reportIdArr": [props.reportId] })
    if (response.status == 200) {
        ElMessage.success("提交成功")
    }
    else {
        ElMessage.error("提交失败")
    }
    router.push(`/molding`)
}
</script>
