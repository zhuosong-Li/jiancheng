<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center; color: black">针车数量填报</el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="4" :offset="19"><el-input v-model="searchOrder" placeholder="请输入订单号" size="default"
                :suffix-icon="Search" clearable @input="filterData"></el-input>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
            <component :is="components[currentDash]" :taskData="taskData">
            </component>
        </el-col>
    </el-row>
</template>
<script setup>
import { Search } from '@element-plus/icons-vue'
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
</script>