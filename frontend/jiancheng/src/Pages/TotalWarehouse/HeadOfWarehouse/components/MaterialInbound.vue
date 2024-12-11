<template>
    <el-row :gutter="20">
        <el-col :span="6" :offset="0">
            <el-button-group>
                <el-button type="primary" size="default" @click="isMaterialDialogVisible = true">搜索条件设置</el-button>
            </el-button-group>
        </el-col>
        <MaterialSearchDialog :visible="isMaterialDialogVisible" :materialSupplierOptions="materialSupplierOptions"
            :materialTypeOptions="materialTypeOptions" :searchForm="searchForm" @update-visible="updateDialogVisible"
            @confirm="handleSearch" />
    </el-row>
    <el-row :gutter="20">
        <el-button v-if="isMultipleSelection" @click="openFinishOutboundDialog">
            完成入库
        </el-button>
        <el-button @click="toggleSelectionMode">
            {{ isMultipleSelection ? "退出" : "选择材料" }}
        </el-button>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="materialTableData" border stripe height="600" @sort-change="sortData"
            @selection-change="handleSelectionChange">
            <el-table-column v-if="isMultipleSelection" type="selection" width="55" :selectable="isSelectable" />
            <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120"
                sortable="custom"></el-table-column>
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
            <el-table-column prop="craftName" label="复合工艺" width="120">
                <template #default="scope">
                    <el-tooltip effect="dark" :content="scope.row.craftName" placement="bottom">
                        <span class="truncate-text">
                            {{ scope.row.craftName }}
                        </span>
                    </el-tooltip>
                </template>
            </el-table-column>
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
            <el-table-column fixed="right" label="操作" width="80">
                <template #default="scope">
                    <el-button-group>
                        <el-button type="primary" size="small" @click="editMaterial(scope.row)">入库</el-button>
                    </el-button-group>
                </template>
            </el-table-column>
        </el-table>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>

    <el-dialog title="入库对话框" v-model="isInboundDialogVisible" width="30%">
        <el-form :model="inboundForm" :rules="rules" ref="inboundForm">
            <el-form-item prop="date" label="入库日期">
                <el-date-picker v-model="inboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                    value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
            </el-form-item>
            <el-form-item prop="unitPrice" label="材料单价" v-if="inboundForm.inboundType != 1">
                <el-input-number :min="0" :precision="2" :step="0.01" v-model="inboundForm.unitPrice"></el-input-number>
            </el-form-item>
            <el-form-item prop="quantity" label="入库数量">
                <el-input-number :min="0" :precision="5" :step="0.00001" v-model="inboundForm.quantity"
                    placeholder="请输入入库数量"></el-input-number>
            </el-form-item>
            <el-form-item prop="inboundType" label="入库类型">
                <el-radio-group v-model="inboundForm.inboundType">
                    <el-radio :value="0">采购入库</el-radio>
                    <el-radio :value="1">生产剩余</el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <span>
                <el-button @click="isInboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="多鞋码入库对话框" v-model="isMultiInboundDialogVisible" width="50%">
        <el-form :model="inboundForm" :rules="rules" ref="inboundForm">
            <el-form-item prop="date" label="入库日期">
                <el-date-picker v-model="inboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                    value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
            </el-form-item>
            <el-form-item prop="unitPrice" label="材料单价" v-if="inboundForm.inboundType != 1">
                <el-input-number :min="0" :precision="2" :step="0.01" v-model="inboundForm.unitPrice"></el-input-number>
            </el-form-item>
            <el-form-item prop="inboundType" label="入库类型">
                <el-radio-group v-model="inboundForm.inboundType">
                    <el-radio :value="0">采购入库</el-radio>
                    <el-radio :value="1">生产剩余</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="sizeMaterialInboundTable" label="入库数量">
                <el-table :data="filteredData" border stripe>
                    <el-table-column prop="shoeSizeName" label="鞋码" width="100"></el-table-column>
                    <el-table-column prop="predictQuantity" label="预计数量"></el-table-column>
                    <el-table-column prop="actualQuantity" label="实际数量"></el-table-column>
                    <el-table-column prop="currentQuantity" label="库存"></el-table-column>
                    <el-table-column prop="inboundQuantity" label="入库数量">
                        <template #default="scope">
                            <el-input-number v-model="scope.row.inboundQuantity" :min="0"></el-input-number>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
        </el-form>
        <template #footer>
            <span>
                <el-button @click="isMultiInboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitSizeInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog title="推进入库流程" v-model="isFinishInboundDialogOpen" width="50%">
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
            <el-button @click="isFinishInboundDialogOpen = false">返回</el-button>
            <el-button @click="finishInbound">完成入库</el-button>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import MaterialSearchDialog from './MaterialSearchDialog.vue';
