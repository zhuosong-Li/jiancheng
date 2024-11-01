<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">数量填报</el-col>
            </el-row>
            <el-dialog title="新建生产数量单" v-model="createReportVis">
                <el-date-picker v-model="dateValue" type="date" :disabled-date="disabledDate" value-format="YYYY-MM-DD"
                    placeholder="选择日期" />
                <template #footer>
                    <span>
                        <el-button type="primary" @click="handleConfirmCreate">保存</el-button>
                    </span>
                </template>
            </el-dialog>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="鞋型信息" :column="3" border>
                        <el-descriptions-item label="订单号">{{ props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ props.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户">{{ props.customerName }}</el-descriptions-item>
                        <el-descriptions-item label="工段">{{ props.teamName }}</el-descriptions-item>
                        <el-descriptions-item label="工段开始日期">{{ props.productionStartDate }}</el-descriptions-item>
                        <el-descriptions-item label="工段结束日期">{{ props.productionEndDate }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-table :data="taskData" :default-sort="{ prop: 'date', order: 'ascending' }" border stripe max-height="500">
                <el-table-column prop="creationDate" label="日期" sortable></el-table-column>
                <el-table-column prop="status" label="状态">
                    <template v-slot="scope">
                        <el-tooltip v-if="scope.row.status === '被驳回'" effect="dark" :content="scope.row.rejectionReason">
                            <span class="rejected">{{ scope.row.status }}</span>
                        </el-tooltip>
                        <span v-else>{{ scope.row.status }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.status === '已提交' || scope.row.status === '已审批'" type="success"
                            @click="openPreviewDialog(scope.row)">查看</el-button>
                        <el-button-group v-else-if="scope.row.status === '未提交' || scope.row.status === '被驳回'">
                            <el-button type="primary" class="block-button" @click="handleEdit(scope.row)">编辑</el-button>
                            <el-button type="success" class="block-button"
                                @click="openPreviewDialog(scope.row)">查看</el-button>
                            <el-button type="warning" class="block-button"
                                @click="handleSubmit(scope.row)">提交</el-button>
                            <el-button type="danger" class="block-button"
                                @click="handleDelete(scope.row, scope.$index)">删除</el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
            <el-row>
                <el-button type="primary" @click="handleCreateReport">
                    <span>新建生产数量单</span>
                </el-button>
            </el-row>
            <div v-if="createVis">
                <AmountReportCreator :currentReport="currentReport" :orderShoeId="props.orderShoeId" :teamName="props.teamName"
                    :handleClose="handleClose" />
            </div>
            <div v-else-if="previewVis">
                <PreviewQuantityReport :shoeRId="props.shoeRId" :currentReport="currentReport" :teamName="props.teamName"
                    :handleClose="handleClose" />
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref, watch, getCurrentInstance } from 'vue';
import AmountReportCreator from '../components/AmountProduced/AmountReportCreator.vue'
import PreviewQuantityReport from '../components/AmountProduced/PreviewQuantityReport.vue';
import AllHeader from '@/components/AllHeader.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios'
const createVis = ref(false)
const createReportVis = ref(false)
const previewVis = ref(false)
const props = defineProps(["orderId", "orderRId", "orderShoeId", "shoeRId", "customerName", "productionStartDate", "productionEndDate", "teamName"])
const taskData = ref([])
const currentReport = ref({})
const dateValue = ref('')
const createdDates = ref(new Set())
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
const orderStartDate = ref('')

onMounted(async () => {
    getOrderStartDate()
    getAllQuantityReports()
})

const getOrderStartDate = async () => {
    let params = {"orderId": props.orderId}
    let response = await axios.get(`${apiBaseUrl}/production/productionmanager/getorderinfo`, { params })
    orderStartDate.value = response.data.orderStartDate
}

const getAllQuantityReports = async () => {
    // get all quantity report for this order_shoe_id
    let params = {
        "orderShoeId": props.orderShoeId,
        "team": props.teamName
    }
    const response1 = await axios.get(`${apiBaseUrl}/production/getallquantityreports`, { params })
    taskData.value = response1.data
}

const dateFormatter = (input) => {
    const date = new Date(input);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate
}

watch(taskData, () => {
    createdDates.value = new Set(taskData.value.map(e => e.creationDate));
}, { deep: true })

const handleEdit = (rowData) => {
    createVis.value = true
    currentReport.value = rowData
}
const disabledDate = (time) => {
    let startDate = new Date(orderStartDate.value)
    startDate.setDate(startDate.getDate() - 1);
    const endDate = new Date()
    return time.getTime() < startDate || time.getTime() > endDate.getTime() || createdDates.value.has(dateFormatter(time));
}
const handleConfirmCreate = async () => {
    if (dateValue.value.length === 0) {
        ElMessage({ type: 'warning', message: '未选择一个日期!' })
        return
    }
    if (createdDates.value.has(dateValue.value)) {
        ElMessage({ type: 'warning', message: '已有该日期的报告!' })
        return
    }
    let body = {
        "orderShoeId": props.orderShoeId,
        "creationDate": dateValue.value,
        "team": props.teamName
    }
    const response = await axios.post(`${apiBaseUrl}/production/createquantityreport`, body)
    ElMessage({ type: 'success', message: '添加成功!' })
    body = {
        reportId: response.data.reportId,
        orderShoeId: props.orderShoeId
    }
    await axios.post(`${apiBaseUrl}/production/createquantityreportdetail`, body)
    createReportVis.value = false
    getAllQuantityReports()
}
const handleCreateReport = () => {
    createReportVis.value = true
}

const openPreviewDialog = (rowData) => {
    currentReport.value = rowData
    previewVis.value = true
}
const handleSubmit = async (rowData) => {
    ElMessageBox.confirm('确定提交？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    })
    .then(async () => {
        const response = await axios.patch(`${apiBaseUrl}/production/submitquantityreport`, { "reportId": rowData.reportId })
        if (response.status == 200) {
            ElMessage.success("提交成功")
            window.location.reload()
        }
        else {
            ElMessage.error("提交失败")
        }
    }).catch(() => {
        ElMessage.info("取消提交");
    })
}

const handleDelete = (row, index) => {
    ElMessageBox.confirm('确定删除此行吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        const params = { "reportId": row.reportId }
        await axios.delete(`${apiBaseUrl}/production/deletequantityreport`, { params })
        taskData.value.splice(index, 1)
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
}
const handleClose = (option) => {
    if (option === 0) createVis.value = false
    else if (option === 1) previewVis.value = false
}
</script>
