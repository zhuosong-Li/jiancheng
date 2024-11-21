<template>
    <el-row :gutter="20">
        <el-col :span="6" :offset="0">
            <el-button-group>
                <el-button type="primary" size="default" @click="isMaterialDialogVisible = true">材料入库筛选</el-button>
            </el-button-group>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderNumberSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getTableData()" @clear="getTableData()"/>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeNumberSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getTableData()"  @clear="getTableData()"/>
        </el-col>
    </el-row>
    <el-table :data="tableData" border stripe height="600" @sort-change="sortData">
        <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120" sortable="custom"></el-table-column>
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
        <el-table-column fixed="right" label="操作" width="120">
            <template #default="scope">
                <el-button type="primary" size="small" @click="viewRecords(scope.row)">入/出库记录</el-button>
            </template>
        </el-table-column>
    </el-table>
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
            @change="getTableData()">
            <el-option v-for="item in materialTypeOptions" :value="item" />
        </el-select>
        请选择材料名称：
        <el-input v-model="materialNameSearch" placeholder="" clearable @keypress.enter="getTableData()" @clear="getTableData"/>
        请选择材料规格：
        <el-input v-model="materialSpecificationSearch" placeholder="" clearable
            @keypress.enter="getTableData()" @clear="getTableData"/>
        请选择材料供应商：
        <el-select v-model="materialSupplierSearch" value-key="" placeholder="" clearable filterable
            @change="getTableData()">
            <el-option v-for="item in materialSupplierOptions" :value="item" />
        </el-select>
        <template #footer>
            <span>
                <el-button type="primary" @click="isMaterialDialogVisible = false">返回</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="材料入库/出库记录" v-model="isRecordDialogVisible" width="60%">
        <el-table :data="recordData" border stripe>
            <el-table-column prop="opType" label="操作类型"></el-table-column>
            <el-table-column prop="date" label="操作时间"></el-table-column>
            <el-table-column prop="amount" label="操作数量"></el-table-column>
        </el-table>
    </el-dialog>
    <el-dialog title="分尺码材料入库/出库记录" v-model="isSizeRecordDialogVisible" width="60%">
        <el-table :data="sizeRecordData" border stripe>
            <el-table-column prop="opType" label="操作类型"></el-table-column>
            <el-table-column prop="date" label="操作时间"></el-table-column>
            <el-table-column v-for="column in columns" :key="column.prop" :prop="column.prop"
                :label="column.label"></el-table-column>
        </el-table>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import { getShoeSizesName } from '@/Pages/utils/getShoeSizesName';

export default {
    data() {
        return {
            isRecordDialogVisible: false,
            isSizeRecordDialogVisible: false,
            isMaterialDialogVisible: false,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            materialTypeSearch: '',
            materialNameSearch: '',
            materialSpecificationSearch: '',
            materialSupplierSearch: '',
            materialTypeOptions: [],
            materialSupplierOptions: [],
            pageSize: 10,
            currentPage: 1,
            recordData: [],
            sizeRecordData: [],
            tableData: [],
            columns: [],
            totalRows: 0,
            getShoeSizesName
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.getAllSuppliers()
        this.getTableData()
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
        async getTableData(sortColumn, sortOrder) {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
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
            this.tableData = response.data.result
            this.totalRows = response.data.total
        },
        formatDecimal(row, column, cellValue, index) {
            return Number(cellValue).toFixed(2)
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getTableData()
        },
        async viewRecords(row) {
            let response = null;
            let params = null;
            if (row.materialCategory == 1) {
                params = { "storageId": row.materialStorageId, "storageName": "sizeMaterial" }
                response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getmaterialinoutboundrecords`, { params })
                this.sizeRecordData = response.data
                this.columns = await this.getShoeSizesName(row.orderId)
                this.isSizeRecordDialogVisible = true
            } else {
                params = { "storageId": row.materialStorageId, "storageName": "material" }
                response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getmaterialinoutboundrecords`, { params })
                this.isRecordDialogVisible = true
                this.recordData = response.data
            }
        },
        async sortData({prop, order}) {
            await this.getTableData(prop, order)
        }
    }
}
</script>