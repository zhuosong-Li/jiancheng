<template>
	<el-container>
		<el-header height="">
			<AllHeader></AllHeader>
		</el-header>
		<el-main height="">
			<el-row :gutter="20" style="text-align: center">
				<el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">订单生产详情</el-col>
			</el-row>
			<el-row :gutter="20">
				<el-col :span="24" :offset="0">
					<el-descriptions title="订单信息" :column="2" border>
						<el-descriptions-item label="客人编号">{{
							$props.customerName
						}}</el-descriptions-item>
						<el-descriptions-item label="订单编号">{{
							$props.orderRId
						}}</el-descriptions-item>
						<el-descriptions-item label="订单创建时间">{{
							$props.orderStartDate
						}}</el-descriptions-item>
						<el-descriptions-item label="订单出货日期">{{
							$props.orderEndDate
						}}</el-descriptions-item>
						<el-descriptions-item label="订单总数量">{{
							$props.orderTotalShoes
						}}</el-descriptions-item>
						<el-descriptions-item label="订单总完成度百分比">{{
							orderPercentageText
						}}</el-descriptions-item>
					</el-descriptions></el-col>
			</el-row>
			<el-row :gutter="20" style="margin-top: 20px">
				<el-col :span="24" :offset="0">
					<el-table :data="orderShoeDataTable" border style="height: 800px">
						<el-table-column type="expand">
							<template #default="props">
								<h3>鞋型详情</h3>
								<el-table :data="props.row.detail" border>
									<el-table-column label="配码编号" prop="batchInfoName" />
									<el-table-column label="颜色" prop="colorName" />
									<el-table-column label="订单总数" prop="batchAmount" />
									<el-table-column label="裁断完成数量" prop="cuttingAmount" />
									<el-table-column label="预备完成数量" prop="preSewingAmount" />
									<el-table-column label="针车完成数量" prop="sewingAmount" />
									<el-table-column label="成型完成数量" prop="moldingAmount" />
									<el-table-column label="面料辅料" prop="materialLogistics" />
									<el-table-column label="扣件拉链鞋带" prop="metalmaterialLogistics" />
									<el-table-column label="鞋底物料" prop="soleLogistics" />
									<el-table-column label="中底物料" prop="insoleLogistics" />
									<el-table-column label="鞋盒物料" prop="packagingMaterialLogistics" />
									<el-table-column label="楦型" prop="lasttypeLogistics" />
									<el-table-column label="完成状态" prop="productionStatus" />
								</el-table>
							</template>
						</el-table-column>

						<el-table-column label="预览图" width="200">
							<template #default="scope">
								<el-image :src="scope.row.imageurl" fit="fill"></el-image>
							</template>
						</el-table-column>
						<el-table-column prop="shoeRId" label="公司编号" width="100"></el-table-column>
						<el-table-column prop="customerProductName" label="客户型号" width="100"></el-table-column>
						<el-table-column prop="percentageText" label="生产状态百分比"></el-table-column>
						<el-table-column prop="totalShoes" label="当前鞋型订单总数"></el-table-column>
						<el-table-column label="操作">
							<template #default="scope">
								<el-button type="primary" size="small"
									@click="viewProductionSchedule(scope.row)">查看排期</el-button>
							</template>
						</el-table-column>
					</el-table>
				</el-col>
			</el-row>
			<el-dialog title="修改排产信息" v-model="isScheduleModify" width="90%">
				<el-tabs v-model="activeTab" type="card" tab-position="top" @tab-click="">
					<el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name">
						<el-row :gutter="20">
							<el-col :span="10" :offset="0">
								<span style="white-space: nowrap">
									{{ tab.lineLabel }}：
									<el-select v-model="tab.lineValue" placeholder="" @change="" multiple disabled>
										<el-option v-for="item in productionLines[tab.name]" :key="item" :label="item"
											:value="item">
										</el-option>
									</el-select>
								</span>
							</el-col>
							<el-col :span="8" :offset="6">
								<el-descriptions title="" border>
									<el-descriptions-item label="外包状态">
										<div v-if="tab.isOutSource === false">
											未设置外包
										</div>
										<div v-else>
											已设置外包
										</div>
									</el-descriptions-item>
								</el-descriptions>
							</el-col>
						</el-row>
						<el-row :gutter="20">
							<el-col :span="10" :offset="0">
								<span>
									{{ tab.dateLabel }}：
									<el-date-picker v-model="tab.dateValue" type="daterange" size="default"
										range-separator="-" disabled>
									</el-date-picker>
								</span>
							</el-col>
							<!-- TODO -->
							<!-- <el-col :span="5" :offset="0">
								<el-button type="primary" size="default" @click="checkDateProductionStatus">查看工期内排产情况</el-button>
							</el-col> -->
							<el-col :span="5" :offset="0">预计每天生产数量：{{ calculateDailyProduction(tab.dateValue)
								}}</el-col>
						</el-row>
						<el-row :gutter="20">
							<el-table v-if="isDateStatusTableVis" :data="dateStatusTable" border stripe>
								<el-table-column type="expand">
									<template #default="props">
										<el-table :data="props.row.shoeList">
											<el-table-column type="index" />
											<el-table-column label="订单号" prop="orderId" />
											<el-table-column label="工厂型号" prop="shoeId" />
											<el-table-column label="鞋型总数量" prop="amount" />
											<el-table-column label="生产周期" prop="datePeriod" />
											<el-table-column label="平均每天数量" prop="averageAmount" />
										</el-table>
									</template>
								</el-table-column>

								<el-table-column prop="date" label="日期"> </el-table-column>
								<el-table-column prop="productAmount" label="已排产鞋型数"> </el-table-column>
								<el-table-column prop="predictAmount" label="预计当日现有生产量"> </el-table-column>
							</el-table>
						</el-row>
					</el-tab-pane>
				</el-tabs>
				<template #footer>
					<span>
						<el-button @click="isScheduleModify = false">关闭</el-button>
					</span>
				</template>
			</el-dialog>
		</el-main>
	</el-container>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
