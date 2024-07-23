<template>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
      >每日生产数量确认</el-col
    >
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
      当前日期为 {{ currentDate() }}, 表格填报情况为 {{ daysBefore(1) }} 的生产数量
    </el-col>
  </el-row>

  <el-row :gutter="20">
    <el-col :span="24" :offset="0">
      <el-table :data="orderTableFilterData" border stripe :cell-style="cellStyle">
        <el-table-column prop="orderId" label="订单号"></el-table-column>
        <el-table-column prop="inheritId" label="鞋型号"></el-table-column>
        <el-table-column prop="customerTypeId" label="客户型号"></el-table-column>
        <el-table-column prop="cuttingAmount" label="昨日裁断数量上报"></el-table-column>
        <el-table-column prop="sewingAmount" label="昨日针车数量上报"></el-table-column>
        <el-table-column prop="moldAmount" label="昨日成型数量上报"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="openAmountApproval(scope.row)"
              >打开生产数量审批页面</el-button
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
      orderTableFilterData: [],
      orderTableData: [
        {
          orderId: 'k24-2111620',
          inheritId: '0E21160',
          customerTypeId: 'VRA-0015',
          cuttingAmount: 400,
          isCuttingApproval: false,
          isSewingApproval: true,
          isMoldApproval: false,
          sewingAmount: 500,
          moldAmount: null
        }
      ]
    }
  },
  mounted() {
    this.orderTableFilterData = this.orderTableData
  },
  methods: {
    cellStyle(cell) {
      console.log(cell.row)
      console.log(cell.column)
      if (cell.row.isCuttingApproval == false && cell.column.label === '昨日裁断数量上报') {
        return { color: 'red' }
      }
      if (cell.row.isSewingApproval == false && cell.column.label === '昨日针车数量上报') {
        return { color: 'red' }
      }
      if (cell.row.isMoldApproval == false && cell.column.label === '昨日成型数量上报') {
        return { color: 'red' }
      }
    },
    currentDate() {
      const date = new Date()
      return date.toDateString()
    },
    daysBefore(num) {
      const date = new Date()
      const returnDate = new Date()
      returnDate.setDate(date.getDate() - num)
      return returnDate.toDateString()
    },
    orderTableFilter() {
      if (!this.orderIdSearch && this.inheritIdSearch) {
        this.orderTableFilterData = this.orderTableData
        return
      }
      this.orderTableFilterData = this.orderTableData.filter((order) => {
        const orderMatch = order.orderId.includes(this.orderIdSearch)
        const inheritMatch = order.inheritId.includes(this.inheritIdSearch)
        return orderMatch && inheritMatch
      })
    },
    openAmountApproval(row) {
      const orderId = row.orderId
      const orderShoeId = row.inheritId
      const url = `${window.location.origin}/productiongeneral/productionamountapproval/orderid=${orderId}&ordershoeid=${orderShoeId}`
      window.open(url, '_blank')
    }
  }
}
</script>
