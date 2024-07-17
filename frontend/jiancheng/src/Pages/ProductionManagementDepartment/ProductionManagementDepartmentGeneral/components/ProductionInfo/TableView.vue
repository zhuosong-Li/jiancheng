<template>
  <div>
    <el-table
      :data="inproductiontableData"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
      default-expand-all
    >
      <el-table-column label="生产中订单">
        <el-table-column prop="customerId" label="客人编号" sortable />
        <el-table-column prop="productionstartDate" label="生产开始日期" sortable />
        <el-table-column prop="totalQuantity" label="订单总数量" sortable />
        <el-table-column prop="prodStatus" label="生产状态" sortable />
        <el-table-column prop="remainingQuantity" label="剩余数量" sortable />
        <el-table-column prop="estimatedproductionDate" label="预计完成时间" sortable />
        <el-table-column prop="deliverDate" label="截止日期" sortable />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="openNewWindow(scope.row)">
              订单详情
            </el-button>
          </template>
          <!-- <el-table-column prop="cuttingStatus" label="裁断" sortable/>
        <el-table-column prop="sewingStatus" label="针车" sortable/>
        <el-table-column prop="moldingStatus" label="成型" sortable/> -->
        </el-table-column>
      </el-table-column>
    </el-table>

    <el-table
      :data="preproductiontableData"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
      default-expand-all
    >
      <el-table-column label="待排产订单">
        <el-table-column prop="customerId" label="客人编号" sortable />
        <el-table-column prop="productionstartDate" label="开始日期" sortable />
        <el-table-column prop="totalQuantity" label="订单总数量" sortable />
        <el-table-column prop="deliverDate" label="截止日期" sortable />
        <el-table-column label="操作" sortable>
          <template #default>
            <el-button link type="primary" size="small" @click="isShoeScheduleVis = true">
              排产
            </el-button>
          </template>
        </el-table-column>
        <!-- <el-table-column prop="cuttingStatus" label="裁断" sortable/>
        <el-table-column prop="sewingStatus" label="针车" sortable/>
        <el-table-column prop="moldingStatus" label="成型" sortable/> -->
      </el-table-column>
    </el-table>
  </div>

  <el-dialog title="订单号 K24-2111620 鞋型排产详情" v-model="isShoeScheduleVis" width="90%">
    <span>
      <el-table :data="shoeProcess" border stripe>
        <el-table-column type="expand">
          <template #default="scope">
            <el-descriptions title="" column="2">
              <el-descriptions-item label="裁断完成情况">{{
                scope.row.details.cutStatus
              }}</el-descriptions-item>
              <el-descriptions-item label="裁断完成数量">{{
                scope.row.details.cutAmount
              }}</el-descriptions-item>
              <el-descriptions-item label="针车预备完成情况">{{
                scope.row.details.sewPreStatus
              }}</el-descriptions-item>
              <el-descriptions-item label="针车预备完成数量">{{
                scope.row.details.sewPreAmount
              }}</el-descriptions-item>
              <el-descriptions-item label="针车完成情况">{{
                scope.row.details.sewStatus
              }}</el-descriptions-item>
              <el-descriptions-item label="针车完成数量">{{
                scope.row.details.sewAmount
              }}</el-descriptions-item>
              <el-descriptions-item label="成型完成情况">{{
                scope.row.details.moldStatus
              }}</el-descriptions-item>
              <el-descriptions-item label="成型完成数量">{{
                scope.row.details.moldAmount
              }}</el-descriptions-item>
            </el-descriptions>
          </template>
        </el-table-column>
        <el-table-column prop="inheritId" label="工厂型号"> </el-table-column>
        <el-table-column prop="customerTypeId" label="客户型号"> </el-table-column>
        <el-table-column prop="remainAmount" label="数量"> </el-table-column>
        <el-table-column prop="cutLine" label="裁断线号"> </el-table-column>
        <el-table-column prop="cutDatePeriod" label="裁断周期"> </el-table-column>
        <el-table-column prop="sewPreLine" label="针车预备线号"> </el-table-column>
        <el-table-column prop="sewPreDatePeriod" label="针车预备周期"> </el-table-column>
        <el-table-column prop="sewLine" label="针车线号"> </el-table-column>
        <el-table-column prop="sewDatePeriod" label="针车周期"> </el-table-column>
        <el-table-column prop="moldLine" label="成型线号"> </el-table-column>
        <el-table-column prop="moldDatePeriod" label="成型周期"> </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="isScheduleModify = true"
              >修改排期</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </span>
    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="primary" @click="">确认</el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog title="修改排产信息" v-model="isScheduleModify" width="60%">
    <el-tabs v-model="activeTab" type="card" tab-position="top" @tab-click="">
      <el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name">
        <el-row :gutter="20">
          <el-col :span="10" :offset="0">
            <span style="white-space: nowrap">
              {{ tab.lineLabel }}：
              <el-select v-model="tab.lineValue" placeholder="" clearable filterable @change="">
                <el-option
                  v-for="item in cuttingLineOption"
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
          <el-col :span="10" :offset="0">
            <span>
              {{ tab.dateLabel }}：
              <el-date-picker
                v-model="tab.dateValue"
                type="daterange"
                size="normal"
                range-separator="-"
                start-placeholder=""
                end-placeholder=""
              >
              </el-date-picker>
            </span>
          </el-col>
          <el-col :span="12" :offset="0"
            >预计每天生产数量：{{ calculateDailyProduction(tab.dateValue) }}</el-col
          >
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24" :offset="0">
            <el-table :data="dateStatusTable" border stripe>
              <el-table-column type="expand">
                <template #default="props">
                  <el-table :data="props.row.shoeList" :border="childBorder">
                    <el-table-column type="index" />
                    <el-table-column label="订单号" prop="orderId" />
                    <el-table-column label="工厂型号" prop="shoeId" />
                    <el-table-column label="鞋型总数量" prop="amount" />
                    <el-table-column label="生产周期" prop="datePeriod" />
                    <el-table-column label="平均每天数量" prop="averageAmount" />
                  </el-table>
                </template>
              </el-table-column>

              <el-table-column prop="date" label="日期"> </el-table-column>
              <el-table-column prop="productAmount" label="已排产鞋型数"> </el-table-column>
              <el-table-column prop="predictAmount" label="预计当日现有生产量"> </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>

    <span> </span>
    <template #footer>
      <span>
        <el-button @click="">取消</el-button>
        <el-button type="primary" @click="">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script>
