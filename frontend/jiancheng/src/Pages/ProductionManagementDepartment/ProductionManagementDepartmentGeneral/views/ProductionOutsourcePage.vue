<template>
	<el-container>
		<el-header height="">
			<AllHeader></AllHeader>
		</el-header>
		<el-main height="">
			<el-row :gutter="20" style="text-align: center">
				<el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">订单鞋型外包页面</el-col>
			</el-row>
			<el-row :gutter="20">
				<el-col :span="24" :offset="0">
					<el-descriptions title="订单信息" border column="2">
						<el-descriptions-item label="订单号">{{ $props.orderRId }}</el-descriptions-item>
						<el-descriptions-item label="鞋型号">{{ $props.shoeRId }}</el-descriptions-item>
						<el-descriptions-item label="客户号">{{ $props.customerName }}</el-descriptions-item>
						<el-descriptions-item label="出货日期">{{ $props.orderEndDate }}</el-descriptions-item>
						<el-descriptions-item label="外包总数">{{ totalShoes }}</el-descriptions-item>
					</el-descriptions>
				</el-col>
			</el-row>
			<el-row :gutter="20" style="margin-top: 20px">
				<el-col :span="24" :offset="0">
					鞋型配码信息
					<el-table :data="shoeInfo" border stripe :max-height="200">
						<el-table-column prop="colorName" label="颜色"></el-table-column>
						<el-table-column prop="batchName" label="配码编号"></el-table-column>
						<el-table-column prop="size34" label="34"></el-table-column>
						<el-table-column prop="size35" label="35"></el-table-column>
						<el-table-column prop="size36" label="36"></el-table-column>
						<el-table-column prop="size37" label="37"></el-table-column>
						<el-table-column prop="size38" label="38"></el-table-column>
						<el-table-column prop="size39" label="39"></el-table-column>
						<el-table-column prop="size40" label="40"></el-table-column>
						<el-table-column prop="size41" label="41"></el-table-column>
						<el-table-column prop="size42" label="42"></el-table-column>
						<el-table-column prop="size43" label="43"></el-table-column>
						<el-table-column prop="size44" label="44"></el-table-column>
						<el-table-column prop="size45" label="45"></el-table-column>
						<el-table-column prop="size46" label="46"></el-table-column>
						<el-table-column prop="totalAmount" label="双数"></el-table-column>
					</el-table>
				</el-col>
			</el-row>
			<el-row :gutter="20">
				<el-col :span="24" :offset="0">
					现有外包流程
					<el-table :data="outsourceInfo" border stripe scrollbar-always-on>
						<el-table-column prop="outsourceTypeArr" label="外包类型" width="200">
							<template #default="scope">
								<el-select v-model="scope.row.outsourceTypeArr" placeholder="" filterable multiple>
									<el-option v-for="item in productionDepartments" :key="item" :label="item"
										:value="item">
									</el-option>
								</el-select>
							</template>
						</el-table-column>
						<el-table-column prop="outsourceFactory" label="外包厂家" width="200">
							<template #default="scope">
								<el-select v-model="scope.row.outsourceFactory" value-key="id" placeholder="" clearable
									filterable>
									<el-option v-for="item in factoryOptions" :key="item.id" :label="item.value"
										:value="item">
									</el-option>
								</el-select>
							</template>

						</el-table-column>
						<el-table-column prop="outsourcePeriod" label="外包周期" width="380">
							<template #default="scope">
								<el-date-picker v-model="scope.row.outsourcePeriodArr" type="daterange"
									value-format="YYYY-MM-DD" response range-separator="-" start-placeholder=""
									end-placeholder="" size="small">
								</el-date-picker>
							</template>
						</el-table-column>
						<el-table-column prop="semifinishedRequired" label="是否需要外发半成品" width="200">
							<template #default="scope">
								<el-radio-group v-model="scope.row.semifinishedRequired">
									<el-radio value="1">是</el-radio>
									<el-radio value="2">否</el-radio>
								</el-radio-group>
							</template>
						</el-table-column>
						<el-table-column prop="semifinishedEstimatedOutboundDate" label="半成品预计发货日期" width="250">
							<template #default="scope">
								<el-date-picker v-model="scope.row.semifinishedEstimatedOutboundDate" type="date"
									value-format="YYYY-MM-DD" response placeholder="选择日期时间"
									:disabled="scope.row.semifinishedRequired == '2'" size="small">
								</el-date-picker>
							</template>
						</el-table-column>
						<el-table-column prop="materialEstimatedOutboundDate" label="材料预计出货日期" width="250">
							<template #default="scope">
								<el-date-picker v-model="scope.row.materialEstimatedOutboundDate" type="date"
									value-format="YYYY-MM-DD" response placeholder="选择日期时间" size="small">
								</el-date-picker>
							</template>
						</el-table-column>
						<el-table-column prop="approvalStatus" label="审批状态"></el-table-column>
						<el-table-column prop="deadlineDate" label="最迟交货日期" width="150">
							<template #default="scope">
								<el-date-picker v-model="scope.row.deadlineDate" type="date" value-format="YYYY-MM-DD"
									response placeholder="选择日期时间">
								</el-date-picker>
							</template>
						</el-table-column>
						<el-table-column label="操作" fixed="right" width="180">
							<template #default="scope">
								<el-button-group>
									<el-button type="primary" size="small"
										@click="checkOutboundInfo(scope.row)">发货情况</el-button>
									<el-button size="small" type="danger"
										@click="deleteRow(scope.$index)">删除</el-button>
								</el-button-group>
							</template>
						</el-table-column>
					</el-table>
				</el-col>
			</el-row>
			<el-row :gutter="20">
				<el-col :span="6" :offset="0">
					<el-button type="primary" size="default" @click="createOutsouce">新建外包流程</el-button>
				</el-col>
				<el-col :span="6" :offset="12">
					<el-button type="success" size="default" @click="saveOutsourceInfo">保存</el-button>
					<el-button type="warning" size="default" @click="submitOutsouceInfo">提交</el-button>
				</el-col>
			</el-row>
		</el-main>
	</el-container>
	<el-dialog title="外包物料发货情况查询" v-model="isOutsourceLogistic" width="80%">
		<el-row :gutter="20">
			<el-col :span="24" :offset="0"> 半成品发货状态： </el-col>
			<el-table :data="semifinishedLogisticData" border stripe>
				<el-table-column prop="semifinishedAmount" label="发货数量"></el-table-column>
				<el-table-column prop="semifinishedStatus" label="发货状态"></el-table-column>
				<el-table-column prop="outboundDatetime" label="发货日期"></el-table-column>
				<el-table-column prop="semifinishedEstimatedOutboundDate" label="预计发货日期"></el-table-column>
			</el-table>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="24" :offset="0"> 材料发货状态： </el-col>
			<el-table :data="materialLogisticData" border stripe>
				<el-table-column prop="materialType" label="材料类型" />
				<el-table-column prop="materialName" label="材料名称" />
				<el-table-column prop="colorName" label="颜色" />
				<el-table-column prop="materialUnit" label="单位" />
				<el-table-column prop="outboundAmount" label="发货数量" />
				<el-table-column prop="outsourceStatus" label="发货状态" />
				<el-table-column prop="outboundDatetime" label="发货日期"></el-table-column>
				<el-table-column prop="materialEstimateOutboundDate" label="预计发货日期"></el-table-column>
			</el-table>
		</el-row>
		<template #footer>
			<span>
				<el-button type="primary" @click="isOutsourceLogistic = false">确认</el-button>
			</span>
		</template>
	</el-dialog>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
