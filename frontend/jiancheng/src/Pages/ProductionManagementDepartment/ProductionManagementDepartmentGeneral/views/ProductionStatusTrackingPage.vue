<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main height="">
            <el-row :gutter="20">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">生产节点管理</el-col>
            </el-row>
            <el-row :gutter="20">
                <Arrow :status="1"></Arrow>
            </el-row>
            <el-dialog title="生产节点状态确认" v-model="isProductionConfirmVis" width="80%">
                <el-row :gutter="20">
                    <el-col :span="24" :offset="0">
                        <el-descriptions title="鞋型信息" border column="2">
                            <el-descriptions-item label="订单号">{{ currentRow.orderRId }}</el-descriptions-item>
                            <el-descriptions-item label="鞋型号">{{ currentRow.shoeRId }}</el-descriptions-item>
                            <el-descriptions-item label="客户型号">{{ currentRow.customerProductName
                                }}</el-descriptions-item>
                            <el-descriptions-item label="目前工段">{{ currentRow.currentStage }}</el-descriptions-item>
                            <el-descriptions-item label="下一工段">{{ currentRow.nextTeam }}</el-descriptions-item>
                            <el-descriptions-item label="外包工段">{{ outsourcedLines }}</el-descriptions-item>
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
        </el-main>
    </el-container>
</template>
<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus';
import Arrow from '@/components/OrderShoeProductionArrorView.vue'
export default {
    data() {
        return {
            orderTableData: [],
            currentRow: {},
        }
    },
    components: {
        AllHeader,
        Arrow
    },
    methods: {
        async getOrderTableData() {
            this.currentRow = rowData
            try {
                let params = { "orderShoeId": rowData.orderShoeId, "nodeName": rowData.nodeName }
                let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoebatchinfoforproduction`, { params })
                this.shoeInfo = response.data

                params = { "orderShoeId": rowData.orderShoeId }
                response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeoutsourceinfo`, { params })
                this.outsourceInfo = response.data
                this.outsourcedLines = ''
                this.outsourceInfo.forEach(row => {
                    let temp = row.outsourceType
                    this.outsourcedLines += temp.toString()
                })
                this.isProductionConfirmVis = true
            }
            catch (error) {
                console.log(error)
            }

        },
        showSecondBox() {
            return ElMessageBox.alert('请再次确认推进流程，此操作不可撤回！', '警告', {
                confirmButtonText: '确认',
                showCancelButton: true,
                cancelButtonText: '取消'
            })
        },
        confirmNode() {
            if (this.outsourcedLines.length != 0) {
                ElMessageBox.alert(`你已设置外包，外包工段为：${this.outsourcedLines}。确认后将启动外包流程。`, '提示', {
                    confirmButtonText: '确认',
                    showCancelButton: true,
                    cancelButtonText: '取消'
                }).then(() => {
                    return this.showSecondBox()
                }).then(async () => {
                    const data = { "orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId, "nodeName": this.currentRow.nodeName }
                    await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/editordershoestatus`, data)
                    try {
                        ElMessage.success("推进流程成功。请通知仓库出货。")
                    }
                    catch (error) {
                        console.log(error)
                        ElMessage.error("推进流程失败")
                    }
                    this.isProductionConfirmVis = false
                    this.getOrderTableData()
                })
            } else {
                this.showSecondBox().then(async () => {
                    const data = { "orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId, "nodeName": this.currentRow.nodeName }
                    await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/editordershoestatus`, data)
                    try {
                        ElMessage.success("推进流程成功")
                    }
                    catch (error) {
                        console.log(error)
                        ElMessage.error("推进流程失败")
                    }
                    this.isProductionConfirmVis = false
                    this.getOrderTableData()
                })
            }
        },
    }
}
</script>