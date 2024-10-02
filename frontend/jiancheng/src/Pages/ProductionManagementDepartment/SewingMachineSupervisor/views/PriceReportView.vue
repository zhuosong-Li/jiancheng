<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">针车工价填报</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="鞋型号信息" :column="4" border>
                        <el-descriptions-item label="订单号">{{ props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ props.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户">{{ props.customerName }}</el-descriptions-item>
                        <el-descriptions-item label="工价单状态">{{ statusName }}</el-descriptions-item>
                        <el-descriptions-item label="针车预备开始日期">{{ props.preSewingProductionStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="针车预备结束日期">{{ props.preSewingProductionEndDate }}</el-descriptions-item>
                        <el-descriptions-item label="针车开始日期">{{ props.productionStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="针车结束日期">{{ props.productionEndDate }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <div v-if="statusName === '未提交' || statusName === '被驳回'">
                <el-tabs v-model="currentTab" type="border-card" tab-position="top">
                    <el-tab-pane v-for="item in panes" :key="item.key" :label="item.label" :name="item.key">
                        <div v-if="item.key === 1 && preSewingTableData !== null">
                            <SewingPriceReportTable :tableData="preSewingTableData"
                                :procedureInfo="preSewingProcedureInfo" />
                        </div>
                        <div v-else-if="item.key === 2 && tableData !== null">
                            <SewingPriceReportTable :tableData="tableData" :procedureInfo="procedureInfo" />
                        </div>
                    </el-tab-pane>
                </el-tabs>
                <el-row>
                    <el-button style="position: fixed; right: 90px;" type="primary"
                        @click="handleSaveData">保存</el-button>
                    <el-button style="position: fixed; right: 20px;" type="success" @click="handleSubmit">提交</el-button>
                </el-row>
            </div>
            <div v-else-if="statusName === '已提交' || statusName === '已审批'">
                <el-tabs v-model="currentTab" type="border-card" tab-position="top">
                    <el-tab-pane v-for="item in panes" :key="item.key" :label="item.label" :name="item.key">
                        <div v-if="item.key === 1 && preSewingTableData !== null">
                            <PreviewReportPage :tableData="preSewingTableData" />
                        </div>
                        <div v-else-if="item.key === 2 && tableData !== null">
                            <PreviewReportPage :tableData="tableData" />
                        </div>
                    </el-tab-pane>
                </el-tabs>

            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue';
import axios from 'axios';
import PreviewReportPage from '../components/LaborPriceReport/PreviewReportPage.vue';
import SewingPriceReportTable from '../components/LaborPriceReport/SewingPriceReportTable.vue';
import AllHeader from '@/components/AllHeader.vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
const router = useRouter();
const preSewingTableData = ref(null)
const pewSewingReportId = ref(null)
const preSewingProcedureInfo = ref({})

const tableData = ref(null)
const reportId = ref(null)
const procedureInfo = ref({})
const statusName = ref('')
const currentTab = ref(1)
const panes = ref([
    {
        label: '针车预备',
        key: 1
    },
    {
        label: '针车',
        key: 2
    },
])
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
const props = defineProps(["orderId", "orderRId", "orderShoeId", "shoeRId", "customerName", "productionStartDate", "productionEndDate", "preSewingProductionStartDate", "preSewingProductionEndDate"])

onMounted(() => {
    getPreSewingProcedures()
    getSewingProcedures()
    getPreSewingPriceReportDetail()
    getPriceReportDetail()
})
const getPreSewingProcedures = async () => {
    await getProcedures(preSewingProcedureInfo, "针车预备")
}

const getSewingProcedures = async () => {
    await getProcedures(procedureInfo, "针车")
}

const getProcedures = async (arr, name) => {
    const params = { team: name }
    const response = await axios.get(`${apiBaseUrl}/production/getallprocedures`, { params })
    response.data.forEach(row => {
        arr.value[row.procedureName] = { "price": row.price, "id": row.procedureId }
    });
}

const getPreSewingPriceReportDetail = async () => {
    const params = {
        "orderShoeId": props.orderShoeId,
        "team": "针车预备"
    }
    const response = await axios.get(`${apiBaseUrl}/production/getpricereportdetailbyordershoeid`, { params })
    if (response.status == 200) {
        preSewingTableData.value = response.data.detail
        pewSewingReportId.value = response.data.metaData.reportId
        statusName.value = response.data.metaData.statusName
    }
}

const getPriceReportDetail = async () => {
    const params = {
        "orderShoeId": props.orderShoeId,
        "team": "针车"
    }
    const response = await axios.get(`${apiBaseUrl}/production/getpricereportdetailbyordershoeid`, { params })
    if (response.status == 200) {
        tableData.value = response.data.detail
        reportId.value = response.data.metaData.reportId
        statusName.value = response.data.metaData.statusName
    }
}

const handleSaveData = async () => {
    console.log(preSewingTableData.value, tableData.value)
    console.log(preSewingProcedureInfo.value, procedureInfo.value)
    preSewingTableData.value.forEach(row => {
        row["price"] = preSewingProcedureInfo.value[row.procedure]["price"]
        row["procedureId"] = preSewingProcedureInfo.value[row.procedure]["id"]
    })
    const response1 = await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: pewSewingReportId.value, newData: preSewingTableData.value })

    tableData.value.forEach(row => {
        row["price"] = procedureInfo.value[row.procedure]["price"]
        row["procedureId"] = procedureInfo.value[row.procedure]["id"]
    })
    const response2 = await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: reportId.value, newData: tableData.value })

    if (response1.status == 200 && response2.status == 200) {
        ElMessage.success("保存成功")
    }
    else {
        ElMessage.error("保存失败")
    }
}

const handleSubmit = async () => {
    const response = await axios.post(`${apiBaseUrl}/production/submitpricereport`,
        { "orderId": props.orderId, "orderShoeId": props.orderShoeId, "reportIdArr": [pewSewingReportId.value, reportId.value] })
    if (response.status == 200) {
        ElMessage.success("提交成功")
    }
    else {
        ElMessage.error("提交失败")
    }
    router.push(`/sewingmachine`)
}
</script>
