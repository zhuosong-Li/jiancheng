<template>
  <el-container>
    <el-header height="">
      <AllHeader></AllHeader>
    </el-header>
    <el-main height="">
      <el-row :gutter="20" style="text-align: center">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
          >订单鞋型工价审批页面</el-col
        >
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24" :offset="0"
          ><el-descriptions title="订单信息" border column="2">
            <el-descriptions-item label="订单号">K24-2111620</el-descriptions-item>
            <el-descriptions-item label="鞋型号">0E21922</el-descriptions-item>
            <el-descriptions-item label="客户号">37号客人</el-descriptions-item>
            <el-descriptions-item label="出货日期">2024-07-19</el-descriptions-item>
          </el-descriptions></el-col
        >
      </el-row>
      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
          鞋型配码信息
          <el-table :data="shoeInfo" border stripe :max-height="200">
            <el-table-column prop="color" label="颜色"></el-table-column>
            <el-table-column prop="shoeSize" label="配码编号"></el-table-column>
            <el-table-column prop="size35" label="35"></el-table-column>
            <el-table-column prop="size36" label="36"></el-table-column>
            <el-table-column prop="size37" label="37"></el-table-column>
            <el-table-column prop="size38" label="38"></el-table-column>
            <el-table-column prop="size39" label="39"></el-table-column>
            <el-table-column prop="size40" label="40"></el-table-column>
            <el-table-column prop="size41" label="41"></el-table-column>
            <el-table-column prop="pairAmount" label="双数"></el-table-column>
            <el-table-column prop="totalAmount" label="总数"></el-table-column>
          </el-table>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24" :offset="0">
          待审批工价
          <el-table :data="wagesInfo" border stripe>
            <el-table-column prop="departmentType" label="工段类型"></el-table-column>
            <el-table-column prop="period" label="生产周期"></el-table-column>
            <el-table-column prop="shipDate" label="发货日期"></el-table-column>
            <el-table-column label="操作">
              <el-button type="primary" size="default" @click="isWagesApprovalVis = true"
                >查看并审核该工价</el-button
              >
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
  <el-dialog title="工价审核界面" v-model="isWagesApprovalVis" width="80%">
    <el-table :data="wageInfo" border stripe max-height="500">
      <el-table-column type="index" label="序号"></el-table-column>
      <el-table-column prop="processName" label="工序名称"></el-table-column>
      <el-table-column prop="wage" label="工价"></el-table-column>
      <el-table-column prop="remark" label="备注"></el-table-column>
      
    </el-table>

    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="danger" @click="openRefuseApprovalDialog">驳回请求</el-button>
        <el-button type="primary" @click="">审批通过</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog title="驳回审批请求" v-model="isRefuseApprovalVis" width="30%">
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        请填写驳回原因（不超过20字）：
        <el-input
          v-model="refuseReason"
          type="textarea"
          placeholder=""
          size="normal"
          resize="none"
          clearable
          @change=""
        ></el-input>
      </el-col>
    </el-row>

    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="success" @click="">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script>
import AllHeader from '@/components/AllHeader.vue'
export default {
  components: {
    AllHeader
  },
  data() {
    return {
      refuseReason: '',
      isRefuseApprovalVis: false,
      wageInfo: [
        {
          processName: '裁断1',
          wage: 0.5
        },
        {
          processName: '裁断2',
          wage: 0.5
        }
      ],
      shoeInfo: [
        {
          color: '黑色',
          shoeSize: 'S12A',
          size35: 0,
          size36: 64,
          size37: 128,
          size38: 192,
          size39: 192,
          size40: 128,
          size41: 64,
          pairAmount: 768,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S12B',
          size35: 14,
          size36: 28,
          size37: 42,
          size38: 42,
          size39: 28,
          size40: 14,
          size41: 0,
          pairAmount: 168,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S6A1',
          size35: 0,
          size36: 14,
          size37: 14,
          size38: 14,
          size39: 14,
          size40: 14,
          size41: 6,
          pairAmount: 84,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S6A2',
          size35: 0,
          size36: 10,
          size37: 20,
          size38: 20,
          size39: 10,
          size40: 0,
          size41: 6,
          pairAmount: 60,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S6B1',
          size35: 2,
          size36: 2,
          size37: 2,
          size38: 2,
          size39: 2,
          size40: 2,
          size41: 0,
          pairAmount: 12,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S6B2',
          size35: 0,
          size36: 6,
          size37: 12,
          size38: 12,
          size39: 6,
          size40: 0,
          size41: 6,
          pairAmount: 36,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S8A1',
          size35: 0,
          size36: 48,
          size37: 48,
          size38: 96,
          size39: 96,
          size40: 48,
          size41: 48,
          pairAmount: 384,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S8A2',
          size35: 0,
          size36: 10,
          size37: 10,
          size38: 10,
          size39: 10,
          size40: 0,
          size41: 8,
          pairAmount: 40,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S8A3',
          size35: 0,
          size36: 13,
          size37: 26,
          size38: 26,
          size39: 26,
          size40: 13,
          size41: 8,
          pairAmount: 104,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S8B1',
          size35: 11,
          size36: 11,
          size37: 22,
          size38: 22,
          size39: 11,
          size40: 11,
          size41: 0,
          pairAmount: 88,
          totalAmount: 1800
        },
        {
          color: '黑色',
          shoeSize: 'S8B2',
          size35: 0,
          size36: 14,
          size37: 14,
          size38: 14,
          size39: 14,
          size40: 0,
          size41: 8,
          pairAmount: 56,
          totalAmount: 1800
        }
      ],
      wagesInfo: [
        {
          departmentType: '裁断',
          period: '2024-07-20-2024-07-26',
          shipDate: '2024-07-24'
        },
        {
          departmentType: '针车',
          period: null,
          shipDate: '2024-07-24'
        }
      ],
      isWagesApprovalVis: false
    }
  },
  methods: {
    openRefuseApprovalDialog() {
      this.isRefuseApprovalVis = true
    }
  }
}
</script>
