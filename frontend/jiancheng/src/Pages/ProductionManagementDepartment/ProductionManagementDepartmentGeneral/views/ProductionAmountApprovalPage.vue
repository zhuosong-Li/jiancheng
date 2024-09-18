<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main height="">
            <el-row :gutter="20" style="text-align: center">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">订单鞋型数量审批页面</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单及鞋型信息" border column="2">
                        <el-descriptions-item label="订单号">{{ $props.orderRId }}</el-descriptions-item>
                        <el-descriptions-item label="鞋型号">{{ $props.shoeRId }}</el-descriptions-item>
                        <el-descriptions-item label="客户型号">{{ $props.customerProductName }}</el-descriptions-item>
                        <el-descriptions-item label="订单截止日期">{{ $props.orderEndDate }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="12" :offset="0">
                    日期范围限制：
                    <el-date-picker v-model="datePeriod" type="daterange" value-format="YYYY-MM-DD" clearable
                        start-placeholder="起始日期" end-placeholder="截止日期" @change="getAmountListData"
                        @clear="getAmountListData">
                    </el-date-picker>
                </el-col>
                <el-col :span="4" :offset="0" style="white-space: nowrap">
                    工段选择：
                    <el-select v-model="departSelect" value-key="" placeholder="" clearable filterable
                        @change="getAmountListData" @clear="getAmountListData">
                        <el-option v-for="item in ['全部', '裁断', '针车预备', '针车', '成型']" :key="item" :label="item"
                            :value="item">
                        </el-option>
                    </el-select>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-table :data="amountListData" border stripe>
                        <el-table-column prop="reportDate" label="日期"></el-table-column>
                        <el-table-column prop="team" label="工段"></el-table-column>
                        <el-table-column prop="startDate" label="生产起始日期"></el-table-column>
                        <el-table-column prop="endDate" label="生产结束日期"></el-table-column>
                        <el-table-column prop="reportStatus" label="状态"></el-table-column>
                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="primary" size="default"
                                    @click="openApprovalDialog(scope.row)">审批</el-button>
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
        </el-main>
    </el-container>
    <el-dialog title="数量审批界面" v-model="isAmountApprovalVis" width="50%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-table :data="shoeBatchAmountData" border stripe>
                    <el-table-column prop="name" label="鞋码编号"></el-table-column>、
                    <el-table-column prop="amount" label="昨日生产数量"></el-table-column>
                    <el-table-column prop="producedAmount" label="累计生产数量"></el-table-column>
                    <el-table-column prop="totalAmount" label="目标数量"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="">取消</el-button>
                <el-button type="danger" @click="openRefusalDialog">驳回请求</el-button>
                <el-button type="primary" @click="openConfirmDialog">审批通过</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog title="驳回审批请求" v-model="isRefuseApprovalVis" width="30%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                请填写驳回原因（不超过20字）：
                <el-input v-model="refuseReason" type="textarea" placeholder="" resize="none" clearable
                    @change=""></el-input>

            </el-col>
        </el-row>

        <template #footer>
            <span>
                <el-button @click="isRefuseApprovalVis = false">取消</el-button>
                <el-button type="success" @click="confirmRefusal">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus';
export default {
    props: ['orderShoeId', 'orderRId', 'shoeRId', 'orderEndDate', 'customerProductName'],
    components: {
        AllHeader
    },
    data() {
        return {
            currentPage: 1,
            pageSize: 10,
            totalRows: 0,
            isRefuseApprovalVis: false,
            isAmountApprovalVis: false,
            refuseReason: '',
            datePeriod: [],
            departSelect: '',
            amountListData: [],
            currentRow: {},
            shoeBatchAmountData: []
        }
    },
    mounted() {
        this.getAmountListData()
    },
    methods: {
        async getAmountListData() {
            let startDate = null, endDate = null
            if (this.datePeriod) {
                startDate = this.datePeriod[0]
                endDate = this.datePeriod[1]
            }
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderShoeId": this.$props.orderShoeId,
                "searchStartDate": startDate,
                "searchEndDate": endDate,
                "team": this.departSelect,
            }
            const response = await axios.get("http://localhost:8000/production/productionmanager/getsubmittedquantityreports", { params })
            this.amountListData = response.data.result
            this.totalRows = response.data.totalLength
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getAmountListData()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getAmountListData()
        },
        async openApprovalDialog(rowData) {
            this.currentRow = rowData
            let params = { reportId: rowData.reportId }
            let response = await axios.get("http://localhost:8000/production/getquantityreportdetail", { params })
            this.shoeBatchAmountData = response.data
            this.shoeBatchAmountData.forEach(row => {
                if (rowData.team == "裁断")
                    row["producedAmount"] = row.cuttingAmount
                else if (rowData.team == "针车预备")
                    row["producedAmount"] = row.preSewingAmount
                else if (rowData.team == "针车")
                    row["producedAmount"] = row.sewingAmount
                else if (rowData.team == "成型")
                    row["producedAmount"] = row.moldingAmount
            })
            this.isAmountApprovalVis = true
        },
        async openConfirmDialog() {
            try {
                const data = {"reportId": this.currentRow.reportId,}
                console.log(data)
                await axios.patch("http://localhost:8000/production/productionmanager/approvequantityreport", data)
                ElMessage({
                    type: 'success',
                    message: '审批成功!'
                });
                this.isAmountApprovalVis = false
                this.getAmountListData()
            }
            catch {
                ElMessage({
                    type: 'warning',
                    message: '软件异常!'
                });
            }
        },
        openRefusalDialog() {
            this.isRefuseApprovalVis = true
        },
        async confirmRefusal() {
            const data = { "reportId": this.currentRow.reportId, "rejectionReason": this.refuseReason }
            await axios.patch("http://localhost:8000/production/productionmanager/rejectquantityreport", data)
            this.isRefuseApprovalVis = false
            this.isAmountApprovalVis = false
            ElMessage({
                type: 'success',
                message: '驳回成功!'
            });
            this.getAmountListData()
        }
    }
}
</script>
