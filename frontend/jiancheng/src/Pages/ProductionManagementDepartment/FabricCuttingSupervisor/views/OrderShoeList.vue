<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">裁断与批皮数量填报</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" :column="2" border>
                        <el-descriptions-item label="订单编号">{{ currentOrderData.orderId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ currentOrderData.createTime }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <el-table :data="taskData" border>
                <el-table-column prop="orderShoeId" label="鞋型号"></el-table-column>
                <el-table-column prop="team" label="工组"></el-table-column>
                <el-table-column prop="statusName" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.reportStatus === -1" type="primary"
                            @click="handleGenerate(scope.row)">生成</el-button>
                        <el-button v-if="scope.row.reportStatus === 0" type="primary"
                            @click="handleClick(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
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
import AmountOrderList from '../components/AmountProduced/AmountOrderList.vue';
import axios from 'axios';
import AllHeader from '@/components/AllHeader.vue';
import router from '@/router';
import Cookies from 'js-cookie';

const currentOrderData = JSON.parse(Cookies.get("currentOrderData"))
const dialogVisible = ref(false);
const orderShoeId = ref('')
const selectedTeam = ref('')
const components = {
    AmountOrderList
}
const taskData = ref([])
const order_shoe_teams = ref({})
onMounted(async () => {
    const params = {
        "orderId": currentOrderData.orderId,
        "ordershoestatus": 23
    }
    const response = await axios.get("http://localhost:8000/production/getallordershoes", { params })
    let teams_dict = {}
    response.data.forEach(row => {
        if (row.reportStatus == -1) {
            row["statusName"] = "未创建产量单"
        } else if (row.reportStatus == 0) {
            row["statusName"] = "已保存产量单"
        }
        else if (row.reportStatus == 1) {
            row["statusName"] = "已提交产量单"
        } else {
            row["statusName"] = "已审核产量单"
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
        await axios.post('http://localhost:8000/fabriccutting/createquantityreport', data)
        dialogVisible.value = false
        window.location.reload();
    } catch (error) {
        console.log(error)
    }
}

const handleClick = (rowData) => {
    Cookies.set("currentAmountReportList", JSON.stringify(rowData))
    router.push({ name: 'fabriccutting-ordershoelist-amountreportlist' })
}
</script>
