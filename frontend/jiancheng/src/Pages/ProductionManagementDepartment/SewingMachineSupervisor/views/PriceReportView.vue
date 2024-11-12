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
                        <el-descriptions-item label="针车预备开始日期">{{ props.preSewingProductionStartDate
                            }}</el-descriptions-item>
                        <el-descriptions-item label="针车预备结束日期">{{ props.preSewingProductionEndDate
                            }}</el-descriptions-item>
                        <el-descriptions-item label="针车开始日期">{{ props.productionStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="针车结束日期">{{ props.productionEndDate }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-row v-if="statusName === '被驳回'" :gutter="20">
                <span>驳回原因：{{ rejectionReason }}</span>
            </el-row>
            <div v-if="statusName === '未提交' || statusName === '被驳回'">
                <el-tabs v-model="currentTab" type="border-card" tab-position="top">
                    <el-tab-pane v-for="item in panes" :key="item.key" :label="item.label" :name="item.key">
                        <div v-if="item.key === 1 && preSewingTableData !== null">
                            <SewingPriceReportTable :tableData="preSewingTableData"
                                :procedureInfo="preSewingProcedureInfo" />
                            <el-button type="info" @click="saveAsTemplate">保存为模板</el-button>
                            <el-button type="info" @click="loadTemplate">加载模板</el-button>
                        </div>
                        <div v-else-if="item.key === 2 && sewingTableData !== null">
                            <SewingPriceReportTable :tableData="sewingTableData" :procedureInfo="procedureInfo" />
                            <el-button type="info" @click="saveAsTemplate">保存为模板</el-button>
                            <el-button type="info" @click="loadTemplate">加载模板</el-button>
                        </div>
                    </el-tab-pane>
                </el-tabs>
                <el-row>
                    <el-button-group style="position: fixed; right: 30px;">
                        <el-button type="primary" @click="handleSaveData">保存</el-button>
                        <el-button type="primary" @click="handleExport">下载为Excel</el-button>
                        <el-button type="success" @click="handleSubmit">提交</el-button>
                    </el-button-group>
                </el-row>
            </div>
            <div v-else-if="statusName === '已提交' || statusName === '已审批'">
                <el-tabs v-model="currentTab" type="border-card" tab-position="top">
                    <el-tab-pane v-for="item in panes" :key="item.key" :label="item.label" :name="item.key">
                        <div v-if="item.key === 1 && preSewingTableData !== null">
                            <PreviewReportPage :tableData="preSewingTableData" />
                            <el-button type="info" @click="saveAsTemplate">保存为模板</el-button>
                            <el-button type="info" @click="loadTemplate">加载模板</el-button>
                        </div>
                        <div v-else-if="item.key === 2 && sewingTableData !== null">
                            <PreviewReportPage :tableData="sewingTableData" />
                            <el-button type="info" @click="saveAsTemplate">保存为模板</el-button>
                            <el-button type="info" @click="loadTemplate">加载模板</el-button>
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
const preSewingProcedureInfo = ref([])

const sewingTableData = ref(null)
const sewingReportId = ref(null)
const procedureInfo = ref([])
const statusName = ref('')
const rejectionReason = ref('')
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
    arr.value = response.data
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
        rejectionReason.value = response.data.metaData.rejectionReason
    }
}

const getPriceReportDetail = async () => {
    const params = {
        "orderShoeId": props.orderShoeId,
        "team": "针车"
    }
    const response = await axios.get(`${apiBaseUrl}/production/getpricereportdetailbyordershoeid`, { params })
    if (response.status == 200) {
        sewingTableData.value = response.data.detail
        sewingReportId.value = response.data.metaData.reportId
        statusName.value = response.data.metaData.statusName
    }
}

const handleSaveData = async () => {
    const response1 = await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: pewSewingReportId.value, newData: preSewingTableData.value })

    const response2 = await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: sewingReportId.value, newData: sewingTableData.value })

    if (response1.status == 200 && response2.status == 200) {
        ElMessage.success("保存成功")
    }
    else {
        ElMessage.error("保存失败")
    }
}

const handleSubmit = async () => {
    if (preSewingTableData.value.length == 0 || sewingTableData.value == 0) {
        ElMessage.error("内容不能为空")
    }
    else {
        await handleSaveData()
        try {
            await axios.post(`${apiBaseUrl}/production/submitpricereport`,
                { "orderId": props.orderId, "orderShoeId": props.orderShoeId, "reportIdArr": [pewSewingReportId.value, sewingReportId.value] })
            ElMessage.success("提交成功")
        }
        catch (error) {
            ElMessage.error("提交失败")
        }
    }

}

const saveAsTemplate = async () => {
    let reportId = null
    let reportData = null
    if (currentTab.value == 1) {
        reportId = pewSewingReportId.value
        reportData = preSewingTableData.value
    }
    else {
        reportId = sewingReportId.value
        reportData = sewingTableData.value
    }
    try {
        console.log(reportData)
        await axios.post(`${apiBaseUrl}/production/storepricereportdetail`,
        { reportId: reportId, newData: reportData })
        await axios.put(`${apiBaseUrl}/production/savetemplate`,
            {"reportId": reportId, "shoeRId": props.shoeRId})
        ElMessage.success("保存成功")
    }
    catch (error) {
        ElMessage.error("保存失败")
    }
}

const loadTemplate = async () => {
    let team = null
    let tableData = null
    if (currentTab.value == 1) {
        team = '针车预备'
        tableData = preSewingTableData
    }
    else {
        team = '针车'
        tableData = sewingTableData
    }
    try {
        let params = {"shoeRId": props.shoeRId, "team": team}
        let response = await axios.get(`${apiBaseUrl}/production/loadtemplate`, {params})
        tableData.value = response.data
        ElMessage.success("加载成功")
    }
    catch (error) {
        ElMessage.error(error)
    }
}

const handleExport = async () => { }
</script>
