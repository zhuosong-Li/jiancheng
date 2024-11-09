<template>
	<el-container>
		<el-header>
			<AllHeader></AllHeader>
		</el-header>
		<el-container>
			<el-main >
			<el-row :gutter="0">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderRid
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户订单" align="center">{{
                        orderData.orderCid
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户商标" align="center">{{
                        orderData.customerBrand
                    }}</el-descriptions-item>
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
	                            @click="openSubmitDialog()"
	                            >上传</el-button
	                        >
	                        <el-button v-if="orderData.wrapRequirementUploadStatus === '已上传包装文件'" type="primary" size="default" @click="download(2)">查看</el-button>
	                    </el-descriptions-item>
	                    <!-- <el-descriptions-item label="生产数量单上传状态" align="center"
	                        >{{ orderDocData.amountDoc }}
	                        <el-button
	                            type="primary"
	                            size="default"
	                            @click="openSubmitDocDialog(1)"
	                            >上传</el-button
	                        >
	                        <el-button v-if="orderDocData.amountDoc === '已上传包装文件'" type="primary" size="default" @click="downloadDoc(1)">查看</el-button>
	                    </el-descriptions-item> -->
	                </el-descriptions>
	            </el-col>
	        </el-row>
	        <el-table :data="orderShoeData" border stripe height = "900" :row-key = "(row) => {return row.orderShoeTypeId}">
            <el-table-column type = "expand" >
                <template #default = "props">
                    <el-table :data = "props.row.orderShoeTypes" border :row-key = "(row) => {return row.packagingInfoId}">
                        <el-table-column type="expand">
                            <template #default="scope">
                                <el-table :data = "scope.row.shoeTypeBatchInfoList">
                                    <el-table-column prop="packagingInfoName" label ="名称"/>
                                    <el-table-column v-for="col in Object.keys(this.attrMappingToRatio).filter(key=>this.batchInfoType[key] != null)"
                                                     :prop="attrMappingToRatio[col]"
                                                     :label="batchInfoType[col]"></el-table-column>
                                    <!-- <el-table-column prop="size34ratio" label ="34"/>
                                    <el-table-column prop="size35ratio" label ="35"/>
                                    <el-table-column prop="size36ratio" label ="36"/>
                                    <el-table-column prop="size37ratio" label ="37"/>
                                    <el-table-column prop="size38ratio" label ="38"/>
                                    <el-table-column prop="size39ratio" label ="39"/>
                                    <el-table-column prop="size40ratio" label ="40"/>
                                    <el-table-column prop="size41ratio" label ="41"/>
                                    <el-table-column prop="size42ratio" label ="42"/>
                                    <el-table-column prop="size43ratio" label ="43"/>
                                    <el-table-column prop="size44ratio" label ="44"/>
                                    <el-table-column prop="size45ratio" label ="45"/>
                                    <el-table-column prop="size46ratio" label ="46"/> -->
                                    <el-table-column prop="totalQuantityRatio" label ="比例和"/>
                                    <el-table-column prop="unitPerRatio" label ="比例单位数量"/>

                                </el-table>
                            </template>
                        </el-table-column>
                        <el-table-column prop="shoeTypeColorName" label="颜色名称" sortable/>
                        <!-- <el-table-column v-for="col in Object.keys(attrMappingToAmount).filter(key=>batchInfoType[key] != null)"
                                        :prop="props.row.orderShoeTypes.shoeTypeBatchData[]"
                                        :label="batchInfoType[col]">
                        </el-table-column> -->
                        <el-table-column prop="shoeTypeBatchData.size34Amount" label="34" />
                        <el-table-column prop="shoeTypeBatchData.size35Amount" label="35" />
                        <el-table-column prop="shoeTypeBatchData.size36Amount" label="36" />
                        <el-table-column prop="shoeTypeBatchData.size37Amount" label="37" />
                        <el-table-column prop="shoeTypeBatchData.size38Amount" label="38" />
                        <el-table-column prop="shoeTypeBatchData.size39Amount" label="39" />
                        <el-table-column prop="shoeTypeBatchData.size40Amount" label="40" />
                        <el-table-column prop="shoeTypeBatchData.size41Amount" label="41" />
                        <el-table-column prop="shoeTypeBatchData.size42Amount" label="42" />
                        <el-table-column prop="shoeTypeBatchData.size43Amount" label="43" />
                        <el-table-column prop="shoeTypeBatchData.size44Amount" label="44" />
                        <el-table-column prop="shoeTypeBatchData.size45Amount" label="45" />
                        <el-table-column prop="shoeTypeBatchData.size46Amount" label="46" />
                        <el-table-column prop = "shoeTypeBatchData.totalAmount" label="总数量"/>
                        
                        <el-table-column label="金额">
                        <template #default="scope">
                            <el-input size = small
                            controls-position = "right"
                            @change="updateValue(scope.row)"
                            v-model = "scope.row.shoeTypeBatchData.unitPrice"
                            :disabled="priceChangeNotAllowed">
                            </el-input>
                        </template> 
                        </el-table-column>
                        <el-table-column label="金额单位">
                        <template #default="scope">
                            <el-input size = small
                            controls-position = "right"
                            @change = "updateCurrencyValue(scope.row)"
                            v-model = "scope.row.shoeTypeBatchData.currencyType"
                            :disabled="unitChangeNotAllowed"
                            >
                            </el-input>
                        </template> 
                        </el-table-column>
                        <el-table-column prop = "shoeTypeBatchData.totalPrice" label="总金额"/>


                    </el-table>
                </template>
            </el-table-column>
            <el-table-column prop = "shoeRid" label = "鞋型编号" sortable/>
			<el-table-column prop = "shoeCid" label = "客户鞋型编号" sortable/>
            <el-table-column prop = "currentStatus" label = "订单状态" />

            <el-table-column label="备注">
            <template #default="scope" >
                    <el-button v-if="!scope.row.orderShoeRemarkExist" type="primary" size="default" @click="oprenRemarkDialog(scope.row)"
                        >添加备注
                    </el-button>
                    <el-text v-if="scope.row.orderShoeRemarkExist">{{scope.row.orderShoeRemark}}</el-text>
            </template>
            </el-table-column>
            <<!-- el-table-column label = "添加客户鞋型编号">
            <template #default="scope">
                    <el-input size="default" v-model = "this.orderShoeData.customerShoeName[scope.row.shoeRId]"
                        ></el-input
                    >
            </template>
            </el-table-column> -->

        </el-table>
        <span>
            <el-button @click="submitPriceForm">保存财务信息</el-button>
            <!-- <el-button @click="submitNewOrder">  </el-button> -->
             <el-button @click="togglePriceChange"> 改变价格修改权限 </el-button>
             <el-button @click="toggleUnitChange"> 改变货币单位修改权限 </el-button>
        </span>

			</el-main>
		</el-container>
	</el-container>

    <el-dialog 
        title="鞋型备注"
        v-model="remarkDialogVis"
        width = "50%"
        >
        <el-form>
            <el-form-item label="工艺备注">
                <el-input type = "textarea" :rows=2 v-model="this.remarkForm.technicalRemark"></el-input>
            </el-form-item>

            <el-form-item label="材料备注">
                <el-input type="textarea" :rows=2 v-model="this.remarkForm.materialRemark"></el-input>
            </el-form-item>
        </el-form>
        
        <template #footer>
            <span>
                <el-button @click="remarkDialogVis=false">取消</el-button>

                <el-button type="primary" @click="submitRemarkForm">提交备注</el-button>
                
            </span>

        </template>
        
        
    
    </el-dialog>
    <el-dialog
        title="包装资料上传"
        v-model="isSubmitDocVis"
        width="30%"
        @close="handleDialogClose"
    >
        <el-upload
            ref="uploadDoc"
            :action="`${this.$apiBaseUrl}/orderimport/submitdoc`"
            :headers="uploadHeaders"
            :auto-upload="false"
            accept=".xls,.xlsx"
            :file-list="fileList"
            :limit="1"
            :data="{ fileType: 2, orderRid: orderData.orderRid }"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
        >
            <el-button  type="primary">选择文件</el-button>
        </el-upload>


        <template #footer>
            <span>
            <el-button @click="handleDialogClose">取消</el-button>
            <el-button type="primary" @click="submitDoc">上传</el-button>
        </span>
        </template>
    </el-dialog>

	
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
import { ElMessage } from 'element-plus'

