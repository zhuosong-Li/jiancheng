<template>
    <div class="content">
        <el-row :gutter="20" style="margin-top: 20px; justify-content: space-between;">
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                进行中订单号筛选：
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
            style="width: 100%; margin-bottom: 20px; height: 540px"
            row-key="id"
            border
            default-expand-all
        >
            <el-table-column label="订单信息">
                <el-table-column prop="orderRId" label="订单编号" sortable />
                <el-table-column prop="factoryId" label="工厂鞋型编号" sortable />
                <el-table-column prop="customerId" label="客户鞋型编号" sortable />
                <el-table-column prop="logisticsStatus" label="当前材料物流状态" sortable />
                <el-table-column prop="projectStatus" label="生产状态" sortable />
                <el-table-column prop="shippingStatus" label="发货状态" sortable />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button
                            link
                            type="primary"
                            size="small"
                            @click="edit('edit', scope.row.orderRId, 'add', scope.row)"
                        >
                            订单详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table-column>
        </el-table>
        <el-row :gutter="20" style="justify-content: end">
            <el-col :span="7" :offset="8">
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

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import useTablePagination from '../../hooks/useTablePagination';
import { Download } from '@element-plus/icons-vue';

const edit = defineEmits(['edit']);

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
} = useTablePagination()

onMounted(() => {
    currentTableData.value = [
        {
            orderRId: '10100000000000000',
            customerName: 'ssssss',
            orderTotalShoes: '',
            finishedShoes: '',
            startDate: '',
            endDate: '',
            orderEndDate: ''
        }
    ]
    getTableData('', routeMsg)
})
</script>

<style scoped>
.content {
    height: calc(100% - 40px);
    width: calc(100% - 40px);
}
</style>
