<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">一次BOM填写</el-col>
    </el-row>
    <component :is="currentDash" :pendingTaskData="textData" :inProgressTaskData="textData2" @backToList="changeToList"
    @changeToPend="changeToPend" @changeToProgress="changeToProgress">
    </component>
</template>
<script>
import { Grid, Memo } from '@element-plus/icons-vue'
import FirstBOMList from './FirstBOMCreate/FirstBOMList.vue'
import FirstOrderPend from './FirstBOMCreate/FirstBOMListPend.vue'
import FirstOrderProgress from './FirstBOMCreate/FirstBOMListProgress.vue'

export default {
    components: {
        FirstBOMList,
        FirstOrderPend,
        FirstOrderProgress
    },
    data() {
        return {
            Grid,
            Memo,
            currentDash: 'FirstBOMList',
            textData: [{
                taskName: "一次BOM填写",
                orderId: "K24-024 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
                orderId: "K24-025 2111622",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
                orderId: "K24-021 2111620",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            ],
            textData2: [{
                taskName: "一次BOM填写",
                orderId: "K24-021 2111628",
                createTime: "2024-06-10",
                prevTime: "2024-06-10 18:00:00",
                prevDepart: "技术部",
                prevUser: "XXX"
            },
            {
                taskName: "一次BOM填写",
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
            this.currentDash = 'FirstBOMList'
        },
        changeToPend() {
            this.currentDash = 'FirstOrderPend'
        },
        changeToProgress() {
            console.log(this.currentDash)
            this.currentDash = 'FirstOrderProgress'
        }

    }
}
</script>
<style></style>