export default {
  data() {
    return {
      activeTab: '裁断排产',
      cuttingLine: 1,
      cuttingDatePicker: '',
      sewPreLine: 1,
      sewPreDatePicker: '',
      dialogOrderSearch: '',
      isShoeScheduleVis: false,
      isScheduleVis: false,
      isScheduleModify: false,
      lineType: '0',
      linenum: '',
      inproductiontableData: [
        {
          customerId: 'K24-014客人37 XTI 2111620',
          productionstartDate: '2024-02-27',
          prodStatus: '已排产',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-05-05',
          totalQuantity: 720,
          remainingQuantity: '720'
        },
        {
          customerId: 'K24-015 客人37XTI 2111622',
          productionstartDate: '2024-06-10',
          prodStatus: '已排产',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-04-20',
          totalQuantity: 2340,
          remainingQuantity: '2340'
        },
        {
          customerId: 'K24-016客人37 XTI 2111623',
          productionstartDate: '2024-06-10',
          prodStatus: '已排产',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-04-20',
          totalQuantity: 3364,
          remainingQuantity: '3364'
        },
        {
          customerId: 'K24-017客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '已排产',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-07-10',
          totalQuantity: 6900,
          remainingQuantity: '6900'
        },
        {
          customerId: 'K24-020客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '已排产',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-05-05',
          totalQuantity: 26620,
          remainingQuantity: '26620'
        },
        {
          customerId: 'K24-019客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '生产中',
          estimatedproductionDate: '2024-04-20',
          deliverDate: '2024-05-05',
          totalQuantity: 13296,
          remainingQuantity: '9042'
        }
      ],
      preproductiontableData: [
        {
          customerId: 'K24-018客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '针车中',
          deliverDate: '2024-07-10',
          totalQuantity: '10094',
          remainingQuantity: '500'
        },

        {
          customerId: 'K24-021客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '针车中',
          deliverDate: '2024-07-10',
          totalQuantity: '64600',
          remainingQuantity: '500'
        },
        {
          customerId: 'K24-022客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '针车中',
          deliverDate: '2024-07-10',
          totalQuantity: '3000',
          remainingQuantity: '500'
        },
        {
          customerId: 'K24-023客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '针车中',
          deliverDate: '2024-07-10',
          totalQuantity: '4320',
          remainingQuantity: '500'
        },
        {
          customerId: 'K24-024客人37 XTI 2111620',
          productionstartDate: '2024-06-10',
          prodStatus: '针车中',
          deliverDate: '2024-07-10',
          totalQuantity: '4800',
          remainingQuantity: '500'
        },
        {
          customerId: 'K24 客人37 2111620',
          productionstartDate: '2024-02-25',
          prodStatus: '针车中',
          deliverDate: '2024-04-20',
          totalQuantity: '2000',
          remainingQuantity: '500'
        }
      ],
      shoeProcess: [
        {
          inheritId: '0E26210',
          customerTypeId: 'VRA-015',
          logisticsStatus: 0,
          remainAmount: 5000,
          cutLine: 1,
          cutDatePeriod: '2024-07-09 至 2024-08-16',
          sewPreLine: 1,
          sewPreDatePeriod: '2024-07-09 至 2024-08-16',
          sewLine: 2,
          sewDatePeriod: '2024-07-09 至 2024-08-16',
          moldLine: 4,
          moldDatePeriod: '2024-07-09 至 2024-08-16',
          details: {
            cutStatus: '未完成',
            cutAmount: '1000/5000',
            sewPreStatus: '未完成',
            sewPreAmount: '1000/5000',
            sewStatus: '未完成',
            sewAmount: '1000/5000',
            moldStatus: '未完成',
            moldAmount: '1000/5000'
          }
        }
      ],
      cuttingLineOption: [1, 2, 3, 4],
      tabs: [
        {
          name: '裁断排产',
          label: '裁断排产',
          lineLabel: '裁断线号选择',
          dateLabel: '裁断工期选择',
          lineValue: null,
          dateValue: null
        },
        {
          name: '针车预备排产',
          label: '针车预备排产',
          lineLabel: '针车线号选择',
          dateLabel: '针车工期选择',
          lineValue: null,
          dateValue: null
        },
        {
          name: '针车排产',
          label: '针车排产',
          lineLabel: '针车线号选择',
          dateLabel: '针车工期选择',
          lineValue: null,
          dateValue: null
        },
        {
          name: '成型排产',
          label: '成型排产',
          lineLabel: '成型线号选择',
          dateLabel: '成型工期选择',
          lineValue: null,
          dateValue: null
        }
      ],
      dateStatusTable: [
        {
          date: '2024-07-16',
          productAmount: 10,
          predictAmount: 2000,
          shoeList: [{
            orderId: 'K24-2111620',
            shoeId: '0E11150',
            amount: 300,
            datePeriod: "2024-07-16 至 2024-07-20",
            averageAmount: 75
          }]
        }
      ]
    }
  },
  methods: {
    openNewWindow(rowkey) {
      let url = ''
      const orderId = rowkey.customerId.replace(' ', '-')
      url = `${window.location.origin}/productiongeneral/productiondetail/customerid=${orderId}`
      window.open(url, '_blank')
    },
    calculateDailyProduction(dateRange) {
      if (dateRange && dateRange.length === 2) {
        const startDate = new Date(dateRange[0]);
        const endDate = new Date(dateRange[1]);
        const timeDiff = Math.abs(endDate - startDate);
        const diffDays = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
        return (5000 / diffDays).toFixed(2);
      }
      return 0;
    },
  }
}
</script>
