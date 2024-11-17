<template>
    <div class="content">
        <el-row :gutter="20" style="margin-top: 20px; justify-content: space-between;">
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                订单号筛选：
                <el-input
                    v-model="orderRIdSearch"
                    placeholder="请输入订单号"
                    clearable
                    @keypress.enter="getTableData(orderRIdSearch, routeMsg)"
                    @clear="getTableData('', routeMsg)"
                />
            </el-col>
            <el-button type="primary" size="middle" @click="" :icon="Download"></el-button>
        </el-row>
        <el-table
            :data="currentTableData"
            style="width: 100%; margin-bottom: 20px; height: 650px;"
            row-key="id"
            border
            default-expand-all
        >
            <el-table-column>
                <el-table-column prop="orderRId" label="订单编号" sortable />
                <el-table-column prop="factoryShoesModel" label="工厂鞋型编号" sortable />
                <el-table-column prop="custShoesModel" label="客户鞋型编号" sortable />
                <el-table-column prop="materialProcurementCost" label="材料采购成本" sortable />
                <el-table-column prop="needleCuttingLaborCost" label="生产人工成本" sortable />
                <el-table-column prop="administrativeExpenses" label="行政费用" sortable />
                <el-table-column prop="logisticsCosts" label="物流费用" sortable />
                <el-table-column prop="externalProcessingCost" label="外加工成本" sortable />
                <el-table-column prop="orderProfit" label="订单利润" sortable />
                <el-table-column prop="efficiencyIndicators" label="效率指标" sortable />
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
import { ref ,onMounted } from 'vue';
import useTablePagination from '../../hooks/useTablePagination';
import { Download } from '@element-plus/icons-vue';

let orderRIdSearch = ref('');
const routeMsg = '';
const {
    currentPage,
    currentPageSize,
    currentTotalRows,
    currentTableData,
    getTableData,
    chageCurrentPageSize,
    changeCurrentPage
} = useTablePagination();

onMounted(() => {
    getTableData('', routeMsg);
})
</script>

<style scoped>
.content {
    height: calc(100% - 40px);
}
</style>
