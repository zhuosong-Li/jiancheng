<template>
    <el-container :direction="vertical">
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main style="overflow-x: hidden">
            <el-row :gutter="20" style="text-align: center">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
                    >投产指令单创建</el-col
                >
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <span style="font-weight: bold; font-size: larger">订单信息：</span>
                    <el-row :gutter="20">
                        <el-col :span="24" :offset="0">
                            <Arrow :status="orderData.status" :key="updateArrowKey"></Arrow>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20">
                        <el-col :span="24" :offset="0">
                            <el-descriptions title="" :column="2" border>
                                <el-descriptions-item label="订单编号" align="center">{{
                                    orderData.orderId
                                }}</el-descriptions-item>
                                <el-descriptions-item label="订单创建时间" align="center">{{
                                    orderData.createTime
                                }}</el-descriptions-item>
                                <el-descriptions-item label="客户名称" align="center">{{
                                    orderData.customerName
                                }}</el-descriptions-item>
                                <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                                <el-descriptions-item label="订单预计截止日期" align="center">{{
                                    orderData.deadlineTime
                                }}</el-descriptions-item>
                            </el-descriptions>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 10px">
                <el-col :span="4" :offset="0">
                    <div style="display: flex; align-items: center; white-space: nowrap">
                        工厂型号搜索：<el-input
                            v-model="inheritIdSearch"
                            placeholder=""
                            size="default"
                            :suffix-icon="Search"
                            clearable
                            @input="tableWholeFilter"
                        ></el-input>
                    </div>
                </el-col>
            </el-row>

            <el-row :gutter="20" style="margin-top: 20px">
                <el-col :span="24" :offset="0">
                    <el-table :data="testTableFilterData" border style="height: 400px">
                        <el-table-column
                            prop="inheritId"
                            label="工厂型号"
                            align="center"
                            width="100"
                        ></el-table-column>
                        <el-table-column
                            prop="customerId"
                            label="客户型号"
                            align="center"
                        ></el-table-column>
                        <el-table-column label="鞋图" align="center">
                            <template #default="scope">
                                <el-image
                                    style="width: 150px; height: 100px"
                                    :src="scope.row.image"
                                    :fit="contain"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="designer"
                            label="设计员"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="editter"
                            label="调版员"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="status"
                            label="状态"
                            align="center"
                        ></el-table-column>
                        <el-table-column label="操作" align="center">
                            <template #default="scope">
                                <el-button
                                    v-if="scope.row.status === '未上传'"
                                    type="primary"
                                    @click="openUploadDialog(scope.row)"
                                    >上传投产指令单</el-button
                                >
                                <el-button
                                    v-else-if="scope.row.status === '已下发'"
                                    type="primary"
                                    @click="openPreviewDialog(scope.row)"
                                    >查看</el-button
                                >
                                <div v-else-if="scope.row.status === '已上传'">
                                    <el-button type="primary" @click="openUploadDialog(scope.row)"
                                        >重新上传投产指令单</el-button
                                    >
                                    <el-button type="success" @click="openPreviewDialog(scope.row)"
                                        >预览投产指令单</el-button
                                    >
                                </div>
                            </template></el-table-column
                        >
                    </el-table></el-col
                >
            </el-row>
            <el-row :gutter="22" style="margin-top: 10px">
                <el-col :span="6" :offset="20"
                    ><el-button type="primary" size="default" @click="openIssueDialog"
                        >下发投产指令单</el-button
                    >
                </el-col>
            </el-row>

            <el-dialog title="正式BOM表下发页面" v-model="isFinalBOM" width="90%">
                <el-descriptions title="订单信息" :column="2" border>
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderId
                    }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间" align="center">{{
                        orderData.createTime
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                    <el-descriptions-item label="订单预计截止日期" align="center">{{
                        orderData.deadlineTime
                    }}</el-descriptions-item>
                </el-descriptions>
                <div style="height: 400px; overflow-y: scroll; overflow-x: hidden">
                    <el-row :gutter="20" style="margin-bottom: 20px">
                        <el-col :span="24">
                            <el-table
                                :data="unIssueBOMData"
                                border
                                style="height: 400px"
                                @selection-change="handleShoeSelectionChange"
                            >
                                <el-table-column type="selection" width="55"></el-table-column>
                                <el-table-column
                                    prop="inheritId"
                                    label="工厂型号"
                                    align="center"
                                    width="100"
                                ></el-table-column>
                                <el-table-column
                                    prop="customerId"
                                    label="客户型号"
                                    align="center"
                                ></el-table-column>
                                <el-table-column label="鞋图" align="center">
                                    <template #default="scope">
                                        <el-image
                                            style="width: 150px; height: 100px"
                                            :src="scope.row.image"
                                            :fit="contain"
                                        />
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="designer"
                                    label="设计员"
                                    align="center"
                                ></el-table-column>
                                <el-table-column
                                    prop="editter"
                                    label="调版员"
                                    align="center"
                                ></el-table-column>
                                <el-table-column label="操作" align="center">
                                    <template #default="scope">
                                        <el-button
                                            type="primary"
                                            size="default"
                                            @click="openPreviewDialog(scope.row)"
                                            >查看投产指令单</el-button
                                        >
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-col>
                    </el-row>
                </div>
                <template #footer>
                    <span>
                        <el-button @click="isFinalBOM = false">取消</el-button>
                        <el-button type="primary" @click="issueBOMs(selectedShoe)"
                            >下发选定BOM表</el-button
                        >
                    </span>
                </template>
            </el-dialog>
            <el-dialog title="上传投产指令单" v-model="UploadVis" width="50%">
                <el-descriptions title="订单信息" :column="2" border>
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderId
                    }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间" align="center">{{
                        orderData.createTime
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                    <el-descriptions-item label="订单预计截止日期" align="center">{{
                        orderData.deadlineTime
                    }}</el-descriptions-item>
                </el-descriptions>
                <el-form :model="orderForm" label-width="120px" :inline="false" size="normal">
                    <el-form-item label="投产指令单上传">
                        <el-upload
                            action="http://localhost:8000/devproductionorder/upload"
                            :on-success="handleUploadSuccess"
                            :on-error="handleUploadError"
                            :headers="uploadHeaders"
                            :before-upload="beforeUpload"
                            :file-list="fileList"
                            :auto-upload="false"
                            :on-remove="handleRemove"
                            :limit="1"
                            list-type="text"
                            accept=".xls,.xlsx"
                            :data="{ orderId: orderData.orderId, orderShoeRId: currentShoeId }"
                            ref="productionOrderUpload"
                        >
                            <el-button size="small" type="primary">点击上传</el-button>
                            <div slot="tip" class="el-upload__tip">只能上传xls/xlsx文件</div>
                        </el-upload>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <span>
                        <el-button @click="UploadVis = false">取消</el-button>
                        <el-button type="primary" @click="confirmUpload">确认上传</el-button>
                    </span>
                </template>
            </el-dialog>
        </el-main>
    </el-container>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import Arrow from '@/components/OrderArrowView.vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

