<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
            >订单管理</el-col
        >
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0"
            >
            <el-button size="default" type="primary" @click="openImportDialog"
                >通过EXCEL上传订单</el-button
            >
            <el-button size="default" type="primary" @click="openCreateOrderDialog"
                >创建订单</el-button
            >
        </el-col>
        <el-col :span="4" :offset="15"
            ><el-input
                v-model="orderRidFilter"
                placeholder="请输入订单号"
                size="default"
                :suffix-icon="Search"
                clearable
                @input="filterByRid()"
            ></el-input>
        </el-col>

        <el-col :span="4" :offset="19"
            ><el-input
                v-model="orderCidFilter"
                placeholder="请输入客户订单号"
                size="default"
                :suffix-icon="Search"
                clearable
                @input="filterByCid()"
            ></el-input>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="displayData" border stripe height="500">
            <el-table-column type="index" width="50" />
            <el-table-column prop="orderRid" label="订单号" />
            <el-table-column prop="customerName" label="客户名" />
            <el-table-column prop="orderCid" label="客户订单号" />
            <el-table-column prop="orderStartDate" label="订单开始日期" sortable />
            <el-table-column prop="orderEndDate" label="订单结束日期" sortable/>
            <el-table-column prop="orderStatus" label="订单状态" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" size="default" @click="openPreviewDialog(scope.row)"
                        >查看详情</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
    </el-row>
