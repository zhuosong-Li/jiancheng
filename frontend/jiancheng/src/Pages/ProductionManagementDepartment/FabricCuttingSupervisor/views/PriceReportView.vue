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
                <el-table-column prop="team" label="工组"></el-table-column>
                <el-table-column prop="statusName" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.reportStatus === -1" type="primary"
                            @click="handleGenerate(scope.row)">生成</el-button>
                        <el-button-group v-else-if="scope.row.reportStatus === 0">
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
                <PriceReportCreator :teams="order_shoe_teams[orderShoeId]" :handleClose="handleClose" />
            </div>
            <!-- <el-dialog :title="currentTitle" v-model="previewVis" width="90%"
                @close="handleClose(1)">
                hello
            </el-dialog> -->
            <el-dialog v-model="dialogVisible" width="600px">
                <h3>选择工组</h3>
                <el-select v-model="selectedTeam" placeholder="工组" style="width: 240px">
                    <el-option v-for="item in order_shoe_teams[orderShoeId]" :value="item" />
                </el-select>
                <template #footer>
                    <span>
                        <el-button @click="dialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="handleSaveTeam" :disabled="selectedTeam==''">生成</el-button>
                    </span>
                </template>
            </el-dialog>
        </el-main>
    </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import PriceReportCreator from '../components/LaborPriceReport/PriceReportCreator.vue'
import AllHeader from '@/components/AllHeader.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
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
const order_shoe_teams = ref({})
const orderShoeId = ref('')
const selectedTeam = ref('')
const dialogVisible = ref(false);
onMounted(async () => {
    let teams = []
    axios.get("http://localhost:8000/production/getallteams?line=cutting").then(response => {
        response.data.forEach(team => {
            teams.push(team)
        })
    })
    const params = {
        "orderId": props.orderId,
        "ordershoestatus": 20
    }
    let teams_dict = {}
    const response = await axios.get("http://localhost:8000/production/getallordershoes", { params })
    response.data.forEach(row => {
        order_shoe_teams.value[row["orderShoeId"]] = structuredClone(teams)
        if (row.reportStatus == -1) {
            row["statusName"] = "未生成工价单"
        } else if (row.reportStatus == 0) {
            row["statusName"] = "已保存工价单"
        }
        else if (row.reportStatus == 1) {
            row["statusName"] = "已提交工价单"
        } else {
            row["statusName"] = "已审核工价单"
        }
        if (!(row["orderShoeId"] in teams_dict)) {
            teams_dict[row["orderShoeId"]] = new Set([row.team])
        }
        else {
            teams_dict[row["orderShoeId"]].add(row.team)
        }
        taskData.value.push(row)
    })
    for (const key in order_shoe_teams.value) {
        order_shoe_teams.value[key] = order_shoe_teams.value[key].filter(element => !teams_dict[key].has(element))
    }
})

const handleGenerate = (rowData) => {
    dialogVisible.value = true
    orderShoeId.value = rowData["orderShoeId"]
}

const handleSaveTeam = async () => {
    const data = {
        "order_shoe_id": orderShoeId.value,
        "team": selectedTeam.value
    }
    try {
        await axios.post('http://localhost:8000/production/createpricereport', data)
        dialogVisible.value = false
        window.location.reload();
    } catch (error) {
        console.log(error)
    }
}

const handleEdit = (rowData) => {
    orderShoeId.value = rowData["orderShoeId"]
    createVis.value = true
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
