<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main height="">
            <el-row :gutter="20" style="text-align: center">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">订单鞋型工价审批页面</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" border column="2">
                        <el-descriptions-item label="订单号">{{ $props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ $props.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户号">{{ $props.customerName }}</el-descriptions-item>
                        <el-descriptions-item label="截止日期">{{ $props.orderEndDate }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px">
                <el-col :span="24" :offset="0">
                    鞋型配码信息
                    <el-table :data="shoeInfo" border stripe :max-height="200">
                        <el-table-column prop="colorName" label="颜色"></el-table-column>
                        <el-table-column prop="batchName" label="配码编号"></el-table-column>
                        <el-table-column prop="size34" label="34"></el-table-column>
                        <el-table-column prop="size35" label="35"></el-table-column>
                        <el-table-column prop="size36" label="36"></el-table-column>
                        <el-table-column prop="size37" label="37"></el-table-column>
                        <el-table-column prop="size38" label="38"></el-table-column>
                        <el-table-column prop="size39" label="39"></el-table-column>
                        <el-table-column prop="size40" label="40"></el-table-column>
                        <el-table-column prop="size41" label="41"></el-table-column>
                        <el-table-column prop="size42" label="42"></el-table-column>
                        <el-table-column prop="size43" label="43"></el-table-column>
                        <el-table-column prop="size44" label="44"></el-table-column>
                        <el-table-column prop="size45" label="45"></el-table-column>
                        <el-table-column prop="size46" label="46"></el-table-column>
                        <el-table-column prop="pairAmount" label="双数"></el-table-column>
                        <el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
                    </el-table>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    鞋型工价表
                    <el-table :data="priceReports" border stripe>
                        <el-table-column prop="team" label="工段类型"></el-table-column>
                        <el-table-column prop="productionStartDate" label="生产开始日期"></el-table-column>
                        <el-table-column prop="productionEndDate" label="生产结束日期"></el-table-column>
                        <el-table-column prop="reportStatus" label="状态"></el-table-column>
                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="primary" @click="getReportDetail(scope.row)">
                                    <span v-if="scope.row.reportStatus === '未审核'">
                                        审核
                                    </span>
                                    <span v-else>
                                        查看
                                    </span>
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
    <el-dialog title="工价审核界面" v-model="isWagesApprovalVis" width="80%">
        <el-table :data="reportDetail" border stripe max-height="500">
            <el-table-column prop="rowId" label="序号"></el-table-column>
            <el-table-column prop="procedure" label="工序名称"></el-table-column>
            <el-table-column prop="price" label="工价"></el-table-column>
            <el-table-column prop="note" label="备注"></el-table-column>
        </el-table>
        <template #footer>
            <span>
                <el-button @click="isWagesApprovalVis = false">关闭</el-button>
                <el-button v-if="currentRow.reportStatus === '未审批'" type="danger"
                    @click="openRefusalDialog">驳回请求</el-button>
                <el-button v-if="currentRow.reportStatus === '未审批'" type="primary"
                    @click="approveReport">审批通过</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="驳回审批请求" v-model="isRefuseApprovalVis" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                请填写驳回原因（不超过20字）：
                <el-input v-model="rejectionReason" type="textarea" placeholder="" resize="none" clearable
                    @change=""></el-input>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="isRefuseApprovalVis = false">取消</el-button>
                <el-button type="success" @click="rejectReport">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import AllHeader from '@/components/AllHeader.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
export default {
    components: {
        AllHeader
    },
    props: ["orderShoeId", "orderId", "orderRId", "shoeRId", "orderEndDate", "customerName"],
    data() {
        return {
            rejectionReason: '',
            isRefuseApprovalVis: false,
            reportDetail: [],
            shoeInfo: [],
            priceReports: [],
            isWagesApprovalVis: false,
            currentRow: {}
        }
    },
    async mounted() {
        await this.getOrderShoeBatchInfo()
        await this.getPriceReportInfo()
    },
    methods: {
        async getOrderShoeBatchInfo() {
            try {
                const params = { "orderShoeId": this.$props.orderShoeId }
                const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoebatchinfo`, { params })
                this.shoeInfo = response.data
            }
            catch(error) {
                console.log(error)
            }
        },
        async getPriceReportInfo() {
            const params = { "orderShoeId": this.$props.orderShoeId }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getallpricereportsforordershoe`, { params })
            this.priceReports = response.data
        },
        async getReportDetail(rowData) {
            this.currentRow = rowData
            const params = { "reportId": rowData.reportId }
            const response = await axios.get(`${this.$apiBaseUrl}/production/getpricereportdetail`, { params })
            this.reportDetail = response.data
            this.isWagesApprovalVis = true
        },
        async approveReport() {
            ElMessageBox.confirm(
                '此操作无法撤回，是否通过？',
                '提示',
            ).then(async () => {
                const data = { "orderId": this.$props.orderId, "orderShoeId": this.$props.orderShoeId, "reportId": this.currentRow.reportId }
                try {
                    await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/approvepricereport`, data)
                    ElMessage.success('审批成功')
                }
                catch(error) {
                    console.log(error)
                    ElMessage.error('驳回失败')
                }
                this.isWagesApprovalVis = false
                this.getPriceReportInfo()
            }).catch(() => {
                ElMessage.info('撤销操作')
            })
        },
        openRefusalDialog() {
            this.isRefuseApprovalVis = true
        },
        async rejectReport() {
            ElMessageBox.confirm(
                '此操作无法撤回，是否驳回？',
                '提示',
            ).then(async () => {
                let reportIdArr = []
                if (this.currentRow.team === '针车预备' || this.currentRow.team === '针车') {
                    this.priceReports.forEach(row => {
                        if (row.team === '针车预备' || row.team === '针车') {
                            reportIdArr.push(row.reportId)
                        }
                    })
                }
                else {
                    reportIdArr = [this.currentRow.reportId]
                }
                const data = { "orderId": this.$props.orderId, "orderShoeId": this.$props.orderShoeId, "reportIdArr": reportIdArr, "rejectionReason": this.rejectionReason }
                try {
                    await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/rejectpricereport`, data)
                    ElMessage.success('驳回成功')
                }
                catch(error) {
                    console.log(error)
                    ElMessage.error('驳回失败')
                }
                this.isRefuseApprovalVis = false
                this.isWagesApprovalVis = false
                this.getPriceReportInfo()
            }).catch(() => {
                ElMessage.info('撤销操作')
            })
        },
    }
}
</script>
