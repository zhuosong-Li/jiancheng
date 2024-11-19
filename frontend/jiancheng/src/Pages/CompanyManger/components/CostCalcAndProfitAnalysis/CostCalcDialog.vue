<template>
    <el-dialog title="添加客户" v-model="addCustomerDialogVisible" width="30%">
        <el-table
            :data="currentTableData"
            style="width: 100%; margin-bottom: 20px; height: 650px"
            row-key="id"
            border
            default-expand-all
        >
            <el-table-column>
                <el-table-column prop="orderRId" label="裁断内部成本" sortable />
                <el-table-column prop="factoryShoesModel" label="裁断外包成本" sortable />
                <el-table-column prop="custShoesModel" label="针车内部成本" sortable />
                <el-table-column prop="materialProcurementCost" label="针车外包成本" sortable />
                <el-table-column prop="needleCuttingLaborCost" label="成型内部成本" sortable />
            </el-table-column>
        </el-table>
    </el-dialog>
</template>

<script setup>
defineProps(['dialogVisible'])
</script>

<style scoped></style>
