<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">裁断与批皮工价填报</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="鞋型号信息" :column="3" border>
                        <el-descriptions-item label="订单号">{{ props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ props.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户">{{ props.customerName }}</el-descriptions-item>
                        <el-descriptions-item label="工段开始日期">{{ props.productionStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="工段结束日期">{{ props.productionEndDate }}</el-descriptions-item>
                        <el-descriptions-item label="工价单状态">{{ statusName }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <div v-if="statusName === '未提交' || statusName === '被驳回'">
                <PriceReportCreator :orderId="props.orderId" :orderShoeId="props.orderShoeId" :reportId="reportId"
                    :tableData="tableData" :procedureInfo="procedureInfo" />
            </div>
            <div v-else-if="statusName === '已提交' || statusName === '已审批'">
                <PreviewReportPage :tableData="tableData" :procedureInfo="procedureInfo" />
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue';
import axios from 'axios';
import PriceReportCreator from '../components/LaborPriceReport/PriceReportCreator.vue'
import PreviewReportPage from '../components/LaborPriceReport/PreviewReportPage.vue';
import AllHeader from '@/components/AllHeader.vue';
const tableData = ref([])
const reportId = ref([])
const procedureInfo = ref({})
const statusName = ref('')
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
const props = defineProps(["orderId", "orderRId", "orderShoeId", "shoeRId", "customerName", "productionStartDate", "productionEndDate"])
onMounted(() => {
    getAllProcedures()
    getPriceReportDetail()
})
const getAllProcedures = async () => {
    const params = { teams: ['裁断'].toString() }
    const response = await axios.get(`${apiBaseUrl}/production/getallprocedures`, { params })
    response.data.forEach(row => {
        procedureInfo.value[row.procedureName] = { "price": row.price, "id": row.procedureId }
    });
}

const getPriceReportDetail = async () => {
    const params = {
        "orderShoeId": props.orderShoeId,
        "team": "裁断"
    }
    const response = await axios.get(`${apiBaseUrl}/production/getpricereportdetailbyordershoeid`, { params })
    tableData.value = response.data.detail
    reportId.value = response.data.metaData.reportId
    statusName.value = response.data.metaData.statusName
}
</script>
