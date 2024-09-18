<template>
    <el-row :gutter="20">
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderNumberSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeNumberSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            <el-button type="primary" @click="getTableData()">搜索</el-button>
        </el-col>
    </el-row>
    <el-table :data="tableData" border stripe height="400">
        <el-table-column prop="orderRId" label="订单号"></el-table-column>
        <el-table-column prop="shoeRId" label="工厂型号"></el-table-column>
        <el-table-column prop="customerProductName" label="客人号"></el-table-column>
        <el-table-column prop="inboundAmount" label="鞋型入库数量" :formatter="formatDecimal"></el-table-column>
        <el-table-column prop="currentAmount" label="鞋型库存" :formatter="formatDecimal"></el-table-column>
        <el-table-column prop="object" label="鞋型部件"></el-table-column>
        <el-table-column prop="statusName" label="状态"></el-table-column>
        <el-table-column label="操作" width="200">
            <template #default="scope">
                <el-button type="primary" size="small" @click="viewRecords(scope.row)">入/出库记录</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>
    <el-dialog title="半成品入库/出库记录" v-model="isRecordDialogVisible" width="60%">
        <el-table :data="recordData" border stripe>
            <el-table-column prop="opType" label="操作类型"></el-table-column>
            <el-table-column prop="date" label="操作时间"></el-table-column>
            <el-table-column prop="amount" label="操作数量"></el-table-column>
        </el-table>
    </el-dialog>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            isRecordDialogVisible: false,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            pageSize: 10,
            currentPage: 1,
            tableData: [],
            totalRows: 0,
        }
    },
    mounted() {
        this.getTableData()
    },
    methods: {
        formatDecimal(row, column, cellValue, index) {
            return Number(cellValue).toFixed(2)
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getTableData()
        },
        async getTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderNumberSearch,
                "shoeRId": this.shoeNumberSearch
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsemifinishedinoutoverview`, { params })
            this.tableData = response.data.result
            this.totalRows = response.data.total
        },
        async viewRecords(row) {
            const params = { "storageId": row.storageId }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsemifinishedinoutboundrecords`, { params })
            this.recordData = response.data
            this.isRecordDialogVisible = true
        },
    }
}
</script>