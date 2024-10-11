<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">每日生产数量确认</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getOrderTableData()" @clear="getOrderTableData()"/>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getOrderTableData()" @clear="getOrderTableData()"/>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            当前日期为 {{ currentDate() }}, 表格填报情况为 {{ daysBefore(1) }} 的生产数量
        </el-col>
    </el-row>

    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table :data="orderTableData" border stripe :cell-style="cellStyle">
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客户型号"></el-table-column>
                <el-table-column prop="cuttingAmount" label="昨日裁断数量上报"></el-table-column>
                <el-table-column prop="preSewingAmount" label="昨日针车预备数量上报"></el-table-column>
                <el-table-column prop="sewingAmount" label="昨日针车数量上报"></el-table-column>
                <el-table-column prop="moldingAmount" label="昨日成型数量上报"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default"
                            @click="openAmountApproval(scope.row)">打开生产数量审批页面</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="15">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            orderRIdSearch: '',
            shoeRIdSearch: '',
            orderTableData: [],
            totalRows: 0,
            currentPage: 1,
            pageSize: 10
        }
    },
    mounted() {
        this.getOrderTableData()
    },
    methods: {
        async getOrderTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch
            }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getallquantityreportsoverview`, {params})
            this.orderTableData = response.data.result
            this.totalRows = response.data.totalLength
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getOrderTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getOrderTableData()
        },
        cellStyle(cell) {
            if (cell.row.isCuttingApproval == false && cell.column.label === '昨日裁断数量上报') {
                return { color: 'red' }
            }
            if (cell.row.isSewingApproval == false && cell.column.label === '昨日针车数量上报') {
                return { color: 'red' }
            }
            if (cell.row.isMoldApproval == false && cell.column.label === '昨日成型数量上报') {
                return { color: 'red' }
            }
        },
        currentDate() {
            const date = new Date()
            return date.toDateString()
        },
        daysBefore(num) {
            const date = new Date()
            const returnDate = new Date()
            returnDate.setDate(date.getDate() - num)
            return returnDate.toDateString()
        },
        openAmountApproval(rowData) {
			const params = {
				"orderId": rowData.orderId,
				"orderRId": rowData.orderRId,
				"orderShoeId": rowData.orderShoeId,
				"shoeRId": rowData.shoeRId,
				"orderStartDate": rowData.orderStartDate,
				"orderEndDate": rowData.orderEndDate,
				"customerProductName": rowData.customerProductName,
			}
			const queryString = new URLSearchParams(params).toString();
			const url = `${window.location.origin}/productiongeneral/productionamountapproval?${queryString}`
			window.open(url, '_blank')
        }
    }
}
</script>
