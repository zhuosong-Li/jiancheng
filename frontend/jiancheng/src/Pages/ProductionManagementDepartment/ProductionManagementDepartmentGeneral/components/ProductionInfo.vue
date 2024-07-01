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
        <el-table-column prop="startDate" label="开始日期" sortable />
        <el-table-column prop="prodStatus" label="生产状态" sortable />
        <el-table-column prop="totalQuantity" label="总生产数量" sortable/> 
        <el-table-column prop="remainingQuantity" label="剩余数量" sortable/> 
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
        <el-table-column prop="startDate" label="开始日期" sortable />
        <el-table-column prop="materialStatus" label="物料状态" sortable />
        <el-table-column prop="deliverDate" label="截止日期" sortable />
        <el-table-column label="操作" sortable >
            <template #default>
            <el-button link type="primary" size="small" @click="openNewWindow(current-row-key)">
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
  </template>
  
<script>
import { Grid, Memo } from '@element-plus/icons-vue'
import DashboardGrid from './Dashboard/DashboardGrid.vue';
import DashboardList from './Dashboard/DashboardList.vue'
import DashboardPend from './Dashboard/DashboardListPend.vue'
import DashboardProgress from './Dashboard/DashboardListProgress.vue'

export default {
    components: {
        DashboardGrid,
        DashboardList,
        DashboardPend,
        DashboardProgress
    },
    data() {
        return {
            Grid,
            Memo,
            currentDash: 'DashboardGrid',
            inproductiontableData: [{
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "裁断中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"

            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "成型中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            },
            {
                customerId: "K24-016客人37 XTI 2111620",
                startDate: "2024-06-10",
                prodStatus: "针车中",
                deliverDate: "2024-07-10",
                totalQuantity:"2000",
                remainingQuantity:"500"
            }
            ],
            preproductiontableData: [{
                customerId: "K24-021 2111628",
                startDate: "2024-06-10",
                materialStatus: "已定-2024-6-12",
                deliverDate: "2024-09-30"
             },
            {
                customerId: "K24-021 2111629",
                startDate: "2024-06-10",
                materialStatus: "已到达",
                deliverDate: "2024-09-30"
            },
            ],
        }
    },
    methods: {
        changeToGrid() {
            this.currentDash = 'DashboardGrid'
        },
        changeToList() {
            this.currentDash = 'DashboardList'
        },
        changeToPend() {
            this.currentDash = 'DashboardPend'
        },
        changeToProgress() {
            console.log(this.currentDash)
            this.currentDash = 'DashboardProgress'
        },
        openNewWindow(rowkey)
        {
            let url = ""
            const orderId = rowkey.customerId.replace(' ','-')
            url = `${window.location.origin}/productiongeneral/productiondetail/customerid=${orderId}`;
            window.open(url, '_blank');
        }

    }
}
</script>
<style></style>