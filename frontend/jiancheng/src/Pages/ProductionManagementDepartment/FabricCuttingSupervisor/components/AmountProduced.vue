<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center; color: black">裁断与批皮数量填报</el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="8" :offset="16">
            <el-input v-model="input3" style="max-width: 600px" placeholder="搜索" clearable @input="filterData">
                <template #prepend>
                    <el-select v-model="select" placeholder="选择" style="width: 115px">
                        <el-option label="订单号" value="1" />
                        <el-option label="客户号" value="2" />
                    </el-select>
                </template>
                <template #append>
                    <el-button :icon="Search" />
                </template>
            </el-input>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <component :is="components[currentDash]" :taskData="taskData">
        </component>
    </el-row>
</template>
<script setup>

import AmountProducedList from './AmountProduced/AmountOrderList.vue'
import { ref } from 'vue';
import { Search } from '@element-plus/icons-vue'
const components = {
    AmountProducedList
}
const input3 = ref('')
const select = ref('')
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