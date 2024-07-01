<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">裁断与批皮数量填报</el-col>
            </el-row>
            <el-row>
                <el-button link @click="handleGoBack">
                    <el-icon>
                        <Back />
                    </el-icon>
                    <span>返回</span>
                </el-button>
            </el-row>
            <el-row>
                <el-button type="primary" @click="handleCreateReport">
                    <span>新建生产数量表</span>
                </el-button>
            </el-row>
            <el-dialog title="请选择日期" v-model="createReportVis">
                <div class="block">
                    <el-date-picker v-model="dateValue" type="date" :disabled-date="disabledDate"
                        value-format="YYYY-MM-DD" placeholder="请选择日期" />
                </div>
                <el-button type="primary" @click="handleConfirmCreate">
                    <span>确定</span>
                </el-button>
            </el-dialog>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions>
                        <el-descriptions-item label="订单编号">{{ currentOrderData.orderId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ reportList.shoeTypeId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ currentOrderData.createTime }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <hr />
            <el-table :data="taskData" :default-sort="{ prop: 'date', order: 'ascending' }">
                <el-table-column prop="date" label="日期" sortable></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.status === '已填写生产数量表'" type="success"
                            @click="openPreviewDialog(scope.row)">查看</el-button>
                        <el-button-group v-else-if="scope.row.status === '未填写生产数量表'">
                            <el-button type="primary" class="block-button"
                                @click="handleGenerate(scope.row)">编辑</el-button>
                            <el-button type="success" class="block-button"
                                @click="openPreviewDialog(scope.row)">查看</el-button>
                            <el-button type="warning" class="block-button"
                                @click="handleConfirm(scope.row)">提交</el-button>
                            <el-button type="danger" class="block-button"
                                @click="handleDelete(scope.$index)">删除</el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
            <div v-if="createVis">
                <AmountReportCreator :tableInput="tableInput[currentId]" :handleSave="handleSave"
                    :handleClose="handleClose" />
            </div>
            <!-- <el-dialog :title="currentTitle" v-model="previewVis" width="90%"
                @close="handleClose(1)">
                hello
            </el-dialog> -->
        </el-main>
    </el-container>
</template>

<script setup>
import { ref, watch } from 'vue';
import AmountReportCreator from '../components/AmountProduced/AmountReportCreator.vue'
import AllHeader from '@/components/AllHeader.vue';
import router from '@/router';
import Cookies from 'js-cookie';
import { ElMessage, ElMessageBox } from 'element-plus';
const createVis = ref(false)
const createReportVis = ref(false)
const previewVis = ref(false)
const currentTitle = ref('')
const rawData = {
    shareData: { "amount": 0, "remain": 500 },
    uniqueData: [
        {
            "rowId": 1,
            "name": "小明",
            "procedure": "单鞋E",
            "unitPrice": 0.03,
            "totalPrice": 0
        },
        {
            "rowId": 2,
            "name": "小红",
            "procedure": "单鞋E",
            "unitPrice": 0.12,
            "totalPrice": 0
        },
        {
            "rowId": 3,
            "name": "小明",
            "procedure": "批-22片",
            "unitPrice": 0.12,
            "totalPrice": 0
        },
        {
            "rowId": 4,
            "name": "小红",
            "procedure": "批-22片",
            "unitPrice": 0.45,
            "totalPrice": 0
        }
    ]
}
const props = defineProps({
    'orderId': String,
    'createTime': String,
    'prevTime': String,
    'prevDepart': String,
    'prevUser': String
})
const taskData = ref([])
for (let i = 0; i < 2; i++) {
    taskData.value.push(
        {
            date: "2024-06-1" + i.toString(),
            status: "未填写生产数量表"
        }
    )
}
for (let i = 2; i < 4; i++) {
    taskData.value.push(
        {
            date: "2024-06-1" + i.toString(),
            status: "已填写生产数量表"
        }
    )
}

const tableInput = ref({})
const currentId = ref('')
const dateValue = ref('')
const reportList = JSON.parse(Cookies.get('currentAmountReportList'))
const currentOrderData = JSON.parse(Cookies.get('currentOrderData'))
const createdDates = ref(new Set())
taskData.value.forEach((data) => {
    tableInput.value[reportList.shoeTypeId + data.date] = JSON.parse(JSON.stringify(rawData))
    createdDates.value.add(data.date)
})

const dateFormatter = (input) => {
    const date = new Date(input);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate
}

watch(taskData, () => {
    createdDates.value = new Set(taskData.value.map(e => e.date));
}, { deep: true })

const handleGenerate = (rowData) => {
    createVis.value = true
    currentId.value = reportList.shoeTypeId + rowData.date
}
const disabledDate = (time) => {
    const startDate = new Date(currentOrderData.createTime)
    const endDate = new Date()
    return time.getTime() < startDate || time.getTime() > endDate.getTime() || createdDates.value.has(dateFormatter(time));
}
const handleConfirmCreate = () => {
    if (dateValue.value.length === 0) {
        ElMessage({ type: 'warning', message: '未选择一个日期!' })
        return
    }
    if (createdDates.value.has(dateValue.value)) {
        ElMessage({ type: 'warning', message: '已有该日期的报告!' })
        return
    }
    taskData.value.push({
        date: dateValue.value,
        status: "未填写生产数量表"
    })
    ElMessage({ type: 'success', message: '添加成功!' })
    tableInput.value[reportList.shoeTypeId + dateValue.value] = JSON.parse(JSON.stringify(rawData))
}
const handleCreateReport = () => {
    createReportVis.value = true
}

const openPreviewDialog = (rowData) => {
    currentTitle.value = "鞋型号 " + rowData.shoeTypeId
    previewVis.value = true
}
const handleConfirm = (e) => {
    console.log(e)
}
const handleSave = (data) => {
    tableInput.value[currentId.value] = data
}
const handleDelete = (index) => {
    ElMessageBox.confirm('确定删除此行吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
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
const handleGoBack = () => {
    router.push({ name: 'fabriccutting-shoetypelist' })
}
const handleClose = (option) => {
    if (option === 0) createVis.value = false
    else if (option === 1) previewVis.value = false
}
</script>
<style scoped>
.block-button {
    display: block;
}
</style>