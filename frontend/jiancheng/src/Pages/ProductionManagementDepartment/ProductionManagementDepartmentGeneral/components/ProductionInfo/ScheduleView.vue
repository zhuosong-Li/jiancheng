<template>
  <el-row :gutter="20" style="margin-top: 20px">
    <el-col :span="8" :offset="0">
      <el-radio-group v-model="lineType" size="large">
        <el-radio-button label="裁断" value="0" />
        <el-radio-button label="针车预备" value="1" />
        <el-radio-button label="针车" value="2" />
        <el-radio-button label="成型" value="3" />
      </el-radio-group>
    </el-col>
    <el-col :span="4" :offset="0" style="white-space: nowrap">
      选择生产线：
      <el-select
        v-model="linenum"
        value-key=""
        placeholder=""
        clearable
        filterable
        @change=""
        :disabled="lineType !== '3'"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="4" :offset="8"
      ><el-button type="primary" size="default" @click="isScheduleVis = true">编辑排期</el-button>
    </el-col>
  </el-row>
  <vue-cal
    :disable-views="['years', 'year']"
    locale="zh-cn"
    :time="false"
    :events="events"
    style="height: 550px"
  >
    <template #event="{ event, view }">
      <!-- <el-image :src="event.image" fit="fill" :lazy="true"></el-image> -->

      <div class="vuecal__event-title">订单号： {{ event.title }}</div>
      <div class="vuecal__event-cotent">鞋型号： {{ event.content }}</div>
      <div>数量：{{ event.number }}</div>
      <div>已使用生产线数量： {{ event.lineUsage }}</div>
    </template>
    <template #cell-content="{ cell, view, events, goNarrower }">
      <span class="vuecal__no-event" v-if="['week', 'day'].includes(view.id) && !events.length"
        >没有任务</span
      >
    </template>
  </vue-cal>
  <el-dialog title="排期编辑页面" v-model="isScheduleVis" width="90%">
    <span>
      <el-text>未排产订单</el-text>
      <el-input
        v-model="dialogOrderSearch"
        placeholder=""
        size="normal"
        clearable
        @change=""
      ></el-input>
      <el-table :data="unprocessedOrder" border stripe style="height: 350px">
        <el-table-column prop="orderId" label="订单编号"> </el-table-column>
        <el-table-column prop="createDate" label="订单创建日期"> </el-table-column>
        <el-table-column label="物流状态">
          <template #default="scope">
            <el-button type="primary" size="default" @click="">查看详细状态</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="shipDate" label="订单出货日期"> </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="isShoeScheduleVis = true"
              >排产</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-text>已排产订单</el-text>
      <el-input
        v-model="dialogOrderSearch"
        placeholder=""
        size="normal"
        clearable
        @change=""
      ></el-input>
      <el-table :data="processedOrder" border stripe style="height: 350px">
        <el-table-column prop="orderId" label="订单编号"> </el-table-column>
        <el-table-column prop="createDate" label="订单创建日期"> </el-table-column>
        <el-table-column label="物流状态">
          <template #default="scope">
            <el-button type="primary" size="default" @click="">查看详细状态</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="remainAmount" label="成型剩余数量"> </el-table-column>
        <el-table-column prop="shipDate" label="订单出货日期"> </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="default" @click="">修改排产</el-button>
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
  <el-dialog title="订单号 K24-2111620 鞋型排产详情" v-model="isShoeScheduleVis" width="90%">
    <span>
      <el-table :data="shoeProcess" border stripe>
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
                  </el-table>
                </template>
              </el-table-column>

              <el-table-column prop="date" label="日期"> </el-table-column>
              <el-table-column prop="productAmount" label="已排产鞋型数"> </el-table-column>
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
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

export default {
  components: {
    VueCal
  },
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
      unprocessedOrder: [
        {
          orderId: 'K24-2111620',
          createDate: '2024-07-08',
          logisticsStatus: 0,
          shipDate: '2024-09-10'
        }
      ],
      processedOrder: [
        {
          orderId: 'K24-2111620',
          createDate: '2024-07-08',
          logisticsStatus: 0,
          remainAmount: 5000,
          cutDatePeriod: '2024-07-09 至 2024-08-16',
          sewPreDatePeriod: '2024-07-09 至 2024-08-16',
          sewDatePeriod: '2024-07-09 至 2024-08-16',
          moldDatePeriod: '2024-07-09 至 2024-08-16',
          shipDate: '2024-09-10'
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
          moldDatePeriod: '2024-07-09 至 2024-08-16'
        }
      ],
      events: [
        {
          start: '2024-07-04',
          end: '2024-07-06',
          title: 'K24-0111620',
          content: '0E21922',
          class: 'leisure',
          number: 500,
          lineUsage: 5,
          image: 'https://via.placeholder.com/50'
        },
        {
          start: '2024-07-06',
          end: '2024-07-07',
          title: 'K24-0111621',
          content: '0E21922',
          class: 'sport',
          image: 'https://via.placeholder.com/50'
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
          shoeList: [{
            orderId: 'K24-2111620',
            shoeId: '0E11150',
            amount: 300,
            datePeriod: "2024-07-16-2024-07-20",
            averageAmount: 75
          }]
        }
      ]
    }
  }
}
</script>
