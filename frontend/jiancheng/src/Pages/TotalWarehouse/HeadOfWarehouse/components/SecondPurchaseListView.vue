<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">二次采购入库</el-col>
    </el-row>
    <component :is="currentDash" :pendingTaskData="textData" :inProgressTaskData="textData2" @backToList="changeToList"
    @changeToPend="changeToPend" @changeToProgress="changeToProgress">
    </component>
</template>
<script>
import { Grid, Memo } from '@element-plus/icons-vue'
import SecondOrderList from './SecondWarehousing/SecondWarehousingList.vue'
import SecondOrderPend from './SecondWarehousing/SecondWarehousingListPend.vue'
import SecondOrderProgress from './SecondWarehousing/SecondWarehousingListProgress.vue'

export default {
    components: {
        SecondOrderList,
        SecondOrderPend,
        SecondOrderProgress
    },
    data() {
        return {
            Grid,
            Memo,
            currentDash: 'SecondOrderList',
            textData: [{
                taskName: "二次采购入库",
                orderId: "K24-024 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-025 2111622",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            ],
            textData2: [{
                taskName: "二次采购入库",
                orderId: "K24-021 2111628",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            {
                taskName: "二次采购入库",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "物控部",
                prevUser: "XXX"
            },
            ],
        }
    },
    methods: {
        changeToList() {
            this.currentDash = 'SecondOrderList'
        },
        changeToPend() {
            this.currentDash = 'SecondOrderPend'
        },
        changeToProgress() {
            console.log(this.currentDash)
            this.currentDash = 'SecondOrderProgress'
        }

    }
}
</script>
<style></style>