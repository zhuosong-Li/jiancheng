<template>
    <el-container>
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main>
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">裁断工价填报</el-col>
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
                        <el-button v-if="scope.row.status === '未生成工价表'" type="primary"
                            @click="handleGenerate(scope.row)">生成</el-button>
                        <el-button-group v-else-if="scope.row.status === '已保存工价表'">
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
                <EditTable :columnList="columnList" :tableInput="[]" :watchFunctions="{}"/>
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
const currentTitle = ref('')
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
            status: "未生成工价表",
            reportType: "裁断"
        }
    )
}
for (let i = 2; i < 4; i++) {
    taskData.push(
        {
            shoeTypeId: "G20240601 " + i.toString(),
            date: "2024-05-24",
            status: "已保存工价表",
            reportType: "批皮"
        }
    )
}
const columnList = [
    {
        prop: "material",
        label: "种类",
        editable: true
    },
    {
        prop: "productNumber",
        label: "货号",
        editable: true
    },
    {
        prop: "procedure",
        label: "工序名称",
        editable: true
    },
    {
        prop: "unitPrice",
        label: "计件单位",
        editable: true
    },
    {
        prop: "note",
        label: "备注",
        editable: true
    },
]
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