export default {
	props: ['orderId', 'orderRId', 'orderStartDate', 'orderEndDate', 'customerName', 'orderShoeId', 'shoeRId'],
	components: {
		AllHeader
	},
	data() {
		return {
			isTransitNeed: false,
			isOutsourceLogistic: false,
			isOutsourcePreviewVis: false,
			factoryOptions: [],
			semifinishedLogisticData: [],
			materialLogisticData: [],
			outsourceInfo: [],
			shoeInfo: [],
			productionDepartments: [],
			prodLineRef: {
				"0": "裁断",
				"1": "针车",
				"2": "成型"
			},
			totalShoes: ''
		}
	},
	mounted() {
		this.getProductionDepartments()
		this.getAllOutsourceFactories()
		this.getOrderShoeBatchInfo()
		this.getOutsourceInfo()
	},
	methods: {
		deleteRow(index) {
			this.outsourceInfo.splice(index, 1)
		},
		async getAllOutsourceFactories() {
			const response = await axios.get(`${this.$apiBaseUrl}/general/getalloutsourcefactories`)
			this.factoryOptions = response.data
			console.log(this.factoryOptions)
		},
		async getProductionDepartments() {
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getproductiondepartments`)
			this.productionDepartments = response.data
		},
		async getOrderShoeBatchInfo() {
			const params = { "orderShoeId": this.$props.orderShoeId }
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoebatchinfo`, { params })
			this.shoeInfo = response.data
			this.shoeInfo.forEach(row => {
				this.totalShoes += row.totalAmount
			})
		},
		async getOutsourceInfo() {
			const params = { "orderShoeId": this.$props.orderShoeId }
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
			this.outsourceInfo = response.data
			this.outsourceInfo.forEach(row => {
				let temp = []
				row.outsourceType.split(",").forEach(number => {
					temp.push(this.prodLineRef[number])
				})
				row.outsourceTypeArr = temp
				row.outsourcePeriodArr = [row.outsourceStartDate, row.outsourceEndDate]
				if (row.approvalStatus) {
					row.approvalStatus = "已审批"
				} else {
					row.approvalStatus = "未审批"
				}
			})
		},
		createOutsouce() {
			this.outsourceInfo.push({})
		},
		async checkOutboundInfo(rowData) {
			const params = {"outsource_info_id": rowData.outsourceInfoId}
			let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcesemifinishedshipping`, {params})
			this.semifinishedLogisticData = response.data
			response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcematerialshipping`, {params})
			this.materialLogisticData = response.data
			this.isOutsourceLogistic = true

		},
		async saveOutsourceInfo() {
			const dataArr = []
			this.outsourceInfo.forEach(row => {
				let element = {
					"type": row.outsourceTypeArr,
					"factoryId": row.outsourceFactory.id,
					"outsourceStartDate": row.outsourcePeriod[0],
					"outsourceEndDate": row.outsourcePeriod[1],
					"semifinishedRequired": row.semifinishedRequired,
					"semifinishedEstimatedOutboundDate": row.semifinishedEstimatedOutboundDate,
					"deadlineDate": row.deadlineDate,
					"materialEstimatedOutboundDate": row.materialEstimatedOutboundDate,
					"outsourceAmount": this.$props.totalShoes,
					"orderShoeId": this.$props.orderShoeId
				}
				dataArr.push(element)
			})
			const response = await axios.put(`${this.$apiBaseUrl}/production/productionmanager/storeoutsourceforordershoe`, dataArr)
			this.getOutsourceInfo()
		},
		async submitOutsouceInfo() {
			const inputData = {"orderShoeId": this.$props.orderShoeId}
			await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/submitoutsourceinfo`, inputData)
			console.log("success")
		}
	}
}
</script>
