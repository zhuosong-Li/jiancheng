<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">供应商管理</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24" :offset="0">
            <el-table :data="supplierData" border style="height: 500px;">
                <el-table-column prop="supplierName" label="供应商名称"></el-table-column>
                <el-table-column prop="supplierField" label="供应商供货类型"></el-table-column>
                <el-table-column prop="addDate" label="添加日期"></el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="4" :offset="20"><el-button type="primary" size="default"
                @click="openCreateDialog">创建新仓库</el-button>
        </el-col>
    </el-row>
</template>

<script>
export default {
    data() {
        return {
            supplierData: [],
        }
    }
}
</script>
