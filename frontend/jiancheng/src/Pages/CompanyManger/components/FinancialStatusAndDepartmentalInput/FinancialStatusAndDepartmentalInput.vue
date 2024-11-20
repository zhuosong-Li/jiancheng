<template>
    <div class="content">
        <el-row :gutter="20" style="margin-top: 20px; justify-content: space-between">
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                订单号筛选：
                <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable />
                <el-button
                    type="primary"
                    size="middle"
                    @click="updataParams('orderRid', orderRIdSearch)"
                    style="margin-left: 20px"
                    >筛选</el-button
                >
            </el-col>
            <el-button type="primary" size="middle" @click="" :icon="Download"></el-button>
        </el-row>
        <el-table
            :data="currentTableData"
            style="width: 100%; margin-bottom: 20px; height: 650px"
            row-key="id"
        >
            <el-table-column>
                <el-table-column type="expand">
                    <template #default="props">
                        <el-table
                            :data="props.row.orderShoes"
                            style="width: 100%; margin-bottom: 20px"
                            row-key="id"
                        >
                            <el-table-column />
                            <el-table-column prop="shoeRId" label="工厂鞋型编号" sortable />
                            <el-table-column prop="shoeName" label="客户鞋型编号" sortable />
                            <el-table-column prop="priceInputStatus" label="鞋型售价填写状态" />
                            <el-table-column prop="materialInboundStatus" label="材料入库状态" />
                            <el-table-column prop="cuttingInputStatus" label="裁断价格填写状态" />
                            <el-table-column prop="sewingInputStatus" label="针车价格填写状态" />
                            <el-table-column prop="moldingInputStatus" label="成型价格填写状态" />
                        </el-table>
                    </template>
                </el-table-column>
                <el-table-column prop="orderRid" label="订单编号" sortable />
                <el-table-column prop="shoeRId" label="工厂鞋型编号" sortable />
                <el-table-column prop="shoeName" label="客户鞋型编号" sortable />
                <el-table-column prop="priceInputStatus" label="鞋型售价填写状态" />
                <el-table-column prop="materialInboundStatus" label="材料入库状态" />
                <el-table-column prop="cuttingInputStatus" label="裁断价格填写状态" />
                <el-table-column prop="sewingInputStatus" label="针车价格填写状态" />
                <el-table-column prop="moldingInputStatus" label="成型价格填写状态" />
            </el-table-column>
        </el-table>
        <el-row :gutter="20" style="justify-content: end">
            <el-col :span="9" :offset="10">
                <el-pagination
                    @size-change="chageCurrentPageSize"
                    @current-change="changeCurrentPage"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 30, 40]"
                    :page-size="currentPageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="currentTotalRows"
                />
            </el-col>
        </el-row>
    </div>
</template>

<script lang="js" setup name="CostCalcAndProfitAnalysis">
import { ref, onMounted, getCurrentInstance } from 'vue'
import useTablePagination from '../../hooks/useTablePagination'
import { Download } from '@element-plus/icons-vue'

const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$apiBaseUrl
const routeMsg = `${$api_baseUrl}/headmanager/financialstatus`
let orderRIdSearch = ref('')
const {
    currentPage,
    currentPageSize,
    currentTotalRows,
    currentTableData,
    getTableData,
    chageCurrentPageSize,
    changeCurrentPage,
    updataParams
} = useTablePagination()

onMounted(() => {
    updataParams('route', routeMsg)
})
</script>

<style scoped>
.content {
    height: calc(100% - 40px);
}
</style>
