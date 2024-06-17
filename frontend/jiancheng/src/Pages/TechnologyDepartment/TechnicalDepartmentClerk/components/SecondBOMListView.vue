<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">二次BOM填写</el-col>
    </el-row>
    <component :is="currentDash" :pendingTaskData="textData" :inProgressTaskData="textData2" @backToList="changeToList"
    @changeToPend="changeToPend" @changeToProgress="changeToProgress">
    </component>
</template>
<script>
import { Grid, Memo } from '@element-plus/icons-vue'
import SecondBOMList from './SecondBOMCreate/SecondBOMList.vue'
import SecondOrderPend from './SecondBOMCreate/SecondBOMListPend.vue'
import SecondOrderProgress from './SecondBOMCreate/SecondBOMListProgress.vue'

export default {
    components: {
        SecondBOMList,
        SecondOrderPend,
        SecondOrderProgress
    },
    data() {
        return {
            Grid,
            Memo,
            currentDash: 'SecondBOMList',
            textData: [{
                taskName: "二次BOM填写",
                orderId: "K24-024 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-025 2111622",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            ],
            textData2: [{
                taskName: "二次BOM填写",
                orderId: "K24-021 2111628",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "二次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            ],
        }
    },
    methods: {
        changeToList() {
            this.currentDash = 'SecondBOMList'
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