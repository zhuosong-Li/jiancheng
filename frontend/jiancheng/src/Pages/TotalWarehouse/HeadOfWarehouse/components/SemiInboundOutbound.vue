<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">半成品出/入库</el-col>
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
            <el-table :data="tableData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="工厂型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客人号"></el-table-column>
                <el-table-column prop="inboundAmount" label="计划入库数量"></el-table-column>
                <el-table-column prop="currentAmount" label="半成品库存"></el-table-column>
                <el-table-column prop="object" label="半成品类型"></el-table-column>
                <el-table-column prop="statusName" label="状态"></el-table-column>
                <el-table-column label="操作" width="300">
                    <template #default="scope">
                        <el-button-group>
                            <el-button type="primary" size="small"
                                @click="inboundSemifinished(scope.row)">入库</el-button>
                            <el-button type="success" size="small"
                                @click="outboundSemifinished(scope.row)">出库</el-button>
                            <el-button v-if="scope.row.statusName === '未完成入库'" type="warning" size="small"
                                @click="finishInbound(scope.row)">完成入库</el-button>
                            <el-button v-if="scope.row.statusName === '已完成入库'" type="warning" size="small"
                                @click="finishOutbound(scope.row)">完成出库</el-button>
                        </el-button-group>
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
    <el-dialog title="半成品入库" v-model="semiInboundDialogVisible" width="35%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <el-form-item label="入库时间">
                        <el-date-picker v-model="inboundForm.inboundDate" type="datetime" placeholder="选择日期时间"
                            value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" />
                    </el-form-item>
                    <el-form-item label="入库数量">
                        <el-input v-model="inboundForm.actualInboundAmount"></el-input>
                    </el-form-item>
                    <el-form-item label="入库类型">
                        <el-radio-group v-model="inboundForm.inboundType">
                            <el-radio :value="0">自产</el-radio>
                            <el-radio :value="1">外包</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-table v-if="inboundForm.inboundType == 1" :data="inboundForm.outsourceInfo" style="width: 100%">
                        <el-table-column width="55">
                            <template #default="scope">
                                <el-radio v-model="inboundForm.selectedOutsource" :value="scope.row.outsourceInfoId" />
                            </template>
                        </el-table-column>
                        <el-table-column prop="outsourceFactory.value" label="工厂名称" />
                        <el-table-column prop="outsourceAmount" label="外包数量" />
                        <el-table-column prop="outsourceType" label="外包类型" />
                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button :disabled="inboundForm.selectedOutsource !== scope.row.outsourceInfoId"
                                    type="warning" size="small" @click="finishOutsourceInbound(scope.row)">
                                    完成外包入库
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-form>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="semiInboundDialogVisible = false">返回</el-button>
                <el-button type="primary" @click="submitInboundForm">入库</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="半成品出库" v-model="semiOutboundDialogVisible" width="35%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <el-form-item label="出库时间">
                        <el-date-picker v-model="outboundForm.outboundDate" type="datetime" placeholder="选择日期时间"
                            style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
                    </el-form-item>
                    <el-form-item label="出库类型">
                        <el-radio-group v-model="outboundForm.outboundType">
                            <el-radio :value="0">自产出库</el-radio>
                            <el-radio :value="1">外包出库</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item v-if="outboundForm.outboundType == 0" label="出库至">
                        <div v-if="currentRow.object === '裁断后材料'">
                            针车
                        </div>
                        <div v-else-if="currentRow.object === '鞋包'">
                            成型
                        </div>
                    </el-form-item>
                    <el-form-item label="出库数量">
                        <el-input v-model="outboundForm.outboundAmount"></el-input>
                    </el-form-item>
                    <el-form-item v-if="outboundForm.outboundType == 0" label="领料人">
                        <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"
                            :disabled="outboundForm.outboundType == 1"></el-input>
                    </el-form-item>
                    <el-table v-if="outboundForm.outboundType == 1" :data="outboundForm.outsourceInfo"
                        style="width: 100%">
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
                                <el-button :disabled="outboundForm.selectedOutsource !== scope.row.outsourceInfoId"
                                    type="warning" size="small" @click="finishOutsourceOutbound(scope.row)">
                                    完成外包出库
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-form-item v-if="outboundForm.outboundType == 1" label="发货地址">
                        <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="semiOutboundDialogVisible = false">返回</el-button>
                <el-button type="primary" @click="submitOutboundForm">出库</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus';
