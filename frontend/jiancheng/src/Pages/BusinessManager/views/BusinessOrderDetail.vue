<template>
    <el-container>
        <el-header>
            <AllHeader></AllHeader>
        </el-header>
        <el-container>
            <el-main>
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
                            <el-descriptions-item label="配码类型" align="center">{{
                                orderData.batchInfoTypeName
                            }}</el-descriptions-item>
                            <el-descriptions-item label="包装资料上传状态" align="center"
                                >{{ orderData.wrapRequirementUploadStatus }}
                                <el-button type="primary" size="default" @click="openSubmitDialog()"
                                    >上传</el-button
                                >
                                <el-button
                                    v-if="
                                        orderData.wrapRequirementUploadStatus === '已上传包装文件'
                                    "
                                    type="primary"
                                    size="default"
                                    @click="download(2)"
                                    >查看</el-button
                                >
                            </el-descriptions-item>
                            <el-descriptions-item label="财务信息操作" align="center">
                                <el-button
                                    v-if="priceUpdateButtonVis"
                                    @click="submitPriceForm"
                                    type="primary"
                                    >保存财务信息</el-button
                                >
                                <el-button v-if="this.role == 4" @click="toggleFinInfoChange">
                                    财务信息修改权限
                                </el-button>
                                <el-button
                                    v-if="this.allowNext"
                                    type="warning"
                                    @click="sendOrderNext"
                                    :disabled="this.role == '21' ? true : false"
                                >
                                    下发
                                </el-button>
                            </el-descriptions-item>
                        </el-descriptions>
                    </el-col>
                </el-row>
                <el-table
                    :data="orderShoeData"
                    border
                    stripe
                    height="700"
                    :row-key="
                        (row) => {
                            return `${row.orderShoeId}`
                        }
                    "
                >
                    <el-table-column type="expand">
                        <template #default="props">
                            <el-table
                                :data="props.row.orderShoeTypes"
                                border
                                :row-key="
                                    (row) => {
                                        return `${row.orderShoeTypeId}`
                                    }
                                "
                            >
                                <el-table-column type="expand">
                                    <template #default="scope">
                                        <el-table :data="scope.row.shoeTypeBatchInfoList">
                                            <el-table-column type="index"></el-table-column>
                                            <el-table-column
                                                prop="packagingInfoName"
                                                label="配码名称"
                                                width="150"
                                            />
                                            <el-table-column
                                                v-for="col in Object.keys(
                                                    this.attrMappingToRatio
                                                ).filter((key) => this.batchInfoType[key] != '')"
                                                :prop="attrMappingToRatio[col]"
                                                :label="batchInfoType[col]"
                                                width="90"
                                            ></el-table-column>
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
                                            <el-table-column
                                                prop="totalQuantityRatio"
                                                label="对/件"
                                                width="240"
                                            />
                                            <el-table-column prop="unitPerRatio" label="件数" />
                                        </el-table>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="shoeTypeColorName"
                                    label="颜色名称"
                                    width="150"
                                    sortable
                                />
                                <!-- <el-table-column v-for="col in Object.keys(attrMappingToAmount).filter(key=>batchInfoType[key] != null)"
                                        :prop="props.row.orderShoeTypes.shoeTypeBatchData[]"
                                        :label="batchInfoType[col]">
                        </el-table-column> -->
                                <el-table-column
                                    v-for="col in Object.keys(this.attrMappingToAmount).filter(
                                        (key) => this.batchInfoType[key] != ''
                                    )"
                                    :prop="`shoeTypeBatchData.${attrMappingToAmount[col]}`"
                                    :label="batchInfoType[col]"
                                    width="90"
                                ></el-table-column>
                                <el-table-column
                                    prop="shoeTypeBatchData.totalAmount"
                                    label="总数量"
                                    width="120"
                                />
                                <el-table-column label="金额" width="120">
                                    <template #default="scope">
                                        <el-input
                                            size="small"
                                            controls-position="right"
                                            @change="updateValue(scope.row)"
                                            v-model="scope.row.shoeTypeBatchData.unitPrice"
                                            :disabled="
                                                !this.unitPriceAccessMapping[
                                                    scope.row.orderShoeTypeId
                                                ]
                                            "
                                        >
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column label="金额单位">
                                    <template #default="scope">
                                        <el-input
                                            size="small"
                                            controls-position="right"
                                            @change="updateCurrencyValue(scope.row)"
                                            v-model="scope.row.shoeTypeBatchData.currencyType"
                                            :disabled="
                                                !this.currencyTypeAccessMapping[
                                                    scope.row.orderShoeTypeId
                                                ]
                                            "
                                        >
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="shoeTypeBatchData.totalPrice"
                                    label="总金额"
                                />
                            </el-table>
                        </template>
                    </el-table-column>
                    <el-table-column prop="shoeRid" label="鞋型编号" sortable />
                    <el-table-column prop="shoeCid" label="客户鞋型编号" sortable />
                    <el-table-column prop="currentStatus" label="鞋型状态" />

                    <el-table-column label="备注">
                        <template #default="scope">
                            <el-button
                                v-if="!scope.row.orderShoeRemarkExist"
                                type="primary"
                                size="default"
                                @click="openRemarkDialog(scope.row)"
                                style="margin-left: 20px"
                                >添加备注
                            </el-button>

                            <el-text v-if="scope.row.orderShoeRemarkExist">{{
                                scope.row.orderShoeRemarkRep
                            }}</el-text>
                            <el-button
                                v-if="scope.row.orderShoeRemarkExist"
                                type="warning"
                                size="default"
                                @click="openEditRemarkDialog(scope.row)"
                                style="margin-left: 20px; margin-top: -20px"
                            >
                                编辑备注
                            </el-button>
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
            </el-main>
        </el-container>
    </el-container>

    <el-dialog title="鞋型备注" v-model="remarkDialogVis" width="50%">
        <el-form>
            <el-form-item label="工艺备注">
                <el-input
                    type="textarea"
                    :rows="2"
                    v-model="this.remarkForm.technicalRemark"
                ></el-input>
            </el-form-item>

            <el-form-item label="材料备注">
                <el-input
                    type="textarea"
                    :rows="2"
                    v-model="this.remarkForm.materialRemark"
                ></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span>
                <el-button @click="remarkDialogVis = false">取消</el-button>

                <el-button type="primary" @click="submitRemarkForm">提交备注</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="包装资料上传" v-model="isSubmitDocVis" width="30%" @close="handleDialogClose">
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
            <el-button type="primary">选择文件</el-button>
        </el-upload>

        <template #footer>
            <span>
                <el-button @click="isSubmitDocVis = false">取消</el-button>
                <el-button type="primary" @click="submitDoc">上传</el-button>
            </span>
        </template>
    </el-dialog>
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
    computed: {
        uploadHeaders() {
            return {
                Authorization: `Bearer ${this.token}`
            }
        },
        allowNext() {
            return this.orderCurStatus == 6 && this.orderCurStatusVal == 1
        },
        // allowChangeUnitPrice: function(row)
        // {
        //     return this.unitPriceAccessMapping[row.orderShoeTypeId]
        // },
        priceUpdateButtonVis() {
            return (
                Object.values(this.unitPriceAccessMapping).includes(true) ||
                Object.values(this.currencyTypeAccessMapping).includes(true)
            )
        }
    },
    data() {
        return {
            token: localStorage.getItem('token'),
            role: localStorage.getItem('role'),
            staffId: localStorage.getItem('staffid'),
            orderData: {},
            orderDBId: '',
            orderCurStatus: '',
            orderCurStatusVal: '',
            orderShoeData: [],
            orderDocData: {},
            expandedRowKeys: [],
            orderShoeTypeIdToUnitPrice: {},
            orderShoeTypeIdToCurrencyType: {},
            isSubmitDocVis: false,
            remarkDialogVis: false,
            priceChangeNotAllowed: false,
            unitChangeNotAllowed: false,
            remarkForm: {
                orderShoeId: '',
                technicalRemark: '',
                materialRemark: ''
            },
            unitPriceAccessMapping: {},
            currencyTypeAccessMapping: {},
            batchInfoType: {},
            attrMappingToRatio: {
                size34Name: 'size34Ratio',
                size35Name: 'size35Ratio',
                size36Name: 'size36Ratio',
                size37Name: 'size37Ratio',
                size38Name: 'size38Ratio',
                size39Name: 'size39Ratio',
                size40Name: 'size40Ratio',
                size41Name: 'size41Ratio',
                size42Name: 'size42Ratio',
                size43Name: 'size43Ratio',
                size44Name: 'size44Ratio',
                size45Name: 'size45Ratio',
                size46Name: 'size46Ratio'
            },
            attrMappingToAmount: {
                size34Name: 'size34Amount',
                size35Name: 'size35Amount',
                size36Name: 'size36Amount',
                size37Name: 'size37Amount',
                size38Name: 'size38Amount',
                size39Name: 'size39Amount',
                size40Name: 'size40Amount',
                size41Name: 'size41Amount',
                size42Name: 'size42Amount',
                size43Name: 'size43Amount',
                size44Name: 'size44Amount',
                size45Name: 'size45Amount',
                size46Name: 'size46Amount'
            }
        }
    },
    mounted() {
        this.getOrderInfo()
        // this.getOrderOrderShoe()
        // this.getOrderOrderShoe()
        console.log(this.role)
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
            this.orderDBId = this.orderData.orderId
            this.orderCurStatus = this.orderData.orderStatus
            this.orderCurStatusVal = this.orderData.orderStatusVal
            this.orderData.orderShoeAllData.forEach((orderShoe) =>
                orderShoe.orderShoeTypes.forEach((orderShoeType) => {
                    this.orderShoeTypeIdToUnitPrice[orderShoeType.orderShoeTypeId] =
                        orderShoeType.shoeTypeBatchData.unitPrice
                    this.orderShoeTypeIdToCurrencyType[orderShoeType.orderShoeTypeId] =
                        orderShoeType.shoeTypeBatchData.currencyType
                    this.unitPriceAccessMapping[orderShoeType.orderShoeTypeId] =
                        orderShoeType.shoeTypeBatchData.unitPrice == 0
                    this.currencyTypeAccessMapping[orderShoeType.orderShoeTypeId] =
                        orderShoeType.shoeTypeBatchData.currencyType == ''
                })
            )
            console.log(this.unitPriceAccessMapping)
            console.log(this.currencyTypeAccessMapping)
        },
        updateStatus() {
            return
        },
        toggleFinInfoChange() {
            Object.keys(this.unitPriceAccessMapping).forEach(
                (key) => (this.unitPriceAccessMapping[key] = !this.unitPriceAccessMapping[key])
            )
            Object.keys(this.currencyTypeAccessMapping).forEach(
                (key) =>
                    (this.currencyTypeAccessMapping[key] = !this.currencyTypeAccessMapping[key])
            )
        },
        setfinInfoAccess() {},
        allowChangeCurrencyType(row) {
            return this.currencyTypeAccessMapping[row.orderShoeTypeId]
        },
        allowChangeUnitPrice(row) {
            return this.unitPriceAccessMapping[row.orderShoeTypeId]
        },
        setFinInfoNotAllowed() {
            this.priceChangeNotAllowed = true
            this.unitChangeNotAllowed = true
            this.priceUpdateButtonVis = false
        },
        openRemarkDialog(row) {
            console.log(row.orderShoeId)
            this.remarkForm.orderShoeId = row.orderShoeId
            this.remarkDialogVis = true
        },
        openEditRemarkDialog(row) {
            this.remarkForm.orderShoeId = row.orderShoeId
            this.remarkForm.technicalRemark = row.orderShoeTechnicalRemark
            this.remarkForm.materialRemark = row.orderShoeMaterialRemark
            this.remarkDialogVis = true
        },
        sendOrderNext() {
            if (this.orderData.wrapRequirementUploadStatus === '已上传包装文件') {
                const value = [...Object.values(this.orderShoeTypeIdToUnitPrice)]
                const unit = [...Object.values(this.currencyTypeAccessMapping)]
                if (value.includes(0)) {
                    ElMessage.error('请检查订单中的金额数据，不允许值为0')
                    return
                }
                if (unit.includes(true)) {
                    ElMessage.error('请检查订单中的金额单位，不允许单位为空')
                    return
                }
                this.$confirm('确认下发订单？', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(async () => {
                        const result = await axios.post(
                            `${this.$apiBaseUrl}/ordercreate/sendnext`,
                            {
                                orderId: this.orderDBId,
                                staffId: this.staffId
                            }
                        )
                        if (result.status === 200) {
                            ElMessage.success('下发成功,正在重新加载数据')
                        } else {
                            ElMessage.error('下发失败')
                        }
                    })
                    .then(async () => {
                        this.getOrderInfo()
                    })
            } else {
                ElMessage.error('包装文件未上传,请上传包装文件后再下发！')
                return
            }
        },
        expandOpen(row, expand) {
            console.log(this.expandedRowKeys)
            this.expandedRowKeys.push(row.shoeTypeId)
            // row.batchQuantityMapping = row.orderShoeTypeBatchInfo.map((batchInfo) => { return batchInfo.packagingInfoId:batchInfo.unitQuantityInPair})Id})
        },
        updateValue(row) {
            console.log(row)
            row.shoeTypeBatchData.totalPrice =
                row.shoeTypeBatchData.unitPrice * row.shoeTypeBatchData.totalAmount
            this.orderShoeTypeIdToUnitPrice[row.orderShoeTypeId] = row.shoeTypeBatchData.unitPrice
        },
        updateCurrencyValue(row) {
            this.orderShoeTypeIdToCurrencyType[row.orderShoeTypeId] =
                row.shoeTypeBatchData.currencyType
            console.log(this.orderShoeTypeIdToCurrencyType)
        },
        async submitPriceForm() {
            console.log(this.orderShoeTypeIdToCurrencyType)
            const response = await axios.post(`${this.$apiBaseUrl}/ordercreate/updateprice`, {
                unitPriceForm: this.orderShoeTypeIdToUnitPrice,
                currencyTypeForm: this.orderShoeTypeIdToCurrencyType,
                orderId: this.orderDBId,
                staffId: this.staffId
            })
            if (response.status === 200) {
                ElMessage.success('变更成功')
                this.getOrderInfo()
            } else {
                ElMessage.error('备注变更失败')
            }
            console.log(this.orderShoeTypeIdToUnitPrice)

            return
        },
        async submitRemarkForm() {
            console.log(this.remarkForm)
            const response = await axios.post(`${this.$apiBaseUrl}/ordercreate/updateremark`, {
                orderShoeRemarkForm: this.remarkForm
            })
            if (response.status === 200) {
                ElMessage.success('信息变更成功')
                this.getOrderInfo()
                this.remarkDialogVis = false
            } else {
                ElMessage.error('信息变更失败')
            }
        },
        openSubmitDialog() {
            this.isSubmitDocVis = true
        },
        handleUploadSuccess(response, file) {
            // Handle the successful response
            console.log('Upload successful:', response)
            ElMessage.success('上传成功')
            this.isSubmitDocVis = false
            this
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
                this.getOrderInfo()
            } catch (error) {
                console.error('Upload error:', error)
                ElMessage.error('上传失败')
            }
        },
        checkdata() {
            console.log(this.orderData)
            console.log(this.orderShoePreviewData)
            console.log(this.orderDocData)
        },
        openSubmitDocDialog() {},
        downloadDoc() {},
        handleDialogClose() {
            console.log('TODO handle dialog close in OrderManagement.Vue')
        }
    }
}
</script>
<style>
/* Add your styles here */
.el-table .cell {
    white-space: pre-line !important;
}
</style>
