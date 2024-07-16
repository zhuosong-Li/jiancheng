<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center; color: black;">针车工价填报</el-col>
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
        <el-col :span="24">
            <component :is="components[currentDash]" :taskData="taskData">
            </component>
        </el-col>
    </el-row>
</template>
<script setup>
import OrderList from './LaborPriceReport/OrderList.vue'
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue';
const components = {
    OrderList
}
let taskData = []
const input3 = ref('')
const select = ref('')
for (let i = 0; i < 4; i++) {
    taskData.push(
        {
            orderId: "K24-024 " + i.toString(),
            customerId: "37",
            createTime: "2024-06-10",
            prevTime: "2024-06-10 18:00:00",
            prevDepart: "技术部",
            prevUser: "XXX"
        }
    )
}
const currentDash = ref('OrderList')
</script>