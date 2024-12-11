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
    <el-table :data="tableData" border stripe height="600" @sort-change="sortData">
        <el-table-column prop="purchaseOrderIssueDate" label="采购订单日期" width="120" sortable="custom"></el-table-column>
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
        <el-table-column fixed="right" label="操作">
            <template #default="scope">
                <el-button-group>
                    <!-- <el-button type="primary" size="small" @click="openInboundDialog">入库</el-button>
                    <el-button type="primary" size="small" @click="openOutboundDialog">出库</el-button> -->
                    <el-button v-if="scope.row.materialCategory == 1" type="primary" size="small" @click="">查看多鞋码库存</el-button>
                    <el-button type="primary" size="small" @click="viewRecords(scope.row)">入/出库记录</el-button>
                </el-button-group>
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

    <el-dialog title="材料入库/出库记录" v-model="isRecordDialogVisible" width="60%">
        <el-table :data="recordData" border stripe>
            <el-table-column prop="operation" label="操作类型"></el-table-column>
            <el-table-column prop="purpose" label="用途"></el-table-column>
            <el-table-column prop="date" label="操作时间"></el-table-column>
            <el-table-column prop="amount" label="操作数量"></el-table-column>
        </el-table>
    </el-dialog>
    <el-dialog title="分尺码材料入库/出库记录" v-model="isSizeRecordDialogVisible" width="60%">
        <el-table :data="sizeRecordData" border stripe>
            <el-table-column prop="operation" label="操作类型"></el-table-column>
            <el-table-column prop="purpose" label="用途"></el-table-column>
            <el-table-column prop="date" label="操作时间"></el-table-column>
            <el-table-column v-for="column in columns" :key="column.prop" :prop="column.prop"
                :label="column.label"></el-table-column>
        </el-table>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import { getShoeSizesName } from '@/Pages/utils/getShoeSizesName';
import MaterialSearchDialog from './MaterialSearchDialog.vue';
export default {
    components: {
        MaterialSearchDialog
    },
    data() {
        return {
            isRecordDialogVisible: false,
            isSizeRecordDialogVisible: false,
            isMaterialDialogVisible: false,
            searchForm: {
                orderNumberSearch: '',
                shoeNumberSearch: '',
                materialTypeSearch: '',
                materialNameSearch: '',
                materialSpecificationSearch: '',
                materialSupplierSearch: '',
                purchaseDivideOrderRIdSearch: '',
            },
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
        openInboundDialog() {

        },
        openOutboundDialog() {

        },
        updateDialogVisible(newVal) {
            this.isMaterialDialogVisible = newVal
        },
        handleSearch(values) {
            this.searchForm = { ...values }
            this.getMaterialTableData()
        },
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
                "materialType": this.searchForm.materialTypeSearch,
                "materialName": this.searchForm.materialNameSearch,
                "materialSpec": this.searchForm.materialSpecificationSearch,
                "supplier": this.searchForm.materialSupplierSearch,
                "orderRId": this.searchForm.orderNumberSearch,
                "shoeRId": this.searchForm.shoeNumberSearch,
                "purchaseOrderRId": this.searchForm.purchaseDivideOrderRIdSearch,
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
        async sortData({ prop, order }) {
            await this.getTableData(prop, order)
        }
    }
}
</script>