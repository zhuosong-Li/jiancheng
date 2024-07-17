<template>
  <el-row :gutter="20">
    <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
      >物流信息一览</el-col
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
          @change=""
        ></el-input>
      </span>
    </el-col>
    <el-col :span="4" :offset="2">
      <span style="white-space: nowrap"
        >客人查询：<el-input
          v-model="customerSearch"
          placeholder=""
          size="normal"
          clearable
          @change=""
        ></el-input>
      </span>
    </el-col>
  </el-row>
  <el-row :gutter="20" style="margin-top: 20px">
    <el-col :span="24" :offset="0">
      <el-table :data="logisticsOrderData" border stripe>
        <el-table-column prop="orderId" label="订单号"></el-table-column>
        <el-table-column prop="customerId" label="客人名称"></el-table-column>
        <el-table-column prop="shipDate" label="出货日期"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="isShoeLogisticVis = true"
              >查看订单物流信息</el-button
            >
          </template>
        </el-table-column>
      </el-table></el-col
    >
  </el-row>

  <el-dialog title="订单 K24-2111620 鞋型物流信息一览" v-model="isShoeLogisticVis" width="90%">
    <el-table :data="logisticsShoeData" border stripe>
      <el-table-column prop="inheritId" label="工厂型号"></el-table-column>
      <el-table-column prop="customerTypeId" label="客户型号"></el-table-column>
      <el-table-column
        prop="fabricStatus"
        label="面料辅料状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column
        prop="smallPartsStatus"
        label="扣件拉链鞋带等小件状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column
        prop="soleStatus"
        label="鞋底状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column
        prop="insoleStatus"
        label="中底状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column
        prop="lastStatus"
        label="楦型状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column
        prop="packingStatus"
        label="包材状态"
        :formatter="statusFormatter"
      ></el-table-column>
      <el-table-column label="详细信息">
        <template #default="scope">
          <el-button type="primary" size="default" @click="isMaterialLogisticVis = true">查看所有材料信息</el-button>
        </template>
      </el-table-column>
    </el-table>

    <template #footer>
      <span>
        <el-button @click="">Cancel</el-button>
        <el-button type="primary" @click="">OK</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog
    title="鞋型所有材料物流信息"
    v-model="isMaterialLogisticVis"
    width="80%">
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        <el-table :data="logisticsMaterialData" border stripe>
          <el-table-column prop="partName" label="部件名称"></el-table-column>
          <el-table-column prop="materialName" label="材料名称"></el-table-column>
          <el-table-column prop="color" label="颜色"></el-table-column>
          <el-table-column prop="approvedUsage" label="核定用量"></el-table-column>
          <el-table-column prop="purchaseAmount" label="采购数量"></el-table-column>
          <el-table-column prop="factoryName" label="供应商名称"></el-table-column>
          <el-table-column prop="materialType" label="材料类型"></el-table-column>
          <el-table-column prop="materialStatus" label="材料状态"></el-table-column>
          
        </el-table>
        
      </el-col>
    </el-row>
    
    <template #footer>
    <span>
      <el-button @click="">Cancel</el-button>
      <el-button type="primary" @click="">OK</el-button>
    </span>
    </template>
  </el-dialog>
  
</template>

<script>
export default {
  data() {
    return {
      isMaterialLogisticVis: false,
      isShoeLogisticVis: false,
      orderIdSearch: '',
      statusFilter: '',
      customerSearch: '',
      logisticsShoeData: [
        {
          inheritId: '0E229940',
          customerTypeId: 'VRA-0015',
          fabricStatus: 0,
          smallPartsStatus: 0,
          soleStatus: 0,
          insoleStatus: 0,
          lastStatus: 0,
          packingStatus: 0
        }
      ],
      logisticsOrderData: [
        {
          orderId: 'K24-2111620',
          customerId: '客人37',
          shipDate: '2024-07-26'
        }
      ],
      logisticsMaterialData: [
        {
          partName: "鞋面",
          materialName: "黑色PU",
          color: "黑色",
          approvedUsage: 500,
          purchaseAmount: 550,
          factoryName: "一一鞋材",
          materialStatus:"未到货",
          materialType:"面料辅料"
        }
      ]
    }
  },
  methods: {
    statusFormatter(row, column, cellValue, index) {
      let returnValue = ''
      switch (cellValue) {
        case 0:
          returnValue = '未订购'
          break
        case 1:
          returnValue = '已订购'
          break
        case 2:
          returnValue = '已到货'
          break
      }
      console.log(returnValue)
      return returnValue
    }
  }
}
</script>
