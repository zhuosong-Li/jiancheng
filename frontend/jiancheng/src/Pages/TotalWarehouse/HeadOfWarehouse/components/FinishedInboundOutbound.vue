<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">成品出/入库</el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderNumberSearch" placeholder="请输入订单号" clearable @keypress.enter="getTableData()"
                @clear="getTableData" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeNumberSearch" placeholder="请输入鞋型号" clearable @keypress.enter="getTableData()"
                @clear="getTableData" />
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table :data="tableData" border stripe height="400">
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="工厂型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客人号"></el-table-column>
                <el-table-column prop="inboundAmount" label="鞋型应入库数量"></el-table-column>
                <el-table-column prop="currentAmount" label="鞋型库存"></el-table-column>
                <el-table-column prop="statusName" label="状态"></el-table-column>
                <el-table-column label="操作" width="200">
                    <template #default="scope">
                        <el-button v-if="scope.row.statusName === '未完成入库'" type="primary" size="small"
                            @click="inboundFinished(scope.row)">入库</el-button>
                        <el-button v-else type="success" size="small"
                            @click="outboundFinished(scope.row)">出库</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="totalRows" />
        </el-col>
    </el-row>
    <el-dialog title="成品入库" v-model="inboundDialogVisible" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <el-form-item label="入库时间">
                        <el-date-picker v-model="inboundDate" type="datetime" placeholder="选择日期时间" style="width: 100%"
                            value-format="YYYY-MM-DD HH:mm:ss" />
                    </el-form-item>
                    <el-form-item label="入库方式">
                        <el-radio-group v-model="inboundType">
                            <el-radio value="1">自产入库</el-radio>
                            <el-radio value="2">外包入库</el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="inboundDialogVisible = false">返回</el-button>
                <el-button type="primary" @click="submitInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="成品出库" v-model="outboundDialogVisible" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <el-form-item label="出库时间">
                        <el-date-picker v-model="outboundForm.outboundDate" type="datetime" placeholder="选择日期时间"
                            style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
                    </el-form-item>
                    <el-form-item label="" prop="">
                        <el-text>成品最迟发货日期：{{ currentRow.endDate }}</el-text>
                    </el-form-item>

                    <el-form-item label="发货地址">
                        <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
                    </el-form-item>
                    <el-form-item label="出货选项">
                        <el-checkbox v-model="outboundForm.isOutboundAll" label="出货该订单所有鞋型" size="large" />
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="outboundDialogVisible = false">返回</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios'
export default {
    data() {
        return {
            inboundType: '1',
            inboundDate: '',
            currentPage: 1,
            pageSize: 10,
            outboundForm: {
                outboundDate: '',
                outboundType: '1',
                section: '',
                receiver: '',
                deadlineDate: '',
                address: '',
                isOutboundAll: false
            },
            inboundDialogVisible: false,
            outboundDialogVisible: false,
            tableData: [],
            totalRows: 0,
            currentRow: {},
            orderNumberSearch: '',
            shoeNumberSearch: '',
        }
    },
    mounted() {
        this.getTableData()
    },
    methods: {
        async getTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderNumberSearch,
                "shoeRId": this.shoeNumberSearch,
                "opType": 1
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getfinishedinoutoverview`, { params })
            this.tableData = response.data.result
            this.totalRows = response.data.total
        },
        async submitInboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "inboundDate": this.inboundDate,
                "type": this.inboundType,
                "amount": this.currentRow.inboundAmount
            }
            const response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundfinished`, data)
            if (response.status == 200) {
                ElMessage.success("入库成功")
            }
            else {
                ElMessage.error("入库失败")
            }
            this.inboundDialogVisible = false
            this.getTableData()
        },
        async submitOutboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "outboundDate": this.outboundForm.outboundDate,
                "outboundAddress": this.outboundForm.address,
                "isOutboundAll": this.outboundForm.isOutboundAll
            }
            const response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/outboundfinished`, data)
            if (response.status == 200) {
                ElMessage.success("出库成功")
            }
            else {
                ElMessage.error("出库失败")
            }
            this.outboundDialogVisible = false
            this.getTableData()
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getTableData()
        },
        handlePageChange(val) {
            this.page = val
            this.getTableData()
        },
        inboundFinished(row) {
            this.inboundDialogVisible = true
            this.currentRow = row
        },
        outboundFinished(row) {
            this.outboundDialogVisible = true
            this.currentRow = row
        }
    }
}
</script>
