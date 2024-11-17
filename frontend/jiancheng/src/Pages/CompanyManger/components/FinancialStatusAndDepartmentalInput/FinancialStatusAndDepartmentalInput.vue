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
                <el-table-column prop="factoryId" label="工厂鞋型编号" sortable />
                <el-table-column prop="customerId" label="客户鞋型编号" sortable />
              <el-table-column prop="saleStatus" label="鞋型售价填写状态" />
              <el-table-column prop="materialStatus" label="材料入库状态" />
              <el-table-column prop="cutFillStatus" label="裁断价格填写状态" />
              <el-table-column prop="needleCarStatus" label="针车价格填写状态" />
              <el-table-column prop="formFillStatus" label="成型价格填写状态" />
              <el-table-column prop="abnormalStatus" label="异常状态说明" />
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
    currentTableData.value = [
        {
            orderRId: '10000000000000001',
            shoesModel: 'ssssss',
            saleStatus: '',
            laborPriceStatus: '',
            materialStatus: '',
            abnormalStatus: ''
        }
    ];
    getTableData('', routeMsg);
});

</script>

<style scoped>
.content {
  height: calc(100% - 40px);
}
</style>
