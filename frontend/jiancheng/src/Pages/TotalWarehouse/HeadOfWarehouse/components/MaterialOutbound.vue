<template>
    <el-row :gutter="20">
        <el-col :span="6" :offset="0">
            <el-button-group>
                <el-button type="primary" size="default" @click="isMaterialDialogVisible = true">材料筛选</el-button>
            </el-button-group>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderNumberSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getMaterialTableData()" @clear="getMaterialTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeNumberSearch" placeholder="请输入鞋型号" clearable @keypress.enter="getMaterialTableData()"
                @clear="getMaterialTableData()" />
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-button v-if="isMultipleSelection" @click="openMultipleOutboundDialog">
            出库
        </el-button>
        <el-button v-if="isMultipleSelection" @click="openFinishOutboundDialog">
            完成出库
        </el-button>
        <el-button @click="toggleSelectionMode">
            {{ isMultipleSelection ? "退出" : "选择材料" }}
        </el-button>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="materialTableData" border stripe height="600" @sort-change="sortData"
            @selection-change="handleSelectionChange">
            <el-table-column v-if="isMultipleSelection" type="selection" width="55" :selectable="isSelectable" />
            <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120" sortable="custom">
            </el-table-column>
            <el-table-column label="采购订单号" width="100">
                <template #default="scope">
                    <el-tooltip effect="dark" :content="scope.row.purchaseDivideOrderRId" placement="bottom">
                        <span class="truncate-text">
                            {{ scope.row.purchaseDivideOrderRId }}
                        </span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="materialType" label="材料类型"></el-table-column>
            <el-table-column prop="materialName" label="材料名称"></el-table-column>
            <el-table-column prop="materialModel" label="材料型号"></el-table-column>
            <el-table-column prop="materialSpecification" label="材料规格"></el-table-column>
            <el-table-column prop="colorName" label="颜色"></el-table-column>
            <el-table-column prop="materialUnit" label="材料单位"></el-table-column>
            <el-table-column prop="estimatedInboundAmount" label="材料应入库数量" :formatter="formatDecimal"></el-table-column>
            <el-table-column prop="actualInboundAmount" label="材料实入库数量" :formatter="formatDecimal"></el-table-column>
            <el-table-column prop="currentAmount" label="材料库存" :formatter="formatDecimal"></el-table-column>
            <el-table-column prop="unitPrice" label="材料单价" :formatter="formatDecimal"></el-table-column>
            <el-table-column prop="totalPrice" label="材料总价" :formatter="formatDecimal"></el-table-column>
            <el-table-column prop="supplierName" label="材料供应商"></el-table-column>
            <el-table-column prop="orderRId" label="材料订单号"></el-table-column>
            <el-table-column prop="shoeRId" label="材料鞋型号"></el-table-column>
            <el-table-column prop="status" label="状态"></el-table-column>
        </el-table>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="materialTableData.length" />
        </el-col>
    </el-row>
    <el-dialog title="材料出库筛选" v-model="isMaterialDialogVisible" width="30%">
        请选择材料类型：
        <el-select v-model="materialTypeSearch" value-key="" placeholder="" clearable filterable
            @change="getMaterialTableData()">
            <el-option v-for="item in materialTypeOptions" :value="item" />
        </el-select>
        请选择材料名称：
        <el-input v-model="materialNameSearch" placeholder="" clearable @keypress.enter="getMaterialTableData()"
            @clear="getMaterialTableData()" />
        请选择材料规格：
        <el-input v-model="materialSpecificationSearch" placeholder="" clearable
            @keypress.enter="getMaterialTableData()" @clear="getMaterialTableData()" />
        请选择材料供应商：
        <el-select v-model="materialSupplierSearch" value-key="" placeholder="" clearable filterable
            @change="getMaterialTableData()">
            <el-option v-for="item in materialSupplierOptions" :value="item" />
        </el-select>

        <template #footer>
            <span>
                <el-button @click="">Cancel</el-button>
                <el-button type="primary" @click="">筛选</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog title="多选材料出库" v-model="isMultiMaterialDialogOpen" width="50%">
        <el-form :model="outboundForm" :rules="rules" ref="outboundForm">
            <el-form-item prop="timestamp" label="出库日期" :rules="rules">
                <el-date-picker v-model="outboundForm.timestamp" type="datetime" placeholder="选择日期时间"
                    style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
            </el-form-item>
            <el-form-item prop="outboundType" label="出库类型">
                <el-radio-group v-model="outboundForm.outboundType">
                    <el-radio :value="0">鞋型使用</el-radio>
                    <el-radio :value="1">废料处理</el-radio>
                    <el-radio :value="2">外包发货</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="section" v-if="outboundForm.outboundType == 0" label="出库工段">
                <el-select v-model="outboundForm.section" placeholder="请输入出库工段" style="width: 240px">
                    <el-option v-for="item in team_options" :label="item.label" :value="item.value"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="receiver" v-if="outboundForm.outboundType == 0" label="领料人">
                <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"></el-input>
            </el-form-item>
            <el-form-item prop="selectedOutsource" label="外包工厂" v-if="outboundForm.outboundType == 2">
                <el-table border stripe v-if="outboundForm.outboundType == 2" :data="outboundForm.outsourceInfo"
                    style="width: 100%">
                    <el-table-column width="55">
                        <template #default="scope">
                            <el-radio v-model="outboundForm.selectedOutsource" :value="scope.row.outsourceInfoId" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="outsourceFactory.value" label="工厂名称" />
                    <el-table-column prop="outsourceAmount" label="外包数量" />
                    <el-table-column prop="outsourceType" label="外包类型" />
                </el-table>
            </el-form-item>

            <el-form-item prop="address" v-if="outboundForm.outboundType == 2" label="发货地址">
                <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
            </el-form-item>
            <el-form-item prop="materials" label="无尺码材料">
                <el-table :data="outboundForm.materials" style="width: 100%" border stripe>
                    <el-table-column prop="materialName" label="材料名称" />
                    <el-table-column prop="currentAmount" label="库存" />
                    <el-table-column prop="outboundAmount" label="出库数量">
                        <template #default="scope">
                            <el-input v-model="scope.row.outboundAmount" type="number"></el-input>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
            <el-form-item prop="sizeMaterials" label="多尺码材料">
                <el-table :data="outboundForm.sizeMaterials" style="width: 100%" border stripe>
                    <el-table-column prop="metaData.materialName" label="材料名称" />
                    <el-table-column prop="metaData.materialUnit" label="单位" />
                    <el-table-column prop="metaData.materialName" label="出库数量">
                        <template #default="scope">
                            <el-button type="primary" @click="openSizeMaterialStockDialog(scope.row)"
                                size="small">展开</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>

        </el-form>
        <template #footer>
            <span>
                <el-button @click="isMultiMaterialDialogOpen = false">取消</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="多鞋码材料出库数量" v-model="isSizeMaterialStockOpen" width="50%">
        <el-form :rules="rules" ref="">
            <el-form-item>
                <el-table :data="selectedSizeMaterialData.quantityList" border stripe :rules>
                    <el-table-column prop="shoeSizeName" label="鞋码"></el-table-column>
                    <el-table-column prop="currentQuantity" label="库存"></el-table-column>
                    <el-table-column label="出库数量">
                        <template #default="scope">
                            <el-input v-model.number="scope.row.outboundAmount" type="number"
                                @input="calculateSum()"></el-input>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button type="primary" @click="isSizeMaterialStockOpen = false">
                确认
            </el-button>
        </template>
    </el-dialog>

    <el-dialog title="推进出库流程" v-model="isFinishOutboundDialogOpen" width="50%">
        <el-descriptions title="已选择订单鞋型" style="margin-top: 20px;">
        </el-descriptions>
        <el-table :data="selectedRows" border stripe>
            <el-table-column prop="orderRId" label="订单号">
            </el-table-column>
            <el-table-column prop="shoeRId" label="鞋型号">
            </el-table-column>
            <el-table-column prop="materialName" label="材料名称">
            </el-table-column>
        </el-table>
        <template #footer>
            <el-button @click="isFinishOutboundDialogOpen = false">返回</el-button>
            <el-button @click="finishOutbound">完成出库</el-button>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { getShoeSizesName } from '@/Pages/utils/getShoeSizesName';
