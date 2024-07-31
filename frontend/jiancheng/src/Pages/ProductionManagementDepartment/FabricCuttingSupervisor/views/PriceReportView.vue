<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">{{ props.taskName
                    }}</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" :column="3" border>
                        <el-descriptions-item label="订单编号">{{ props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ props.createTime }}</el-descriptions-item>
                        <el-descriptions-item label="客户">{{ props.customerName }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <el-table :data="taskData" border>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="date" label="提交日期"></el-table-column>
                <el-table-column prop="statusName" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.statusName === '未生成工价单'" type="primary"
                            @click="handleGenerate(scope.row)">生成</el-button>
                        <el-button-group v-else-if="scope.row.statusName === '已保存工价单'">
                            <el-button type="primary" class="block-button" @click="handleEdit(scope.row)">编辑</el-button>
                            <el-button type="success" class="block-button"
                                @click="openPreviewDialog(scope.row)">预览</el-button>
                            <el-button type="warning" class="block-button"
                                @click="handleConfirm(scope.row)">提交</el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
            <div v-if="createVis">
                <PriceReportCreator :orderShoeId="orderShoeId" :handleClose="handleClose" />
            </div>
            <!-- <el-dialog :title="currentTitle" v-model="previewVis" width="90%"
                @close="handleClose(1)">
                hello
            </el-dialog> -->
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import PriceReportCreator from '../components/LaborPriceReport/PriceReportCreator.vue'
import AllHeader from '@/components/AllHeader.vue';
const createVis = ref(false)
const previewVis = ref(false)
const currentTitle = ref('')
const props = defineProps({
    'orderId': Number,
    'orderRId': String,
    'createTime': String,
    'customerName': String,
    'taskName': String
})
const taskData = ref([])
const orderShoeId = ref('')
onMounted(async () => {
    const params = {
        "orderId": props.orderId,
        "ordershoestatus": 20
    }
    const response = await axios.get("http://localhost:8000/production/getallordershoespricereport", { params })
    for (const key in response.data) {
        let value = response.data[key]
        let obj = { "orderShoeId": key, "shoeRId": value.shoeRId, "date": value.date }
        if (value.status == -1) {
            obj["statusName"] = "未生成工价单"
        } else if (value.status == 0) {
            obj["statusName"] = "已保存工价单"
        }
        else if (value.status == 1) {
            obj["statusName"] = "已提交工价单"
        } else {
            obj["statusName"] = "已审核工价单"
        }
        taskData.value.push(obj)
    }
})

const handleGenerate = async (rowData) => {
    orderShoeId.value = rowData["orderShoeId"]
    const data = {
        "orderShoeId": orderShoeId.value,
        "line": "cutting"
    }
    await axios.post("http://localhost:8000/production/createpricereport", data)
    window.location.reload()
}

const handleEdit = (rowData) => {
    createVis.value = true
    orderShoeId.value = rowData["orderShoeId"]
}
const openPreviewDialog = (rowData) => {
    currentTitle.value = "鞋型号 " + rowData.shoeTypeId
    previewVis.value = true
}
const handleConfirm = (e) => {
    console.log(e)
}
const handleClose = (option) => {
    if (option === 0) createVis.value = false
    else if (option === 1) previewVis.value = false
}
</script>
