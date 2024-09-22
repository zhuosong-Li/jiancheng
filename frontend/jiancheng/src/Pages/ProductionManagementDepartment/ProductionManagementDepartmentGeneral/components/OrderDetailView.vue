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
									<el-table-column label="预览图" width="200">
										<template #default="scope">
											<el-image :src="scope.row.imageurl" fit="fill"></el-image>
										</template>
									</el-table-column>
									<el-table-column label="颜色" prop="colorName" />
									<el-table-column label="配码编号" prop="batchInfoName" />
									<el-table-column label="订单总数" prop="batchAmount" />
									<el-table-column label="裁断完成数量" prop="cuttingAmount" />
									<el-table-column label="预备完成数量" prop="preSewingAmount" />
									<el-table-column label="针车完成数量" prop="sewingAmount" />
									<el-table-column label="成型完成数量" prop="moldingAmount" />
									<el-table-column label="完成状态" prop="productionStatus" />
								</el-table>
							</template>
						</el-table-column>
						<el-table-column prop="shoeRId" label="公司编号" width="100"></el-table-column>
						<el-table-column prop="customerProductName" label="客户型号" width="100"></el-table-column>
						<el-table-column prop="percentageText" label="生产状态百分比"></el-table-column>
						<el-table-column prop="totalShoes" label="当前鞋型订单总数"></el-table-column>
						<el-table-column prop="status" label="状态"></el-table-column>
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
									<el-select v-model="tab.lineValue" placeholder="" @change="" multiple>
										<el-option v-for="item in productionLines[tab.name]" :key="item" :label="item"
											:value="item">
										</el-option>
									</el-select>
								</span>
							</el-col>
							<el-col :span="8" :offset="6">
								<el-descriptions title="" border>
									<el-descriptions-item label="外包状态">
										<div v-if="tab.isOutsourced === false">
											未设置外包
										</div>
										<div v-else>
											已设置外包
										</div>
									</el-descriptions-item>
									<el-descriptions-item label="操作">
										<el-button v-if="tab.isOutsourced === false" type="primary" size="default"
											@click="startOutSourceFlow()">启动外包流程</el-button>
										<el-button-group v-else>
											<el-button type="primary" size="default"
												@click="startOutSourceFlow()">查看外包流程</el-button>
											<el-button type="warning" size="default" @click="">删除外包流程</el-button>
										</el-button-group>
									</el-descriptions-item>
								</el-descriptions>
							</el-col>
						</el-row>
						<el-row :gutter="20">
							<el-col :span="10" :offset="0">
								<span>
									{{ tab.dateLabel }}：
									<el-date-picker v-model="tab.dateValue" type="daterange" size="default"
										range-separator="-" :disabled-date="disableDate" value-format="YYYY-MM-DD">
									</el-date-picker>
								</span>
							</el-col>
							<el-col :span="5" :offset="0">
								<el-button type="primary" size="default" @click="checkDateProductionStatus(tab)">{{
									tab.isDateStatusTableVis ? '关闭表格' : '查看工期内排产情况' }}</el-button>
							</el-col>
							<el-col :span="5" :offset="0">预计每天生产数量：{{ calculateDailyProduction(currentRow.totalShoes,
								tab.dateValue)
								}}</el-col>
						</el-row>
						<el-row :gutter="20">
							<el-table v-if="tab.isDateStatusTableVis" :data="tab.dateStatusTable" border stripe>
								<el-table-column type="expand">
									<template #default="props">
										<el-table :data="props.row.detail" border stripe>
											<el-table-column type="index" />
											<el-table-column label="订单号" prop="orderRId" />
											<el-table-column label="工厂型号" prop="shoeRId" />
											<el-table-column label="鞋型总数量" prop="totalAmount" />
											<el-table-column label="工段生产开始" prop="productionStartDate" />
											<el-table-column label="工段生产结束" prop="productionEndDate" />
											<el-table-column label="平均每天数量" prop="averageAmount" />
										</el-table>
									</template>
								</el-table-column>

								<el-table-column prop="date" label="日期"> </el-table-column>
								<el-table-column prop="orderShoeCount" label="已排产鞋型数"> </el-table-column>
								<el-table-column prop="predictAmount" label="预计当日现有生产量"> </el-table-column>
							</el-table>
						</el-row>
					</el-tab-pane>
				</el-tabs>
				<template #footer>
					<span>
						<el-button @click="isScheduleModify = false">取消</el-button>
						<el-button type="primary" @click="modifyProductionSchedule">保存</el-button>
						<el-button v-if="currentRow.status === '未排产'" type="success"
							@click="startProduction">开始生产</el-button>
					</span>
				</template>
			</el-dialog>
		</el-main>
	</el-container>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus';
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
			activeTab: '裁断',
			cuttingLine: 1,
			cuttingDatePicker: '',
			sewPreLine: 1,
			sewPreDatePicker: '',
			dialogOrderSearch: '',
			isShoeScheduleVis: false,
			isScheduleVis: false,
			isScheduleModify: false,
			// 0: 裁断，1：预备，2：针车，3：成型
			tabs: [
				{
					name: '裁断',
					label: '裁断排产',
					lineLabel: '裁断线号选择',
					dateLabel: '裁断工期选择',
					lineValue: [],
					dateValue: [],
					dateStatusTable: [],
					isOutsourced: 0,
					isDateStatusTableVis: false,
				},
				{
					name: '针车预备',
					label: '针车预备排产',
					lineLabel: '针车预备线号选择',
					dateLabel: '针车预备工期选择',
					lineValue: [],
					dateValue: [],
					dateStatusTable: [],
					isOutsourced: 0,
					isDateStatusTableVis: false,
				},
				{
					name: '针车',
					label: '针车排产',
					lineLabel: '针车线号选择',
					dateLabel: '针车工期选择',
					lineValue: [],
					dateValue: [],
					dateStatusTable: [],
					isOutsourced: 0,
					isDateStatusTableVis: false,
				},
				{
					name: '成型',
					label: '成型排产',
					lineLabel: '成型线号选择',
					dateLabel: '成型工期选择',
					lineValue: [],
					dateValue: [],
					dateStatusTable: [],
					isOutsourced: 0,
					isDateStatusTableVis: false,
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
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getproductionlines`)
			this.productionLines = response.data
		},
		async getOrderShoeTableData() {
			const params = { "orderId": this.$props.orderId }
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getorderproductiondetail`, { params })
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
		async viewProductionSchedule(rowData) {
			this.isScheduleModify = true
			this.currentRow = rowData
			const params = { "orderShoeId": rowData.orderShoeId }
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoescheduleinfo`, { params })
			this.tabs[0].lineValue = response.data.cuttingLineNumbers.split(",")
			this.tabs[0].dateValue = [response.data.cuttingStartDate, response.data.cuttingEndDate]
			this.tabs[0].isOutsourced = response.data.isCuttingOutsourced

			this.tabs[1].lineValue = response.data.preSewingLineNumbers.split(",")
			this.tabs[1].dateValue = [response.data.preSewingStartDate, response.data.preSewingEndDate]
			this.tabs[1].isOutsourced = response.data.isSewingOutsourced

			this.tabs[2].lineValue = response.data.sewingLineNumbers.split(",")
			this.tabs[2].dateValue = [response.data.sewingStartDate, response.data.sewingEndDate]
			this.tabs[2].isOutsourced = response.data.isSewingOutsourced

			this.tabs[3].lineValue = response.data.moldingLineNumbers.split(",")
			this.tabs[3].dateValue = [response.data.moldingStartDate, response.data.moldingEndDate]
			this.tabs[3].isOutsourced = response.data.isMoldingOutsourced
		},
		async modifyProductionSchedule() {
			const data = {
				"orderShoeId": this.currentRow.orderShoeId,
				"cuttingInfo": {
					"lineValue": this.tabs[0].lineValue.join(","),
					"isOutsourced": this.tabs[0].isOutsourced,
					"startDate": this.tabs[0].dateValue[0],
					"endDate": this.tabs[0].dateValue[1]
				},
				"preSewingInfo": {
					"lineValue": this.tabs[1].lineValue.join(","),
					"isOutsourced": this.tabs[2].isOutsourced,
					"startDate": this.tabs[1].dateValue[0],
					"endDate": this.tabs[1].dateValue[1]
				},
				"sewingInfo": {
					"lineValue": this.tabs[2].lineValue.join(","),
					"isOutsourced": this.tabs[2].isOutsourced,
					"startDate": this.tabs[2].dateValue[0],
					"endDate": this.tabs[2].dateValue[1]
				},
				"moldingInfo": {
					"lineValue": this.tabs[3].lineValue.join(","),
					"isOutsourced": this.tabs[3].isOutsourced,
					"startDate": this.tabs[3].dateValue[0],
					"endDate": this.tabs[3].dateValue[1]
				}
			}
			const response = await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/editproductionschedule`, data)
			if (response.status == 200) {
				ElMessage.success("修改成功")
			}
			else {
				ElMessage.error("修改失败")
			}
			this.isScheduleModify = false
		},
		async startProduction() {
			ElMessageBox.alert('点击确认后，你仍可修改排期，但推进流程操作不可撤回', '警告', {
				confirmButtonText: '确认',
				showCancelButton: true,
				cancelButtonText: '取消'
			}).then(async () => {
				const data = { "orderId": this.$props.orderId, "orderShoeId": this.currentRow.orderShoeId }
				const response = await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/startproduction`, data)
				if (response.status == 200) {
					ElMessage.success("生产开始")
				}
				else {
					ElMessage.error("排期异常")
				}
				this.isScheduleModify = false
				this.getOrderShoeTableData()
			})
		},
		async checkDateProductionStatus(tab) {
			if (tab.isDateStatusTableVis === true) {
				tab.isDateStatusTableVis = false
			}
			else {
				const params = { "startDate": tab.dateValue[0], "endDate": tab.dateValue[1], "team": tab.name }
				const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/checkdateproductionstatus`, { params })
				tab.dateStatusTable = response.data
				tab.dateStatusTable.forEach(element => {
					let amount = 0
					element.detail.forEach(row => {
						row.averageAmount = this.calculateDailyProduction(row.totalAmount, [row.productionStartDate, row.productionEndDate])
						amount += Number(row.averageAmount)
					})
					element.predictAmount = amount;
				})
				tab.isDateStatusTableVis = true
			}
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
		calculateDailyProduction(totalShoes, dateRange) {
			if (dateRange && dateRange.length === 2) {
				const startDate = new Date(dateRange[0]);
				const endDate = new Date(dateRange[1]);
				const timeDiff = Math.abs(endDate - startDate);
				const diffDays = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
				return (Number(totalShoes) / diffDays).toFixed(2);
			}
			return 0;
		},
		disableDate(time) {
			const startDate = new Date(this.$props.orderStartDate)
			const endDate = new Date(this.$props.orderEndDate)
			return time.getTime() < startDate || time.getTime() > endDate.getTime();
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