import axios from 'axios'
export default {
    components: {
        AllHeader,
        Arrow
    },
    props: ['orderId'],
    data() {
        return {
            token: localStorage.getItem('token'),
            currentShoeId: '',
            fileList: [],
            UploadVis: false,
            createEditSymbol: 0,
            sizeData: [],
            currentSizeData: [],
            currentSizeIndex: 0,
            isSizeDialogVisible: false,
            selectedShoe: '',
            unIssueBOMData: [],
            updateKey: 0,
            editVis: false,
            editBomId: '',
            previewBomId: '',
            newBomId: '',
            currentBomShoeId: '',
            materialSelectRow: null,
            Search,
            materialAddfinished: false,
            materialTypeSearch: '',
            materialSearch: '',
            factorySearch: '',
            assetFilterTable: [],
            colorOptions: [],
            newMaterialVis: false,
            updateArrowKey: 0,
            orderData: {},
            createVis: false,
            testTableData: [],
            testTableFilterData: [],
            bomTestData: [],
            editBomData: [],
            originalBomTestData: [],
            factoryOptions: [
                { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
                { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
                { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' }
                // Add more options here
            ],
            isPreviewDialogVisible: false,
            selectedFile: null,
            inheritIdSearch: '',
            isFinalBOM: false,
            orderProduceInfo: []
        }
    },
    async mounted() {
        this.$setAxiosToken()
        this.getOrderInfo()
        this.getAllShoeListInfo()
        this.getAllColorOptions()
        this.getAllDepartmentOptions()
    },
    computed: {
        uploadHeaders() {
            return {
                Authorization: `Bearer ${this.token}`
            }
        }
    },
    methods: {
        async getAllMaterialList() {
            const response = await axios.get(
                'http://localhost:8000/logistics/getmaterialtypeandname'
            )
            this.assetTable = response.data
            this.assetFilterTable = this.assetTable
        },
        async getOrderInfo() {
            const response = await axios.get(
                `http://localhost:8000/order/getorderInfo?orderid=${this.orderId}`
            )
            this.orderData = response.data
            console.log(this.orderData)
            this.updateArrowKey += 1
        },
        async getAllShoeListInfo() {
            const response = await axios.get(
                `http://localhost:8000/devproductionorder/getordershoelist?orderid=${this.orderId}`
            )
            this.testTableData = response.data
            this.tableWholeFilter()
        },
        async handleGenerate(row) {
            this.newBomId = row.bomId
            this.createVis = true
            this.getOrderShoeBatchInfo(this.orderData.orderId, row.inheritId)
            this.getBOMDetails(row)
            this.currentBomShoeId = row.inheritId
            this.createEditSymbol = 0
        },
        handleGenerateClose() {
            this.createVis = false
        },
        getFilteredFactoryOptions(materialName) {
            const filteredOptions = this.factoryOptions.filter(
                (option) => option.materialName === materialName
            )
            return [{ factoryName: '询价' }, ...filteredOptions]
        },
        async openEditDialog(row) {
            await this.getBOMDetails(row)
            await this.getOrderShoeBatchInfo(this.orderData.orderId, row.inheritId)
            this.newBomId = row.bomId
            this.createVis = true
            this.currentBomShoeId = row.inheritId
            this.createEditSymbol = 0
        },
        async openPreviewDialog(row) {
            window.open(
                `http://localhost:8000/devproductionorder/download?ordershoerid=${row.inheritId}&orderid=${this.orderData.orderId}`
            )
        },

        openIssueDialog() {
            this.isFinalBOM = true
            this.unIssueBOMData = this.testTableData.filter((row) => row.status === '已上传')
        },
        openUploadDialog(row) {
            this.UploadVis = true
            this.currentShoeId = row.inheritId
            console.log(this.currentShoeId)
        },
        closePreviewDialog() {
            this.isPreviewDialogVisible = false
        },
        tableWholeFilter() {
            if (!this.inheritIdSearch) {
                this.testTableFilterData = this.testTableData
                return
            }

            this.testTableFilterData = this.testTableData.filter((task) => {
                const inheritMatch = task.inheritId.includes(this.inheritIdSearch)
                return inheritMatch
            })
        },
        confirmUpload() {
            this.$confirm('确定上传投产指令单吗？', '提示', {
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
                    await this.$refs.productionOrderUpload.submit()
                    loadingInstance.close()
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消上传'
                    })
                })
        },
        handleUploadSuccess(response, file, fileList) {
            this.$message({
                message: '上传成功',
                type: 'success'
            })
            this.UploadVis = false
            this.getAllShoeListInfo()
        },
        handleUploadError() {
            this.$message.error('上传失败')
        },
        async issueBOMs(selectedShoe) {
            const loadingInstance = this.$loading({
                lock: true,
                text: '等待中，请稍后...',
                background: 'rgba(0, 0, 0, 0.7)'
            })
            const response = await axios.post('http://localhost:8000/devproductionorder/issue', {
                orderId: this.orderData.orderId,
                orderShoeIds: selectedShoe.map((shoe) => shoe.inheritId)
            })
            loadingInstance.close()
            if (response.status !== 200) {
                this.$message({
                    type: 'error',
                    message: '下发失败'
                })
                return
            }
            this.$message({
                type: 'success',
                message: '下发成功'
            })
            this.isFinalBOM = false
            this.getAllShoeListInfo()
        },
        confirmBOMIssue() {
            this.$confirm('确定下发选定投产指令单吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(() => {
                    this.issueBOMs(this.selectedShoe)
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消下发'
                    })
                })
        },
        handleMaterialSelectionChange(selection) {
            if (selection.length > 1) {
                // Ensure only one row is selected
                this.$refs.materialSelectTable.clearSelection()
                this.$refs.materialSelectTable.toggleRowSelection(
                    selection[selection.length - 1],
                    true
                )
            } else {
                this.materialSelectRow = selection[0]
            }
            console.log(this.materialSelectRow)
        },
        handleShoeSelectionChange(selection) {
            this.selectedShoe = selection
            console.log(this.selectedShoe)
        }
    },
    deleteCurrentRow(index, datafield) {
        this.$confirm('确定删除此行吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
            .then(() => {
                datafield.splice(index, 1)
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                })
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                })
            })
    },
    arraySpanMethod({ row, column, rowIndex, columnIndex }) {
        if (columnIndex === 0) {
            if (rowIndex > 0 && row.color === this.orderProduceInfo[rowIndex - 1].color) {
                return [0, 0]
            }
            let rowspan = 1
            for (let i = rowIndex + 1; i < this.orderProduceInfo.length; i++) {
                if (this.orderProduceInfo[i].color === row.color) {
                    rowspan++
                } else {
                    break
                }
            }
            return [rowspan, 1]
        }
        if (column.property === 'total') {
            let firstOccurrenceIndex = rowIndex
            for (let i = rowIndex - 1; i >= 0; i--) {
                if (this.orderProduceInfo[i].color === row.color) {
                    firstOccurrenceIndex = i
                } else {
                    break
                }
            }
            if (rowIndex !== firstOccurrenceIndex) {
                return [0, 0]
            }
            let rowspan = 1
            for (let i = firstOccurrenceIndex + 1; i < this.orderProduceInfo.length; i++) {
                if (this.orderProduceInfo[i].color === row.color) {
                    rowspan++
                } else {
                    break
                }
            }
            return [rowspan, 1]
        }
    },
    categroryFormatter(row) {
        if (row.materialCategory == 0) {
            return '无配码'
        } else {
            return '有配码'
        }
    }
}
</script>

<style scoped>
/* Add your styles here */
</style>
