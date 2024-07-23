<template>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">外包审批</el-col>
  </el-row>
  <el-row :gutter="20" style="margin-top: 20px">
    <el-col :span="4" :offset="0">
      <span style="white-space: nowrap"
        >订单号查询：<el-input
          v-model="orderIdSearch"
          placeholder=""
          size="normal"
          clearable
          @input="orderTableFilter"
        ></el-input>
      </span>
    </el-col>
    <el-col :span="4" :offset="4">
      <span style="white-space: nowrap"
        >工厂鞋型查询：<el-input
          v-model="inheritIdSearch"
          placeholder=""
          size="normal"
          clearable
          @input="orderTableFilter"
        ></el-input>
      </span>
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0">
      <el-table :data="orderTableFilterData" border stripe>
        <el-table-column prop="orderId" label="订单号"></el-table-column>
        <el-table-column prop="inheritId" label="鞋型号"></el-table-column>
        <el-table-column prop="customerTypeId" label="客户型号"></el-table-column>
        <el-table-column prop="isCuttingOutSourced" label="裁断申请"></el-table-column>
        <el-table-column prop="isSewingOutSourced" label="针车申请"></el-table-column>
        <el-table-column prop="isMoldOutSourced" label="成型申请"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="openOutSourcePage(scope.row)"
              >打开鞋型外包页面</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<script>
export default {
  data() {
    return {
      orderIdSearch: '',
      inheritIdSearch: '',
      orderTableData: [
        {
          orderId: 'k24-2111620',
          inheritId: '0E21160',
          customerTypeId: 'VRA-0015',
          isCuttingOutSourced: '是',
          isSewingOutSourced: '否',
          isMoldOutSourced: '否'
        }
      ],
      orderTableFilterData: []
    }
  },
  mounted() {
    this.orderTableFilterData = this.orderTableData
  },
  methods: {
    openOutSourcePage(row) {
      const orderId = row.orderId
      const orderShoeId = row.inheritId
      const url = `${window.location.origin}/productionmanager/productionoutsource/orderid=${orderId}&ordershoeid=${orderShoeId}`
      window.open(url, '_blank')
    }
  }
}
</script>
