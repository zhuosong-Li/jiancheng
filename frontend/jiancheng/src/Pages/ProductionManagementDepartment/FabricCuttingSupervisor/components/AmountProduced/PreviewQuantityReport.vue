<template>
    <el-dialog :title="currentTitle" v-model="previewVis" width="90%" @close="handleClose">
        <el-table :data="tableData" border>
            <el-table-column prop="colorName" label="颜色"></el-table-column>
            <el-table-column prop="name" label="鞋码编号"></el-table-column>
            <el-table-column prop="amount" label="生产数量"></el-table-column>
            <el-table-column prop="remainAmount" label="目前剩余数量" />
        </el-table>
        <template #footer>
            <span>
                <el-button @click="handleClose">退出</el-button>
                <el-button type="primary" @click="handleExport">保存为Excel</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue';
import axios from 'axios'
import { exportTableToExcel } from '@/Pages/ProductionManagementDepartment/utils';
const props = defineProps(['shoeRId', 'currentReport', 'handleClose'])
const previewVis = ref(true)
const columns = ref([])
const tableData = ref([])
const currentTitle = ref('')
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
onMounted(async () => {
    console.log(props.currentReport)
    currentTitle.value = "鞋型号_" + props.shoeRId + "_生产数量单_" + props.currentReport.creationDate
    let params = { reportId: props.currentReport.reportId, team: 0 }
    const response = await axios.get(`${apiBaseUrl}/production/getquantityreportdetail`, { params })
    response.data.forEach(row => {
        row["remainAmount"] = row["totalAmount"] - row["producedAmount"]
        tableData.value.push(row)
    })
    let obj = [
        { prop: "colorName", label: "颜色" },
        { prop: "name", label: "鞋码编号" },
        { prop: "amount", label: "生产数量" },
        { prop: "remainAmount", label: "目前剩余数量" },
    ]
    columns.value = obj
})

const handleExport = () => {
    exportTableToExcel(tableData.value, columns.value, currentTitle.value + ".xlsx")
}

const handleClose = () => {
    previewVis.value = false
    props.handleClose(1)
}
</script>