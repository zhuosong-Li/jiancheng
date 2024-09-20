<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">材料入库</el-col>
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
        <el-table :data="materialTableData" border stripe height="500" @sort-change="sortData">
            <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120" sortable="custom"></el-table-column>
            <el-table-column prop="purchaseDivideOrderRId" label="采购订单号" show-overflow-tooltip></el-table-column>
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
                    <el-button type="primary" size="small" @click="editMaterial(scope.row)">入库</el-button>
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

    <el-dialog title="材料搜索" v-model="isMaterialDialogVisible" width="30%">
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
                <el-button type="primary" @click="isMaterialDialogVisible = false">返回</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog title="入库对话框" v-model="isInboundDialogVisible" width="30%">
        <el-form-item label="入库数量">
            <el-input v-model="inboundForm.quantity" placeholder="请输入入库数量"></el-input>
        </el-form-item>
        <el-form-item label="入库日期">
            <el-date-picker v-model="inboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
        </el-form-item>
        <el-form-item label="入库类型">
            <el-radio-group v-model="inboundForm.inboundType">
                <el-radio :disabled="isPurchaseInboundDisabled" value="1">采购入库</el-radio>
                <el-radio value="2">生产剩余</el-radio>
            </el-radio-group>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isInboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="多鞋码入库对话框" v-model="isMultiInboundDialogVisible" width="50%">
        <el-table :data="multipleInboundForm" border stripe>
            <el-table-column prop="shoeSize" label="鞋码"></el-table-column>
            <el-table-column prop="internalSize" label="内码"></el-table-column>
            <el-table-column prop="externalSize" label="外显"></el-table-column>
            <el-table-column prop="predictQuantity" label="预计数量"></el-table-column>
            <el-table-column prop="actualQuantity" label="实际数量"></el-table-column>
            <el-table-column prop="currentQuantity" label="当前数量"></el-table-column>
            <el-table-column label="入库数量">
                <template #default="scope">
                    <el-input v-model="scope.row.inboundQuantity" placeholder="请输入入库数量"></el-input>
                </template>
            </el-table-column>
        </el-table>

        <el-form-item label="入库日期">
            <el-date-picker v-model="inboundForm.date" type="datetime" placeholder="选择日期时间" style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"></el-date-picker>
        </el-form-item>
        <el-form-item label="入库类型">
            <el-radio-group v-model="inboundForm.inboundType">
                <el-radio :disabled="isPurchaseInboundDisabled" value="1">采购入库</el-radio>
                <el-radio value="2">生产剩余</el-radio>
            </el-radio-group>
        </el-form-item>
        <template #footer>
            <span>
                <el-button @click="isMultiInboundDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitSizeInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            isMultiInboundDialogVisible: false,
            isInboundDialogVisible: false,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            materialTypeSearch: '',
            materialNameSearch: '',
            materialSpecificationSearch: '',
            materialSupplierSearch: '',
            multipleInboundForm: [],
            materialTypeOptions: [],
            materialSupplierOptions: [],
            isMaterialDialogVisible: false,
            pageSize: 10,
            currentPage: 1,
            inboundForm: {
                quantity: '',
                date: '',
                inboundType: ''
            },
            materialTableData: [],
            currentRow: {},
            totalRows: 0,
            isPurchaseInboundDisabled: false
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
                "opType": 1,
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
        async submitInboundForm() {
            let data = {
                "materialStorageId": this.currentRow.materialStorageId,
                "date": this.inboundForm.date,
                "amount": this.inboundForm.quantity,
                "type": this.inboundForm.inboundType
            }
            let response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundmaterial`, data)
            console.log(response)
            this.isInboundDialogVisible = false
            this.getMaterialTableData()

            // let params = {"orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId}
            // response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/notifyrequiredmaterialarrival`, {params})
            // if (response.data["message"] == "yes") {
            //     // notify production manager that material is ready
            //     data = {"senderId": 5, "receiverIds": [6, 7], "content": "鞋型号" + this.currentRow.shoeRId + "所需材料已到齐。请联系相关人员出货。"}
            //     await axios.post(`${this.$apiBaseUrl}/message/sendmessage`, data)
            //     this.$message({type: 'success', message: '已通知生产经理该鞋型物料到齐'})
            // }
        },
        async submitSizeInboundForm() {
            let data = {
                "sizeMaterialStorageId": this.currentRow.materialStorageId,
                "date": this.inboundForm.date,
                "type": this.inboundForm.inboundType
            }
            this.multipleInboundForm.forEach(row => {
                if (row.inboundQuantity) {
                    data["size" + row.shoeSize + "Amount"] = row.inboundQuantity
                } else {
                    data["size" + row.shoeSize + "Amount"] = 0
                }

            })
            let response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundsizematerial`, data)
            console.log(response)
            this.isMultiInboundDialogVisible = false
            this.getMaterialTableData()

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
            let params = {"orderShoeId": row.orderShoeId}
            let response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/checkinboundoptions`, { params })
            this.isPurchaseInboundDisabled = !response.data[1]
            if (row.materialCategory == 1) {
                params = { "sizeMaterialStorageId": row.materialStorageId }
                response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsizematerialbyid`, { params })
                this.multipleInboundForm = response.data
                this.isMultiInboundDialogVisible = true
                this.currentRow = row
            } else {
                this.isInboundDialogVisible = true
                this.currentRow = row
            }
        },
        async sortData({prop, order}) {
            await this.getMaterialTableData(prop, order)
        }
    }
}
</script>
