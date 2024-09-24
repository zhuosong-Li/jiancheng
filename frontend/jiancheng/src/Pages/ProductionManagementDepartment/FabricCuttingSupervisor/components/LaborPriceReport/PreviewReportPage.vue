<template>
    <el-table :data="props.tableData" border>
        <el-table-column prop="rowId" label="序号" />
        <el-table-column prop="procedure" label="工序"></el-table-column>
        <el-table-column prop="price" label="单位价格"></el-table-column>
        <el-table-column prop="note" label="备注"></el-table-column>
    </el-table>
</template>
<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue';
import { exportTableToExcel } from '@/Pages/ProductionManagementDepartment/utils';
const proxy = getCurrentInstance()
const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl
const props = defineProps(['tableData'])
const previewVis = ref(true)
const columns = ref([])
const currentTitle = ref('')
onMounted(() => {
    // currentTitle.value = "鞋型号" + props.currentRowData.shoeRId + "工价单"
    // let obj = [
    //     { prop: "rowId", label: "序号" },
    //     { prop: "procedure", label: "工序" },
    //     { prop: "price", label: "单位价格" },
    //     { prop: "note", label: "备注" },
    // ]
    // columns.value = obj
})

const handleExport = () => {
    exportTableToExcel(tableData.value, columns.value, currentTitle.value + ".xlsx")
}
</script>
