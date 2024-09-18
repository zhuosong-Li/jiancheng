<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">外包信息页面</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getOutsourceOverview()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getOutsourceOverview()" />
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table :data="orderTableData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="ShoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客户型号"></el-table-column>
                <el-table-column prop="isCuttingOutsourced" label="裁断外包"></el-table-column>
                <el-table-column prop="isSewingOutsourced" label="针车外包"></el-table-column>
                <el-table-column prop="isMoldingOutsourced" label="成型外包"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default"
                            @click="startOutSourceFlow(scope.row)">打开鞋型外包页面</el-button>

                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
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
            currentPage: 1,
            pageSize: 10,
            totalRows: 0
        }
    },
    mounted() {
        this.getOutsourceOverview()
    },
    methods: {
        handleSizeChange(val) {
            this.pageSize = val
            this.getOutsourceOverview()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getOutsourceOverview()
        },
        async getOutsourceOverview() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch
            }
            const response = await axios.get("http://localhost:8000/production/productionmanager/getorderoutsourceoverview", {params})
            this.orderTableData = response.data.result
            this.totalRows = response.data.totalLength
        },
		startOutSourceFlow(rowData) {
			const params = {
				"orderId": rowData.orderId,
				"orderRId": rowData.orderRId,
				"orderShoeId": rowData.orderShoeId,
				"shoeRId": rowData.shoeRId,
				"orderStartDate": rowData.orderStartDate,
				"orderEndDate": rowData.orderEndDate,
				"customerName": rowData.customerName,
			}
			const queryString = new URLSearchParams(params).toString();
			const url = `${window.location.origin}/productiongeneral/productionoutsource?${queryString}`
			window.open(url, '_blank')
		},
    },

}
</script>
