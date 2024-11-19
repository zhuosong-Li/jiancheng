<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">物流信息一览</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getlogisticsOrderData()" @clear="getlogisticsOrderData"/>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getlogisticsOrderData()" @clear="getlogisticsOrderData"/>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
            <el-table :data="logisticsOrderData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="orderEndDate" label="订单截止日期"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default"
                            @click="openLogisticsDialog(scope.row)">查看订单物流信息</el-button>
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
                    <el-table-column prop="estimatedInboundAmount" label="核定用量"></el-table-column>
                    <el-table-column prop="actualInboundAmount" label="采购数量"></el-table-column>
                    <el-table-column prop="supplierName" label="供应商名称"></el-table-column>
                    <el-table-column prop="materialArrivalDate" label="材料预计到达日期"></el-table-column>
                    <el-table-column prop="status" label="材料状态"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="12" :offset="15">
                <el-pagination @size-change="handleLogisticsPageChange" @current-change="handleLogisticsPageChange"
                    :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
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
            logisticsCurrentPage: 1,
            logisticsPageSize: 10
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
            this.logisticsCurrentPage = val
            this.viewLogisticDetail()
        },
        openLogisticsDialog(rowData) {
            this.logisticsCurrentPage = 1
            this.viewLogisticDetail(rowData)
            this.isMaterialLogisticVis = true
        },
        async viewLogisticDetail(rowData) {
            const params = {
                "page": this.logisticsCurrentPage,
                "pageSize": this.logisticsPageSize,
                "orderRId": rowData.orderRId,
                "shoeRId": rowData.shoeRId
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialinfo`, { params })
            this.logisticsMaterialData = response.data.result
            this.logisticsRows = response.data.total
        },
    }
}
</script>