export default {
    data() {
        return {
            inboundForm: {
                selectedOutsource: null,
                inboundDate: '',
                inboundType: 0,
                actualInboundAmount: '',
                outsourceInfo: []
            },
            currentPage: 1,
            pageSize: 10,
            outboundForm: {
                outboundDate: '',
                receiver: '',
                deadlineDate: '',
                address: '',
                outboundAmount: '',
                outboundType: 0,
                outsourceInfo: [],
                selectedOutsource: null
            },
            semiInboundDialogVisible: false,
            semiOutboundDialogVisible: false,
            tableData: [],
            totalRows: 0,
            orderNumberSearch: '',
            shoeNumberSearch: '',
            currentRow: {}
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
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsemifinishedinoutoverview`, { params })
            this.tableData = response.data.result
            this.totalRows = response.data.total
        },
        async submitInboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "outsourceInfoId": this.inboundForm.selectedOutsource,
                "inboundDate": this.inboundForm.inboundDate,
                "inboundType": this.inboundForm.inboundType,
                "amount": this.inboundForm.actualInboundAmount
            }
            try {
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundsemifinished`, data)
                ElMessage.success("入库成功")
            }
            catch (error) {
                console.log(error)
                ElMessage.error("入库失败")
            }
            this.getTableData()
        },
        async finishOutsourceInbound(row) {
            try {
                let data = { "outsourceInfoId": row.outsourceInfoId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutsourceinbound`, data)
                ElMessage.success("外包入库成功")
                this.getOutsourceInfoForInbound()
            }
            catch (error) {
                console.log(error)
                ElMessage.error("外包入库失败")
            }
        },
        async submitOutboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "outboundDate": this.outboundForm.outboundDate,
                "outboundAmount": this.outboundForm.outboundAmount,
                "picker": this.outboundForm.receiver,
                "outboundType": this.outboundForm.outboundType,
                "outsourceInfoId": this.outboundForm.selectedOutsource,
                "outboundAddress": this.outboundForm.address
            }
            const response = await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/outboundsemifinished`, data)
            if (response.status == 200) {
                ElMessage.success("出库成功")
            }
            else {
                ElMessage.error("出库失败")
            }
            this.semiOutboundDialogVisible = false
            this.getTableData()
        },
        async finishOutsourceOutbound(row) {
            try {
                let data = { "outsourceInfoId": row.outsourceInfoId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutsourceoutbound`, data)
                ElMessage.success("外包出库成功")
                await this.getOutsourceInfoForOutbound()
            }
            catch (error) {
                console.log(error)
                ElMessage.error("外包出库失败")
            }
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getTableData()
        },
        async getOutsourceInfoForInbound() {
            let params = { "orderShoeId": this.currentRow.orderShoeId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
            this.inboundForm.outsourceInfo = []
            response.data.forEach(element => {
                let length = element.outsourceType.length
                if (element.outsourceStatus == 5 || element.outsourceStatus == 6) {
                    if ((this.currentRow.object === '裁断后材料' && element.outsourceType[length - 1] === '裁断') || (this.currentRow.object === '鞋包' && element.outsourceType[length - 1] === '针车')) {
                        this.inboundForm.outsourceInfo.push(element)
                    }
                }
            });
            if (this.inboundForm.outsourceInfo.length > 0) {
                this.inboundForm.selectedOutsource = this.inboundForm.outsourceInfo[0].outsourceInfoId
            }
        },
        async getOutsourceInfoForOutbound() {
            let params = { "orderShoeId": this.currentRow.orderShoeId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
            this.outboundForm.outsourceInfo = []
            response.data.forEach(element => {
                if (element.outsourceStatus == 2 || element.outsourceStatus == 4) {
                    if ((this.currentRow.object === '裁断后材料' && element.outsourceType[0] === '针车') ||
                        (this.currentRow.object === '鞋包' && element.outsourceType[0] === '成型')) {
                        this.outboundForm.outsourceInfo.push(element)
                    }
                }
            });
            if (this.outboundForm.outsourceInfo.length > 0) {
                this.outboundForm.selectedOutsource = this.outboundForm.outsourceInfo[0].outsourceInfoId
            }
        },
        async inboundSemifinished(row) {
            this.currentRow = row
            await this.getOutsourceInfoForInbound()
            this.semiInboundDialogVisible = true
        },
        async outboundSemifinished(row) {
            this.currentRow = row
            await this.getOutsourceInfoForOutbound()
            this.semiOutboundDialogVisible = true
        },
        finishInbound(row) {
            ElMessageBox.alert('该操作完成对此鞋型半成品入库，是否继续？', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                const data = { "storageId": row.storageId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishinboundsemifinished`, data)
                try {
                    ElMessage.success("操作成功")
                }
                catch (error) {
                    console.log(error)
                    ElMessage.error("操作异常")
                }
                this.getTableData()
            })
        },
        finishOutbound(row) {
            ElMessageBox.alert('该操作完成对此鞋型半成品出库，是否继续？', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                const data = { "storageId": row.storageId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishoutboundsemifinished`, data)
                try {
                    ElMessage.success("操作成功")
                }
                catch (error) {
                    console.log(error)
                    ElMessage.error("操作异常")
                }
                this.getTableData()
            })
        }
    }
}
</script>