export default {
    components: {
        MaterialSearchDialog
    },
    data() {
        return {
            isMultiInboundDialogVisible: false,
            isInboundDialogVisible: false,
            searchForm: {
                orderNumberSearch: '',
                shoeNumberSearch: '',
                materialTypeSearch: '',
                materialNameSearch: '',
                materialSpecificationSearch: '',
                materialSupplierSearch: '',
                purchaseDivideOrderRIdSearch: "",
            },
            materialTypeOptions: [],
            materialSupplierOptions: [],
            isMaterialDialogVisible: false,
            pageSize: 10,
            currentPage: 1,
            inboundFormTemplate: {
                quantity: 0,
                date: '',
                inboundType: null,
                unitPrice: 0,
                sizeMaterialInboundTable: [],
            },
            inboundForm: {},
            materialTableData: [],
            currentRow: {},
            totalRows: 0,
            isMultipleSelection: false,
            selectedRows: [],
            isFinishInboundDialogOpen: false,
            rules: {
                date: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                inboundType: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                quantity: [
                    {
                        required: true,
                        validator: (rule, value, callback) => {
                            console.log(value)
                            if (!(value > 0)) {
                                callback(new Error("入库数量不能零"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ],
                sizeMaterialInboundTable: [
                    {
                        validator: (rule, value, callback) => {
                            const validRows = value.filter((row) => row.inboundQuantity > 0);
                            if (validRows.length == 0) {
                                callback(new Error("出库数量不能为空"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ],
            },
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.getAllSuppliers()
        this.getMaterialTableData()
    },
    computed: {
        filteredData() {
            return this.inboundForm.sizeMaterialInboundTable.filter((row) => {
                return (
                    row.predictQuantity > 0
                );
            });
        },
    },
    methods: {
        updateDialogVisible(newVal) {
            this.isMaterialDialogVisible = newVal

        },
        handleSearch(values) {
            this.searchForm = {...values}
            this.getMaterialTableData()
        },
        isSelectable(row) {
            return row.status === "未完成入库"
        },
        handleSelectionChange(selection) {
            this.selectedRows = selection
        },
        openFinishOutboundDialog() {
            if (this.selectedRows.length == 0) {
                ElMessage.error("未选择材料")
                return
            }
            this.isFinishInboundDialogOpen = true
        },
        toggleSelectionMode() {
            this.isMultipleSelection = !this.isMultipleSelection;
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
                "opType": 1,
                "materialType": this.searchForm.materialTypeSearch,
                "materialName": this.searchForm.materialNameSearch,
                "materialSpec": this.searchForm.materialSpecificationSearch,
                "supplier": this.searchForm.materialSupplierSearch,
                "orderRId": this.searchForm.orderNumberSearch,
                "shoeRId": this.searchForm.shoeNumberSearch,
                "purchaseDivideOrderRId": this.searchForm.purchaseDivideOrderRIdSearch,
                "sortColumn": sortColumn,
                "sortOrder": sortOrder
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialinfo`, { params })
            this.materialTableData = response.data.result
            this.totalRows = response.data.total
        },
        async submitInboundForm() {
            this.$refs.inboundForm.validate(async (valid) => {
                if (valid) {
                    let data = {
                        "materialStorageId": this.currentRow.materialStorageId,
                        "date": this.inboundForm.date,
                        "amount": this.inboundForm.quantity,
                        "inboundType": this.inboundForm.inboundType,
                        "unitPrice": this.inboundForm.unitPrice,
                    }
                    try {
                        await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundmaterial`, data)
                        ElMessage.success("入库成功")
                    }
                    catch (error) {
                        console.log(error)
                        ElMessage.error("入库失败")
                    }
                    this.isInboundDialogVisible = false
                    this.getMaterialTableData()
                }
                else {
                    console.log("invalid")
                }
            })
        },
        async submitSizeInboundForm() {
            this.$refs.inboundForm.validate(async (valid) => {
                if (valid) {
                    try {
                        let data = {
                            "sizeMaterialStorageId": this.currentRow.materialStorageId,
                            "date": this.inboundForm.date,
                            "inboundType": this.inboundForm.inboundType,
                            "unitPrice": this.inboundForm.unitPrice
                        }
                        this.inboundForm.sizeMaterialInboundTable.forEach((row, index) => {
                            data["size" + index + "Amount"] = row.inboundQuantity
                        })
                        await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundsizematerial`, data)
                        ElMessage.success("入库成功")
                    }
                    catch (error) {
                        ElMessage.error("入库失败")
                    }
                    this.getMaterialTableData()
                    this.isMultiInboundDialogVisible = false
                }
                else {
                    console.log("Form validation error")
                }
            })

            // let params = {"orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId}
            // response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/notifyrequiredmaterialarrival`, {params})
            // if (response.data["message"] == "yes") {
            //     // notify production manager that material is ready
            //     data = {"senderId": 5, "receiverIds": [6, 7], "content": "鞋型号" + this.currentRow.shoeRId + "所需材料已到齐。请联系相关人员出货。"}
            //     await axios.post(`${this.$apiBaseUrl}/message/sendmessage`, data)
            //     this.$message({type: 'success', message: '已通知生产经理该鞋型物料到齐'})
            // }
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getMaterialTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getMaterialTableData()
        },

        formatDecimal(row, column, cellValue, index) {
            return Number(cellValue).toFixed(2)
        },
        async editMaterial(row) {
            this.inboundForm = { ...this.inboundFormTemplate }
            this.inboundForm.unitPrice = row.unitPrice
            if (row.materialCategory == 1) {
                let params = { "sizeMaterialStorageId": row.materialStorageId, "orderId": row.orderId }
                let response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsizematerialbyid`, { params })
                this.inboundForm.sizeMaterialInboundTable = response.data
                this.inboundForm.sizeMaterialInboundTable.forEach(row => {
                    row.inboundQuantity = 0
                })
                this.isMultiInboundDialogVisible = true
                this.currentRow = row
            } else {
                this.isInboundDialogVisible = true
                this.currentRow = row
            }
        },
        async finishInbound() {
            ElMessageBox.alert('该操作完成对选择鞋型材料入库，是否继续？', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                try {
                    let data = []
                    this.selectedRows.forEach(row => {
                        data.push({ "orderId": row.orderId, "storageId": row.materialStorageId, "materialCategory": row.materialCategory })
                    })
                    await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishinboundmaterial`, data)
                    ElMessage.success("操作成功")
                }
                catch (error) {
                    console.log(error)
                    ElMessage.error("操作异常")
                }
                this.getMaterialTableData()
                this.isFinishInboundDialogOpen = false
            })
        },
        async sortData({ prop, order }) {
            await this.getMaterialTableData(prop, order)
        }
    }
}
</script>
