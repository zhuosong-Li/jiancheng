<template>
	<div>
		<el-row :gutter="20" style="margin-top: 20px">
			<el-col :span="4" :offset="0" style="white-space: nowrap;">
				订单号筛选：
				<el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable @keypress.enter="getInproductionTableData()"
					@clear="getInproductionTableData()" />
			</el-col>
		</el-row>
		<el-table :data="inProductionTableData" style="width: 100%; margin-bottom: 20px" row-key="id" border
			default-expand-all>
			<el-table-column label="订单信息">
				<el-table-column prop="orderRId" label="订单编号" sortable />
				<el-table-column prop="customerName" label="客户名称" sortable />
				<el-table-column prop="orderTotalShoes" label="订单总数量" sortable />
				<el-table-column prop="finishedShoes" label="已生产数量" sortable />
				<el-table-column prop="startDate" label="生产开始日期" sortable />
				<el-table-column prop="endDate" label="预计完成时间" sortable />
				<el-table-column prop="orderEndDate" label="截止日期" sortable />
				<el-table-column label="操作">
					<template #default="scope">
						<el-button link type="primary" size="small" @click="openNewWindow(scope.row)">
							订单详情
						</el-button>
					</template>
				</el-table-column>
			</el-table-column>
		</el-table>
		<el-row :gutter="20">
			<el-col :span="12" :offset="14">
				<el-pagination @size-change="handleInProdSizeChange" @current-change="handleInProdPageChange"
					:current-page="inProdPage" :page-sizes="[10, 20, 30, 40]" :page-size="inProdPageSize"
					layout="total, sizes, prev, pager, next, jumper" :total="inproductionTotalRows" />
			</el-col>
		</el-row>
	</div>
</template>
<script>
import axios from 'axios'
export default {
	props: ["character"],
	data() {
		return {
			inProductionTableData: [],
			inproductionTotalRows: 0,
			inProdPage: 1,
			inProdPageSize: 10,
			orderRIdSearch: ""
		}
	},
	mounted() {
		this.getInproductionTableData()
	},
	methods: {
		async getInproductionTableData() {
			const params = {
				"page": this.inProdPage,
				"pageSize": this.inProdPageSize,
				"orderRId": this.orderRIdSearch
			}
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getinprogressorders`, { params })
			this.inProductionTableData = response.data.result
			this.inproductionTotalRows = response.data.total
		},
		handleInProdSizeChange(val) {
			this.inProdPageSize = val
			this.getInproductionTableData()
		},
		handleInProdPageChange(val) {
			this.inProdPage = val
			this.getInproductionTableData()
		},
		openNewWindow(rowData) {
			let url = ""
			let params = {
				"orderId": rowData.orderId,
				"orderRId": rowData.orderRId
			}
			const queryString = new URLSearchParams(params).toString();
			url = `${window.location.origin}/productiongeneral/productiondetail?${queryString}`
			window.open(url, '_blank')
		},
		calculateDailyProduction(dateRange) {
			if (dateRange && dateRange.length === 2) {
				const startDate = new Date(dateRange[0]);
				const endDate = new Date(dateRange[1]);
				const timeDiff = Math.abs(endDate - startDate);
				const diffDays = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
				return (5000 / diffDays).toFixed(2);
			}
			return 0;
		},
	}
}
</script>