export default {
    props: ['orderId'],
    components: {
    	AllHeader
    },
    computed:{
        uploadHeaders() {
              return {
                Authorization: `Bearer ${this.token}`
              };
            }
    },
    data() {
        return {
            token: localStorage.getItem('token'),
            orderData: {},
            orderShoeData:[],
            orderDocData:{},
            expandedRowKeys:[],
            orderShoeTypeIdToUnitPrice:{},
            orderShoeTypeIdToCurrencyType:{},
            isSubmitDocVis:false,
            remarkDialogVis:false,
            priceChangeNotAllowed:false,
            unitChangeNotAllowed:false,
            remarkForm:{
                        orderShoeId:'',
                        technicalRemark:'',
                        materialRemark:''
            },
            batchInfoType:{},
            attrMappingToRatio:{
                "size34Name":"size34Ratio",
                "size35Name":"size35Ratio",
                "size36Name":"size36Ratio",
                "size37Name":"size37Ratio",
                "size38Name":"size38Ratio",
                "size39Name":"size39Ratio",
                "size40Name":"size40Ratio",
                "size41Name":"size41Ratio",
                "size42Name":"size42Ratio",
                "size43Name":"size43Ratio",
                "size44Name":"size44Ratio",
                "size45Name":"size45Ratio",
                "size46Name":"size46Ratio",
            },
            attrMappingToAmount:{
                "size34Name":"size34Amount",
                "size35Name":"size35Amount",
                "size36Name":"size36Amount",
                "size37Name":"size37Amount",
                "size38Name":"size38Amount",
                "size39Name":"size39Amount",
                "size40Name":"size40Amount",
                "size41Name":"size41Amount",
                "size42Name":"size42Amount",
                "size43Name":"size43Amount",
                "size44Name":"size44Amount",
                "size45Name":"size45Amount",
                "size46Name":"size46Amount",
            },

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
          console.log(response.data)
          this.orderData = response.data
          this.orderShoeData = response.data.orderShoeAllData
          this.batchInfoType = response.data.batchInfoType
      	},
        togglePriceChange()
        {
            this.priceChangeNotAllowed = !this.priceChangeNotAllowed
        },
        toggleUnitChange()
        {
            this.unitChangeNotAllowed = !this.unitChangeNotAllowed
        },
        oprenRemarkDialog(row)
        {
            console.log(row.orderShoeId)
            this.remarkForm.orderShoeId = row.orderShoeId
            this.remarkDialogVis = true
        },
      	expandOpen(row, expand){
            console.log(this.expandedRowKeys)
            this.expandedRowKeys.push(row.shoeTypeId)
            // row.batchQuantityMapping = row.orderShoeTypeBatchInfo.map((batchInfo) => { return batchInfo.packagingInfoId:batchInfo.unitQuantityInPair})Id})
        },
        updateValue(row)
        {
            row.shoeTypeBatchData.totalPrice = row.shoeTypeBatchData.unitPrice * row.shoeTypeBatchData.totalAmount
            this.orderShoeTypeIdToUnitPrice[row.orderShoeTypeId] = row.shoeTypeBatchData.unitPrice

        },
        updateCurrencyValue(row)
        {
            this.orderShoeTypeIdToCurrencyType[row.orderShoeTypeId] = row.shoeTypeBatchData.currencyType
            console.log(this.orderShoeTypeIdToCurrencyType)

        },
        async submitPriceForm()
        {   
            const response = await axios.post(
                `${this.$apiBaseUrl}/ordercreate/updateprice`, {
                    "unitPriceForm":this.orderShoeTypeIdToUnitPrice,
                    "currencyTypeForm":this.orderShoeTypeIdToCurrencyType
                })
            if (response.status === 200)
            {
                ElMessage.success('变更成功')
                this.getOrderInfo()
            }
            else
            {
                ElMessage.error('备注变更失败')
            }
            console.log(this.orderShoeTypeIdToUnitPrice)

            return
        },
        async submitRemarkForm(){
            console.log(this.remarkForm)
            const response = await axios.post(
                `${this.$apiBaseUrl}/ordercreate/updateremark`, {
                    "orderShoeRemarkForm":this.remarkForm
            })
            if (response.status === 200)
            {
                ElMessage.success('信息变更成功')
                this.getOrderInfo()
                this.remarkDialogVis = false
            }
        },
        openSubmitDialog(){
            this.isSubmitDocVis = true
        },
        handleUploadSuccess(response, file) {
            // Handle the successful response
            console.log('Upload successful:', response)
            ElMessage.success('上传成功')
            this.isSubmitDocVis = false
        },
        handleUploadError(error, file) {
            // Handle any errors that occurred during the upload
            console.error('Upload error:', error)
            ElMessage.error('上传失败')
            this.fileList = []
            this.isSubmitDocVis = false

        },
        download(type) {
            window.open(
                `${this.$apiBaseUrl}/orderimport/downloadorderdoc?orderrid=${this.orderData.orderRid}&filetype=${type}`
            )
        },
        async submitDoc() {
            try {
                const loadingInstance = this.$loading({
                        lock: true,
                        text: '等待中，请稍后...',
                        background: 'rgba(0, 0, 0, 0.7)'
                    })
                // Manually submit the file without reopening the dialog
                console.log(this.$refs.uploadDoc)
                await this.$refs.uploadDoc.submit()
                loadingInstance.close()
            }
            catch (error) {
                console.error('Upload error:', error)
                ElMessage.error('上传失败')
            }

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
        handleDialogClose(){
            console.log("TODO handle dialog close in OrderManagement.Vue")
        },

	}
}
</script>
<style >
/* Add your styles here */
.el-table .cell {
    white-space: pre-line !important;
}
</style>