<template>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
      >生产节点管理</el-col
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
    <el-col :span="4" :offset="4">
      <span style="white-space: nowrap"
        >状态点查询：
        <el-select
          v-model="statusPointSearch"
          value-key=""
          placeholder=""
          clearable
          filterable
          @change="orderTableFilter"
        >
          <el-option
            v-for="item in [
              '生产开始',
              '裁断批皮完成',
              '针车预备完成',
              '针车完成',
              '成型完成',
              '生产完成'
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
        <el-table-column prop="statusPoint" label="需确认状态点"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="isProductionConfirmVis = true"
              >确认状态完成</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
  <el-dialog title="生产节点状态确认" v-model="isProductionConfirmVis" width="80%">
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        <el-descriptions title="鞋型信息" border column="2">
          <el-descriptions-item label="订单号"></el-descriptions-item>
          <el-descriptions-item label="鞋型号"></el-descriptions-item>
          <el-descriptions-item label="客户型号"></el-descriptions-item>
          <el-descriptions-item label="目前工段"></el-descriptions-item>
        </el-descriptions>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        鞋型配码信息
        <el-table :data="shoeInfo" border stripe :max-height="200">
          <el-table-column prop="color" label="颜色"></el-table-column>
          <el-table-column prop="shoeSize" label="配码编号"></el-table-column>
          <el-table-column prop="pairAmount" label="双数"></el-table-column>
          <el-table-column prop="finishedAmount" label="完成数"></el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="success" @click="confirmNode">确认推进流程</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script>
import { ElMessage, ElMessageBox } from 'element-plus'
export default {
  data() {
    return {
      isProductionConfirmVis: false,
      orderIdSearch: '',
      inheritIdSearch: '',
      statusPointSearch: '',
      orderTableFilterData: [],
      orderTableData: [
        {
          orderId: 'K24-211620',
          inheritId: '0E222222',
          statusPoint: '裁断批皮完成'
        }
      ]
    }
  },
  mounted() {
    this.orderTableFilterData = this.orderTableData
  },
  methods: {
    confirmNode() {
      ElMessageBox.alert('请再次确认推进流程，此操作不可撤回！', '警告', {
        confirmButtonText: '确认',
        showCancelButton: true,
        cancelButtonText: '取消'
      })
    },
    orderTableFilter() {
      if (!this.statusPointSearch) {
        this.orderTableFilterData = this.orderTableData
        return
      }
      this.orderTableFilterData = this.orderTableData.filter((order) => {
        const statusMatch = order.statusPoint.includes(this.statusPointSearch)
        return statusMatch
      })
    }
  }
}
</script>
