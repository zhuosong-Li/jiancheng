<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
            >订单查询</el-col
        >
    </el-row>
    <el-row :gutter="20">
        <el-col :span="6" :offset="0" style="white-space: nowrap">
            订单号搜索：
            <el-input
                v-model="orderSearch"
                placeholder=""
                size="normal"
                :suffix-icon="Search"
                clearable
                @change="tableFilter"
            ></el-input>
        </el-col>
        <el-col :span="6" :offset="6" style="white-space: nowrap">
            客人名称搜索：
            <el-input
                v-model="customerSearch"
                placeholder=""
                size="normal"
                :suffix-icon="Search"
                clearable
                @change="tableFilter"
            ></el-input>
        </el-col>
    </el-row>
    <el-row>
        <el-table :data="orderFilterData" border stripe height="600">
            <el-table-column type="expand">
                <template #default="props">
                    <el-table :data="props.row.shoes" :border="true">
                        <el-table-column label="工厂型号" prop="shoeRid" />
                        <el-table-column label="客户型号" prop="customerId" />
                        <el-table-column label="一次BOM编号" prop="firstBom">
                            <template #default="scope">
                                <el-link
                                    :disabled="scope.row.firstBom === 'N/A'"
                                    :underline="false"
                                    type="primary"
                                    @click="handleFirstBomDetail(scope.row.firstBom)"
                                >
                                    {{ scope.row.firstBom }}
                                </el-link>
                            </template>
                        </el-table-column>
                        <el-table-column label="二次BOM编号" prop="secondBom">
                            <template #default="scope">
                                <el-link
                                    :disabled="scope.row.secondBom === 'N/A'"
                                    :underline="false"
                                    type="primary"
                                    @click="handleSecondBomDetail(scope.row.secondBom)"
                                >
                                    {{ scope.row.secondBom }}
                                </el-link>
                            </template>
                        </el-table-column>
                        <el-table-column label="一次采购订单编号" prop="firstOrder">
                            <template #default="scope">
                                <el-link
                                    :disabled="scope.row.firstOrder === 'N/A'"
                                    :underline="false"
                                    type="primary"
                                    @click="handlePurchaseOrderDetail(scope.row.firstOrder)"
                                >
                                    {{ scope.row.firstOrder }}
                                </el-link>
                            </template>
                        </el-table-column>
                        <el-table-column label="二次采购订单编号" prop="secondOrder">
                            <template #default="scope">
                                <el-link
                                    :disabled="scope.row.secondOrder === 'N/A'"
                                    :underline="false"
                                    type="primary"
                                    @click="handlePurchaseOrderDetail(scope.row.secondOrder)"
                                >
                                    {{ scope.row.secondOrder }}
                                </el-link>
                            </template>
                        </el-table-column>
                        <el-table-column prop="statuses" label="鞋型状态"></el-table-column>
                    </el-table>
                </template>
            </el-table-column>
            <el-table-column prop="orderRid" label="订单号"></el-table-column>
            <el-table-column prop="customerName" label="客人名称"></el-table-column>
            <el-table-column prop="createTime" label="订单日期"></el-table-column>
            <el-table-column prop="deadlineTime" label="交货日期"></el-table-column>
            <el-table-column prop="status" label="订单状态"></el-table-column>
            <el-table-column label="操作" width="350">
                <template #default="scope">
                    <el-button type="primary" size="default" @click="handleRowClick(scope.row)">查看一次采购订单</el-button>
                    <el-button type="primary" size="default" @click="handleSecondRowClick(scope.row)">查看二次采购订单</el-button>
                </template>
            </el-table-column>
            
        </el-table>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="6" :offset="16">
            <el-pagination
                @current-change="handlePageChange"
                v-model:current-page="currentPage"
                :page-sizes="[10, 20, 30, 40]"
                :page-size="10"
                layout="total, sizes, prev, pager, next, jumper"
                :total="totalData"
            ></el-pagination>
        </el-col>
    </el-row>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
    data() {
        return {
            Search,
            orderSearch: '',
            orderData: [],
            orderFilterData: [],
            customerSearch: '',
            currentPage: 1,
            pageSize: 10,
            totalPages: 0,
            totalData: 0,
        }
    },
    async mounted() {
        this.$setAxiosToken()
        await this.getOrderPageInfo()
        await this.getOrderData(this.currentPage)
    },
    methods: {
        async getOrderPageInfo() {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getorderpageinfo`, {
                params: {
                    orderSearch: this.orderSearch,
                    customerSearch: this.customerSearch,
                },
            })
            this.totalData = response.data.totalOrders
            this.totalPages = Math.ceil(this.totalData / this.pageSize)
        },
        async getOrderData(page) {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getorderfullinfo`, {
                params: {
                    page: page,
                    pageSize: this.pageSize,
                    orderSearch: this.orderSearch,
                    customerSearch: this.customerSearch,
                },
            })
            this.orderFilterData = response.data
        },
        handlePageChange(page) {
            this.currentPage = page
            this.getOrderData(page)
        },
        tableFilter() {
            // Reset to the first page on filter
            this.currentPage = 1
            this.getOrderPageInfo()
            this.getOrderData(this.currentPage)
        },
        handleRowClick(row) {
            const url = `${window.location.origin}/logistics/firstpurchase/orderid=${row.orderId}`;
            window.open(url, '_blank');
        },
        handleSecondRowClick(row) {
            const url = `${window.location.origin}/logistics/secondpurchase/orderid=${row.orderId}`;
            window.open(url, '_blank');
        },
    },
}
</script>
