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
                size="normal"
                :suffix-icon="Search"
                clearable
                @input="filterByRid()"
            ></el-input>
        </el-col>

        <el-col :span="4" :offset="19"
            ><el-input
                v-model="orderCidFilter"
                placeholder="请输入客户订单号"
                size="normal"
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
        <el-form :model="orderForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="请输入订单号">
                <el-input v-model="orderForm.orderRId"></el-input>
            </el-form-item>
            <el-form-item label="请选择客户">
                <el-select v-model="orderForm.customerId" filterable placeholder="请选择客户">
                    <el-option
                        v-for="item in customerList"
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
    <
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
        <el-form :model="newOrderForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="请输入订单号">
                <el-input v-model="newOrderForm.orderRId"></el-input>
            </el-form-item>
            <el-form-item label="请选择客户">
                <el-select v-model="newOrderForm.customerId" filterable placeholder="请选择客户">
                    <el-option
                        v-for="item in customerList"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-row :gutter="20">
            <el-col :span="4" :offset="0" style="white-space: nowrap;">
                鞋型号搜索：
                <el-input v-model="shoeRidFilter" 
                placeholder="" size="normal" 
                :suffix-icon="Search"
                clearable 
                @input="filterByShoeRid()">
            </el-input> 
            </el-col>
            
            </el-row>
            <el-table
                :data="shoeTableDisplayData"
                style="width: 100%"
                stripe
                border
                height="500"
                @selection-change="newOrderForm.orderShoeTypes = $event"
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


    <el-dialog title="创建订单详情填写" v-model="orderCreationSecondInfoVis" width="80%">


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
            customerList: [],
            orderStatusList: [],
            previewOrderVis: false,
            orderInfoVis: false,
            fileList: [],
            isImportVis: false,
            isSubmitDocVis: false,
            orderCreationInfoVis: false,
            orderCreationSecondInfoVis: false,
            Search,
            Upload,
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
                customerId: null,
                orderShoeTypes:[],

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
        orderCreationSecondStep() {
            this.orderCreationInfoVis = false
            this.orderCreationSecondInfoVis = true
            console.log(this.newOrderForm)


        },
        hendleSelectionChange() {
            console.log("selection Changed")
        },
        async getAllCutomers() {
            const response = await axios.get(`${this.$apiBaseUrl}/customer/getallcustomers`)
            this.customerList = response.data
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
            console.log("123123123")
            if (!this.shoeRidFilter){
                this.shoeTableDisplayData = this.shoeTableData
            }
            else{
                this.shoeTableTemp = this.shoeTableData.filter((task) => {
                const filterMatch = task.shoeRId.includes(this.shoeRidFilter)
                return filterMatch
            })
                this.shoeTableDisplayData = this.shoeTableTemp
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
