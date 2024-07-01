<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center; color: black">裁断与批皮数量填报</el-col>
    </el-row>
    <component :is="components[currentDash]" :taskData="taskData">
    </component>
</template>
<script setup>

import AmountProducedList from './AmountProduced/AmountOrderList.vue'
import { ref } from 'vue';
const components = {
    AmountProducedList
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
const currentDash = ref('AmountProducedList')
// const changeToList = () => {
//     currentDash.value = 'PriceReportList'
// }
// const changeToPend = () => {
//     currentDash.value = 'PriceReportPend'
// }
// const changeToProgress = () => {
//     currentDash.value = 'PriceReportProgress'
// }
</script>