<el-dialog title="订单详情" v-model="previewOrderVis" width="90%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderRid
                    }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间" align="center">{{
                        orderData.orderStartDate
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                    <el-descriptions-item label="订单预计截止日期" align="center">{{
                        orderData.orderEndDate
                    }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="包装资料上传状态" align="center"
                        >{{ orderDocData.productionDoc }}
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
        </el-row>
        <el-row :gutter="20">
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
        </el-row>

        <template #footer>
            <span>
                <el-button type="primary" @click="previewOrderVis = false">确认</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        title="订单EXCEL导入"
        v-model="isImportVis"
        width="100%"
        @close="closeClearUploadData"
    >
        <el-upload
            ref="upload"
            :action="`${this.$apiBaseUrl}/orderimport/getuploadorder`"
            :headers="uploadHeaders"
            :before-upload="beforeUpload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            accept=".xls,.xlsx"
            :file-list="fileList"
            limit="1"
        >
            <el-button type="warning" :icon="Upload">上传文件选择</el-button>
        </el-upload>
        <el-table :data="uploadData" border stripe :span-method="mergeCells" height="500">
            <el-table-column prop="inheritId" label="工厂型号"></el-table-column>
            <el-table-column prop="customerId" label="客户型号"></el-table-column>
            <el-table-column prop="colorCN" label="中文颜色"></el-table-column>
            <el-table-column prop="colorEN" label="英文颜色"></el-table-column>
            <el-table-column prop="sizeId" label="配码"></el-table-column>
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
            <el-table-column prop="pairEachBox" label="双/件"></el-table-column>
            <el-table-column prop="boxCount" label="件数"></el-table-column>
            <el-table-column prop="pairCount" label="双数"></el-table-column>
            <el-table-column prop="pairCount" label="双数"></el-table-column>
            <el-table-column prop="currencyType" label="货币单位"></el-table-column>
            <el-table-column prop="pricePerPair" label="单价"></el-table-column>
            <el-table-column prop="totalPrice" label="总价"></el-table-column>
        </el-table>

        <template #footer>
            <span>
                <el-button @click="closeClearUploadData">取消</el-button>
                <el-button type="primary" @click="confirmImportFile">确认导入</el-button>
            </span>
        </template>
    </el-dialog>
    
    <el-dialog title="订单详情填写" v-model="orderInfoVis" width="40%">
        <el-form :model="orderForm" label-width="120px" :inline="false" size="default">
            <el-form-item label="请输入订单号">
                <el-input v-model="orderForm.orderRId"></el-input>
            </el-form-item>
            <el-form-item label="请选择客户">
                <el-select v-model="orderForm.customerId" filterable placeholder="请选择客户">
                    <el-option
                        v-for="item in customerNameList"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="订单开始日期">
                <el-date-picker
                    v-model="orderForm.orderStartDate"
                    type="date"
                    placeholder="选择日期"
                    value-format="YYYY-MM-DD"
                ></el-date-picker>
            </el-form-item>
            <el-form-item label="订单结束日期">
                <el-date-picker
                    v-model="orderForm.orderEndDate"
                    type="date"
                    placeholder="选择日期"
                    value-format="YYYY-MM-DD"
                ></el-date-picker>
            </el-form-item>
            <el-form-item label="订单状态">
                <el-select v-model="orderForm.status" filterable placeholder="请选择订单状态">
                    <el-option
                        v-for="item in orderStatusList"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="业务员">
                <el-input v-model="orderForm.salesman"></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span>
                <el-button @click="orderInfoVis = false">取消</el-button>
                <el-button type="primary" @click="confirmImportInfo">确认</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        :title="submitDocType === 0 ? '上传生产订单' : '上传生产数量单'"
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
            :data="{ fileType: submitDocType, orderRid: orderData.orderRid }"
            :on-success="handleUploadDocSuccess"
            :on-error="handleUploadDocError"
        >
            <el-button  type="primary">选择文件</el-button>
        </el-upload>


        <template #footer>
            <span>
            <el-button @click="handleDialogClose">取消</el-button>
            <el-button type="primary" @click="submitUpload">上传</el-button>
        </span>
        </template>
    </el-dialog>


    <el-dialog title="创建订单鞋型填写" v-model="orderCreationInfoVis" width="80%">
        <el-form :model="newOrderForm" label-width="120px" :inline="false" size="default">
            <el-form-item label="请输入订单号">
                <el-input v-model="newOrderForm.orderRId"></el-input>
            </el-form-item>
            <el-form-item label="请输入客户订单号">
                <el-input v-model="newOrderForm.orderCid"></el-input>
            </el-form-item>
            <el-form-item label="请选择客户">
                <el-select v-model="newOrderForm.customerName" filterable placeholder="请选择客户" @change="updateCustomerBrand">
                    <el-option
                        v-for="item in this.customerNameList"
                        :key="item"
                        :label="item"
                        :value="item"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="请选择客户商标">
                <el-select v-model="newOrderForm.customerBrand" filterable placeholder="请选择商标" @change="updateCustomerId">
                    <el-option
                        v-for="item in this.customerBrandList"
                        :key="item"
                        :label="item"
                        :value="item"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-row :gutter="20">
            <el-col :span="4" :offset="0" style="white-space: nowrap;">
                鞋型号搜索：
                <el-input v-model="shoeRidFilter" 
                placeholder="" size="default" 
                :suffix-icon="Search"
                clearable 
                @input="filterByShoeRidWithSelection">
            </el-input> 
            </el-col>
            </el-row>
            <el-table
                title=""
                :data="shoeTableDisplayData"
                style="width: 100%"
                stripe
                border
                height="500"
                ref="shoeSelectionTable"
                @selection-change="handleSelectionShoeType"
            >
                <!-- <el-table-column>
                    <el-input type = "checkbox" id= shoeRid v-model = "checkedgroup">
                    </el-input>
                    <el-checkbox 
                    prop="check" 
                    v-model = "checkgroup"/>
                </el-table-column> -->
                <el-table-column
                    size = "small"
                    type = "selection"
                    align = "center">
                </el-table-column>
                <el-table-column
                    prop="shoeRId"
                    label="鞋型编号"
                ></el-table-column>
                <el-table-column
                    prop="shoeColor"
                    label="鞋型颜色"
                ></el-table-column>
                <el-table-column
                    prop="shoeImage"
                    label="鞋型图片"
                    align="center">
                    <template #default="scope">
                        <el-image :src="scope.row.shoeImage" style="width: 150px; height: 100px;"/>
                    </template>
                </el-table-column>
            </el-table>
            <el-form-item label="业务员">
                <el-input v-model="newOrderForm.salesman"></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span>
                <el-button @click="orderCreationInfoVis = false">取消</el-button>
                <el-button type="primary" @click="orderCreationSecondStep">确认</el-button>
            </span>
        </template>
    </el-dialog>


    <el-dialog title="创建订单详情填写" v-model="orderCreationSecondInfoVis" width="90%">
        <el-col :span="4" :offset="15"
            ><el-input
                v-model="batchNameFilter"
                placeholder="请输入配码名称"
                size="default"
                :suffix-icon="Search"
                clearable
                @input="filterBatchData"
            ></el-input>
        </el-col>
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="订单号" align="center">{{
                        this.newOrderForm.orderRId
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户订单号" align="center">{{
                        this.newOrderForm.orderCid
                    }}</el-descriptions-item>
                </el-descriptions>
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="客户名称" align="center">{{
                        this.newOrderForm.customerName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户商标" align="center">{{
                        this.newOrderForm.customerBrand
                    }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <el-table :data="this.newOrderForm.orderShoeTypes" border stripe height = "900">
            <el-table-column type = "expand">
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
                        <el-table-column prop="totalQuantityInRatio"         label="比例和"/>
                        <el-table-column prop="unitQuantity" label="单位数量"/>
                        <el-table-column prop="totalQuantity" label="总数量"/>
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

        </el-table>
        <!-- <el-row :gutter="20">
            <el-table :data="customerDisplayBatchData" border stripe height="500">

                

                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default" @click="openPreviewDialog(scope.row)"
                            >查看详情</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </el-row> -->
        <span>
            <el-button @click="editCustomerBatchDialogVisible = false">取消</el-button>
            <el-button @click="openAddBatchInfoDialog(scope.row)"> 添加配码</el-button>
        </span>
    </el-dialog>

    <el-dialog
        title = "配码添加"
        v-model="addBatchInfoDialogVis"
        width = "90%">
        <el-col :span="4" :offset="15"
            ><el-input
                v-model="batchNameFilter"
                placeholder="请输入配码名称"
                size="normal"
                :suffix-icon="Search"
                clearable
                @input="filterBatchData"
            ></el-input>
        </el-col>
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="客户名称" align="center">{{
                        batchDialogCurCustomerName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户商标" align="center">{{
                        batchDialogCurCustomerBrand
                    }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-table :data="customerDisplayBatchData" border stripe height="500" 
            @selection-change="scope.row.orderShoeTypeBatchInfo = $event">
                <el-table-column
                    size = "small"
                    type = "selection"
                    align = "center">
                </el-table-column>
                <el-table-column prop="packagingInfoName" label="配码名称" sortable/>
                <el-table-column prop="packagingInfoLocale" label="配码地区" sortable/>
                <el-table-column prop="size34Ratio" label="34" sortable/>
                <el-table-column prop="size35Ratio" label="35" sortable/>
                <el-table-column prop="size36Ratio" label="36" sortable/>
                <el-table-column prop="size37Ratio" label="37" sortable/>
                <el-table-column prop="size38Ratio" label="38" sortable/>
                <el-table-column prop="size39Ratio" label="39" sortable/>
                <el-table-column prop="size40Ratio" label="40" sortable/>
                <el-table-column prop="size41Ratio" label="41" sortable/>
                <el-table-column prop="size42Ratio" label="42" sortable/>
                <el-table-column prop="size43Ratio" label="43" sortable/>
                <el-table-column prop="size44Ratio" label="44" sortable/>
                <el-table-column prop="size45Ratio" label="45" sortable/>
                <el-table-column prop="size46Ratio" label="46" sortable/>
                <el-table-column prop="totalQuantityInRatio" label="比例和"sortable/>
                <!-- <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default" @click="openPreviewDialog(scope.row)"
                            >查看详情</el-button
                        >
                    </template>
                </el-table-column>
 -->            </el-table>
        </el-row>
        <span>
            <el-button @click="editCustomerBatchDialogVisible = false">取消</el-button>
            <el-button @click="openAddCustomerBatchDialog()"> 添加配码</el-button>
        </span>
        <el-button @click="CustomerBatchDialog()"> 添加配码</el-button>
    </el-dialog>

</template>

<script>
import { Download, Search, Upload } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
    data() {
        return {
            token: localStorage.getItem('token'),
            submitDocType: 0,
            orderShoePreviewData: [],
            orderData: {},
            orderDocData: {},
            customerNameList: [],
            customerBrandList: [],
            customerBatchData: [],
            customerDisplayBatchData:[],
            selectedShoeList:[],
            orderStatusList: [],
            orderBatchInfo:[],
            previewOrderVis: false,
            orderInfoVis: false,
            fileList: [],
            isImportVis: false,
            isSubmitDocVis: false,
            orderCreationInfoVis: false,
            orderCreationSecondInfoVis: false,
            parentBoarder:false,
            childBoarder:false,
            addBatchInfoDialogVis:false,
            Search,
            Upload,
            batchNameFilter:'',
            orderRidFilter: '',
            orderCidFilter: '',
            displayData: [],
            filterData: [],
            unfilteredData: [],
            uploadData: [],
            updatekey: 0,
            tempFileName: '',
            shoeTableData: [],
            shoeTableDisplayData: [],
            shoeTableTemp:[],
            shoeRidFilter: '',
            checkgroup:[],
            orderForm: {
                orderRId: '',
                orderCid: '',
                customerId: null,
                orderStartDate: '',
                orderEndDate: '',
                status: '',
                salesman: ''
            },
            newOrderForm:{
                orderRId:'',
                orderCid: '',
                customerId: null,
                orderStartDate: '',
                orderEndDate: '',
                status: '',
                salesman: '',
                orderShoeTypes:[],
                batchInfoMapping:[],
                batchInfoQuantity:[]
            }
        }
    },
    computed: {
    uploadHeaders() {
      return {
        Authorization: `Bearer ${this.token}`
      };
    }
  },
    mounted() {
        this.$setAxiosToken()
        this.getAllOrders()
        this.getAllCutomers()
        this.getAllOrderStatus()
        this.getAllShoes()
        console.log(this.$refs.shoeTypeSelectionTable)
    },
    methods: {

        openImportDialog() {
            this.isImportVis = true
        },
        openCreateOrderDialog() {
            this.orderCreationInfoVis = true
            this.shoeTableDisplayData = this.shoeTableData
        },  
        async openPreviewDialog(row) {
            this.orderData = row
            await this.getOrderOrderShoe(row.orderRid)
            await this.getOrderDocInfo(row.orderRid)
            this.previewOrderVis = true
        },
        openSubmitDocDialog(type) {
            this.isSubmitDocVis = true
            if (type == 0) {
                this.submitDocType = 0
            } else {
                this.submitDocType = 1
            }
        },
        openAddBatchInfoDialog(row) {
            this.addBatchInfoDialogVis = true
            console.log(row)
        },

        orderCreationSecondStep() {
            this.orderCreationInfoVis = false
            this.orderCreationSecondInfoVis = true
            this.newOrderForm.orderShoeTypes.forEach(item => {
                item.orderShoeTypeBatchInfo = []
            })
            this.getCustomerBatchInfo(this.newOrderForm.customerId)
            console.log(this.newOrderForm)

        },
        handleSelectionShoeType(selection) {
            this.selectedShoeList = selection
            this.newOrderForm.orderShoeTypes = selection
        },
        async getCustomerBatchInfo(customerId) {
            const response = await axios.get(`${this.$apiBaseUrl}/customer/getcustomerbatchinfo`,{
                params: {
                    customerid: customerId
                }
            })
            console.log(response.data)
            this.customerBatchData = response.data
            this.customerDisplayBatchData = response.data
        },
        async getAllCutomers() {
            const response = await axios.get(`${this.$apiBaseUrl}/customer/getcustomerdetails`)
            this.customerDetails = response.data
            this.customerNameList = [... new Set(response.data.map(item => item.customerName))]
        },
        updateCustomerBrand() {
            console.log(this.newOrderForm.customerName)
            this.customerBrandList = [... new Set(this.customerDetails.filter(item =>item.customerName == this.newOrderForm.customerName).map(item => item.customerBrand))]
        },
        updateCustomerId() {
            this.newOrderForm.customerId = this.customerDetails.filter(item => item.customerName == this.newOrderForm.customerName)
            .filter(item => item.customerBrand == this.newOrderForm.customerBrand)[0].customerId
            console.log(this.newOrderForm.customerId)
        },
        filterBatchData(){
            if (!this.batchNameFilter){
                this.customerDisplayBatchData = this.customerBatchData
            }
            else{
                this.customerFilteredBatchData = this.customerBatchData.filter((task) => {
                    const filteredData = task.packagingInfoName.includes(this.batchNameFilter)
                    return filteredData
                })
                this.customerDisplayBatchData = this.customerFilteredBatchData
            }
        },
        async getAllOrders() {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getallorders`)
            this.unfilteredData = response.data
            this.displayData = this.unfilteredData
        },
        async getAllOrderStatus() {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getallorderstatus`)
            this.orderStatusList = response.data
        },
        async getOrderOrderShoe(orderRid) {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getordershoeinfo`, {
                params: {
                    orderrid: orderRid
                }
            })
            this.orderShoePreviewData = response.data
        },
        async getAllShoes() {
            const response = await axios.get(`${this.$apiBaseUrl}/shoe/getallshoes`);
            this.shoeTableData = response.data;
        },
        async getOrderDocInfo(orderRid) {
            const response = await axios.get(`${this.$apiBaseUrl}/order/getorderdocinfo`, {
                params: {
                    orderrid: orderRid
                }
            })
            this.orderDocData = response.data
        },
        async submitUpload() {
            try {
                const loadingInstance = this.$loading({
                        lock: true,
                        text: '等待中，请稍后...',
                        background: 'rgba(0, 0, 0, 0.7)'
                    })
                // Manually submit the file without reopening the dialog
                await this.$refs.uploadDoc.submit().then(() => {
                    loadingInstance.close()
                })
            }
            catch (error) {
                console.error('Upload error:', error)
                ElMessage.error('上传失败')

            }

        },
        filterByCid(){
            if (!this.orderCidFilter){
                this.displayData = this.unfilteredData
            }
            else {
                this.filterData = this.unfilteredData.filter((task) => {
                const filterMatch = task.orderCid.includes(this.orderCidFilter)
                return filterMatch
            })
                this.displayData = this.filterData
            }
        },
        filterByRid(){
            if (!this.orderRidFilter){
                this.displayData = this.unfilteredData
            }
            else {
                this.filterData = this.unfilteredData.filter((task) => {
                const filterMatch = task.orderRid.includes(this.orderRidFilter)
                return filterMatch
            })
                this.displayData = this.filterData
            }
        },
        filterByShoeRid(){
            if (!this.shoeRidFilter){
                this.shoeTableDisplayData = this.shoeTableData
            }
            else{
                this.shoeTableTemp = this.shoeTableData.filter((task) => {
                const filterMatch = task.shoeRId.includes(this.shoeRidFilter)
                return filterMatch})

                this.shoeTableDisplayData = this.shoeTableTemp}
        },
        filterByShoeRidWithSelection(){
            if (!this.shoeRidFilter){
                this.shoeTableDisplayData = this.shoeTableData
            }
            else
            {

                this.shoeTableTemp = this.shoeTableData.filter((task) => {
                const filterMatch = task.shoeRId.includes(this.shoeRidFilter)
                return filterMatch})
                // console.log(this.shoeTableTemp)
                // console.log(this.selectedShoeList)
                this.shoeTableDisplayData = Array.from(new Set([...this.shoeTableTemp.concat(this.selectedShoeList)]))
                // this.selectedShoeList.forEach(row => {
                //     this.$refs.shoeTypeSelectionTable.toggleRowSelection(row, true)
                // })
                const selectedShoeTypeIds = this.selectedShoeList.map(row => row.shoeTypeId)
                const rowsToToggle = this.shoeTableDisplayData.filter(row => selectedShoeTypeIds.includes(row.shoeTypeId))

                this.$nextTick(()=>{
                    selectedShoeTypeIds.forEach(item =>
                    {
                    this.$refs.shoeSelectionTable.toggleRowSelection(this.shoeTableDisplayData.find(row => {
                        return row.shoeTypeId == item
                    }),true)
                    }) 
                })
                


                // this.shoeTableDisplayData.forEach(row => 
                //     {
                //     if (row.shoeTypeId in selectedShoeTypeIds)
                //         {
                //         this.$refs.shoeSelectionTable.toggleRowSelection(row, true)
                //         } 
                //     })
                
            }
        },
        handleUploadSuccess(response, file) {
            // Handle the successful response
            this.tempFileName = response.tempFileName
            this.uploadData = response.data
            console.log('Upload successful:', response)
            console.log(this.tempFileName)
        },
        async handleUploadError(error, file) {
            // Handle any errors that occurred during the upload
            console.error('Upload error:', error)
            ElMessage.error('上传失败')
        },
        handleUploadDocSuccess(response, file) {
            // Handle the successful response
            console.log('Upload successful:', response)
            ElMessage.success('上传成功')
            this.getOrderDocInfo(this.orderData.orderRid)
            this.isSubmitDocVis = false
        },
        handleUploadDocError(error, file) {
            // Handle any errors that occurred during the upload
            console.error('Upload error:', error)
            ElMessage.error('上传失败')
            this.fileList = []
            this.getOrderDocInfo(this.orderData.orderRid)
            this.isSubmitDocVis = false

        },
        downloadDoc(type) {
            window.open(
                `${this.$apiBaseUrl}/orderimport/downloadorderdoc?orderrid=${this.orderData.orderRid}&filetype=${type}`
            )
        },
        mergeCells({ row, column, rowIndex, columnIndex }) {
            const mergeColumns = ['inheritId', 'customerId', 'colorCN', 'colorEN']

            if (mergeColumns.includes(column.property)) {
                // Check if the previous row has the same value for the column
                if (
                    rowIndex > 0 &&
                    row[column.property] === this.uploadData[rowIndex - 1][column.property]
                ) {
                    return {
                        rowspan: 0, // Hide the current cell
                        colspan: 0
                    }
                } else {
                    // Count how many consecutive rows have the same value
                    let rowspan = 1
                    for (let i = rowIndex + 1; i < this.uploadData.length; i++) {
                        if (this.uploadData[i][column.property] === row[column.property]) {
                            rowspan++
                        } else {
                            break
                        }
                    }
                    return {
                        rowspan: rowspan, // Merge cells
                        colspan: 1
                    }
                }
            }
        },
        mergeCellsPreview({ row, column, rowIndex, columnIndex }) {
            const mergeColumns = ['inheritId', 'customerId', 'colorCN', 'colorEN', 'status']

            // Only merge 'status' when both 'status' and 'inheritId' are the same
            if (mergeColumns.includes(column.property)) {
                if (column.property === 'status') {
                    // For 'status', also check 'inheritId' to ensure they match before merging
                    if (
                        rowIndex > 0 &&
                        row[column.property] ===
                            this.orderShoePreviewData[rowIndex - 1][column.property] &&
                        row['inheritId'] === this.orderShoePreviewData[rowIndex - 1]['inheritId']
                    ) {
                        return {
                            rowspan: 0, // Hide the current cell
                            colspan: 0
                        }
                    } else {
                        let rowspan = 1
                        for (let i = rowIndex + 1; i < this.orderShoePreviewData.length; i++) {
                            if (
                                this.orderShoePreviewData[i][column.property] ===
                                    row[column.property] &&
                                this.orderShoePreviewData[i]['inheritId'] === row['inheritId']
                            ) {
                                rowspan++
                            } else {
                                break
                            }
                        }
                        return {
                            rowspan: rowspan, // Merge cells
                            colspan: 1
                        }
                    }
                } else {
                    // Default merging logic for other columns
                    if (
                        rowIndex > 0 &&
                        row[column.property] ===
                            this.orderShoePreviewData[rowIndex - 1][column.property]
                    ) {
                        return {
                            rowspan: 0, // Hide the current cell
                            colspan: 0
                        }
                    } else {
                        let rowspan = 1
                        for (let i = rowIndex + 1; i < this.orderShoePreviewData.length; i++) {
                            if (
                                this.orderShoePreviewData[i][column.property] ===
                                row[column.property]
                            ) {
                                rowspan++
                            } else {
                                break
                            }
                        }
                        return {
                            rowspan: rowspan, // Merge cells
                            colspan: 1
                        }
                    }
                }
            }
        },
        handleDialogClose(){
            console.log("TODO handle dialog close in OrderManagement.Vue")
        },
        async closeClearUploadData() {
            this.isImportVis = false
            this.$refs.upload.clearFiles()
            this.uploadData = []
            this.updatekey++
            await axios.delete(`${this.$apiBaseUrl}/orderimport/deleteuploadtempfile`, {
                params: {
                    fileName: this.tempFileName
                }
            })
        },
        confirmImportFile() {
            console.log('confirm import file')
            if (this.uploadData.length === 0) {
                this.$message({
                    type: 'error',
                    message: '请先上传文件'
                })
                return
            }
            this.orderInfoVis = true
        },
        confirmImportInfo() {
            console.log('confirm import info')

            this.$confirm('确认导入订单信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                    const loadingInstance = this.$loading({
                        lock: true,
                        text: '等待中，请稍后...',
                        background: 'rgba(0, 0, 0, 0.7)'
                    })
                    const response = await axios.post(
                        `${this.$apiBaseUrl}/orderimport/confirmimportorder`,
                        {
                            fileName: this.tempFileName,
                            orderInfo: this.orderForm
                        }
                    )
                    loadingInstance.close()
                    if (response.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '导入成功'
                        })
                        this.orderInfoVis = false
                        this.orderForm = {
                            orderRId: '',
                            customerId: null,
                            orderStartDate: '',
                            orderEndDate: '',
                            status: '',
                            salesman: ''
                        }
                        this.closeClearUploadData()
                        this.getAllOrders()
                    } else {
                        this.$message({
                            type: 'error',
                            message: '导入失败'
                        })
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消导入'
                    })
                })
        }
    }
}
</script>
