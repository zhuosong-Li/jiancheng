<template>
  <el-container>
    <el-header height="">
      <AllHeader></AllHeader>
    </el-header>
    <el-main height="">
      <el-row :gutter="20" style="text-align: center">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
          >订单鞋型外包页面</el-col
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
          现有外包流程
          <el-table :data="outSourceInfo" border stripe>
            <el-table-column prop="outSourceType" label="外包类型"></el-table-column>
            <el-table-column prop="outSourceFactory" label="外包厂家"></el-table-column>
            <el-table-column prop="outSourceAmount" label="外包数量"></el-table-column>
            <el-table-column prop="outSourcePeriod" label="外包周期"></el-table-column>
            <el-table-column label="仓库材料发货情况">
              <template #default="scope">
                <el-button type="primary" size="default" @click="isOutSourceLogistic = true"
                  >查看外包物料发货情况</el-button
                >
              </template>
            </el-table-column>
            <el-table-column prop="shipDate" label="最迟交货日期"></el-table-column>
            <el-table-column label="操作">
              <el-button type="primary" size="default" @click="isOutSouceCreateVis = true"
                >编辑</el-button
              >
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6" :offset="0">
          <el-button type="primary" size="default" @click="isOutSouceCreateVis = true"
            >新建外包流程</el-button
          >
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="24" :offset="0"> </el-col>
      </el-row>
    </el-main>
  </el-container>
  <el-dialog title="外包流程新建/修改" v-model="isOutSouceCreateVis" width="80%">
    <el-row :gutter="20">
      <el-col :span="6" :offset="0">
        外包类型：
        <el-select v-model="addOutSource.outSourceType" placeholder="" clearable filterable>
          <el-option
            v-for="item in ['裁断', '针车', '成型', '裁断+针车', '全部外包']"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="6" :offset="0">
        外包工厂选择：
        <el-select v-model="addOutSource.outSourceFactory" placeholder="" clearable filterable>
          <el-option v-for="item in factoryOptions" :key="item" :label="item" :value="item">
          </el-option>
        </el-select>
      </el-col>
      <el-col :span="6" :offset="0">
        外包周期选择：
        <el-date-picker
          v-model="addOutSource.outSourcePeriod"
          type="daterange"
          size="normal"
          range-separator="-"
          start-placeholder=""
          end-placeholder=""
        >
        </el-date-picker>
      </el-col>
      <el-col :span="4" :offset="0">
        最迟交货日期选择：
        <el-date-picker
          v-model="addOutSource.shipDate"
          type="day"
          size="normal"
          placeholder="选择日期时间"
        >
        </el-date-picker>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="4" :offset="0">
        <el-checkbox v-model="addOutSource.isTransitNeed" label="是否需要外发半成品" :indeterminate="false" @change="">是否需要外发半成品</el-checkbox>
      </el-col>
      <el-col :span="8" :offset="2">
        半成品最迟发货日期：
        <el-date-picker
          v-model="addOutSource.outSourceTransitShipDate"
          type="day"
          size="normal"
          placeholder="选择日期时间"
          :disabled="!addOutSource.isTransitNeed"
        >
        </el-date-picker>
      </el-col>
      <el-col :span="8" :offset="0">
        材料最迟发货日期：
        <el-date-picker
          v-model="addOutSource.outSpirceMaterialShipDate"
          type="day"
          size="normal"
          placeholder="选择日期时间"
        >
        </el-date-picker>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        <el-table :data="materialSelectData" border stripe>
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="partName" label="部件名称" />
          <el-table-column prop="color" label="颜色" />
          <el-table-column prop="materialName" label="材料名称" />
          <el-table-column prop="unit" label="单位" />
          <el-table-column prop="shipAmount" label="应发货数量" />
          <el-table-column prop="status" label="状态" />
          <el-table-column prop="section" label="使用工段" />
          <el-table-column prop="date" label="到货日期" />
        </el-table>
      </el-col>
    </el-row>

    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="primary" @click="isOutSourcePreviewVis = true">预览</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog title="预览外发信息" v-model="isOutSourcePreviewVis" width="80%">
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        <el-descriptions title="外包信息一览">
          <el-descriptions-item label="外包类型">{{
            outSourceFinData.outSourceType
          }}</el-descriptions-item>
          <el-descriptions-item label="外包工厂">{{
            outSourceFinData.outSourceFactory
          }}</el-descriptions-item>
          <el-descriptions-item label="外包周期">{{
            outSourceFinData.outSourcePeriod
          }}</el-descriptions-item>
          <el-descriptions-item label="最迟交货日期">{{
            outSourceFinData.shipDate
          }}</el-descriptions-item>
          <el-descriptions-item label="半成品最迟发货日期">{{
            outSourceFinData.outSourceTransitShipDate
          }}</el-descriptions-item>
          <el-descriptions-item label="材料最迟发货日期">{{
            outSourceFinData.outSpirceMaterialShipDate
          }}</el-descriptions-item>
        </el-descriptions>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24" :offset="0">
        <el-table :data="outSourceFinData.materialData" border stripe>
          <el-table-column prop="partName" label="部件名称" />
          <el-table-column prop="color" label="颜色" />
          <el-table-column prop="materialName" label="材料名称" />
          <el-table-column prop="unit" label="单位" />
          <el-table-column prop="shipAmount" label="应发货数量" />
          <el-table-column prop="status" label="状态" />
          <el-table-column prop="section" label="使用工段" />
          <el-table-column prop="date" label="到货日期" />
        </el-table>
      </el-col>
    </el-row>

    <template #footer>
      <span>
        <el-button @click="">Cancel</el-button>
        <el-button type="success" @click="">确认下发</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog title="外包物料发货情况查询" v-model="isOutSourceLogistic" width="80%">
    <el-row :gutter="20">
      <el-col :span="24" :offset="0"> 半成品发货状态： </el-col>
      <el-table :data="transitLogisticData" border stripe>
        <el-table-column prop="inheritId" label="公司型号"></el-table-column>
        <el-table-column prop="shipAmount" label="发货数量"></el-table-column>
        <el-table-column prop="status" label="发货状态"></el-table-column>
        <el-table-column prop="shipDate" label="发货日期"></el-table-column>
        <el-table-column prop="deadDate" label="最迟发货日期"></el-table-column>
      </el-table>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24" :offset="0"> 材料发货状态： </el-col>
      <el-table :data="materialLogisticData" border stripe>
        <el-table-column prop="partName" label="部件名称" />
        <el-table-column prop="color" label="颜色" />
        <el-table-column prop="materialName" label="材料名称" />
        <el-table-column prop="unit" label="单位" />
        <el-table-column prop="shipAmount" label="应发货数量" />
        <el-table-column prop="status" label="发货状态" />
        <el-table-column prop="shipDate" label="发货日期"></el-table-column>
        <el-table-column prop="deadDate" label="最迟发货日期"></el-table-column>
      </el-table>
    </el-row>

    <template #footer>
      <span>
        <el-button type="primary" @click="isOutSourceLogistic = false">确认</el-button>
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
      outSourceFinData: {
        outSourceType: '',
        outSourceFactory: '',
        outSourcePeriod: [],
        outSourceTransitShipDate: '',
        outSpirceMaterialShipDate: '',
        shipDate: '',

        materialData: [
          {
            partName: '鞋面',
            color: '红色',
            materialName: '牛皮',
            unit: '平方米',
            shipAmount: 10,
            status: '未到货',
            date: '2024-07-21'
          }
        ]
      },
      materialSelectData: [
        {
          partName: '鞋面',
          color: '红色',
          materialName: '牛皮',
          unit: '平方米',
          shipAmount: 10,
          status: '未到货',
          date: '2024-07-21'
        },
        {
          partName: '鞋底',
          color: '黑色',
          materialName: '橡胶',
          unit: '千克',
          shipAmount: 20,
          status: '已到货',
          date: '2024-07-20'
        },
        {
          partName: '鞋垫',
          color: '白色',
          materialName: '记忆海绵',
          unit: '平方米',
          shipAmount: 15,
          status: '未到货',
          date: '2024-07-22'
        },
        {
          partName: '鞋带',
          color: '蓝色',
          materialName: '尼龙',
          unit: '米',
          shipAmount: 100,
          status: '未到货',
          date: '2024-07-21'
        },
        {
          partName: '鞋面',
          color: '绿色',
          materialName: '绒面革',
          unit: '平方米',
          shipAmount: 8,
          status: '已到货',
          date: '2024-07-19'
        }
      ],
      addOutSource: {
        outSourceType: '',
        outSourceFactory: '',
        outSourcePeriod: [],
        outSourceAmount: 0,
        outSourceTransitShipDate: '',
        outSpirceMaterialShipDate: '',
        shipDate: '',
        isTransitNeed: false
      },
      isTransitNeed:false,
      isOutSourceLogistic: false,
      isOutSouceCreateVis: false,
      isOutSourcePreviewVis: false,
      factoryOptions: ['XX鞋业', 'YY鞋业', 'ZZ鞋业'],
      transitLogisticData: [
        {
          inheritId: '0E11150',
          shipAmount: 500,
          status: '未发货',
          shipDate: '',
          deadDate: '2024-07-25'
        }
      ],
      materialLogisticData: [
        {
          partName: '鞋面',
          color: '红色',
          materialName: '牛皮',
          unit: '平方米',
          shipAmount: 10,
          status: '已发货',
          shipDate: '2024-07-21',
          deadDate: '2024-07-25'
        }
      ],
      outSourceInfo: [
        {
          outSourceType: '裁断',
          outSourceFactory: 'XX鞋业',
          outSourceAmount: 500,
          outSourcePeriod: '2024-07-05-2024-07-18',
          shipDate: '2024-07-19'
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
      ]
    }
  },
  methods: {}
}
</script>
