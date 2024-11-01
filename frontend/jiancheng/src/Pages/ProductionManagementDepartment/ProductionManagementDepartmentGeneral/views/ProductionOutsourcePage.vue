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
					<el-descriptions title="订单信息" :column="3" border>
						<el-descriptions-item label="客户名称">{{ orderInfo.customerName }}</el-descriptions-item>
						<el-descriptions-item label="鞋型号">{{ orderInfo.shoeRId }}</el-descriptions-item>
						<el-descriptions-item label="订单编号">{{ orderInfo.orderRId }}</el-descriptions-item>
						<el-descriptions-item label="订单创建日期">{{ orderInfo.orderStartDate }}</el-descriptions-item>
						<el-descriptions-item label="订单截止日期">{{ orderInfo.orderEndDate }}</el-descriptions-item>
						<el-descriptions-item label="订单总数量">{{ orderInfo.orderTotalShoes }}</el-descriptions-item>
					</el-descriptions>
				</el-col>
			</el-row>
			<el-row :gutter="20" style="margin-top: 20px">
				<el-col :span="24" :offset="0">
					鞋型配码信息
					<el-table :data="shoeInfo" :span-method="shoeBatchInfoTableSpanMethod" border stripe
						:max-height="500">
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
						<el-table-column prop="pairAmount" label="双数"></el-table-column>
						<el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
					</el-table>
				</el-col>
			</el-row>
			<el-row :gutter="20">
				现有外包流程
				<el-table :data="outsourceInfo" border stripe scrollbar-always-on>
					<el-table-column prop="outsourceType" label="外包类型"></el-table-column>
					<el-table-column prop="outsourceFactory.value" label="外包厂家"></el-table-column>
					<el-table-column prop="outsourceAmount" label="外包数量"></el-table-column>
					<el-table-column prop="outsourceStartDate" label="外包开始日期"></el-table-column>
					<el-table-column prop="outsourceEndDate" label="外包结束日期"></el-table-column>
					<el-table-column prop="outsourceStatus" label="状态"></el-table-column>
					<el-table-column label="操作" fixed="right" width="180">
						<template #default="scope">
							<el-button-group>
								<el-button type="primary" size="small"
									@click="checkOutboundInfo(scope.row)">发货情况</el-button>
								<el-button type="primary" size="small" @click="editRow(scope.row)">编辑</el-button>
								<el-button type="warning" size="small"
									@click="submitOutsourceInfo(scope.row)">提交</el-button>
								<el-button size="small" type="danger" @click="deleteRow(scope.row)">删除</el-button>
							</el-button-group>
						</template>
					</el-table-column>
				</el-table>
			</el-row>
			<el-row :gutter="20">
				<el-col :span="6" :offset="0">
					<el-button type="primary" size="default" @click="editRow(null)">新建外包流程</el-button>
				</el-col>
			</el-row>
		</el-main>
	</el-container>
	<el-dialog title="外包编辑页面" v-model="showOutsourceEditPage" width="95%">
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">外包类型</el-col>
			<el-col :span="8" :offset="0">
				<el-select v-model="currentRow.outsourceType" placeholder="" filterable multiple>
					<el-option v-for="item in productionDepartments" :key="item" :label="item"
						:value="item"></el-option>
				</el-select>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">外包厂家</el-col>
			<el-col :span="8" :offset="0">
				<el-select v-model="currentRow.outsourceFactory" value-key="id" placeholder="" filterable clearable>
					<el-option v-for="item in factoryOptions" :key="item.id" :label="item.value" :value="item">
					</el-option>
				</el-select>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">外包周期</el-col>
			<el-col :span="8" :offset="0">
				<el-date-picker v-model="currentRow.outsourcePeriodArr" type="daterange" value-format="YYYY-MM-DD"
					response range-separator="至">
				</el-date-picker>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">材料出货日期</el-col>
			<el-col :span="8" :offset="0">
				<el-date-picker v-model="currentRow.materialEstimatedOutboundDate" type="date" value-format="YYYY-MM-DD"
					response placeholder="选择日期时间">
				</el-date-picker>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">是否需要外发半成品</el-col>
			<el-col :span="8" :offset="0">
				<el-radio-group v-model="currentRow.semifinishedRequired">
					<el-radio :value="true">是</el-radio>
					<el-radio :value="false">否</el-radio>
				</el-radio-group>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">半成品发货日期</el-col>
			<el-col :span="8" :offset="0">
				<el-date-picker v-model="currentRow.semifinishedEstimatedOutboundDate" type="date"
					value-format="YYYY-MM-DD" response :disabled="currentRow.semifinishedRequired == false"
					placeholder="选择日期时间">
				</el-date-picker>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">最迟交货日期</el-col>
			<el-col :span="8" :offset="0">
				<el-date-picker v-model="currentRow.deadlineDate" type="date" value-format="YYYY-MM-DD" response
					placeholder="选择日期时间">
				</el-date-picker>
			</el-col>
		</el-row>
		<el-row :gutter="20">
			<el-col :span="4" :offset="1">外包数量</el-col></el-row>
		<el-row :gutter="20">
			<el-col :span="23" :offset="1">
				<el-table :data="outsourceShoeBatchInfo" :span-method="outsourceShoeBatchInfoTableSpanMethod" border
					stripe :max-height="500">
					<el-table-column prop="colorName" label="颜色"></el-table-column>
					<el-table-column prop="batchName" label="配码编号"></el-table-column>
					<el-table-column prop="size34" label="34">
						<template v-slot="scope">
							<el-input v-model="scope.row.size34" />
						</template>
					</el-table-column>
					<el-table-column prop="size35" label="35">
						<template v-slot="scope">
							<el-input v-model="scope.row.size35" />
						</template>
					</el-table-column>
					<el-table-column prop="size36" label="36">
						<template v-slot="scope">
							<el-input v-model="scope.row.size36" />
						</template>
					</el-table-column>
					<el-table-column prop="size37" label="37">
						<template v-slot="scope">
							<el-input v-model="scope.row.size37" />
						</template>
					</el-table-column>
					<el-table-column prop="size38" label="38">
						<template v-slot="scope">
							<el-input v-model="scope.row.size38" />
						</template>
					</el-table-column>
					<el-table-column prop="size39" label="39">
						<template v-slot="scope">
							<el-input v-model="scope.row.size39" />
						</template>
					</el-table-column>
					<el-table-column prop="size40" label="40">
						<template v-slot="scope">
							<el-input v-model="scope.row.size40" />
						</template>
					</el-table-column>
					<el-table-column prop="size41" label="41">
						<template v-slot="scope">
							<el-input v-model="scope.row.size41" />
						</template>
					</el-table-column>
					<el-table-column prop="size42" label="42">
						<template v-slot="scope">
							<el-input v-model="scope.row.size42" />
						</template>
					</el-table-column>
					<el-table-column prop="size43" label="43">
						<template v-slot="scope">
							<el-input v-model="scope.row.size43" />
						</template>
					</el-table-column>
					<el-table-column prop="size44" label="44">
						<template v-slot="scope">
							<el-input v-model="scope.row.size44" />
						</template>
					</el-table-column>
					<el-table-column prop="size45" label="45">
						<template v-slot="scope">
							<el-input v-model="scope.row.size45" />
						</template>
					</el-table-column>
					<el-table-column prop="size46" label="46">
						<template v-slot="scope">
							<el-input v-model="scope.row.size46" />
						</template>
					</el-table-column>
					<el-table-column prop="pairAmount" label="双数"></el-table-column>
					<el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
				</el-table>
			</el-col>
		</el-row>
		<template #footer>
			<span>
				<el-button type="" @click="showOutsourceEditPage = false">退出</el-button>
				<el-button type="primary" @click="saveOutsourceInfo">保存</el-button>
			</span>
		</template>
	</el-dialog>
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
import { ElMessage } from 'element-plus';
import { shoeBatchInfoTableSpanMethod } from '../../utils';
export default {
	props: ['orderId', 'orderShoeId'],
	components: {
		AllHeader
	},
	data() {
		return {
			isOutsourceLogistic: false,
			isOutsourcePreviewVis: false,
			showOutsourceEditPage: false,
			factoryOptions: [],
			semifinishedLogisticData: [],
			materialLogisticData: [],
			outsourceInfo: [],
			shoeInfo: [],
			outsourceShoeBatchInfo: [],
			productionDepartments: [],
			totalShoes: 0,
			currentRow: {},
			outsourceShoeBatchInfoTableSpanMethod: null,
			shoeBatchInfoTableSpanMethod: null,
			orderInfo: {
				customerName: '',
				orderRId: '',
				orderStartDate: '',
				orderEndDate: '',
				orderTotalShoes: '',
			}
		}
	},
	mounted() {
		this.getOrderShoeInfo()
		this.getProductionDepartments()
		this.getAllOutsourceFactories()
		this.getOrderShoeBatchInfo()
		this.getOutsourceInfo()
	},
	methods: {
		async getOrderShoeInfo() {
			let params = { "orderId": this.$props.orderId, "orderShoeId": this.$props.orderShoeId }
			let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getorderinfo`, { params })
			this.orderInfo = response.data
			response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getorderamount`, { params })
			this.orderInfo.orderTotalShoes = response.data.orderTotalShoes
		},
		async editRow(rowData) {
			this.outsourceShoeBatchInfo = JSON.parse(JSON.stringify(this.shoeInfo));
			if (rowData === null) {
				this.currentRow = {}
				this.outsourceShoeBatchInfo.forEach(row => {
					for (let i = 34; i < 47; i++) {
						row[`size${i}`] = 0
					}
				})
			}
			else {
				this.currentRow = rowData
				let params = { "orderShoeId": this.$props.orderShoeId, "outsourceInfoId": rowData.outsourceInfoId }
				let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcebatchinfo`, { params })
				this.outsourceShoeBatchInfo = response.data
			}
			this.outsourceShoeBatchInfoTableSpanMethod = shoeBatchInfoTableSpanMethod(this.outsourceShoeBatchInfo)
			this.showOutsourceEditPage = true
		},
		async deleteRow(rowData) {
			const params = { "orderShoeId": this.$props.orderShoeId, "outsourceInfoId": rowData.outsourceInfoId }
			try {
				await axios.delete(`${this.$apiBaseUrl}/production/productionmanager/deleteoutsourceinfo`, { params })
				ElMessage.success("删除成功")
			}
			catch (error) {
				console.log(error)
				ElMessage.error("删除失败")
			}
			this.getOutsourceInfo()
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
			this.shoeBatchInfoTableSpanMethod = shoeBatchInfoTableSpanMethod(this.shoeInfo)
		},
		async getOutsourceInfo() {
			const params = { "orderShoeId": this.$props.orderShoeId }
			const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
			this.outsourceInfo = response.data
			this.outsourceInfo.forEach(row => {
				row.outsourcePeriodArr = [row.outsourceStartDate, row.outsourceEndDate]
			})
		},
		createOutsource() {
			this.showOutsourceEditPage = true
		},
		async checkOutboundInfo(rowData) {
			const params = { "outsource_info_id": rowData.outsourceInfoId }
			let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcesemifinishedshipping`, { params })
			this.semifinishedLogisticData = response.data
			response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcematerialshipping`, { params })
			this.materialLogisticData = response.data
			this.isOutsourceLogistic = true

		},
		async saveOutsourceInfo() {
			let element = {
				"outsourceInfoId": this.currentRow.outsourceInfoId,
				"type": this.currentRow.outsourceType,
				"factoryId": this.currentRow.outsourceFactory.id,
				"outsourceStartDate": this.currentRow.outsourcePeriodArr[0],
				"outsourceEndDate": this.currentRow.outsourcePeriodArr[1],
				"semifinishedRequired": this.currentRow.semifinishedRequired,
				"semifinishedEstimatedOutboundDate": this.currentRow.semifinishedEstimatedOutboundDate,
				"deadlineDate": this.currentRow.deadlineDate,
				"materialEstimatedOutboundDate": this.currentRow.materialEstimatedOutboundDate,
				"outsourceAmount": this.outsourceShoeBatchInfo,
				"orderShoeId": this.$props.orderShoeId
			}

			try {
				await axios.put(`${this.$apiBaseUrl}/production/productionmanager/storeoutsourceforordershoe`, element)
				ElMessage.success("保存成功")
			}
			catch (error) {
				console.log(error)
				ElMessage.error("保存失败")
			}
			this.getOutsourceInfo()
		},
		async submitOutsourceInfo(row) {
			let inputData = { "outsourceInfoId": row.outsourceInfoId }
			try {
				await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/submitoutsourceinfo`, inputData)
				ElMessage.success("提交成功")
			}
			catch (error) {
				console.log(error)
				ElMessage.error("提交失败")
			}
			this.getOutsourceInfo()
		},
	}
}
</script>