export default {
	props: ['orderId', 'orderRId', 'orderStartDate', 'orderEndDate', 'customerName', 'orderTotalShoes'],
	components: {
		AllHeader
	},
	data() {
		return {
			orderPercentageText: '',
			orderShoeDataTable: [],
			isPreviewDialogVisible: false,
			isScheduleModify: false,
			isShoeScheduleVis: false,
			// schedule production
			activeTab: 'cutting',
			cuttingLine: 1,
			cuttingDatePicker: '',
			sewPreLine: 1,
			sewPreDatePicker: '',
			dialogOrderSearch: '',
			isShoeScheduleVis: false,
			isScheduleVis: false,
			isScheduleModify: false,
			isDateStatusTableVis: false,
			// 0: 裁断，1：预备，2：针车，3：成型
			tabs: [
				{
					name: 'cutting',
					label: '裁断排产',
					lineLabel: '裁断线号选择',
					dateLabel: '裁断工期选择',
					lineValue: [],
					dateValue: [],
					isOutSource: 0
				},
				{
					name: 'preSewing',
					label: '针车预备排产',
					lineLabel: '针车线号选择',
					dateLabel: '针车工期选择',
					lineValue: [],
					dateValue: [],
					isOutSource: 1
				},
				{
					name: 'sewing',
					label: '针车排产',
					lineLabel: '针车线号选择',
					dateLabel: '针车工期选择',
					lineValue: [],
					dateValue: [],
					isOutSource: 0
				},
				{
					name: 'molding',
					label: '成型排产',
					lineLabel: '成型线号选择',
					dateLabel: '成型工期选择',
					lineValue: [],
					dateValue: [],
					isOutSource: 0
				}
			],
			dateStatusTable: [
				{
					date: '2024-07-16',
					productAmount: 10,
					predictAmount: 2000,
					shoeList: [{
						orderId: 'K24-2111620',
						shoeId: '0E11150',
						amount: 300,
						datePeriod: "2024-07-16 至 2024-07-20",
						averageAmount: 75
					}]
				}
			],
			productionLines: {},
			currentRow: {}
		}
	},
	mounted() {
		this.getProductionLineOptions()
		this.getOrderShoeTableData()
	},
	methods: {
		async getProductionLineOptions() {
			const response = await axios.get("http://localhost:8000/production/productionmanager/getproductionlines")
			this.productionLines = response.data
		},
		async getOrderShoeTableData() {
			const params = { "orderId": this.$props.orderId }
			const response = await axios.get("http://localhost:8000/production/productionmanager/getorderproductiondetail", { params })
			this.orderShoeDataTable = response.data
			let totalCuttingAmount = 0, totalSewingAmount = 0, totalMoldingAmount = 0
			let cuttingAmount = 0, sewingAmount = 0, moldingAmount = 0
			this.orderShoeDataTable.forEach(row => {
				let totalShoes = Number(row.totalShoes)
				cuttingAmount = 0, sewingAmount = 0, moldingAmount = 0
				row.detail.forEach(subRow => {
					cuttingAmount += Number(subRow.cuttingAmount)
					sewingAmount += Number(subRow.sewingAmount)
					moldingAmount += Number(subRow.moldingAmount)
				})
				let cuttingPercent = Math.round(cuttingAmount / totalShoes * 100)
				let sewingPercent = Math.round(sewingAmount / totalShoes * 100)
				let moldingPercent = Math.round(moldingAmount / totalShoes * 100)
				row.percentageText = `裁断:${cuttingPercent.toString()}% 针车:${sewingPercent.toString()}% 成型:${moldingPercent.toString()}%`
				totalCuttingAmount += cuttingAmount
				totalSewingAmount += sewingAmount
				totalMoldingAmount += moldingAmount
			})
			let orderTotalShoes = Number(this.$props.orderTotalShoes)
			let totalCuttingPercent = Math.round(totalCuttingAmount / orderTotalShoes * 100)
			let totalSewingPercent = Math.round(totalSewingAmount / orderTotalShoes * 100)
			let totalMoldingPercent = Math.round(totalMoldingAmount / orderTotalShoes * 100)
			this.orderPercentageText = `裁断:${totalCuttingPercent.toString()}% 针车:${totalSewingPercent.toString()}% 成型:${totalMoldingPercent.toString()}%`
		},
		async scheduleProduction(rowData) {
			this.isScheduleModify = true
		},
		async viewProductionSchedule(rowData) {
			this.isScheduleModify = true
			this.currentRow = rowData
			const params = { "orderShoeId": rowData.orderShoeId }
			const response = await axios.get("http://localhost:8000/production/productionmanager/getordershoescheduleinfo", { params })
			console.log(response.data)
			this.tabs[0].lineValue = response.data.cuttingLineNumbers.split(",")
			this.tabs[0].dateValue = [response.data.cuttingStartDate, response.data.cuttingEndDate]
			this.tabs[0].isOutSource = response.data.isCuttingOutsourced

			this.tabs[1].lineValue = response.data.preSewingLineNumbers.split(",")
			this.tabs[1].dateValue = [response.data.preSewingStartDate, response.data.preSewingEndDate]
			this.tabs[1].isOutSource = response.data.isSewingOutsourced

			this.tabs[2].lineValue = response.data.sewingLineNumbers.split(",")
			this.tabs[2].dateValue = [response.data.sewingStartDate, response.data.sewingEndDate]
			this.tabs[2].isOutSource = response.data.isSewingOutsourced

			this.tabs[3].lineValue = response.data.moldingLineNumbers.split(",")
			this.tabs[3].dateValue = [response.data.moldingStartDate, response.data.moldingEndDate]
			this.tabs[3].isOutSource = response.data.isMoldingOutsourced
			console.log(this.tabs)
		},
		async checkDateProductionStatus() {

		},
		startOutSourceFlow() {
			const params = {
				"orderId": this.$props.orderId,
				"orderRId": this.$props.orderRId,
				"orderShoeId": this.currentRow.orderShoeId,
				"shoeRId": this.currentRow.shoeRId,
				"orderStartDate": this.$props.orderStartDate,
				"orderEndDate": this.$props.orderEndDate,
				"customerName": this.$props.customerName
			}
			const queryString = new URLSearchParams(params).toString();
			const url = `${window.location.origin}/productiongeneral/productionoutsource?${queryString}`
			window.open(url, '_blank')
		},
		calculateDailyProduction(dateRange) {
			if (dateRange && dateRange.length === 2) {
				const startDate = new Date(dateRange[0]);
				const endDate = new Date(dateRange[1]);
				const timeDiff = Math.abs(endDate - startDate);
				const diffDays = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
				return (this.currentRow.totalShoes / diffDays).toFixed(2);
			}
			return 0;
		},
		statusJudge({ row, column, rowIndex, columnIndex }) {
			const progressColumns = ['fabricCuttingProgress', 'preproductionProgress', 'sewingProgress', 'moldingProgress'];
			const columnProperty = column.property;
			let style = {
				background: '',
				color: '#fff',
				opacity: 0.8
			};
			if (progressColumns.includes(columnProperty)) {
				const [current, total] = row[columnProperty].split('/').map(Number);
				if (current === total) {
					style.background = 'rgba(0, 128, 0, 0.8)'; // Green background for complete progress
					return style
				}

			}
			if (row[columnProperty].includes('已定')) {
				style.background = 'rgba(255, 255, 0, 0.8)'; // Yellow background for "已定"
				style.color = '#000'
				return style
			} else if (row[columnProperty].includes('已到')) {
				style.background = 'rgba(0, 128, 0, 0.8)'; // Green background for "已到"
				return style
			}
			if (columnProperty === 'productionStatus' && row.productionStatus === '100%') {
				style.background = 'rgba(0, 128, 0, 0.8)'; // Green background for 100% completion
				return style
			}
		}
	}
}
</script>
