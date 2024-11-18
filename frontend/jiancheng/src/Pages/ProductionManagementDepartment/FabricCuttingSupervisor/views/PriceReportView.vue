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
                        <el-descriptions-item label="订单号">{{ orderInfo.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ orderInfo.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户型号">{{ orderInfo.customerProductName }}</el-descriptions-item>
                        <el-descriptions-item label="工段开始日期">{{ orderInfo.cuttingStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="工段结束日期">{{ orderInfo.cuttingEndDate }}</el-descriptions-item>
                        <el-descriptions-item label="工价单状态">{{ statusName }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-row v-if="statusName === '被驳回'" :gutter="20">
                <span>驳回原因：{{ rejectionReason }}</span>
            </el-row>
            <PriceReportCreator :tableData="tableData" :procedureInfo="procedureInfo" :readOnly="readOnly"/>
            <el-row :gutter="20">
                <el-button-group style="position: fixed; right: 30px;">
                    <el-button type="info" @click="saveAsTemplate(reportId, orderInfo.shoeId, 0, tableData)">保存为模板</el-button>
                    <el-button v-if="!readOnly" type="info" @click="loadTemplateHelper">加载模板</el-button>
                    <el-button type="primary" @click="">下载为Excel</el-button>
                    <el-button v-if="!readOnly" type="primary" @click="handleSaveData">保存</el-button>
                    <el-button v-if="!readOnly" type="success" @click="handleSubmit">提交</el-button>
                </el-button-group>
            </el-row>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref, getCurrentInstance, readonly } from 'vue';
import axios from 'axios';
import PriceReportCreator from '../components/LaborPriceReport/PriceReportCreator.vue'
import PreviewReportPage from '../components/LaborPriceReport/PreviewReportPage.vue';
import AllHeader from '@/components/AllHeader.vue';
import { ElMessage } from 'element-plus';
import { loadTemplate, saveAsTemplate } from '../../utils';
const tableData = ref([])
const reportId = ref([])
const procedureInfo = ref([])
const statusName = ref('')
const rejectionReason = ref('')
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
const props = defineProps(["orderId", "orderShoeId"])
const orderInfo = ref({})
const readOnly = ref(true)

onMounted(() => {
    getOrderInfo()
    getAllProcedures()
    getPriceReportDetail()
    setReadOnly()
})

const setReadOnly = () => {
    if (statusName.value === '已审批' || statusName.value === '已提交') {
        readOnly.value = true
    }
    else {
        readOnly.value = false
    }
}

const loadTemplateHelper = async () => {
    tableData.value = await loadTemplate(orderInfo.value.shoeId, 0)
}

const getOrderInfo = async () => {
    let params = { "orderId": props.orderId, "orderShoeId": props.orderShoeId }
    let response = await axios.get(`${apiBaseUrl}/production/productionmanager/getorderinfo`, { params })
    orderInfo.value = response.data
    console.log(orderInfo.value)
    params = { "orderShoeId": props.orderShoeId }
    response = await axios.get(`${apiBaseUrl}/production/getproductioninfo`, { params })
    orderInfo.value = { ...orderInfo.value, ...response.data }
    console.log(orderInfo.value)
}

const getAllProcedures = async () => {
    const params = { teams: ['裁断'].toString() }
    const response = await axios.get(`${apiBaseUrl}/production/getallprocedures`, { params })
    procedureInfo.value = response.data
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
    rejectionReason.value = response.data.metaData.rejectionReason
}

const handleSaveData = async () => {
    try {
        await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: reportId.value, newData: tableData.value })
        ElMessage.success("保存成功")
    }
    catch(error) {
        console.log(error)
        ElMessage.error("保存失败")
    }
}
const handleSubmit = async (rowData) => {
    if (tableData.value.length == 0) {
        ElMessage.error("内容不能为空")
    }
    else {
        await handleSaveData()
        const response = await axios.post(`${apiBaseUrl}/production/submitpricereport`, 
        { "orderId": props.orderId, "orderShoeId": props.orderShoeId, "reportIdArr": [reportId.value] })
        if (response.status == 200) {
            ElMessage.success("提交成功")
            await getPriceReportDetail()
        }
        else {
            ElMessage.error("提交失败")
        }
    }
}
</script>
