<template>
    <el-table :data="taskData">
        <el-table-column prop="orderId" label="订单号"></el-table-column>
        <el-table-column prop="createTime" label="订单创建时间"></el-table-column>
        <el-table-column prop="prevTime" label="前序流程下发时间"></el-table-column>
        <el-table-column prop="prevDepart" label="前序处理部门"></el-table-column>
        <el-table-column prop="prevUser" label="前序处理人"></el-table-column>
        <el-table-column label="操作"> 
            <template #default="{ row }">
                <el-button type="primary"
                    @click="handleView(row)">查看</el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup>
const props = defineProps(['taskData'])
const handleView = (row) => {
    let url = ""
    // const orderId = row.orderId.replace(' ','-')
    const queryString = new URLSearchParams(row).toString();
    url = `${window.location.origin}/fabriccutting/priceReport?${queryString}`;
    window.open(url, '_blank');
}
</script>
<style scoped>
.block-button {
  display: block;
}
</style>