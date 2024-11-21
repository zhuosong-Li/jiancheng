<template>
    <div class="content">
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
            <el-button :disabled="!flagShow" type="primary" @click="showexamineData()"
                >审批订单</el-button
            >
            <el-button :disabled="flagShow" type="primary" @click="showAllData()"
                >所有订单</el-button
            >
        </el-row>
        <el-row :gutter="20">
            <el-table :data="displayData" stripe height="650">
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
                            v-show="!flagShow"
                            type="primary"
                            @click="openOrderDetail(scope.row.orderDbId)"
                            >审批生产订单</el-button
                        >
                        <el-button
                            v-show="flagShow"
                            type="primary"
                            @click="deleteOrder(scope.row.orderRid)"
                            >删除订单</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
        <el-row :gutter="20" style="justify-content: end; width: 100%">
            <el-pagination
                @size-change="chageCurrentPageSize"
                @current-change="changeCurrentPage"
                :current-page="currentPage"
                :page-sizes="[10, 20, 30, 40]"
                :page-size="currentPageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="currentTotalRows"
            />
        </el-row>
    </div>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
import axios from 'axios'
import { ref, onMounted, getCurrentInstance } from 'vue'
import { ElMessage } from 'element-plus'

let orderRidFilter = ref('')
let orderCidFilter = ref('')
let displayData = ref([])
let unfilteredData = ref([])
let filterData = ref([])
let allData = ref([])
let flagShow = ref(false)
let isFilter = ref(false)
const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$apiBaseUrl

let currentPage = ref(1)
let currentPageSize = ref(10)
let currentTotalRows = ref(0)

onMounted(() => {
    getAllOrders()
})

async function getAllOrders() {
    const response = await axios.get(`${$api_baseUrl}/order/getallorders`)
    allData.value = response.data
    // 此处需要增加订单状态筛选功能，保留状态为生产订单确认的数据
    const arr = []
    for (let i = 0; i < response.data.length; i++) {
        if (response.data[i].orderStatus === '生产订单总经理确认') {
            arr.push(response.data[i])
        }
    }
    unfilteredData.value = arr
    displayData.value = unfilteredData.value
    currentTotalRows.value = displayData.value.length
}

async function deleteOrder(value) {
    // 此处更换删除订单的路由
    const response = await axios.post(`${$api_baseUrl}/order/getallorders`, {'orderRid': value})
    if (response.status === 200) {
        ElMessage.success('删除成功,数据正在更新,请稍后')
        getAllOrders()
    } else {
        ElMessage.error('修改失败')
    }
    
}

function openOrderDetail(orderId) {
    let url = ''
    url = `${window.location.origin}/companyManager/orderConfirmDetail/orderid=${orderId}`
    window.open(url, '_blank')
}

function filterByRid() {
    if (!orderRidFilter.value) {
        if (!flagShow.value) {
            displayData.value = unfilteredData.value
        } else {
            displayData.value = allData.value
        }
    } else {
        if (flagShow.value) {
            filterData.value = allData.value.filter((task) => {
                const filterMatch = task.orderRid.includes(orderRidFilter.value)
                return filterMatch
            })
        } else {
            filterData.value = unfilteredData.value.filter((task) => {
                const filterMatch = task.orderRid.includes(orderRidFilter.value)
                return filterMatch
            })
        }
        isFilter.value = true
    }
    if (isFilter.value) {
        dataCut2()
    } else {
        dataCut()
    }
}
function filterByCid() {
    if (!orderCidFilter.value) {
        if (!flagShow.value) {
            displayData.value = unfilteredData.value
        } else {
            displayData.value = allData.value
        }
    } else {
        if (flagShow.value) {
            filterData.value = allData.value.filter((task) => {
                const filterMatch = task.orderCid.includes(orderCidFilter.value)
                return filterMatch
            })
        } else {
            filterData.value = unfilteredData.value.filter((task) => {
                const filterMatch = task.orderCid.includes(orderCidFilter.value)
                return filterMatch
            })
        }
        isFilter.value = true
    }
    if (isFilter.value) {
        dataCut2()
    } else {
        dataCut()
    }
}

function showAllData() {
    displayData.value = allData.value
    currentTotalRows.value = displayData.value.length
    flagShow.value = true
    orderRidFilter.value = ''
    orderCidFilter.value = ''
    isFilter.value = false
    dataCut()
}

function showexamineData() {
    displayData.value = unfilteredData.value
    currentTotalRows.value = displayData.value.length
    flagShow.value = false
    orderRidFilter.value = ''
    orderCidFilter.value = ''
    isFilter.value = false
    dataCut()
}

function chageCurrentPageSize(val) {
    if (currentPageSize.value !== val) {
        currentPageSize.value = val
        if (isFilter.value) {
            dataCut2()
        } else {
            dataCut()
        }
    }
}

function changeCurrentPage(val) {
    if (currentPage.value !== val) {
        currentPage.value = val
        if (isFilter.value) {
            dataCut2()
        } else {
            dataCut()
        }
    }
}
function dataCut() {
    if (!flagShow.value) {
        displayData.value = unfilteredData.value.slice(
            (currentPage.value - 1) * currentPageSize.value,
            currentPageSize.value * currentPage.value
        )
    } else {
        displayData.value = allData.value.slice(
            (currentPage.value - 1) * currentPageSize.value,
            currentPageSize.value * currentPage.value
        )
    }
}
function dataCut2() {
    currentTotalRows.value = filterData.value.length
    displayData.value = filterData.value.slice(
        (currentPage.value - 1) * currentPageSize.value,
        currentPageSize.value * currentPage.value
    )
}
</script>

<style scoped>
.content {
    height: calc(100% - 40px);
}
</style>
