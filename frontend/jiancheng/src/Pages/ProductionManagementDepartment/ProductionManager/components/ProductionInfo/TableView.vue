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
  </div>
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
          dateValue: null,
          isOutSource: 0
        },
        {
          name: '针车预备排产',
          label: '针车预备排产',
          lineLabel: '针车线号选择',
          dateLabel: '针车工期选择',
          lineValue: null,
          dateValue: null,
          isOutSource: 1
        },
        {
          name: '针车排产',
          label: '针车排产',
          lineLabel: '针车线号选择',
          dateLabel: '针车工期选择',
          lineValue: null,
          dateValue: null,
          isOutSource: 0
        },
        {
          name: '成型排产',
          label: '成型排产',
          lineLabel: '成型线号选择',
          dateLabel: '成型工期选择',
          lineValue: null,
          dateValue: null,
          isOutSource: 0
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
    startOutSourceFlow() {
      const orderId = "K24-2111620"
      const orderShoeId = "0E255530"
      const url = `${window.location.origin}/productiongeneral/productionoutsource/orderid=${orderId}&ordershoeid=${orderShoeId}`
      window.open(url, '_blank')

    }
  }
}
</script>
