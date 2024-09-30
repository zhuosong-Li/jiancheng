<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">生产节点管理</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable @keypress.enter="getOrderTableData()"
                @clear="getOrderTableData()" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable @keypress.enter="getOrderTableData()"
                @clear="getOrderTableData()" />
        </el-col>
        <el-col :span="4" :offset="4">
            <span style="white-space: nowrap">状态点查询：
                <el-select v-model="nodeNameSearch" clearable filterable
                    @change="getOrderTableData()" @clear="getOrderTableData()">
                    <el-option v-for="item in [
                        '生产开始',
                        '裁断开始',
                        '针车预备开始',
                        '针车开始',
                        '成型开始',
                        '生产结束'
                    ]" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </span>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-table :data="orderTableData" border stripe>
            <el-table-column prop="orderRId" label="订单号"></el-table-column>
            <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
            <el-table-column prop="nodeName" label="需确认状态点"></el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" size="default" @click="handleConfirmation(scope.row)">确认状态完成</el-button>
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
    <el-dialog title="生产节点状态确认" v-model="isProductionConfirmVis" width="80%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="鞋型信息" border column="2">
                    <el-descriptions-item label="订单号">{{ currentRow.orderRId }}</el-descriptions-item>
                    <el-descriptions-item label="鞋型号">{{ currentRow.shoeRId }}</el-descriptions-item>
                    <el-descriptions-item label="客户型号">{{ currentRow.customerProductName }}</el-descriptions-item>
                    <el-descriptions-item label="目前工段">{{ currentRow.currentStage }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                鞋型配码信息
                <el-table :data="shoeInfo" border stripe :max-height="200">
                    <el-table-column prop="color" label="颜色"></el-table-column>
                    <el-table-column prop="batchInfoName" label="配码编号"></el-table-column>
                    <el-table-column prop="totalAmount" label="双数"></el-table-column>
                    <el-table-column prop="finishedAmount" label="完成数"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <el-button @click="isProductionConfirmVis = false">取消</el-button>
            <el-button type="success" @click="confirmNode">确认推进流程</el-button>
        </template>
    </el-dialog>
</template>
<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
export default {
    data() {
        return {
            currentPage: 1,
            pageSize: 10,
            totalRows: 0,
            isProductionConfirmVis: false,
            orderRIdSearch: '',
            shoeRIdSearch: '',
            nodeNameSearch: '',
            orderTableData: [],
            currentRow: {},
            shoeInfo: [],
        }
    },
    mounted() {
        this.getOrderTableData()
    },
    methods: {
        handleSizeChange(val) {
            this.pageSize = val
            this.getOrderTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getOrderTableData()
        },
        async getOrderTableData() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch,
                "nodeName": this.nodeNameSearch
            }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getfinishednodes`, { params })
            this.orderTableData = response.data.result
            this.totalRows = response.data.totalLength
        },
        async handleConfirmation(rowData) {
            this.currentRow = rowData
            if (this.currentRow.nodeName === '生产开始') {
                this.currentRow.currentStage = '生产前'
            }
            else if (this.currentRow.nodeName === '裁断开始') {
                this.currentRow.currentStage = '裁断'
            }
            else if (this.currentRow.nodeName === '针车预备开始') {
                this.currentRow.currentStage = '针车预备'
            }
            else if (this.currentRow.nodeName === '针车开始') {
                this.currentRow.currentStage = '针车'
            }
            else if (this.currentRow.nodeName === '成型开始') {
                this.currentRow.currentStage = '成型'
            }
            else if (this.currentRow.nodeName === '生产结束') {
                this.currentRow.currentStage = '生产结束'
            }
            const params = {"orderShoeId": rowData.orderShoeId, "nodeName": rowData.nodeName}
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoebatchinfoforproduction`, { params })
            this.shoeInfo = response.data
            this.isProductionConfirmVis = true
        },
        confirmNode() {
            ElMessageBox.alert('请再次确认推进流程，此操作不可撤回！', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                const data = { "orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId, "nodeName": this.currentRow.nodeName }
                const response = await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/editordershoestatus`, data)
                if (response.status == 200) {
                    ElMessage.success("推进流程成功")
                }
                else {
                    ElMessage.error("推进流程失败")
                }
                this.isProductionConfirmVis = false
                this.getOrderTableData()
            })
        },

    }
}
</script>