import { toRaw } from 'vue';
export default {
    data() {
        return {
            isMultiOutboundDialogVisible: false,
            materialTypeSearch: '',
            materialNameSearch: '',
            materialSpecificationSearch: '',
            materialSupplierSearch: '',
            materialTypeOptions: [],
            materialSupplierOptions: [],
            outboundForm: {},
            outboundFormTemplate: {
                timestamp: null,
                outboundType: 0,
                section: null,
                receiver: null,
                address: null,
                deadlineDate: null,
                outsourceInfoId: null,
                outsourceInfo: [],
                selectedOutsource: null,
                materials: [],
                sizeMaterials: []
            },
            isOutboundDialogVisible: false,
            currentPage: 1,
            pageSize: 10,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            materialTableData: [],
            isMaterialDialogVisible: false,
            materialDialogData: {},
            team_options: [
                { "label": "裁断", "value": 0 },
                { "label": "针车", "value": 1 },
                { "label": "成型", "value": 2 },
            ],
            totalRows: 0,
            currentRow: {},
            isMultipleSelection: false,
            selectedRows: [],
            isSelectedRowsEmpty: false,
            getShoeSizesName,
            isMultiMaterialDialogOpen: false,
            isSizeMaterialStockOpen: false,
            selectedSizeMaterialData: [],
            isFinishOutboundDialogOpen: false,
            uniqueSelectedRows: [],
            rules: {
                timestamp: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                outboundType: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                section: [
                    {
                        validator: (rule, value, callback) => {
                            if (this.outboundForm.outboundType == 0 && value === null) {
                                callback(new Error('此项为必填项'));
                            } else {
                                callback();
                            }
                        },
                        trigger: 'change'
                    }
                ],
                receiver: [
                    {
                        validator: (rule, value, callback) => {
                            if (this.outboundForm.outboundType == 0 && !value) {
                                callback(new Error('此项为必填项'));
                            } else {
                                callback();
                            }
                        },
                        trigger: 'change'
                    }
                ],
                address: [
                    {
                        validator: (rule, value, callback) => {
                            if (this.outboundForm.outboundType == 2 && !value) {
                                callback(new Error('此项为必填项'));
                            } else {
                                callback();
                            }
                        },
                        trigger: 'change'
                    }
                ],
                selectedOutsource: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                materials: [
                    {
                        validator: (rule, value, callback) => {
                            const invalidRows = value.filter((row) => !row.outboundAmount);
                            if (invalidRows.length > 0) {
                                callback(new Error("出库数量不能为空"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                    {
                        validator: (rule, value, callback) => {
                            const invalidRows = value.filter((row) => row.outboundAmount <= 0);
                            if (invalidRows.length > 0) {
                                callback(new Error("出库数量需为正数"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ],
                sizeMaterials: [
                    {
                        validator: (rule, value, callback) => {
                            console.log(value)
                            const invalidRows = value.filter((row) => row.metaData.enteredAmount == 0);
                            if (invalidRows.length > 0) {
                                callback(new Error("出库数量不能为空"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ]
            },
        }
    },
    computed: {
        filteredColumns() {
            return this.shoeSizeColumns.filter(column =>
                this.orderShoeBatchInfo.some(row => row[column.prop] !== undefined && row[column.prop] !== null && row[column.prop] !== 0)
            );
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.getAllSuppliers()
        this.getMaterialTableData()
    },
    methods: {
        isSelectable(row) {
            return row.status === '已完成入库'
        },
        calculateSum() {
            this.selectedSizeMaterialData.metaData["enteredAmount"] = this.selectedSizeMaterialData.quantityList.reduce((sum, row) => sum + (row.outboundAmount || 0), 0);
        },
        openSizeMaterialStockDialog(row) {
            console.log(row)
            this.selectedSizeMaterialData = row
            this.isSizeMaterialStockOpen = true
        },
        async openMultipleOutboundDialog() {
            if (this.selectedRows.length == 0) {
                ElMessage.error("未选择材料")
                return
            }
            const uniqueCombinations = new Set(this.selectedRows.map(row => `${row.orderId}-${row.orderShoeId}`))
            if (uniqueCombinations.size > 1) {
                ElMessage.error("只能选同一订单鞋型出库")
                return
            }
            const sanitizedObject = JSON.parse(JSON.stringify(this.outboundFormTemplate));
            this.outboundForm = structuredClone(sanitizedObject)
            let arr = this.outboundForm.sizeMaterials
            this.selectedRows.forEach(async (row) => {
                if (row.materialCategory == 1) {
                    this.selectedSizeMaterialData = []
                    row["enteredAmount"] = 0
                    let params = { "sizeMaterialStorageId": row.materialStorageId, "orderId": row.orderId }
                    let response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsizematerialbyid`, { params })
                    arr.push({ "metaData": row, "quantityList": response.data })

                } else {
                    this.outboundForm.materials.push(row)
                }
            })
            this.isMultiMaterialDialogOpen = true
        },
        toggleSelectionMode() {
            this.isMultipleSelection = !this.isMultipleSelection;
        },
        handleSelectionChange(selection) {
            this.selectedRows = selection
        },
        async getAllMaterialTypes() {
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialtypes`)
            this.materialTypeOptions = response.data
        },
        async getAllSuppliers() {
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallsuppliernames`)
            this.materialSupplierOptions = response.data
        },
        async getMaterialTableData(sortColumn, sortOrder) {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "opType": 2,
                "materialType": this.materialTypeSearch,
                "materialName": this.materialNameSearch,
                "materialSpec": this.materialSpecificationSearch,
                "supplier": this.materialSupplierSearch,
                "orderRId": this.orderNumberSearch,
                "shoeRId": this.shoeNumberSearch,
                "sortColumn": sortColumn,
                "sortOrder": sortOrder
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialinfo`, { params })
            this.materialTableData = response.data.result
            this.totalRows = response.data.total
        },
        async submitOutboundForm() {
            console.log(this.outboundForm)
            this.$refs.outboundForm.validate(async (valid) => {
                if (valid) {
                    console.log("Form is valid. Proceeding with submission.");
                    let materialOutboundList = []
                    this.outboundForm.materials.forEach(row => {
                        materialOutboundList.push({ "id": row.materialStorageId, "amount": row.outboundAmount })
                    })
                    let sizeMaterialOutboundList = []
                    this.outboundForm.sizeMaterials.forEach(row => {
                        let obj = { "id": row.metaData.materialStorageId, 'typeName': row.quantityList[0].typeName, outboundAmounts: [] }
                        row.quantityList.forEach(shoeSizeInfo => {
                            obj.outboundAmounts.push({ shoeSizeName: shoeSizeInfo["shoeSizeName"], amount: shoeSizeInfo["outboundAmount"] })
                        })
                        sizeMaterialOutboundList.push(obj)
                    })
                    let data = {
                        "materialOutboundList": materialOutboundList,
                        "sizeMaterialOutboundList": sizeMaterialOutboundList,
                        "timestamp": this.outboundForm.timestamp,
                        "type": this.outboundForm.outboundType,
                        "outboundDepartment": this.outboundForm.section,
                        "outboundAddress": this.outboundForm.address,
                        "picker": this.outboundForm.receiver,
                        "outsourceInfoId": null
                    }
                    if (this.outboundForm.selectedOutsource) {
                        data["outsourceInfoId"] = this.outboundForm.selectedOutsource.outsourceInfoId
                    }
                    console.log(data)
                    try {
                        await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/outboundmaterial`, data)
                        ElMessage.success("出库成功")
                    }
                    catch (error) {
                        console.log(error)
                        ElMessage.error("出库失败")
                    }
                    this.isOutboundDialogVisible = false
                    this.getMaterialTableData()
                } else {
                    console.log("invalid")
                }
            })
        },

        openFinishOutboundDialog() {
            if (this.selectedRows.length == 0) {
                ElMessage.error("未选择材料")
                return
            }
            this.isFinishOutboundDialogOpen = true
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getMaterialTableData()
        },
        handlePageChange(val) {
            this.page = val
            this.getMaterialTableData()
        },
        formatDecimal(row, column, cellValue, index) {
            return Number(cellValue).toFixed(2)
        },
        async getOutsourceInfo() {
            let params = { "orderShoeId": this.currentRow.orderShoeId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
            this.outboundForm.outsourceInfo = []
            console.log(response.data)
            response.data.forEach(element => {
                if ((element.outsourceStatus == 2 || element.outsourceStatus == 4) && element.materialRequired) {
                    this.outboundForm.outsourceInfo.push(element)
                }
            });
        },
        async finishOutsourceOutbound(row) {
            try {
                let data = { "outsourceInfoId": row.outsourceInfoId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutsourceoutbound`, data)
                await this.getOutsourceInfo()
                ElMessage.success("外包出库成功")
            }
            catch (error) {
                console.log(error)
                ElMessage.error("外包出库失败")
            }
        },
        async finishOutbound() {
            ElMessageBox.alert('该操作完成对选择鞋型材料出库', '提示', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                let data = []
                this.selectedRows.forEach(row => {
                    data.push({ storageId: row.materialStorageId, materialCategory: row.materialCategory })
                })
                try {
                    await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutboundmaterial`, data)
                    ElMessage.success("操作成功")
                }
                catch (error) {
                    console.log(error)
                    ElMessage.error("操作异常")
                }
                this.isFinishOutboundDialogOpen = false
                this.getMaterialTableData()
            })
        },
        async sortData({ prop, order }) {
            await this.getMaterialTableData(prop, order)
        }
    }
}
</script>
