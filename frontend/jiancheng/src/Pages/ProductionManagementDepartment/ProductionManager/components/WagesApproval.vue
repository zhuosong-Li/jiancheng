<template>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">工价审批</el-col>
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
    <el-col :span="4" :offset="4">
      <span style="white-space: nowrap"
        >工段筛选：
        <el-select
          v-model="departmentSearch"
          value-key=""
          placeholder=""
          clearable
          filterable
          @change="orderTableFilter"
        >
          <el-option
            v-for="item in [
              '裁断',
              '批皮',
              '针车预备',
              '针车',
              '成型'
            ]"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </span>
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0">
      <el-table :data="orderTableFilterData" border stripe>
        <el-table-column prop="orderId" label="订单号"></el-table-column>
        <el-table-column prop="inheritId" label="鞋型号"></el-table-column>
        <el-table-column prop="customerTypeId" label="客户型号"></el-table-column>
        <el-table-column prop="department" label="需审批工段"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="openWageApproval(scope.row)"
              >打开工价审批页面</el-button
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
      orderIdSearch:'',
      inheritIdSearch:'',
      departmentSearch:'',
      orderTableFilterData: [],
      orderTableData: [
        {
          orderId: 'k24-2111620',
          inheritId: '0E21160',
          customerTypeId: 'VRA-0015',
          department: '裁断'
        }
      ]

    }
  },
  mounted() {
    this.orderTableFilterData = this.orderTableData
  },
  methods: {
    openWageApproval(row) {
      const orderId = row.orderId
      const orderShoeId = row.inheritId
      const url = `${window.location.origin}/productionmanager/productionwageapproval/orderid=${orderId}&ordershoeid=${orderShoeId}`
      window.open(url, '_blank')
    }
  }
}
</script>
