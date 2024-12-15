<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">物流信息一览</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable @keypress.enter="getlogisticsOrderData()"
                @clear="getlogisticsOrderData" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable @keypress.enter="getlogisticsOrderData()"
                @clear="getlogisticsOrderData" />
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
            <el-table :data="logisticsOrderData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="orderEndDate" label="订单截止日期"></el-table-column>
                <el-table-column label="物流信息">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="openLogisticsDialog(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table></el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>
    <el-dialog title="鞋型所有材料物流信息" v-model="isMaterialLogisticVis" width="80%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-table :data="logisticsMaterialData" border stripe>
                    <el-table-column prop="materialType" label="材料类型"></el-table-column>
                    <el-table-column prop="materialName" label="材料名称"></el-table-column>
                    <el-table-column prop="colorName" label="颜色"></el-table-column>
                    <el-table-column prop="materialUnit" label="材料单位"></el-table-column>
                    <el-table-column prop="supplierName" label="供应商名称"></el-table-column>
                    <el-table-column prop="estimatedInboundAmount" label="采购数量"></el-table-column>
                    <el-table-column prop="actualInboundAmount" label="实际入库数量"></el-table-column>
                    <el-table-column prop="currentAmount" label="库存"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="12" :offset="15">
                <el-pagination @size-change="handleLogisticsPageChange" @current-change="handleLogisticsPageChange"
                    :current-page="currentLogisticsPage" :page-sizes="[10, 20, 30, 40]" :page-size="logisticsPageSize"
                    layout="total, sizes, prev, pager, next, jumper" :total="logisticsRows" />
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button type="primary" @click="isMaterialLogisticVis = false">返回</el-button>
            </span>
        </template>
    </el-dialog>

</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            isMaterialLogisticVis: false,
            isShoeLogisticVis: false,
            orderRIdSearch: '',
            statusFilter: '',
            shoeRIdSearch: '',
            logisticsShoeData: [],
            logisticsOrderData: [],
            logisticsMaterialData: [],
            totalRows: 0,
            currentPage: 1,
            pageSize: 10,
            logisticsRows: 0,
            currentLogisticsPage: 1,
            logisticsPageSize: 10,
            currentRow: {},
        }
    },
    mounted() {
        this.getlogisticsOrderData()
    },
    methods: {
        async getlogisticsOrderData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch
            }
            const response = await axios.get(`${this.$apiBaseUrl}/production/getallordershoeinfo`, { params })
            this.logisticsOrderData = response.data.result
            this.totalRows = response.data.totalLength
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getlogisticsOrderData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getlogisticsOrderData()
        },
        handleLogisticsPageChange(val) {
            this.logisticsPageSize = val
            this.viewLogisticDetail()
        },
        handleLogisticsPageChange(val) {
            this.currentLogisticsPage = val
            this.viewLogisticDetail()
        },
        openLogisticsDialog(rowData) {
            this.currentRow = rowData
            this.currentLogisticsPage = 1
            this.viewLogisticDetail()
            this.isMaterialLogisticVis = true
        },
        async viewLogisticDetail() {
            const params = {
                "page": this.currentLogisticsPage,
                "pageSize": this.logisticsPageSize,
                "orderRId": this.currentRow.orderRId,
                "shoeRId": this.currentRow.shoeRId
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialinfo`, { params })
            this.logisticsMaterialData = response.data.result
            this.logisticsRows = response.data.total
        },
    }
}
</script>
