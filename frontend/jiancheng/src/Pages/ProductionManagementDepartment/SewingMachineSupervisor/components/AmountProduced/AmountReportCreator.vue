<template>
    <el-dialog title="生产数量表" v-model="createVis" width="90%" :before-close="handleGenerateClose">
        <el-table :data="priceReport" show-summary border :style="{ marginBottom: '20px' }">
            <el-table-column prop="rowId" label="序号" />
            <el-table-column prop="procedure" label="工序" />
            <el-table-column prop="price" label="单位价格" />
            <el-table-column prop="totalPrice" label="总价格" />
        </el-table>
        <el-table :data="tableData" border :style="{ marginBottom: '20px' }">
            <el-table-column prop="colorName" label="颜色"></el-table-column>
            <el-table-column prop="name" label="鞋码编号"></el-table-column>
            <el-table-column label="生产数量">
                <template #default="scope">
                    <el-input v-model="scope.row.amount" style="width: 100px" type="number" min="0"
                        :max="scope.row.remainAmount" @blur="() => checkValue(scope.row)" />
                </template>
            </el-table-column>
            <el-table-column prop="remainAmount" label="目前剩余数量" />
        </el-table>

        <template #footer>
            <span>
                <el-button @click="handleGenerateClose">取消</el-button>
                <el-button type="primary" @click="handleSaveData">保存</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { watch, ref, onMounted, getCurrentInstance } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
const props = defineProps(['currentReport', 'orderShoeId', 'teamName', 'handleClose'])
const tableData = ref([])
const createVis = ref(true)
const priceReport = ref([])
const producedAmount = ref(0)
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
onMounted(async () => {
    let params = { "orderShoeId": props.orderShoeId, 'team': props.teamName, "status": 2 }
    // get price report detail
    let response = await axios.get(`${apiBaseUrl}/production/getpricereportdetailbyordershoeid`, { params })
    priceReport.value = response.data.detail
    // get quantity report detail
    params = { "reportId": props.currentReport.reportId }
    response = await axios.get(`${apiBaseUrl}/production/getquantityreportdetail`, { params })
    response.data.forEach(row => {
        if (props.teamName === '针车预备') {
            row["remainAmount"] = row["totalAmount"] - row["preSewingAmount"]
        }
        else {
            row["remainAmount"] = row["totalAmount"] - row["sewingAmount"]
        }
        tableData.value.push(row)
        producedAmount.value += row["amount"]
    })
    tableData.value.forEach(row => {
        watch(
            () => row.amount,
            (newVal, oldVal) => {
                newVal = Number(newVal), oldVal = Number(oldVal)
                producedAmount.value = producedAmount.value + newVal - oldVal
                priceReport.value.forEach((priceRow) => {
                    priceRow.totalPrice = (producedAmount.value * priceRow.price).toFixed(2)
                })
            }, { deep: true }
        )
    })
})

const checkValue = (row) => {
    if (row.amount < 0) {
        row.amount = 0
    } else if (row.remainAmount < 0) {
        row.amount = Number(row.amount) + row.remainAmount
    }
}

const handleSaveData = () => {
    ElMessageBox.confirm('确定保存数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        const data = { 
            "reportId": props.currentReport.reportId,
            "data": tableData.value
        }
        const response = await axios.put(`${apiBaseUrl}/production/editquantityreportdetail`, data)
        if (response.status == 200) {
            ElMessage.success("保存成功")
        }
        else {
            ElMessage.error("保存失败")
        }
        handleGenerateClose()
    }).catch(() => {
        ElMessage.info("取消保存");
        handleGenerateClose()
    })
}
const handleGenerateClose = () => {
    createVis.value = false
    props.handleClose(0)
}
</script>