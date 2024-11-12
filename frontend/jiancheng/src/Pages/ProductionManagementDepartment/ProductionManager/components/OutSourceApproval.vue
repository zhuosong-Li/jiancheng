<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">外包信息页面</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            订单号筛选：
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable @keypress.enter="getOutsourceOverview()"
                @clear="getOutsourceOverview" />
        </el-col>
        <el-col :span="4" :offset="2" style="white-space: nowrap;">
            鞋型号筛选：
            <el-input v-model="shoeRIdSearch" placeholder="请输入鞋型号" clearable @keypress.enter="getOutsourceOverview()"
                @clear="getOutsourceOverview" />
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table :data="orderTableData" border stripe>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="鞋型号"></el-table-column>
                <el-table-column prop="customerProductName" label="客户型号"></el-table-column>
                <el-table-column prop="outsourceAmount" label="外包数量"></el-table-column>
                <el-table-column prop="factoryName" label="外包工厂"></el-table-column>
                <el-table-column label="外包工段">
                    <template #default="scope">
                        {{ scope.row.outsourceType.join(",") }}
                    </template>
                </el-table-column>
                <el-table-column prop="outsourceStatus" label="状态">
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="openApprovalDialog(scope.row)">
                            {{ scope.row.outsourceStatus === '已提交' ? "审批" : "查看" }}
                        </el-button>
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
    <el-dialog title="审批页面" v-model="isApprovalDialogOpen" width="90%">
        <el-descriptions title="订单信息" border>
            <el-descriptions-item label="订单号">
                {{ currentRow.orderRId }}
            </el-descriptions-item>
            <el-descriptions-item label="订单开始日期">
                {{ currentRow.orderStartDate }}
            </el-descriptions-item>
            <el-descriptions-item label="订单结束日期">
                {{ currentRow.orderEndDate }}
            </el-descriptions-item>
        </el-descriptions>
        <el-descriptions title="外包信息" border style="margin-top: 20px;">
            <el-descriptions-item label="工厂型号">
                {{ currentRow.shoeRId }}
            </el-descriptions-item>
            <el-descriptions-item label="外包开始日期">
                {{ currentRow.outsourceStartDate }}
            </el-descriptions-item>
            <el-descriptions-item label="外包结束日期">
                {{ currentRow.outsourceEndDate }}
            </el-descriptions-item>
            <el-descriptions-item label="外包最迟交货日期">
                {{ currentRow.deadlineDate }}
            </el-descriptions-item>
            <el-descriptions-item label="外包工厂">
                {{ currentRow.factoryName }}
            </el-descriptions-item>
            <el-descriptions-item label="外包工段">
                {{ currentRow.outsourceType.join(",") }}
            </el-descriptions-item>
            <el-descriptions-item label="外包数量">
                {{ currentRow.outsourceAmount }}
            </el-descriptions-item>
            <el-descriptions-item label="半成品外发日期">
                {{ currentRow.semifinishedEstimatedOutboundDate }}
            </el-descriptions-item>
            <el-descriptions-item label="材料外发日期">
                {{ currentRow.materialEstimatedOutboundDate }}
            </el-descriptions-item>
        </el-descriptions>
        <el-descriptions title="外包具体数量" style="margin-top: 20px;">
        </el-descriptions>
        <el-table :data="outsourceShoeBatchInfo" border stripe :max-height="500">
            <el-table-column prop="colorName" label="颜色"></el-table-column>
            <el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
            <el-table-column v-for="column in filteredColumns" :key="column.prop" :prop="column.prop"
                :label="column.label">
            </el-table-column>
        </el-table>
        <template #footer>
            <el-button type="primary" @click="isApprovalDialogOpen = false">返回</el-button>
            <el-button v-if="currentRow.outsourceStatus === '已提交'" type="success"
                @click="approveOutsource">通过</el-button>
            <el-button v-if="currentRow.outsourceStatus === '已提交'" type="danger"
                @click="openRejectDialog">驳回</el-button>
        </template>
    </el-dialog>

    <el-dialog title="驳回审批请求" v-model="isRejectOpen" width="30%" draggable>
        请填写驳回原因（不超过50字）
        <el-input v-model="rejectionInput" type="textarea"></el-input>
        <el-button @click="rejectOutsource">确认</el-button>
        <el-button @click="isRejectOpen = false">取消</el-button>
    </el-dialog>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus';
import { getShoeSizesName } from '../../utils';
export default {
    data() {
        return {
            orderRIdSearch: '',
            shoeRIdSearch: '',
            orderTableData: [],
            currentPage: 1,
            pageSize: 10,
            totalRows: 0,
            isApprovalDialogOpen: false,
            currentRow: {},
            isRejectOpen: false,
            rejectionInput: null,
            getShoeSizesName,
            shoeSizeColumns: [],
            outsourceShoeBatchInfo: []
        }
    },
    mounted() {
        this.getOutsourceOverview()
    },
    computed: {
        filteredColumns() {
            return this.shoeSizeColumns.filter(column =>
                this.outsourceShoeBatchInfo.some(row => row[column.prop] !== undefined && row[column.prop] !== null && row[column.prop] !== 0)
            );
        }
    },
    methods: {
        handleSizeChange(val) {
            this.pageSize = val
            this.getOutsourceOverview()
        },
        handlePageChange(val) {
            this.currentPage = val
            this.getOutsourceOverview()
        },
        async getOutsourceOverview() {
            const params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch
            }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourceapprovaloverview`, { params })
            this.orderTableData = response.data.result
            this.totalRows = response.data.totalLength
        },
        async openApprovalDialog(row) {
            this.currentRow = row
            this.shoeSizeColumns = await this.getShoeSizesName(row.orderShoeId)
            console.log(this.shoeSizeColumns)
            await this.getOutsourceBatchInfo(row)
            this.isApprovalDialogOpen = true
        },
        async getOutsourceBatchInfo(row) {
            let params = { "orderShoeId": row.orderShoeId, "outsourceInfoId": row.outsourceInfoId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getoutsourcebatchinfo`, { params })
            this.outsourceShoeBatchInfo = response.data
        },
        async approveOutsource() {
            try {
                let data = { "outsourceInfoId": this.currentRow.outsourceInfoId }
                await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/approveoutsource`, data)
                ElMessage.success("审批成功")
                this.getOutsourceOverview()
                this.isApprovalDialogOpen = false
            }
            catch (error) {
                ElMessage.error("审批失败")
                console.log(error)
            }
        },
        async rejectOutsource() {
            try {
                let data = { "outsourceInfoId": this.currentRow.outsourceInfoId, "rejectionReason": this.rejectionInput }
                await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/rejectoutsource`, data)
                ElMessage.success("驳回成功")
                this.getOutsourceOverview()
                this.isRejectOpen = false
                this.isApprovalDialogOpen = false
            }
            catch (error) {
                ElMessage.error("驳回失败")
                console.log(error)
            }
        },
        async openRejectDialog() {
            this.rejectionInput = null
            this.isRejectOpen = true
        }
    },

}
</script>
