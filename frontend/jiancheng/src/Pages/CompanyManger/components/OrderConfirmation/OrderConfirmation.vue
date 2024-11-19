<template>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0"
            ><el-input
                v-model="orderRidFilter"
                placeholder="请输入订单号"
                size="default"
                :suffix-icon="Search"
                clearable
                @input="filterByRid()"
            ></el-input>
        </el-col>
        <el-col :span="4" :offset="0"
            ><el-input
                v-model="orderCidFilter"
                placeholder="请输入客户订单号"
                size="default"
                :suffix-icon="Search"
                clearable
                @input="filterByCid()"
            ></el-input>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="displayData" border stripe height="650">
            <el-table-column type="index" width="50" />
            <el-table-column prop="orderRid" label="订单号" />
            <el-table-column prop="customerName" label="客户名" />
            <el-table-column prop="orderCid" label="客户订单号" />
            <el-table-column prop="orderStartDate" label="订单开始日期" sortable />
            <el-table-column prop="orderEndDate" label="订单结束日期" sortable />
            <el-table-column prop="orderStatus" label="订单状态" />
            <el-table-column label="操作" width="300">
                <template #default="scope">
                    <el-button
                        type="primary"
                        size="default"
                        @click="openOrderDetail(scope.row.orderDbId)"
                        >审批生产订单</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
    </el-row>
</template>

<script setup>
import { Download, Search, Upload } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref, onMounted,getCurrentInstance } from 'vue'

let orderRidFilter = ref('')
let orderCidFilter = ref('')
let displayData = ref([])
let unfilteredData = ref([])
let filterData = ref([])
const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$api_baseUrl

onMounted(() => {
    getAllOrders()
})

async function getAllOrders() {
    const response = await axios.get(`${$api_baseUrl}/order/getallorders`)
    // 此处需要增加订单状态筛选功能，保留状态为生产订单确认的数据
    unfilteredData.value = response.data
    displayData.value = unfilteredData.value
}

function openOrderDetail(orderId) {
    let url = ''
    url = `${window.location.origin}/business/businessorderdetail/orderid=${orderId}`
    window.open(url, '_blank')
}

function filterByRid() {
    if (!orderRidFilter.value) {
        displayData.value = unfilteredData.value
    } else {
        filterData.value = unfilteredData.value.filter((task) => {
            const filterMatch = task.orderRid.includes(orderRidFilter.value)
            return filterMatch
        })
        displayData.value = filterData.value
    }
}
function filterByCid() {
    if (!orderCidFilter.value) {
        displayData.value = unfilteredData.value
    } else {
        filterData.value = unfilteredData.value.filter((task) => {
            const filterMatch = task.orderCid.includes(orderCidFilter.value)
            return filterMatch
        })
        displayData.value = filterData.value
    }
}
</script>

<style scoped></style>
