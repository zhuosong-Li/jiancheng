<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">工价审批</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable
                @keypress.enter="getOrderTableData()" @clear="getOrderTableData()"/>
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable
                @keypress.enter="getOrderTableData()" @clear="getOrderTableData()"/>
        </el-col>
        <el-col :span="4" :offset="4">
            <span style="white-space: nowrap">工段筛选：
                <el-select v-model="departmentSearch" value-key="" placeholder="" clearable filterable
                    @change="getOrderTableData()">
                    <el-option v-for="item in ['裁断','针车','成型']" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </span>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table :data="orderTableData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客户型号"></el-table-column>
                <el-table-column prop="team" label="需审批工段"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default"
                            @click="openWageApproval(scope.row)">打开工价审批页面</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="15">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            orderRIdSearch: '',
            shoeRIdSearch: '',
            departmentSearch: '',
            orderTableData: [],
            currentPage: 1,
            pageSize: 10,
            totalRows: 0
        }
    },
    mounted() {
        this.getOrderTableData()
    },
    methods: {
        async getOrderTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch,
                "team": this.departmentSearch
            }
            const response = await axios.get("http://localhost:8000/production/productionmanager/getpricereportapprovaloverview", { params })
            this.orderTableData = response.data.result
            this.totalRows = response.data.totalLength
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getOrderTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getOrderTableData()
        },
        openWageApproval(row) {
			const queryString = new URLSearchParams(row).toString();
			const url = `${window.location.origin}/productionmanager/productionwageapproval?${queryString}`
            window.open(url, '_blank')
        }
    }
}
</script>
