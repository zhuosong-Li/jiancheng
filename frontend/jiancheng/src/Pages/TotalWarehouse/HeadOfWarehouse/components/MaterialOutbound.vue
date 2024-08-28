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
                @keypress.enter="getMaterialTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeNumberSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getMaterialTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            <el-button type="primary" @click="getMaterialTableData()">搜索</el-button>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="materialTableData" border stripe height="500">
            <el-table-column prop="materialType" label="材料类型"></el-table-column>
            <el-table-column prop="materialName" label="材料名称"></el-table-column>
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
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="outboundMaterial(scope.row)">出库</el-button>
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
        <el-input v-model="materialNameSearch" placeholder="" clearable @keypress.enter="getMaterialTableData()" />
        请选择材料规格：
        <el-input v-model="materialSpecificationSearch" placeholder="" clearable
            @keypress.enter="getMaterialTableData()" />
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
    <el-dialog title="出库对话框" v-model="isOutboundDialogVisible" width="30%">
        <el-form-item label="出库数量">
            <el-input v-model="outboundForm.quantity" placeholder="请输入出库数量"></el-input>
        </el-form-item>
        <el-form-item label="出库日期">
            <el-date-picker v-model="outboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
        </el-form-item>
        <el-form-item label="出库类型">
            <el-radio-group v-model="outboundForm.outboundType">
                <el-radio value="1">鞋型使用</el-radio>
                <el-radio value="2">废料处理</el-radio>
                <el-radio value="3">外包发货</el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item label="出库工段">
            <el-select v-model="outboundForm.section" placeholder="请输入出库工段"
                :disabled="outboundForm.outboundType !== '1'" style="width: 240px">
                <el-option v-for="item in team_options" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="领料人">
            <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"
                :disabled="outboundForm.outboundType !== '1'"></el-input>
        </el-form-item>
        <el-form-item label="外包信息">
        </el-form-item>
        <el-text>材料最迟发货日期：{{ outboundForm.deadlineDate }}</el-text>
        <el-form-item label="发货地址">
            <el-input v-model="outboundForm.address" placeholder="请输入发货地址"
                :disabled="outboundForm.outboundType !== '3'"></el-input>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isOutboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="多鞋码出库对话框" v-model="isMultiOutboundDialogVisible" width="50%">
        <el-table :data="multipleOutboundForm" border stripe>
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
                <el-radio value="1">内部使用</el-radio>
                <el-radio value="2">废料处理</el-radio>
                <el-radio value="3">外包发货</el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item label="出库工段">
            <el-select v-model="outboundForm.section" placeholder="请输入出库工段"
                :disabled="outboundForm.outboundType !== '1'" style="width: 240px">
                <el-option v-for="item in team_options" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="领料人">
            <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"
                :disabled="outboundForm.outboundType !== '1'"></el-input>
        </el-form-item>
        <el-form-item label="外包信息">

        </el-form-item>
        <el-text>材料最迟发货日期：{{ outboundForm.deadlineDate }}</el-text>
        <el-form-item label="发货地址">
            <el-input v-model="outboundForm.address" placeholder="请输入发货地址"
                :disabled="outboundForm.outboundType !== '3'"></el-input>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isMultiOutboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitSizeOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios';
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
                outboundType: '1',
                section: '',
                receiver: '',
                address: '',
                deadlineDate: '',
            },
            isOutboundDialogVisible: false,
            currentPage: 1,
            pageSize: 10,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            materialTableData: [],
            multipleOutboundForm: [],
            isMaterialDialogVisible: false,
            materialDialogData: {},
            team_options: [
                { "label": "裁断", "value": "F" },
                { "label": "针车", "value": "S" },
                { "label": "成型", "value": "M" },
            ],
            totalRows: 0,
            currentRow: {},
            isProductionOutboundDisabled: false,
            isOutsourceOutboundDisabled: false,
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.getAllSuppliers()
        this.getMaterialTableData()
    },
    methods: {
        async getAllMaterialTypes() {
            const response = await axios.get("http://localhost:8000/warehouse/warehousemanager/getallmaterialtypes")
            this.materialTypeOptions = response.data
        },
        async getAllSuppliers() {
            const response = await axios.get("http://localhost:8000/warehouse/warehousemanager/getallsuppliernames")
            this.materialSupplierOptions = response.data
        },
        async getMaterialTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "opType": 2,
                "materialType": this.materialTypeSearch,
                "materialName": this.materialNameSearch,
                "materialSpec": this.materialSpecificationSearch,
                "supplier": this.materialSupplierSearch,
                "orderRId": this.orderNumberSearch,
                "shoeRId": this.shoeNumberSearch
            }
            const response = await axios.get("http://localhost:8000/warehouse/warehousemanager/getallmaterialinfo", { params })
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
            const response = await axios.patch("http://localhost:8000/warehouse/warehousemanager/outboundmaterial", data)
            console.log(response)
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
            this.multipleOutboundForm.forEach(row => {
                if (row.outboundQuantity) {
                    data["size" + row.shoeSize + "Amount"] = row.outboundQuantity
                } else {
                    data["size" + row.shoeSize + "Amount"] = 0
                }

            })
            const response = await axios.patch("http://localhost:8000/warehouse/warehousemanager/outboundsizematerial", data)
            console.log(response)
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
            let params = {"orderShoeId": row.orderShoeId}
            let response = await axios.get("http://localhost:8000/warehouse/warehousemanager/checkinboundoptions", { params })
            this.isProductionOutboundDisabled = !response.data[1]
            this.isOutsourceOutboundDisabled = !response.data[3]
            if (row.materialCategory == 1) {
                params = { "sizeMaterialStorageId": row.materialStorageId }
                response = await axios.get("http://localhost:8000/warehouse/warehousemanager/getsizematerialbyid", { params })
                this.multipleOutboundForm = response.data
                this.isMultiOutboundDialogVisible = true
                this.currentRow = row
            } else {
                this.isOutboundDialogVisible = true
                this.currentRow = row
            }
        },
    }
}
</script>
