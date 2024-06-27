<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center; color: black;">成型工价填报</el-col>
    </el-row>
    <component :is="components[currentDash]" :taskData="taskData">
    </component>
</template>
<script setup>
import OrderList from './LaborPriceReport/OrderList.vue'
import { ref } from 'vue';
const components = {
    OrderList
}
let taskData = []
for (let i = 0; i < 2; i++) {
    taskData.push(
        {
            orderId: "K24-024 " + i.toString(),
            createTime: "2024-06-10",
            prevTime: "2024-06-10 18:00:00",
            prevDepart: "技术部",
            prevUser: "XXX"
        }
    )
}
for (let i = 2; i < 4; i++) {
    taskData.push(
        {
            orderId: "K24-024 " + i.toString(),
            createTime: "2024-06-10",
            prevTime: "2024-06-10 18:00:00",
            prevDepart: "技术部",
            prevUser: "XXX"
        }
    )
}
const currentDash = ref('OrderList')
</script>
