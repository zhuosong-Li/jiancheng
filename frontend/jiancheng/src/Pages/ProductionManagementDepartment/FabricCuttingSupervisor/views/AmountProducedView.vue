<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">裁断数量填报</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" :column="2">
                        <el-descriptions-item label="订单编号">{{ props.orderId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ props.createTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序流程下发时间">{{ props.prevTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理部门">{{ props.prevDepart }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理人">{{ props.prevUser }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <el-table :data="taskData">
                <el-table-column prop="shoeTypeId" label="鞋型号"></el-table-column>
                <el-table-column prop="date" label="日期"></el-table-column>
                <el-table-column prop="reportType" label="工价表"></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.status === '未填写数量表'" type="primary"
                            @click="handleGenerate(scope.row)">生成</el-button>
                        <el-button-group v-else-if="scope.row.status === '已保存数量表'">
                            <el-button type="primary" class="block-button"
                                @click="handleGenerate(scope.row)">编辑</el-button>
                            <el-button type="success" class="block-button"
                                @click="openPreviewDialog(scope.row)">预览</el-button>
                            <el-button type="warning" class="block-button"
                                @click="handleConfirm(scope.row)">确认下发</el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog :title="currentTitle" v-model="createVis" width="90%"
                @close="handleClose(0)">
                <EditTable :columnList="columnList" :tableInput="tableInput" :watchFunctions="watchFunctions"/>
            </el-dialog>
            <el-dialog :title="currentTitle" v-model="previewVis" width="90%"
                @close="handleClose(1)">
                hello
            </el-dialog>
        </el-main>
    </el-container>
</template>

<script setup>
import { ref } from 'vue';
import EditTable from '@/components/EditTable.vue';
import AllHeader from '@/components/AllHeader.vue';
const createVis = ref(false)
const previewVis = ref(false)
const currentTitle = ref('工价单号 ')
const props = defineProps({
    'orderId': String,
    'createTime': String,
    'prevTime': String,
    'prevDepart': String,
    'prevUser': String
})
let taskData = []
for (let i = 0; i < 2; i++) {
    taskData.push(
        {
            shoeTypeId: "G20240601 " + i.toString(),
            date: "2024-06-01",
            reportType: "批皮",
            status: "未填写数量表"
        }
    )
}
for (let i = 2; i < 4; i++) {
    taskData.push(
        {
            shoeTypeId: "G20240601 " + i.toString(),
            date: "2024-05-24",
            reportType: "裁断",
            status: "已保存数量表"
        }
    )
}
const columnList = [
    {
        prop: "material",
        label: "种类",
        editable: false
    },
    {
        prop: "name",
        label: "姓名",
        editable: false
    },
    {
        prop: "productNumber",
        label: "货号",
        editable: false
    },
    {
        prop: "procedure",
        label: "工序名称",
        editable: false
    },
    {
        prop: "amount",
        label: "生产数量",
        editable: true
    },
    {
        prop: "remain",
        label: "剩余数量",
        editable: false
    },
    {
        prop: "unitPrice",
        label: "计件单位",
        editable: false
    },
    {
        prop: "totalPrice",
        label: "总金额",
        editable: false
    },
    {
        prop: "note",
        label: "备注",
        editable: true
    },
]
const tableInput = [
    {
        material: "人造皮",
        name: "小明",
        productNumber: "101",
        procedure: "单鞋E",
        amount: 0,
        remain: 500,
        unitPrice: 0.47,
        totalPrice: 0,
        note: ""
    },
    {
        material: "人造皮",
        name: "小红",
        productNumber: "102",
        procedure: "批-22片",
        amount: 0,
        remain: 500,
        unitPrice: 0.61,
        totalPrice: 0,
        note: ""
    },
]
const watchFunctions = {
    "amount": (newVal, oldVal, childContext) => {
        newVal = Number(newVal), oldVal = Number(oldVal)
        childContext.remain.content = childContext.remain.content + oldVal - newVal
        childContext.totalPrice.content = childContext.unitPrice.content * newVal
    }
}
const handleGenerate = (rowData) => {
    currentTitle.value = "鞋型号 " + rowData.shoeTypeId
    createVis.value = true
}
const openPreviewDialog = (rowData) => {
    currentTitle.value = "鞋型号 " + rowData.shoeTypeId
    previewVis.value = true
}
const handleConfirm = (e) => {
    console.log(e)
}
const handleClose = (option) => {
    if (option === 0) createVis.value = false
    else if (option === 1) previewVis.value = false
}
</script>
<style scoped>
.block-button {
    display: block;
}
</style>