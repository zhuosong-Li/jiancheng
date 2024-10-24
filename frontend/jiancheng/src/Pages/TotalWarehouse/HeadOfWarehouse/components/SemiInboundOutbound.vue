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
                <el-table-column prop="storageType" label="自产/外包"></el-table-column>
                <el-table-column label="操作" width="300">
                    <template #default="scope">
                        <el-button-group>
                            <el-button type="primary" size="small"
                                @click="inboundSemifinished(scope.row)">入库</el-button>
                            <el-button type="success" size="small"
                                @click="outboundSemifinished(scope.row)">出库</el-button>
                            <el-button type="warning" size="small"
                                @click="finishInoutbound(scope.row)">完成出入库</el-button>
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
    <el-dialog title="半成品入库" v-model="semiInboundDialogVisible" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <el-form-item label="入库时间">
                        <el-date-picker v-model="inboundDate" type="datetime" placeholder="选择日期时间"
                            value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" />
                    </el-form-item>
                    <el-form-item label="入库数量">
                        <el-input v-model="actualInboundAmount"></el-input>
                    </el-form-item>
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
    <el-dialog title="半成品出库" v-model="semiOutboundDialogVisible" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-form label-position="right" label-width="100px">
                    <div v-if="currentRow.storageType === '自产'">
                        <el-form-item label="出库时间">
                            <el-date-picker v-model="outboundForm.outboundDate" type="datetime" placeholder="选择日期时间"
                                style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
                        </el-form-item>
                        <el-form-item label="出库工段">
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
                        <el-form-item label="领料人">
                            <el-input v-model="outboundForm.receiver" placeholder="请输入领料人"></el-input>
                        </el-form-item>
                    </div>
                    <div v-else>
                        <el-form-item label="外包信息"> </el-form-item>
                        <el-text>半成品最迟发货日期：{{ outboundForm.deadlineDate }}</el-text>
                        <el-form-item label="发货地址">
                            <el-input v-model="outboundForm.address" placeholder="请输入发货地址"></el-input>
                        </el-form-item>
                    </div>
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
            inboundDate: '',
            actualInboundAmount: '',
            currentPage: 1,
            pageSize: 10,
            outboundForm: {
                outboundDate: '',
                receiver: '',
                deadlineDate: '',
                address: '',
                outboundAmount: ''
            },
            semiInboundDialogVisible: false,
            semiOutboundDialogVisible: false,
            tableData: [],
            totalRows: 0,
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
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getsemifinishedinoutoverview`, { params })
            this.tableData = response.data.result
            this.totalRows = response.data.total
        },
        async submitInboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "inboundDate": this.inboundDate,
                "amount": this.actualInboundAmount
            }
            try {
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/inboundsemifinished`, data)
                ElMessage.success("入库成功")
            }
            catch (error) {
                console.log(error)
                ElMessage.error("入库失败")
            }
            this.semiInboundDialogVisible = false
            this.getTableData()
        },
        async submitOutboundForm() {
            let data = {
                "orderId": this.currentRow.orderId,
                "orderShoeId": this.currentRow.orderShoeId,
                "storageId": this.currentRow.storageId,
                "outboundDate": this.outboundForm.outboundDate,
                "outboundAmount": this.outboundForm.outboundAmount,
                "picker": this.outboundForm.receiver
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
        handleSizeChange(val) {
            this.pageSize = val
            this.getTableData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getTableData()
        },
        inboundSemifinished(row) {
            this.semiInboundDialogVisible = true
            this.currentRow = row
        },
        outboundSemifinished(row) {
            this.semiOutboundDialogVisible = true
            this.currentRow = row
        },
        finishInoutbound(row) {
            ElMessageBox.alert('你仍可前往出入库记录修改库存信息，是否继续？', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            }).then(async () => {
                const data = { "storageId": row.storageId }
                await axios.patch(`${this.$apiBaseUrl}/warehouse/warehousemanager/finishinoutbound`, data)
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
