<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">针车数量填报</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" :column="2">
                        <el-descriptions-item label="订单编号">{{ currentOrderData.orderId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ currentOrderData.createTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序流程下发时间">{{ currentOrderData.prevTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理部门">{{ currentOrderData.prevDepart }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理人">{{ currentOrderData.prevUser }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <el-table :data="taskData">
                <el-table-column prop="shoeTypeId" label="鞋型号"></el-table-column>
                <el-table-column prop="groupType" label="工组"></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" @click="handleClick(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>

<script setup>
import { ref } from 'vue';
import AmountOrderList from '../components/AmountProduced/AmountOrderList.vue';

import AllHeader from '@/components/AllHeader.vue';
import router from '@/router';
import Cookies from 'js-cookie';
const props = defineProps({
    'orderId': String,
    'createTime': String,
    'prevTime': String,
    'prevDepart': String,
    'prevUser': String
})
const currentOrderData = JSON.parse(Cookies.get("currentOrderData"))
const components = {
    AmountOrderList
}
let taskData = []
for (let i = 0; i < 2; i++) {
    taskData.push(
        {
            shoeTypeId: "G20240601 " + i.toString(),
            status: "未完成2天生产数量表",
            groupType: "线上组"
        }
    )
}
for (let i = 2; i < 4; i++) {
    taskData.push(
        {
            shoeTypeId: "G20240601 " + i.toString(),
            status: "完成所有生产数量表",
            groupType: "预备组"
        }
    )
}
const handleClick = (rowData) => {
    Cookies.set("currentAmountReportList", JSON.stringify(rowData))
    router.push({ name: 'sewingMachine-shoetypelist-amountreportlist'})
}
</script>
<style scoped>
.block-button {
    display: block;
}
</style>