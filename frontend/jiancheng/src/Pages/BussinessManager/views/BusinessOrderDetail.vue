<template>
	<el-container>
		<el-header>
			<AllHeader></AllHeader>
		</el-header>
		<el-container>
			<el-main>
			<el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderRid
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户订单" align="center">{{
                        orderData.orderCid
                    }}</el-descriptions-item>

                 <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户商标" align="center">{{
                        orderData.customerBrand
                    }}</el-descriptions-item>
                	</el-descriptions>
                    <el-descriptions-item label="订单创建时间" align="center">{{
                        orderData.startDate
                    }}</el-descriptions-item>
                    <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                    <el-descriptions-item label="订单预计截止日期" align="center">{{
                        orderData.endDate
                    }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
	        </el-row>
	        <el-row :gutter="20">
	            <el-col :span="24" :offset="0">
	                <el-descriptions title="" :column="2" border>
	                    <el-descriptions-item label="包装资料上传状态" align="center"
	                        >{{ orderData.wrapRequirementUploadStatus }}
	                        <el-button
	                            type="primary"
	                            size="default"
	                            @click="openSubmitDocDialog(0)"
	                            >上传</el-button
	                        >
	                        <el-button v-if="orderDocData.productionDoc === '已上传'" type="primary" size="default" @click="downloadDoc(0)">查看</el-button>
	                    </el-descriptions-item>
	                    <el-descriptions-item label="生产数量单上传状态" align="center"
	                        >{{ orderDocData.amountDoc }}
	                        <el-button
	                            type="primary"
	                            size="default"
	                            @click="openSubmitDocDialog(1)"
	                            >上传</el-button
	                        >
	                        <el-button v-if="orderDocData.amountDoc === '已上传'" type="primary" size="default" @click="downloadDoc(1)">查看</el-button>
	                    </el-descriptions-item>
	                </el-descriptions>
	            </el-col>
	            <el-button type = primary size = 'default' @click="checkdata">CHECK</el-button>
	        </el-row>
	        <el-table :data="this.orderShoeData" border stripe height = "900"
        	:row-key = "(row) => {return row.shoeId}"
                @expand-change = "expandOpen" :expand-row-keys = "expandedRowKeys" >
            <el-table-column type = "expand" >
                <template #default = "props">
                    <el-table :data = "props.row.orderShoeTypeBatchInfo" border>
                        <el-table-column prop="packagingInfoName" label="配码名称" sortable/>
                        <el-table-column prop="packagingInfoLocale" label="配码地区" sortable/>
                        <el-table-column prop="size34Ratio" label="34" />
                        <el-table-column prop="size35Ratio" label="35" />
                        <el-table-column prop="size36Ratio" label="36" />
                        <el-table-column prop="size37Ratio" label="37" />
                        <el-table-column prop="size38Ratio" label="38" />
                        <el-table-column prop="size39Ratio" label="39" />
                        <el-table-column prop="size40Ratio" label="40" />
                        <el-table-column prop="size41Ratio" label="41" />
                        <el-table-column prop="size42Ratio" label="42" />
                        <el-table-column prop="size43Ratio" label="43" />
                        <el-table-column prop="size44Ratio" label="44" />
                        <el-table-column prop="size45Ratio" label="45" />
                        <el-table-column prop="size46Ratio" label="46" />
                        <el-table-column prop="totalQuantityInRatio" label="比例和"/>
                        <el-table-column label="单位数量">
                        <template #default="scope">
                            <el-input size = small
                            v-model = "props.row.quantityMapping[scope.row.packagingInfoId]"
                            placeholder = '123'controls-position = "right"
                            >
                            </el-input>
                        </template>
                        </el-table-column>
                        <el-table-column label="总数量">
                        </el-table-column>
                    </el-table>
                </template>
            </el-table-column>
            <el-table-column prop = "shoeRId" label = "鞋型编号" sortable/>
            <el-table-column prop = "shoeColor" label = "鞋型颜色" />
            <el-table-column prop = "shoeImage" label = "鞋型图片" />
            <el-table-column>
            <template #default="scope">
                    <el-button type="primary" size="default" @click="openAddBatchInfoDialog(scope.row)"
                        >添加配码</el-button
                    >
            </template>
            </el-table-column>
            <el-table-column label = "添加客户鞋型编号">
            <template #default="scope">
                    <el-input size="default" v-model = "this.orderShoeData.customerShoeName[scope.row.shoeRId]"
                        ></el-input
                    >
            </template>
            </el-table-column>

        </el-table>
			</el-main>
		</el-container>
	</el-container>


	
        <!-- <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-table
                    :data="orderShoePreviewData"
                    border
                    :span-method="mergeCellsPreview"
                    stripe
                    height="500"
                >
                    <el-table-column prop="inheritId" label="工厂型号"></el-table-column>
                    <el-table-column prop="customerId" label="客户型号"></el-table-column>
                    <el-table-column prop="status" label="鞋型状态"></el-table-column>
                    <el-table-column prop="colorCN" label="中文颜色"></el-table-column>
                    <el-table-column prop="colorEN" label="英文颜色"></el-table-column>
                    <el-table-column prop="sizeId" label="配码"></el-table-column>
                    <el-table-column label="尺码信息" align="center">
                        <el-table-column prop="7/35" label="7/35"></el-table-column>
                        <el-table-column prop="7.5/36" label="7.5/36"></el-table-column>
                        <el-table-column prop="8/37" label="8/37"></el-table-column>
                        <el-table-column prop="8.5/38" label="8.5/38"></el-table-column>
                        <el-table-column prop="9/39" label="9/39"></el-table-column>
                        <el-table-column prop="9.5/40" label="9.5/40"></el-table-column>
                        <el-table-column prop="10/41" label="10/41"></el-table-column>
                        <el-table-column prop="10.5/42" label="10.5/42"></el-table-column>
                        <el-table-column prop="11/43" label="11/43"></el-table-column>
                        <el-table-column prop="12/44" label="12/44"></el-table-column>
                        <el-table-column prop="13/45" label="13/45"></el-table-column>
                    </el-table-column>
                    <el-table-column prop="pairCount" label="双数"></el-table-column>
                </el-table>
            </el-col>
        </el-row> -->

<!--         <template #footer>
            <span>
                <el-button type="primary" @click="previewOrderVis = false">确认</el-button>
            </span>
        </template> -->
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
export default {
    props: ['orderId'],
    components: {
    	AllHeader
    },
    data() {
        return {
            orderData: {},
            orderShoeData:[],
            orderDocData:{},
            expandedRowKeys:[],
        }
    },
    mounted() {
        this.getOrderInfo()
        // this.getOrderOrderShoe()
        // this.getOrderOrderShoe()
    },
    methods: {
    	async getOrderInfo() {
          const response = await axios.get(
              `${this.$apiBaseUrl}/order/getbusinessorderinfo?orderid=${this.orderId}`
          )
          this.orderData = response.data
          this.orderShoeData = response.data["orderShoeAllData"]
          console.log(this.orderData)
      	},
      	expandOpen(row, expand){
            console.log(this.expandedRowKeys)
            this.expandedRowKeys.push(row.shoeTypeId)
            // row.batchQuantityMapping = row.orderShoeTypeBatchInfo.map((batchInfo) => { return batchInfo.packagingInfoId:batchInfo.unitQuantityInPair})Id})
        },
      // async getOrderOrderShoe() {
      //       const response = await axios.get(`${this.$apiBaseUrl}/order/getbusinessorderinfo`, {
      //           params: {
      //               orderid: this.orderId
      //           }
      //       })
      //       this.orderShoePreviewData = response.data
    // 	},
    // async getOrderDocInfo() {
    //         const response = await axios.get(`${this.$apiBaseUrl}/order/getorderdocinfo`, {
    //             params: {
    //                 orderrid: this.orderId
    //             }
    //         })
    //         this.orderDocData = response.data
    // 	},
    	checkdata(){
    		console.log(this.orderData)
    		console.log(this.orderShoePreviewData)
    		console.log(this.orderDocData)
    	},
    	openSubmitDocDialog(){

    	},
    	downloadDoc(){

    	},


	}
}
</script>
<style scoped>
/* Add your styles here */
</style>