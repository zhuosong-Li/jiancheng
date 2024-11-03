<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">材料出库</el-col>
    </el-row>
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
        <el-table :data="materialTableData" border stripe height="500" @sort-change="sortData">
            <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120"
                sortable="custom"></el-table-column>
            <el-table-column prop="purchaseDivideOrderRId" label="采购订单号" show-overflow-tooltip></el-table-column>
            <el-table-column prop="materialType" label="材料类型"></el-table-column>
            <el-table-column prop="materialName" label="材料名称"></el-table-column>
            <el-table-column prop="materialModel" label="材料型号"></el-table-column>
            <el-table-column prop="materialSpecification" label="材料规格"></el-table-column>
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
            <el-table-column fixed="right" label="操作" width="150">
                <template #default="scope">
                    <el-button-group>
                        <el-button type="primary" size="small" @click="outboundMaterial(scope.row)">出库</el-button>
                        <el-button v-if="scope.row.status === '已完成入库'" type="warning" size="small"
                            @click="finishOutbound(scope.row)">完成出库</el-button>
                    </el-button-group>
                </template>
            </el-table-column>
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
    <el-dialog title="出库对话框" v-model="isOutboundDialogVisible" width="35%">
        <el-form-item label="出库日期">
            <el-date-picker v-model="outboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
        </el-form-item>
        <el-form-item label="出库数量">
            <el-input v-model="outboundForm.quantity" placeholder="请输入出库数量"></el-input>
        </el-form-item>
        <el-form-item label="出库类型">
            <el-radio-group v-model="outboundForm.outboundType">
                <el-radio :value="0">鞋型使用</el-radio>
                <el-radio :value="1">废料处理</el-radio>
                <el-radio :value="2">外包发货</el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item v-if="outboundForm.outboundType == 0" label="出库工段">
            <el-select v-model="outboundForm.section" placeholder="请输入出库工段" style="width: 240px">
                <el-option v-for="item in team_options" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item v-if="outboundForm.outboundType == 0" label="领料人">
            <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"></el-input>
        </el-form-item>
        <el-table v-if="outboundForm.outboundType == 2" :data="outboundForm.outsourceInfo" style="width: 100%">
            <el-table-column width="55">
                <template #default="scope">
                    <el-radio v-model="outboundForm.selectedOutsource" :value="scope.row.outsourceInfoId" />
                </template>
            </el-table-column>
            <el-table-column prop="outsourceFactory.value" label="工厂名称" />
            <el-table-column prop="outsourceAmount" label="外包数量" />
            <el-table-column prop="outsourceType" label="外包类型" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button :disabled="outboundForm.selectedOutsource !== scope.row.outsourceInfoId" type="warning"
                        size="small" @click="finishOutsourceOutbound(scope.row)">
                        完成外包出库
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-form-item v-if="outboundForm.outboundType == 2" label="发货地址">
            <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isOutboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="多鞋码出库对话框" v-model="isMultiOutboundDialogVisible" width="50%">
        <el-table :data="outboundForm.multipleOutboundTable" border stripe>
            <el-table-column prop="shoeSize" label="鞋码"></el-table-column>
            <el-table-column prop="internalSize" label="内码"></el-table-column>
            <el-table-column prop="externalSize" label="外显"></el-table-column>
            <el-table-column prop="predictQuantity" label="预计数量"></el-table-column>
            <el-table-column prop="actualQuantity" label="实际数量"></el-table-column>
            <el-table-column prop="currentQuantity" label="材料库存"></el-table-column>
            <el-table-column label="出库数量">
                <template #default="scope">
                    <el-input v-model="scope.row.outboundQuantity" placeholder="请输入出库数量"></el-input>
                </template>
            </el-table-column>
        </el-table>

        <el-form-item label="出库日期">
            <el-date-picker v-model="outboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
        </el-form-item>
        <el-form-item label="出库类型">
            <el-radio-group v-model="outboundForm.outboundType">
                <el-radio :value="0">鞋型使用</el-radio>
                <el-radio :value="1">废料处理</el-radio>
                <el-radio :value="2">外包发货</el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item v-if="outboundForm.outboundType == 0" label="出库工段">
            <el-select v-model="outboundForm.section" placeholder="请输入出库工段" style="width: 240px">
                <el-option v-for="item in team_options" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item v-if="outboundForm.outboundType == 0" label="领料人">
            <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"></el-input>
        </el-form-item>
        <el-table v-if="outboundForm.outboundType == 2" :data="outboundForm.outsourceInfo" style="width: 100%">
            <el-table-column width="55">
                <template #default="scope">
                    <el-radio v-model="outboundForm.selectedOutsource" :value="scope.row.outsourceInfoId" />
                </template>
            </el-table-column>
            <el-table-column prop="outsourceFactory.value" label="工厂名称" />
            <el-table-column prop="outsourceAmount" label="外包数量" />
            <el-table-column prop="outsourceType" label="外包类型" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button :disabled="outboundForm.selectedOutsource !== scope.row.outsourceInfoId" type="warning"
                        size="small" @click="finishOutsourceOutbound(scope.row)">
                        完成外包出库
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-form-item v-if="outboundForm.outboundType == 2" label="发货地址">
            <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isOutboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
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
            outboundForm: {
                quantity: '',
                date: '',
                outboundType: 0,
                section: '',
                receiver: '',
                address: '',
                deadlineDate: '',
                outsourceInfo: [],
                selectedOutsource: null,
                multipleOutboundTable: []
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
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.getAllSuppliers()
        this.getMaterialTableData()
    },
    methods: {
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
            if (Number(this.outboundForm.quantity) > Number(this.currentRow.currentAmount)) {
                this.$message({ type: 'warning', message: '出库数量大于库存' });
                return
            }
            let data = {
                "materialStorageId": this.currentRow.materialStorageId,
                "date": this.outboundForm.date,
                "amount": this.outboundForm.quantity,
                "type": this.outboundForm.outboundType,
                "outboundDepartment": this.outboundForm.section,
                "outboundAddress": this.outboundForm.address,
                "picker": this.outboundForm.receiver
            }
            const response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/outboundmaterial`, data)
            if (response.status == 200) {
                ElMessage.success("出库成功")
            }
            else {
                ElMessage.error("出库失败")
            }
            this.isOutboundDialogVisible = false
            this.getMaterialTableData()
        },
        async submitSizeOutboundForm() {
            let data = {
                "sizeMaterialStorageId": this.currentRow.materialStorageId,
                "date": this.outboundForm.date,
                "type": this.outboundForm.outboundType,
                "outboundDepartment": this.outboundForm.section,
                "outboundAddress": this.outboundForm.address,
                "picker": this.outboundForm.receiver
            }
            this.outboundForm.multipleOutboundTable.forEach(row => {
                if (row.outboundQuantity) {
                    data["size" + row.shoeSize + "Amount"] = row.outboundQuantity
                } else {
                    data["size" + row.shoeSize + "Amount"] = 0
                }
            })
            const response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/outboundsizematerial`, data)
            if (response.status == 200) {
                ElMessage.success("出库成功")
            }
            else {
                ElMessage.error("出库失败")
            }
            this.isMultiOutboundDialogVisible = false
            this.getMaterialTableData()
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
        async outboundMaterial(row) {
            this.currentRow = row
            await this.getOutsourceInfo()
            if (row.materialCategory == 1) {
                let params = { "sizeMaterialStorageId": row.materialStorageId }
                let response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsizematerialbyid`, { params })
                this.outboundForm.multipleOutboundTable = response.data
                this.isMultiOutboundDialogVisible = true
            } else {
                this.isOutboundDialogVisible = true
            }
        },
        async getOutsourceInfo() {
            let params = { "orderShoeId": this.currentRow.orderShoeId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
            this.outboundForm.outsourceInfo = []
            console.log(response.data)
            response.data.forEach(element => {
                if (element.outsourceStatus == 2 || element.outsourceStatus == 4) {
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
        async finishOutbound(row) {
            ElMessageBox.alert('该操作完成对此鞋型材料出库，是否继续？', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                const data = { "storageId": row.materialStorageId, "materialCategory": row.materialCategory }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutboundmaterial`, data)
                try {
                    ElMessage.success("操作成功")
                }
                catch (error) {
                    console.log(error)
                    ElMessage.error("操作异常")
                }
                this.getMaterialTableData()
            })
        },
        async sortData({ prop, order }) {
            await this.getMaterialTableData(prop, order)
        }
    }
}
</script>
